import customtkinter as tk
from customtkinter import StringVar
from threading import Thread
from os import popen
from time import sleep

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.status = StringVar()
        self.title("Cloudflare WARP")
        self.geometry("470x200")
        tk.CTkLabel(master=self, text="Enable Cloudflare WARP", width=375).grid(row=1, column=1, pady=10)
        tk.CTkLabel(master=self, text="Disable Cloudflare WARP", width=375).grid(row=2, column=1)
        tk.CTkLabel(master=self, textvariable=self.status, width=50,font=("Arial", 10)).grid(row=3, column=1,columnspan=2, pady=100)
        tk.CTkButton(master=self, text="Enable", command=lambda: Thread(target=self.enableCallback).start(), width=75).grid(row=1, column=2)
        tk.CTkButton(master=self, text="Disable", command=lambda: Thread(target=self.disableCallback).start(), width=75, ).grid(row=2, column=2, padx=5)
        self.statusCheck()
    def enableCallback(self):
        popen("warp-cli connect").read()
        self.statusCheck()
        return True

    def disableCallback(self):
        popen("warp-cli disconnect").read()
        self.statusCheck()
        return True

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