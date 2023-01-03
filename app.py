from tkinter import Tk, Label, Button
from tkinter import StringVar
from threading import Thread
from os import popen
from time import sleep

root = Tk()
root.title("Cloudflare WARP")
root.geometry("470x200")
status = StringVar()
enableLabel = Label(root, text="Enable Cloudflare WARP", width=50).grid(row=1, column=1)
disableLabel = Label(root, text="Disable Cloudflare WARP", width=50).grid(row=2, column=1)
statusLabel = Label(root, textvariable=status, width=50).grid(row=3, column=1, columnspan=2)

def enableCallback():
    popen("warp-cli connect").read()
    statusCheck()
    return True

def disableCallback():
    popen("warp-cli disconnect").read()
    statusCheck()
    return True

def statusCheck():
    command= popen("warp-cli status").read()
    for i in command.split("\n"):
        if len(i) > 7:
            print(i)
            break
    status.set(i)
    if "Connecting" in i:
        sleep(1)
        statusCheck()
    
    return True

Button(root, text="Enable", command=lambda: Thread(target=enableCallback).start(), width=10).grid(row=1, column=2)
Button(root, text="Disable", command=lambda: Thread(target=disableCallback).start(), width=10).grid(row=2, column=2)

statusCheck()
root.mainloop()
