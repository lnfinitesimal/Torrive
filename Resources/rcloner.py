import json
import re  # nosec
import ipywidgets as widgets  # pylint: disable=import-error
from IPython.display import HTML, clear_output, display  # pylint: disable=import-error
from google.colab import files  # pylint: disable=import-error
from glob import glob
from sys import exit as exx

# Ultilities Methods ==========================================================


def createButton(name, *, func=None, style="", icon="check"):
    import ipywidgets as widgets  # pylint: disable=import-error

    button = widgets.Button(
        description=name, button_style=style, icon=icon, disabled=not bool(func)
    )
    button.style.font_weight = "900"
    button.on_click(func)
    output = widgets.Output()
    display(button, output)


def generateRandomStr():
    from uuid import uuid4

    return str(uuid4()).split("-")[0]


def checkAvailable(path_="", userPath=False):
    from os import path as _p

    if path_ == "":
        return False
    else:
        return (
            _p.exists(path_)
            if not userPath
            else _p.exists(f"/usr/local/sessionSettings/{path_}")
        )


def findProcess(process, command="", isPid=False):
    from psutil import pids, Process  # pylint: disable=import-error

    if isinstance(process, int):
        if process in pids():
            return True
    else:
        for pid in pids():
            try:
                p = Process(pid)
                if process in p.name():
                    for arg in p.cmdline():
                        if command in str(arg):
                            return True if not isPid else str(pid)
                        else:
                            pass
                else:
                    pass
            except:  # nosec
                continue


def runSh(args, *, output=False, shell=False):
    import subprocess
    import shlex  # nosec

    if not shell:
        if output:
            proc = subprocess.Popen(  # nosec
                shlex.split(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while True:
                output = proc.stdout.readline()
                if output == b"" and proc.poll() is not None:
                    return
                if output:
                    print(output.decode("utf-8").strip())
        return subprocess.run(shlex.split(args)).returncode  # nosec
    else:
        if output:
            return (
                subprocess.run(
                    args,
                    shell=True,  # nosec
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                .stdout.decode("utf-8")
                .strip()
            )
        return subprocess.run(args, shell=True).returncode  # nosec


def accessSettingFile(file="", setting={}):
    from json import load, dump

    if not isinstance(setting, dict):
        print("Only accept Dictionary object.")
        exx()
    fullPath = f"/usr/local/sessionSettings/{file}"
    try:
        if not len(setting):
            if not checkAvailable(fullPath):
                print(f"File unavailable: {fullPath}.")
                exx()
            with open(fullPath) as jsonObj:
                return load(jsonObj)
        else:
            with open(fullPath, "w+") as outfile:
                dump(setting, outfile)
    except:
        print(f"Error accessing the file: {fullPath}.")


def memGiB():
    from os import sysconf as _sc  # pylint: disable=no-name-in-module

    return _sc("SC_PAGE_SIZE") * _sc("SC_PHYS_PAGES") / (1024.0 ** 3)


# Prepare prerequisites =======================================================

def addUtils():
    if checkAvailable("/content/sample_data"):
        runSh("rm -rf /content/sample_data")
    if not checkAvailable("/usr/local/sessionSettings"):
        runSh("mkdir -p -m 777 /usr/local/sessionSettings")
    if not checkAvailable("/content/upload.txt"):
        runSh("touch /content/upload.txt")
    if not checkAvailable("/root/.ipython/rcloner.py"):
        runSh(
            "wget -qq https://github.com/Cavemanly/Cloudy/blob/main/Resources/rcloner.py \
                -O /root/.ipython/rcloner.py"
        )
    if not checkAvailable("checkAptUpdate.txt", userPath=True):
        runSh("apt update -qq -y")
        runSh("apt-get install -y iputils-ping")
        data = {"apt": "updated", "ping": "installed"}
        accessSettingFile("checkAptUpdate.txt", data)

def prepareSession():
    if checkAvailable("ready.txt", userPath=True):
        return
    else:
        addUtils()
        accessSettingFile("ready.txt", {"prepared": "True"})


# rClone ======================================================================

def displayOutput(operationName="", color="#ce2121"):
    if color == "success":
        hColor = "#28a745"
        displayTxt = f"👍 Operation {operationName} has been successfully completed."
    elif color == "danger":
        hColor = "#dc3545"
        displayTxt = f"❌ Operation {operationName} has been errored."
    elif color == "info":
        hColor = "#17a2b8"
        displayTxt = f"👋 Operation {operationName} has some info."
    elif color == "warning":
        hColor = "#ffc107"
        displayTxt = f"⚠ Operation {operationName} has been warning."
    else:
        hColor = "#ffc107"
        displayTxt = f"{operationName} works."
    display(
        HTML(
            f"""
            <center>
                <h2 style="font-family:monospace;color:{hColor};">
                    {displayTxt}
                </h2>
                <br>
            </center>
            """
        )
    )