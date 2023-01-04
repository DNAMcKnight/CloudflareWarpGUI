from tkinter import Tk, Label, Button
from tkinter import StringVar, PhotoImage
from threading import Thread
from os import popen, getcwd
from time import sleep

root = Tk()
root.title("Cloudflare WARP")
root.geometry("470x200")
white = PhotoImage(file=f"{getcwd()}/images/white.png")
orange = PhotoImage(file=f"{getcwd()}/images/orange.png")
root.iconphoto(True, white)
status = StringVar()
enableLabel = Label(root, text="Enable Cloudflare WARP", width=50).grid(row=1, column=1, pady= 10)
disableLabel = Label(root, text="Disable Cloudflare WARP", width=50).grid(row=2, column=1)
statusLabel = Label(root, textvariable=status, width=50).grid(row=3, column=1, columnspan=2, pady=110)


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

Button(root, text="Enable", command=lambda: Thread(target=enableCallback).start(), width=10).grid(row=1, column=2)
Button(root, text="Disable", command=lambda: Thread(target=disableCallback).start(), width=10).grid(row=2, column=2)

statusCheck()
root.mainloop()
