from tkinter import *
from os import popen, getcwd
from time import sleep
from threading import Thread


root = Tk()
rootMenu = Menu(root)
root.title("Cloudflare WARP")
root.geometry("470x200")
white = PhotoImage(file=f"{getcwd()}/images/white.png")
orange = PhotoImage(file=f"{getcwd()}/images/orange.png")
root.iconphoto(True, white)


class App:
    def __init__(self, master):
        self.status= StringVar()
        self.taskbarText = StringVar()
        self.taskbarCheck = None
        self.statusCheck()
        self.enableFrame(master)
        self.disableFrame(master)
        self.statusFrame(master)
        
    def enableFrame(self, master):
        frame = Frame(master=master)
        frame.pack(pady=5)
        self.enableLabel = Label(frame, text="Enable Cloudflare WARP")
        self.enableLabel.grid(row=0,column=0, padx=20)
        self.enableButton = Button(frame, text="Enable", command=lambda: Thread(target=self.enableCallback).start(),width=10)
        self.enableButton.grid(row=0, column=1)
        
    def disableFrame(self, master):
        frame = Frame(master=master)
        frame.pack(pady=5)
        self.enableLabel = Label(frame, text="Disable Cloudflare WARP")
        self.enableLabel.grid(row=1,column=0, padx=20)
        self.enableButton = Button(frame, text="Disable", command=lambda: Thread(target=self.disableCallback).start(),width=10)
        self.enableButton.grid(row=1, column=1)
    
    def statusFrame(self, master):
        frame = Frame(master=master)
        frame.pack(pady=20)
        self.statusLabel = Label(frame, textvariable=self.status)
        self.statusLabel.pack()
    
    def enableCallback(self, ):
        popen("warp-cli connect").read()
        root.geometry("470x200")
        self.statusCheck()
        root.iconphoto(True, orange)
        return True
    
    def disableCallback(self):
        popen("warp-cli disconnect").read()
        self.statusCheck()
        root.iconphoto(True, white)
        return True
    
    def taskbar(self):
        if taskbarCheck == False:
            self.taskbarText.set("Disable warp taskbar icon")
            taskbarCheck = True
            popen("warp-taskbar").read()
        else:
            self.taskbarText.set("Enable warp taskbar icon")
            taskbarCheck = False
            popen("pkill -f warp-taskbar").read()
    
    def statusCheck(self):
        command= popen("warp-cli status").read()
        for i in command.split("\n"):
            if len(i) > 7:
                print((i.split())[-1])
                break
        self.status.set(i)
        if "Connecting" in i:
            sleep(1)
            self.statusCheck()
        if i.split()[-1] == "Connected":
            root.iconphoto(True, orange)
        return True
    
    def on_exit(self):
        global root
        popen("warp-cli disconnect").read()
        popen("pkill -f warp-taskbar").read()
        root.exit()
    
if __name__ == "__main__":
    app = App(root)
    root.mainloop()