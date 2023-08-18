from tkinter import *
from tkinter import messagebox
from os import popen,path, remove
from os.path import exists
from time import sleep
from threading import Thread
from popup import Popup
from settings import Settings, CustomButton
import json, sys,subprocess,webbrowser


# Path changes if you're using the compiled version of the app
if getattr(sys, 'frozen', False):
    path = f"{sys._MEIPASS}/"
else:
    path = ""
    
root = Tk()
rootMenu = Menu(root)
root.title("Cloudflare WARP v1.2.0")
width, height = 470, 200
widthCenter = int(root.winfo_screenwidth() / 2 - width / 2)
heightCenter = int(root.winfo_screenheight() / 2 - height / 2)
root.geometry(f"{str(width)}x{str(height)}+{widthCenter}+{heightCenter}")
root.resizable(False, False)

# To easily use colors and images together this little dict does the job.
visuals = {
    "blue": {"buttons": {"normal": PhotoImage(file=f"{path}assets/blue.png"), "highlight": PhotoImage(file=f"{path}assets/blue_highlight.png")}, "colors": {"normal": "#0466C8", "highlight": "#0074FD"}},
    "red": {"buttons": {"normal": PhotoImage(file=f"{path}assets/red.png"), "highlight": PhotoImage(file=f"{path}assets/red_highlight.png")}, "colors": {"normal": "#BC232D", "highlight": "#DF2935"}},
    "colors": {"bg": "#1E1E1E"},
    "images": {"logo": {"white": PhotoImage(file=f"{path}assets/white.png"), "black": PhotoImage(file=f"{path}assets/black.png"), "orange": PhotoImage(file=f"{path}assets/orange.png")},"pfp": PhotoImage(file=f"{path}assets/pfp.png")},
    "handburger": {"buttons": {"normal": PhotoImage(file=f"{path}assets/menuRed.png"), "highlight": PhotoImage(file=f"{path}assets/menuBlue.png")}},
    "close": {"buttons": {"normal": PhotoImage(file=f"{path}assets/closeRed.png"), "highlight": PhotoImage(file=f"{path}assets/closeBlue.png")}}
}

root.configure(bg=visuals["colors"]["bg"])
if sys.platform == "win32":
    root.iconphoto(True, visuals["images"]["logo"]["black"])
else:
    root.iconphoto(True, visuals["images"]["logo"]["white"])
TASKBAR_STATE = False
ONE_TIME_CHECK = False
# Label(root, image=bgImage).place(x=0, y=0, relheight=1, relwidth=1)


