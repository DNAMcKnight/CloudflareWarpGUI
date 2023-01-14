import customtkinter as tk
from customtkinter import StringVar
from threading import Thread
from os import popen
from time import sleep
import sys

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.status = StringVar()
        self.taskbarText = StringVar()
        self.taskbarCheck = None
        self.title("Cloudflare WARP")
        self.geometry("470x200")
        self.taskbar()
        self.dependencyCheck()
        self.statusCheck()
    def dependencyCheck(self):
        check = True
        # check if user is using linux
        if sys.platform != "linux":
            tk.CTkLabel(master=self, text="Sorry but this script only works on Linux!", width=375).pack(pady=50)
            tk.CTkButton(master=self, text="Exit", command=lambda: Thread(target=sys.exit(), width=75)).pack(pady=10)
            check = False
        # check the python version
        if sys.version_info.major < 3:
            tk.CTkLabel(master=self, text="The script requires python 3 or above!", width=375).pack(pady=50)
            tk.CTkButton(master=self, text="Exit", command=lambda: Thread(target=sys.exit(), width=75)).pack(pady=10)
            check = False
        # check if the daemon is running
        if (popen("systemctl is-active  warp-svc").read()).rstrip() == "inactive":
            tk.CTkLabel(master=self, text="Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run first.", width=375).pack(pady=20)
            tk.CTkButton(master=self, text="Exit", command=lambda: Thread(target=sys.exit(), width=75)).pack(pady=10)
            check = False
        self.menu() if check else ""
        return True
        
    # generates the menu to enable/disable warp
    def menu(self):
        tk.CTkLabel(master=self, text="Enable Cloudflare WARP", width=375).grid(row=1, column=1, pady=10)
        tk.CTkLabel(master=self, text="Disable Cloudflare WARP", width=375).grid(row=2, column=1)
        tk.CTkCheckBox(master=self, textvariable=self.taskbarText,command=lambda: Thread(target=self.taskbar).start()).grid(row=3, column=1,columnspan=2,pady=5)
        tk.CTkLabel(master=self, textvariable=self.status, width=50,font=("Arial", 10)).grid(row=4, column=1,columnspan=2, pady=60)
        tk.CTkButton(master=self, text="Enable", command=lambda: Thread(target=self.enableCallback).start(), width=75).grid(row=1, column=2)
        tk.CTkButton(master=self, text="Disable", command=lambda: Thread(target=self.disableCallback).start(), width=75, ).grid(row=2, column=2, padx=5)
    # connect callback, it runs status check to update until connection status changes to connected    
    def enableCallback(self):
        popen("warp-cli connect").read()
        self.statusCheck()
        return True

    def disableCallback(self):
        popen("warp-cli disconnect").read()
        self.statusCheck()
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
                print(i)
                break
        self.status.set(i)
        if "Connecting" in i:
            sleep(1)
            self.statusCheck()
        
        return True
    
if __name__ == "__main__":
    app = App()
    app.mainloop()