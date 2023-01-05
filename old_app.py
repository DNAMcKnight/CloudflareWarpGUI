from tkinter import Tk, Label, Button,messagebox, Checkbutton
from tkinter import StringVar, PhotoImage, IntVar
from threading import Thread
from os import popen, getcwd
from time import sleep
import sys, json

root = Tk()
root.title("Cloudflare WARP")
root.geometry("470x200")
root.resizable(False, False)
white = PhotoImage(file=f"{getcwd()}/images/white.png")
orange = PhotoImage(file=f"{getcwd()}/images/orange.png")
root.iconphoto(True, white)
status = StringVar()
enableLabel = Label(root, text="Enable Cloudflare WARP", width=50).grid(row=1, column=1, pady= 10)
disableLabel = Label(root, text="Disable Cloudflare WARP", width=50).grid(row=2, column=1)
statusLabel = Label(root, textvariable=status, width=50).grid(row=3, column=1, columnspan=2, pady=110)

def introMessage():
    with open("settings.json", "r") as f:
        settings = json.load(f)
        if settings["startupMsg"]:
            messagebox.showinfo("Thank You!", "Thank you for using my App, please support me by giving a star ⭐ !")
        with open("settings.json", "w") as write:
            settings['startupMsg'] = False
            json.dump(settings, write)

def startup():
    introMessage()
    if sys.platform != "linux":
        messagebox.showerror("Error", "Sorry but this script only works on Linux!")
        sys.exit()
    if sys.version_info.major < 3:
        messagebox.showerror("Error", "The script requires python 3 or above!")
        sys.exit()
    if (popen("systemctl is-active  warp-svc").read()).rstrip() == "inactive":
        messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run first.")
        sys.exit()



def enableCallback():
    popen("warp-cli connect").read()
    statusCheck()
    root.iconphoto(True, orange)
    return True

def disableCallback():
    popen("warp-cli disconnect").read()
    statusCheck()
    root.iconphoto(True, white)
    return True

def statusCheck():
    command= popen("warp-cli status").read()
    for i in command.split("\n"):
        if len(i) > 7:
            print((i.split())[-1])
            break
    status.set(i)
    if "Connecting" in i:
        sleep(1)
        statusCheck()
    if i.split()[-1] == "Connected":
        root.iconphoto(True, orange)
    return True

def on_exit():
    popen("warp-cli disconnect").read()
    root.quit()
    

Button(root, text="Enable", command=lambda: Thread(target=enableCallback).start(), width=10).grid(row=1, column=2)
Button(root, text="Disable", command=lambda: Thread(target=disableCallback).start(), width=10).grid(row=2, column=2)

root.protocol("WM_DELETE_WINDOW", on_exit)
startup()
statusCheck()
root.mainloop()
