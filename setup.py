import os, ctypes, subprocess, sys, requests
from io import BytesIO
from psutil import Process

user = Process().username()
uname = os.uname()
distribute = uname.version
release = uname.release
instruction = uname.machine

if instruction != 'x86_64':
    print('\033[93mWarning: some modules may not be supported since you are not using x86_64 \033[0m')
    print('\033[96myou may ignore the above warning since it is just a warning\033[0m')
print('\033[94m'+distribute+'\033[0m')
if sys.platform == 'win32':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    if os.path.exists('c:\\program files\\workbench') == True:
        print('\033[91mpath already exist\033[0m')
        input('press Enter to exit...')
        sys.exit()

    def set_desktop():
        with BytesIO() as f:
            print('\033[92mgetting zip from github main branch\033[0m')
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
    if os.path.exists(f'/home/{user}/workbench') == True:
        print('\033[91mpath already exist\033[0m')
        input('press Enter to exit...')
        sys.exit()
    with BytesIO() as f:
        print('\033[92mgetting zip from github main branch...\033[0m')
        url = 'https://github.com/YC-Lammy/workbench/archive/refs/heads/main.zip' # the computer may not have git
        r = requests.get(url, allow_redirects=True)
        print('\033[96mwriting zip to BytesIO...\033[0m')
        f.write(r.content)
        import zipfile

        with zipfile.ZipFile(f, 'r') as zip_ref:
            print('\033[93mextracting zip...\033[0m')
            zip_ref.extractall(f'/home/{user}/workbench')

elif sys.platform == 'darwin':# i have no access to mac so don't know if it works
    if os.path.exists(f'/Users/{user}/workbench') == True:
        print('\033[91mpath already exist\033[0m')
        input('press Enter to exit...')
        sys.exit()
    with BytesIO() as f:
        print('\033[92mgetting zip from github main branch...\033[0m')
        url = 'https://github.com/YC-Lammy/workbench/archive/refs/heads/main.zip' # the computer may not have git
        r = requests.get(url, allow_redirects=True)
        print('\033[96mwriting zip to BytesIO...\033[0m')
        f.write(r.content)

        import zipfile

        with zipfile.ZipFile(f, 'r') as zip_ref:
            print('\033[93mextracting zip...\033[0m')
            zip_ref.extractall(f'/Users/{user}/workbench')

print('\033[95mfinish install \033[0m')