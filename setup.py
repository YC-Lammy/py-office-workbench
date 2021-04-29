import os, ctypes, subprocess, sys, requests
from io import BytesIO
from psutil import Process

user = Process().username()

if sys.platform == 'win32':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    if os.path.exists('c:\\program files\\workbench') == True:
        print('path already exist')
        input('press Enter to exit...')

    def set_desktop():
        with BytesIO() as f:
            url = 'https://github.com/YC-Lammy/workbench/archive/refs/heads/main.zip' # the computer may not have git
            r = requests.get(url, allow_redirects=True)
            f.write(r.content)
            import zipfile
            with zipfile.ZipFile(f, 'r') as zip_ref:
                zip_ref.extractall('c:\\program files\\workbench')

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        set_desktop()
    else:
        # Rerun the program with admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "setup.py", None, 10)

elif sys.platform == 'linux':
    if os.path.exists('c:\\program files\\workbench') == True:
        print('path already exist')
        input('press Enter to exit...')
    with BytesIO() as f:
        url = 'https://github.com/YC-Lammy/workbench/archive/refs/heads/main.zip' # the computer may not have git
        r = requests.get(url, allow_redirects=True)
        f.write(r.content)
        import zipfile

        with zipfile.ZipFile(f, 'r') as zip_ref:
            zip_ref.extractall(f'/home/{user}/workbench')

elif sys.platform == 'darwin':
    pass # i have no access to mac