class App:
    def __init__(self, master, refresh):
        self.bg = visuals["colors"]["bg"]
        self.clear = False
        self.startup(refresh)
        self.status = StringVar()
        self.taskbarCheck = True
        Thread(target=self.statusCheck).start()
        self.handburgerMenu(master)
        self.enableFrame(master)
        self.disableFrame(master)
        self.checkboxFrame(master)
        self.statusFrame(master)
        self.taskbar(startup=True)
        self.contextMenu(master)
    # The default menu is left unused, we might make one in the near future.
    def handburgerMenu(self, master, options= False):
        """handburger menu instead fo default menu"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(padx=20, pady=0)
        text = "" if options else ""
        if options is True:
            Label(frame, bg=self.bg, foreground="white",width=30, text=text,font=("Arial", 18)).grid(row=0, column=0)
            self.burgerLabel = self.buttonCreate(master=frame, bg=self.bg, type=visuals["close"], callback=self.handburgerCallback, text="")
            self.burgerLabel.grid(row=0, column=1,pady=5)
            return frame
        self.burgerLabel = self.buttonCreate(master=frame, bg=self.bg, type=visuals["handburger"], callback=self.handburgerCallback, text="")
        self.burgerLabel.grid(row=0, column=0, pady=5)
        Label(frame, bg=self.bg, foreground="white",width=27, text=text,font=("Arial", 18)).grid(row=0, column=1)
        Label(frame, bg=self.bg, foreground="white", width=60).grid(row=0, column=2)
        root.geometry(f"{str(width)}x{str(height)}")
        return frame
    
    def handburgerScreen(self, master):
        frame = Frame(master=master, bg= self.bg)
        frame.pack()
        settings =self.enableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["blue"], callback=self.settingsCallback, text="Settings")
        settings.grid(row=1, column=1, padx=25)
        refresh = self.enableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["blue"], callback=self.refreshCallback, text="Refresh")
        refresh.grid(row=2, column=1, padx=25)
        about = self.enableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["blue"], callback=self.aboutCallback, text="About")
        about.grid(row=3, column=1, padx=25)
        _exit = self.enableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["blue"], callback=root.quit, text="Exit")
        _exit.grid(row=4, column=1, padx=25)
        
        Popup(root=root, text= "App settings.", bind=settings)
        Popup(root=root, text= "This will refresh the app.", bind=refresh)
        Popup(root=root, text= "About the app.", bind= about)
        Popup(root=root, text= "Exit the app.", bind= _exit)
        return True
        
    def handburgerCallback(self):
        if self.clear == False:
            for widget in root.winfo_children():
                widget.destroy()
            self.handburgerMenu(root, options=True)
            self.handburgerScreen(root)
            self.contextMenu(root)
            self.clear = True 
        else:
            self.refreshCallback()

    def contextMenu(self, master):
        """creates a menu"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack()
        self.menu = Menu(
            frame, 
            tearoff=False,
            # bg="#243347", 
            # foreground="white", 
            activebackground=visuals['blue']['colors']['highlight'], 
            activeforeground='White',
            relief=FLAT,
            font=("Arial", 11)
            )
        self.menu.add_command(label="🔄 Refresh", command=self.refreshCallback)
        self.menu.add_command(label="⚙Settings" if sys.platform != "linux" else "⚙ Settings", command=self.settingsCallback)
        self.menu.add_command(label="🐙 About", command=self.aboutCallback)
        self.menu.add_command(label="🛑 Exit", command=self.on_exit)
        return True
    
    def refreshCallback(self):
        for widget in root.winfo_children():
            widget.destroy()
        global TASKBAR_STATE
        TASKBAR_STATE = self.taskbarCheck
        self.__init__(root, refresh=True)
    
    def settingsCallback(self):
        for widget in root.winfo_children():
                widget.destroy()
        self.handburgerMenu(root, options=True)
        self.settingsScreen(root)
        
    def aboutCallback(self):
        for widget in root.winfo_children():
            widget.destroy()
        self.handburgerMenu(root, options=True)
        self.aboutScreen(root)
        
    def aboutScreen(self, master):
        root.geometry(f"{str(width)}x{str(240)}")
        frame = Frame(master=master, bg=self.bg)
        frame.pack()
        image = Button(
            frame,
            image=visuals["images"]["pfp"],
            borderwidth=0,
            command=lambda: Thread(target=self.profileFetch).start(),
            bg=self.bg,
            activebackground=self.bg,
            highlightthickness=0,
            foreground="white",
        )
        image.grid(row=1, column=0)
        Popup(root=root, text= "Click Me!", bind=image)
        Label(frame, text= "This app is an open source project created by DNAMcKnight hosted on Github. Click the link below to go to the download page or visit the website for more details.", justify=CENTER, wraplength=350, bg=self.bg, foreground="white").grid(row=2, column=0)
        button = Frame(master=frame, bg=self.bg)
        self.buttonCreate(master=button, bg=self.bg, type=visuals["blue"], callback=self.releaseFetch, text="Download").grid(row=0,column=0, padx=10)
        self.buttonCreate(master=button, bg=self.bg, type=visuals["blue"], callback=self.websiteFetch, text="Website").grid(row=0,column=1)
        button.grid(row=3,column=0, pady=10)
        
    def settingsScreen(self, master):
        root.geometry(f"{str(width)}x{str(230)}")
        frame = Frame(master=master, bg=self.bg)
        frame.pack()
        Label(frame, text="First Time Startup Message", bg=self.bg, foreground="white", width=25).grid(row=1, column=0)
        CustomButton(master=frame, bg=self.bg, type=visuals, key="startupMsg").button().grid(row=1, column=1, padx=25)
        Label(frame, text="Windows Warning Message", bg=self.bg, foreground="white", width=25).grid(row=2, column=0)
        CustomButton(master=frame, bg=self.bg, type=visuals, key="winWarningMsg").button().grid(row=2, column=1, padx=25)
        Label(frame, text="Taskbar Icon on By Default", bg=self.bg, foreground="white", width=25).grid(row=3, column=0)
        CustomButton(master=frame, bg=self.bg, type=visuals, key="defaultTaskbar").button().grid(row=3, column=1, padx=25)
        Label(frame, text="Auto Connect At Startup", bg=self.bg, foreground="white", width=25).grid(row=4, column=0)
        CustomButton(master=frame, bg=self.bg, type=visuals, key="autoConnect").button().grid(row=4, column=1, padx=25)
        Label(frame, text="Keep connection Alive After Closing", bg=self.bg, foreground="white", width=30).grid(row=5, column=0)
        CustomButton(master=frame, bg=self.bg, type=visuals, key="keepAlive").button().grid(row=5, column=1, padx=25)

    
    def profileFetch(self):
        url = "https://github.com/DNAMcKnight"
        webbrowser.open(url, new = 0, autoraise = True)
        
    def releaseFetch(self):
        url = "https://github.com/DNAMcKnight/CloudflareWarpGUI/releases/"
        webbrowser.open(url, new = 0, autoraise = True)

    def websiteFetch(self):
        url = "https://dnamcknight.github.io/CloudflareWarpGUI/"
        webbrowser.open(url, new = 0, autoraise = True)
    
    def menuCallback(self, coords):
        self.menu.tk_popup(x=coords.x_root+1, y=coords.y_root+1)
    
    # This contains the Text and button all put together in a frame.
    def enableFrame(self, master):
        """Enable frame that has text and a button attached to it"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(pady=5)
        # spacer = Frame(frame, height= 10, bg=self.bg).grid(row=0,pady=10)
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
        if not text:
            width = 32
        else:
            width = 75
        button = Button(
            frame,
            image=type["buttons"]["normal"],
            borderwidth=0,
            text=text,
            command=lambda: Thread(target=callback).start(),
            width=width,
            bg=bg,
            activebackground=bg,
            highlightthickness=0,
            foreground="white",
        )
        button.grid(row=0, column=0)
        if text:
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
            if "colors" in data:
                frame.winfo_children()[1].config(bg=data["colors"]["highlight"])
        else:
            frame.winfo_children()[0].config(image=data["buttons"]["normal"])
            if "colors" in data:
                frame.winfo_children()[1].config(bg=data["colors"]["normal"])
        return True


    def checkboxFrame(self, master):
        """checkbox frame  for the checkbox"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(pady=10)
        self.checkButton = Checkbutton(
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
        self.checkButton.pack()
        self.taskbarText.set("Disable warp taskbar icon")
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
        if sys.platform == "win32":
            root.iconphoto(True, visuals["images"]["logo"]["black"])
        else:
            root.iconphoto(True, visuals["images"]["logo"]["white"])
        return True

    def taskbar(self, startup = False):
        """Enables/disables the taskbar icon on Windows and Linux"""
        global TASKBAR_STATE, ONE_TIME_CHECK
        if Settings().check("defaultTaskbar") and not ONE_TIME_CHECK:
            self.taskbarCheck = False
            ONE_TIME_CHECK = True
        elif TASKBAR_STATE and startup:
            self.taskbarCheck = False
            if sys.platform == "win32":
                subprocess.call('TASKKILL /F /IM "Cloudflare WARP.exe"', shell=True)
            else:
                popen("pkill -f warp-taskbar").read()
                       
        if self.taskbarCheck == False:
            self.taskbarText.set("Disable warp taskbar icon")
            self.checkButton.select()
            self.taskbarCheck = True
            if sys.platform == "win32":
                Thread(target=popen("C:/Program Files/Cloudflare/Cloudflare WARP/Cloudflare WARP.exe").read).start()
            else:
                Thread(target=popen("warp-taskbar").read).start()
        else:
            self.taskbarText.set("Enable warp taskbar icon")
            self.taskbarCheck = False
            if sys.platform == "win32":
                subprocess.call('TASKKILL /F /IM "Cloudflare WARP.exe"', shell=True)
            else:
                popen("pkill -f warp-taskbar").read()
        print(f"taskbar state {TASKBAR_STATE}")
        
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
        if not exists('config.json'):
            Settings().startup()
        with open("config.json", "r") as f:
            data = json.load(f)
            if data["startupMsg"]:
                messagebox.showinfo("Thank You!", "Thank you for using my App, please support me by giving this project a star at https://github.com/DNAMcKnight/CloudflareWarpGUI")
            with open("config.json", "w") as write:
                data["startupMsg"] = False
                json.dump(data, write, indent=2)

    def startup(self, refresh = False):
        """This is responsible to check if the system meets the requirements to run the program"""
        if refresh is False:
            self.introMessage()
        self.taskbarText = StringVar()
        root.bind('<Button-3>', self.menuCallback)
        if sys.version_info.major < 3:
            messagebox.showerror("Error", "The script requires python 3 or above!")
            sys.exit()
        if sys.platform != "linux":
            print(Settings().check('winWarningMsg'))
            if Settings().check('winWarningMsg'):
                msg = messagebox.askokcancel("Warning", "Some features are not yet compatible with windows!")
                if msg is True:
                    Settings().change("winWarningMsg", False)
            command = popen("warp-cli status").read()            
            temp = Label(root, text="Dowloading cloudflare warp please wait...", bg=self.bg, foreground="white")
            if not command:
                temp.pack()
                warp = messagebox.askyesno("Warning", "Warp is required to run this program, would you like to install it?")
                url = "https://cloudflarewarp.com"
                webbrowser.open(url,new = 0, autoraise = True) if warp else ""
                temp.destroy()
                if warp:
                    messagebox.showinfo("Success!","After installing warp please relaunch the app to use it.")
                else:
                    messagebox.showerror("Error", "Warp is required, please install Cloudflare Warp from https://cloudflarewarp.com and try again.")
                sys.exit()
        
        elif (popen("systemctl is-active  warp-svc").read()).rstrip() == "inactive":
            messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run first.")
            sys.exit()
        
        if Settings().check("autoConnect") == True:
            popen("warp-cli connect").read()
            
        
        
    def on_exit(self):
        """On exit this function is run to kill all the processes."""
        if Settings().check('keepAlive') == False:
            popen("warp-cli disconnect").read()
        
        if sys.platform == "win32":
            subprocess.call('TASKKILL /F /IM "Cloudflare WARP.exe"', shell=True)
        else:
            popen("pkill -f warp-taskbar").read()

        sys.exit()



if __name__ == "__main__":
    try:
        app = App(root, False)
        root.protocol("WM_DELETE_WINDOW", app.on_exit)
        root.mainloop()
    except json.decoder.JSONDecodeError:
        remove("config.json")
        messagebox.showinfo("Oops Settings error!","Settings were reset to default due to an error.")
        app = App(root, False)
        root.protocol("WM_DELETE_WINDOW", app.on_exit)
        root.mainloop()