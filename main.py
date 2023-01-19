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
root.resizable(False, False)
cwd = getcwd()

visuals = {
    "blue": {"buttons": {"normal": PhotoImage(file=f"{cwd}/images/blue.png"), "highlight": PhotoImage(file=f"{cwd}/images/blue_highlight.png")}, "colors": {"normal": "#0466C8", "highlight": "#0074FD"}},
    "red": {"buttons": {"normal": PhotoImage(file=f"{cwd}/images/red.png"), "highlight": PhotoImage(file=f"{cwd}/images/red_highlight.png")}, "colors": {"normal": "#BC232D", "highlight": "#DF2935"}},
    "colors": {"bg": "#1E1E1E"},
    "images": {"logo": {"white": PhotoImage(file=f"{cwd}/images/white.png"), "orange": PhotoImage(file=f"{cwd}/images/orange.png")}},
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
        # self.menu(master)

    def menu(self, master):
        """creates a menu"""
        root.config(menu=rootMenu)
        fileMenu = Menu(rootMenu)
        rootMenu.add_cascade(label="File", menu=fileMenu)
        rootMenu.add_separator()
        fileMenu.add_command(label="Settings", command=master.quit)
        rootMenu.add_separator()
        fileMenu.add_command(label="Exit", command=master.quit)
        return True

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

    def disableFrame(self, master):
        """Disable frame that has text and a button attached to it"""
        frame = Frame(master=master, bg=self.bg)
        frame.pack(pady=5)
        self.enableLabel = Label(frame, text="Disable Cloudflare WARP", bg=self.bg, foreground="white", width=25)
        self.enableLabel.grid(row=1, column=0)
        self.disableButton = self.buttonCreate(master=frame, bg=self.bg, type=visuals["red"], callback=self.disableCallback, text="Disable")
        self.disableButton.grid(row=1, column=1, padx=25)
        return True

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
        frame = Frame(master=master, bg="#344966", width=master.winfo_screenwidth())
        frame.pack(side=BOTTOM, fill=X)
        # df2935
        self.statusLabel = Label(frame, textvariable=self.status, bg="#344966", foreground="white", padx=5, pady=4)
        self.statusLabel.pack(side=LEFT)
        return True

    def enableCallback(self):
        popen("warp-cli connect").read()
        self.statusCheck()
        root.iconphoto(True, visuals["images"]["logo"]["orange"])
        return True

    def disableCallback(self):
        popen("warp-cli disconnect").read()
        self.statusCheck()
        root.iconphoto(True, visuals["images"]["logo"]["white"])
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
        with open("settings.json", "r") as f:
            settings = json.load(f)
            if settings["startupMsg"]:
                messagebox.showinfo("Thank You!", "Thank you for using my App, please support me by giving a star ⭐")
            with open("settings.json", "w") as write:
                settings["startupMsg"] = False
                json.dump(settings, write)

    def startup(self):
        self.introMessage()
        if sys.platform != "linux":
            # messagebox.showerror("Error", "Sorry but this script only works on Linux!")
            # print(sys.platform)
            # sys.exit()
        if sys.version_info.major < 3:
            messagebox.showerror("Error", "The script requires python 3 or above!")
            sys.exit()
        if (popen("systemctl is-active  warp-svc").read()).rstrip() == "inactive":
            messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run first.")
            sys.exit()

    def on_exit(self):
        popen("warp-cli disconnect").read()
        popen("pkill -f warp-taskbar").read()
        root.quit()


if __name__ == "__main__":
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()
