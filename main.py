from tkinter import *
from tkinter import messagebox
from os import popen, getcwd
from time import sleep
from threading import Thread
import json, sys


root = Tk()
rootMenu = Menu(root)
root.title("Cloudflare WARP")
root.geometry("470x200")
root.configure(bg="#1E1E1E")
root.resizable(False, False)
cwd = getcwd()
enableImage = PhotoImage(file=f"{cwd}/images/Enable.png")
disableImage = PhotoImage(file=f"{cwd}/images/Disable.png")
bg = PhotoImage(file=f"{cwd}/images/bg.png")
white = PhotoImage(file=f"{cwd}/images/white.png")
orange = PhotoImage(file=f"{cwd}/images/orange.png")
root.iconphoto(True, white)

Label(root, image=bg).place(x=0, y=0, relheight=1, relwidth=1)

class App:
    def __init__(self, master):
        self.startup()
        self.status= StringVar()
        self.taskbarText = StringVar()
        self.taskbarCheck = None
        self.taskbar()
        self.statusCheck()
        self.enableFrame(master)
        self.disableFrame(master)
        self.checkboxFrame(master)
        self.statusFrame(master)
        # self.menu(master)
        
    def menu(self, master):
        global rootMenu
        root.config(menu=rootMenu)
        fileMenu = Menu(rootMenu)
        rootMenu.add_cascade(label="File", menu=fileMenu)
        rootMenu.add_separator()
        fileMenu.add_command(label="Settings", command=master.quit)
        rootMenu.add_separator()
        fileMenu.add_command(label="Exit", command=master.quit)
    
    def enableFrame(self, master):
        frame = Frame(master=master,bg="#1E1E1E")
        frame.pack(pady=5)
        self.enableLabel = Label(frame, text="Enable Cloudflare WARP",bg="#1E1E1E", foreground="white", width=30)
        self.enableLabel.grid(row=0,column=0, padx=20)
        self.enableButton = Button(frame,image=enableImage, borderwidth=0, text="Enable", command=lambda: Thread(target=self.enableCallback).start(),width=75,bg="#1E1E1E",activebackground="#1E1E1E",highlightthickness=0, foreground="white")
        self.enableButton.grid(row=0, column=1)
        
    def disableFrame(self, master):
        frame = Frame(master=master,bg="#1E1E1E")
        frame.pack(pady=5)
        self.enableLabel = Label(frame, text="Disable Cloudflare WARP",bg="#1E1E1E", foreground="white",width=30)
        self.enableLabel.grid(row=1,column=0, padx=20)
        self.enableButton = Button(frame,image=disableImage,borderwidth=0, text="Disable",command=lambda: Thread(target=self.disableCallback).start(),width=75,bg="#1E1E1E",activebackground="#1E1E1E",highlightthickness=0, foreground="white")
        self.enableButton.grid(row=1, column=1)
    
    def checkboxFrame(self, master):
        frame = Frame(master=master,bg="#1E1E1E")
        frame.pack(pady=35)
        checkButton = Checkbutton(frame, textvariable=self.taskbarText,command=lambda: Thread(target=self.taskbar).start(),bg="#1E1E1E", borderwidth=0,activebackground="#1E1E1E",highlightthickness=0,activeforeground="white",foreground="grey")
        checkButton.pack()
    
    
    def statusFrame(self, master):
        frame = Frame(master=master,bg="#1E1E1E")
        frame.pack()
        self.statusLabel = Label(frame, textvariable=self.status,bg="#343434", foreground="white")
        self.statusLabel.grid(row=2, column=0, columnspan=3)
    
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
        if self.taskbarCheck == False:
            self.taskbarText.set("Disable warp taskbar icon")
            self.taskbarCheck = True
            popen("warp-taskbar").read()
        else:
            self.taskbarText.set("Enable warp taskbar icon")
            self.taskbarCheck = False
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
    
    def introMessage(self):
        with open("settings.json", "r") as f:
            settings = json.load(f)
            if settings["startupMsg"]:
                messagebox.showinfo("Thank You!", "Thank you for using my App, please support me by giving a star ⭐ !")
            with open("settings.json", "w") as write:
                settings['startupMsg'] = False
                json.dump(settings, write)

    def startup(self):
        self.introMessage()
        if sys.platform != "linux":
            messagebox.showerror("Error", "Sorry but this script only works on Linux!")
            sys.exit()
        if sys.version_info.major < 3:
            messagebox.showerror("Error", "The script requires python 3 or above!")
            sys.exit()
        if (popen("systemctl is-active  warp-svc").read()).rstrip() == "inactive":
            messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run first.")
            sys.exit()
            
    def on_exit(self):
        global root
        popen("warp-cli disconnect").read()
        popen("pkill -f warp-taskbar").read()
        root.quit()
    
if __name__ == "__main__":
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()