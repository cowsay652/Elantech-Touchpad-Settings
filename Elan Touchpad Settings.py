# Elan Touchpad Settings

from appJar import gui
from winreg import *
from sys import exit


def get_value(entry):
    try:
        key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\\Elantech\\SmartPad", 0, KEY_QUERY_VALUE)  # Open key
    except Exception:
        # Raise error and exit
        app.warningBox("Registry path not found", "The registry path does not exist. Please ensure that you have installed Elantech drivers.")
        exit(0)

    return QueryValueEx(key, entry)

def set_value(entry, entry_type, data):
    try:
        key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\\Elantech\\SmartPad", 0, KEY_SET_VALUE)  # Open key
    except Exception:
        # Raise error and exit
        app.warningBox("Registry path not found", "The registry path does not exist. Please ensure that you have installed Elantech drivers.")
        exit(0)

    SetValueEx(key, entry, 0, entry_type, data)  # Set value for Registry entry
    CloseKey(key)

def apply(press):
    if app.getCheckBox("Right Click") == True:
        set_value("Tap_Two_Finger", REG_DWORD, 1)  # Sets registry values
        set_value("Tap_Two_Finger_Enable", REG_DWORD, 1)
    else:
        set_value("Tap_Two_Finger", REG_DWORD, 7)
        set_value("Tap_Two_Finger_Enable", REG_DWORD, 0)

    if app.getCheckBox("Use touchpad while using keyboard") == True:
        set_value("DisableWhenType_Enable", REG_DWORD, 0)
    else:
        set_value("DisableWhenType_Enable", REG_DWORD, 1)


def about(press):
    if press == "About":
        app.showSubWindow("About")
    else:
        app.hideSubWindow("About")


# Configure
right_click1 = get_value("Tap_Two_Finger")[0] == 1
right_click2 = get_value("Tap_Two_Finger_Enable")[0] == 1

if right_click1 == False or right_click2 == False: right_click = False
else: right_click = True

disable_type = get_value("DisableWhenType_Enable")[0] == 0


app = gui("Elan Touchpad Settings", useTtk=True)

app.setTtkTheme("vista")

app.setPadding(5, 5)
app.addCheckBox("Right Click")
app.addCheckBox("Use touchpad while using keyboard")
app.addButtons(["Apply", "About"], [apply, about])

app.setCheckBox("Right Click", ticked=right_click, callFunction=False)
app.setCheckBox("Use touchpad while using keyboard", ticked=disable_type, callFunction=False)

app.startSubWindow("About")
app.setPadding(5, 5)
app.addLabel("title", "Elantech Touchpad Settings")
app.getLabelWidget("title").config(font=("Segoe UI", "10", "bold"))
app.addLabel("version", "Version : 1.0")
app.addLabel("creator", "Created by: The Sleepy Penguin")
app.setFont(9)
app.addWebLink("YouTube Channel", "https://www.youtube.com/channel/UCszc1c-MjZB4p-hqUswlNVw")
app.addWebLink("GitHub", "https://github.com/The-Sleepy-Penguin")
app.addButton("OK", about)
app.setButtonSticky("OK", "es")
app.stopSubWindow()

app.go()
