from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
def jupyter_notebook(screen_width,screen_height):
    from subprocess import Popen, PIPE, STDOUT

    process = Popen(["jupyter", "notebook", "--no-browser"], stdin=PIPE, stdout=PIPE, stderr=STDOUT,cwd="/")

    for stdout_line in process.stdout:
        url = str(stdout_line)
        if 'http' in url and '[' not in url:
            break
    process.stdout.close()
    layout = QHBoxLayout()
    view = QWebEngineView()
    view.load(url[2:-3].strip())
    view.setZoomFactor(1.4)
    layout.addWidget(view)
    return layout