import os, ctypes, subprocess, sys
user = os.environ['USERPROFILE']
file = 'exec.py'
if os.path.exists('c:\\program files\\GlassTwist\\deepspeech-0.8.2-models.scorer') == False:
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


    def set_dir():
        proc = subprocess.Popen(
            'cd/ & cd program files & mkdir workstation '
            , shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        out, err = proc.communicate()
        print(out)


    def set_desktop():
        proc2 = subprocess.Popen(
            f'move {file} "c:\\program files\\workstation" & cd/ & cd {user} & cd desktop & mklink workstation "{file}" ',
            shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        out, err = proc2.communicate()
        print(out)


    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
if is_admin():
    set_dir()
    set_desktop()
else:
    # Rerun the program with admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "setup.py", None, 10)