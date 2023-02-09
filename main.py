from tkinter import *
from tkinter import messagebox
from os import popen,path
from os.path import exists
from time import sleep
from threading import Thread
import json, sys,subprocess,webbrowser, settings


# Path changes if you're using the compiled version of the app
if getattr(sys, 'frozen', False):
    path = f"{sys._MEIPASS}/"
else:
    path = ""
    
root = Tk()
rootMenu = Menu(root)
root.title("Cloudflare WARP")
width, height = 470, 200
widthCenter = int(root.winfo_screenwidth() / 2 - width / 2)
heightCenter = int(root.winfo_screenheight() / 2 - height / 2)
root.geometry(f"470x200+{widthCenter}+{heightCenter}")
root.resizable(False, False)

# To easily use colors and images together this little dict does the job.
visuals = {
    "blue": {"buttons": {"normal": PhotoImage(file=f"{path}assets/blue.png"), "highlight": PhotoImage(file=f"{path}assets/blue_highlight.png")}, "colors": {"normal": "#0466C8", "highlight": "#0074FD"}},
    "red": {"buttons": {"normal": PhotoImage(file=f"{path}assets/red.png"), "highlight": PhotoImage(file=f"{path}assets/red_highlight.png")}, "colors": {"normal": "#BC232D", "highlight": "#DF2935"}},
    "colors": {"bg": "#1E1E1E"},
    "images": {"logo": {"white": PhotoImage(file=f"{path}assets/white.png"), "orange": PhotoImage(file=f"{path}assets/orange.png")}},
}

root.configure(bg=visuals["colors"]["bg"])
root.iconphoto(True, visuals["images"]["logo"]["white"])

# Label(root, image=bgImage).place(x=0, y=0, relheight=1, relwidth=1)


class App:
    def __init__(self, master):
        self.bg = visuals["colors"]["bg"]
        self.startup()
        self.status = StringVar()
        self.taskbarText = StringVar()
        self.taskbarCheck = None
        self.taskbar()
        self.statusCheck()
        self.enableFrame(master)
        self.disableFrame(master)
        self.checkboxFrame(master)
        self.statusFrame(master)
        self.contextMenu(master)
    # The default menu is left unused, we might make one in the near future.
    def contextMenu(self, master):
        """creates a menu"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack()
        self.menu = Menu(
            frame, 
            tearoff=False,
            bg="#243347", 
            foreground="white", 
            activebackground=visuals['blue']['colors']['highlight'], 
            activeforeground='White',
            relief=FLAT,
            font=("Bold", 11)
            )
        self.menu.add_command(label="🔄 Refresh", command="")
        self.menu.add_command(label="⚙ Settings", command=self.settingsCallback)
        self.menu.add_command(label="🐙 About", command=self.aboutCallback)
        self.menu.add_command(label="🛑 Exit", command=master.quit)
        return True
    
    def settingsCallback(self):
        url = "config.json"
        webbrowser.open(url,new = 0, autoraise = True)
    
    def aboutCallback(self):
        url = "https://dnamcknight.github.io/CloudflareWarpGUI/"
        webbrowser.open(url,new = 0, autoraise = True)
    
    def menuCallback(self, coords):
        self.menu.tk_popup(x=coords.x_root+1, y=coords.y_root+1)
    
    # This contains the Text and button all put together in a frame.
    def enableFrame(self, master):
        """Enable frame that has text and a button attached to it"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(pady=5)
        spacer = Frame(frame, height= 10, bg=self.bg).grid(row=0,pady=10)
        self.enableLabel = Label(frame, text="Enable Cloudflare WARP", bg=self.bg, foreground="white", width=25)
        self.enableLabel.grid(row=1, column=0)
        self.enableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["blue"], callback=self.enableCallback, text="Enable")
        self.enableButton.grid(row=1, column=1, padx=25)
        return True

    # Same as the enableFrame
    def disableFrame(self, master):
        """Disable frame that has text and a button attached to it"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(pady=5)
        self.enableLabel = Label(frame, text="Disable Cloudflare WARP", bg=self.bg, foreground="white", width=25)
        self.enableLabel.grid(row=1, column=0)
        self.disableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["red"], callback=self.disableCallback, text="Disable")
        self.disableButton.grid(row=1, column=1, padx=25)
        return True

    # This handles all the button Text and Image and hover for us
    def buttonCreate(self, master, bg, type, callback, text):
        """generates a button using an image"""
        frame = Frame(master=master, bg=bg)
        button = Button(
            frame,
            image=type["buttons"]["normal"],
            borderwidth=0,
            text=text,
            command=lambda: Thread(target=callback).start(),
            width=75,
            bg=bg,
            activebackground=bg,
            highlightthickness=0,
            foreground="white",
        )
        button.grid(row=0, column=0)
        buttonText = Label(frame, text=text, bg=type["colors"]["normal"], foreground="white")
        buttonText.grid(row=0, column=0)
        buttonText.bind("<Button-1>", lambda event: button.invoke())
        frame.bind("<Enter>", lambda event: self.buttonHighlight(frame, "Enter", type))
        frame.bind("<Leave>", lambda event: self.buttonHighlight(frame, "Leave", type))
        return frame

    def buttonHighlight(self, frame, state, data):
        """Changes the highlight depending on the backgound color"""
        if state == "Enter":
            frame.winfo_children()[0].config(image=data["buttons"]["highlight"])
            frame.winfo_children()[1].config(bg=data["colors"]["highlight"])
        else:
            frame.winfo_children()[0].config(image=data["buttons"]["normal"])
            frame.winfo_children()[1].config(bg=data["colors"]["normal"])
        return True


    def checkboxFrame(self, master):
        """checkbox frame  for the checkbox"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(pady=10)
        checkButton = Checkbutton(
            frame,
            textvariable=self.taskbarText,
            command=lambda: Thread(target=self.taskbar).start(),
            bg=self.bg,
            borderwidth=0,
            activebackground=self.bg,
            highlightthickness=0,
            activeforeground="white",
            foreground="grey",
        )
        checkButton.pack()
        return True

    def statusFrame(self, master):
        """This is the taskbar"""
        frame = Frame(master=master, bg="#344966", width=master.winfo_screenwidth())
        frame.pack(side=BOTTOM, fill=X)
        # df2935
        self.statusLabel = Label(frame, textvariable=self.status, bg="#344966", foreground="white", padx=5, pady=4)
        self.statusLabel.pack(side=LEFT)
        return True

    def enableCallback(self):
        """Callback function for enable button which also changes the icon"""
        popen("warp-cli connect").read()
        self.statusCheck()
        root.iconphoto(True, visuals["images"]["logo"]["orange"])
        return True

    def disableCallback(self):
        """Callback for disable button and changes the icon"""
        popen("warp-cli disconnect").read()
        self.statusCheck()
        root.iconphoto(True, visuals["images"]["logo"]["white"])
        return True

    def taskbar(self):
        """Enables/disables the taskbar icon on Windows and Linux"""
        if self.taskbarCheck == False:
            self.taskbarText.set("Disable warp taskbar icon")
            self.taskbarCheck = True
            if sys.platform == "win32":
                popen("C:/Program Files/Cloudflare/Cloudflare WARP/Cloudflare WARP.exe").read()
            else:
                popen("warp-taskbar").read()
        else:
            self.taskbarText.set("Enable warp taskbar icon")
            self.taskbarCheck = False
            if sys.platform == "win32":
                subprocess.call('TASKKILL /F /IM "Cloudflare WARP.exe"', shell=True)
            else:
                popen("pkill -f warp-taskbar").read()

    def statusCheck(self):
        """This does the connection checks and updates taskbar"""
        command = popen("warp-cli status").read()            
        
        for i in command.split("\n"):
            if len(i) > 7:
                print((i.split())[-1])
                break
        self.status.set(i.replace("update:", ":"))
        if "Connecting" in i:
            sleep(1)
            self.statusCheck()
        if i.split()[-1] == "Connected":
            root.iconphoto(True, visuals["images"]["logo"]["orange"])
        return True

    def introMessage(self):
        """This is where the first time intro message is generated"""
        #TODO If there is no settings file, create one and save the settings within it.
        if not exists(f'{path}config.json'):
            settings.startup()
        with open(f"{path}config.json", "r") as f:
            data = json.load(f)
            if data["startupMsg"]:
                messagebox.showinfo("Thank You!", "Thank you for using my App, please support me by giving a star ⭐")
            with open(f"{path}config.json", "w") as write:
                data["startupMsg"] = False
                json.dump(data, write)

    def startup(self):
        """This is responsible to check if the system meets the requirements to run the program"""
        self.introMessage()
        root.bind('<Button-3>', self.menuCallback)
        if sys.version_info.major < 3:
            messagebox.showerror("Error", "The script requires python 3 or above!")
            sys.exit()
        if sys.platform != "linux":
            messagebox.showinfo("Warning", "Some features are not yet compatible with windows!")
            command = popen("warp-cli status").read()            
            temp = Label(root, text="Dowloading cloudflare warp please wait...", bg=self.bg, foreground="white")
            if not command:
                temp.pack()
                warp = messagebox.askyesno("Warning", "Warp is required to run this program, would you like to install it?")
                popen("winget install -e --id Cloudflare.Warp").read() if warp else ""
                temp.destroy()
                if warp:
                    messagebox.showinfo("Success!","Warp has been installed successfully! Please relaunch the app to use it.")
                else:
                    messagebox.showerror("Error", "Warp is required, please install Cloudflare Warp from https://cloudflarewarp.com and try again.")
                sys.exit()
        
        elif (popen("systemctl is-active  warp-svc").read()).rstrip() == "inactive":
            messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run first.")
            sys.exit()
        

    def on_exit(self):
        """On exit this function is run to kill all the processes."""
        popen("warp-cli disconnect").read()
        if sys.platform == "win32":
            subprocess.call('TASKKILL /F /IM "Cloudflare WARP.exe"', shell=True)
        else:
            popen("pkill -f warp-taskbar").read()

        root.quit()


if __name__ == "__main__":
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()
