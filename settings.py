from pathlib import Path
from tkinter import Frame, Button, Label
from threading import Thread
import json, sys, traceback


class Settings:
    def __init__(self) -> None:
        self.default = {
            "startupMsg": True,
            "winWarningMsg": True,
            "defaultTaskbar": False,
            "autoConnect": False,
            "keepAlive": False
                        }
    def startup(self) -> bool:
        settings = Path(f'config.json')
        if settings.exists():
            return True
        with open('config.json', 'w') as f:
            json.dump(self.default, f, indent=2)
        return False

    def change(self,key: str, value: bool) -> bool:
        with open(f"config.json", "r") as f:
            data = json.load(f)
            with open(f"config.json", "w") as write:
                data[key] = value
                json.dump(data, write, indent=2)
                return True
        return False

    def check(self,key: str) -> bool:
        try:
            with open(f"config.json", "r") as f:
                data = json.load(f)
                if key in data:
                    if data[key] != True and data[key] != False:
                        print("returning default")
                        return self.default[key]
                    return data[key]
                return None
        except json.decoder.JSONDecodeError:
            print("decode error")
            return self.default[key]

    
class CustomButton(Settings):
    def __init__(self, master, bg, type, key):
        self.master = master
        self.bg = bg
        self.type = type
        self.key = key
        self.state = self.check(key)
        self.text = "Disable" if self.state == True else "Enable"
        
    def button(self):
        frame = Frame(master=self.master, bg=self.bg)
        type = self.type["blue"] if self.text == "Enable" else self.type["red"]
        if not self.text:
            width = 32
        else:
            width = 75
        self.button = Button(
            frame,
            image=type["buttons"]["normal"],
            borderwidth=0,
            text=self.text,
            command=lambda: Thread(target=self.buttonCallback, args=(frame,)).start(),
            width=width,
            bg=self.bg,
            activebackground=self.bg,
            highlightthickness=0,
            foreground="white",
        )
        self.button.grid(row=0, column=0)
        if self.text:
            buttonText = Label(frame, text=self.text, bg=type["colors"]["normal"], foreground="white")
            buttonText.grid(row=0, column=0)
            buttonText.bind("<Button-1>", lambda event: self.button.invoke())
        frame.bind("<Enter>", lambda event: self.buttonHighlight(frame, "Enter", self.type))
        frame.bind("<Leave>", lambda event: self.buttonHighlight(frame, "Leave", self.type))
        return frame
        
    def buttonCallback(self, frame):
        self.change(self.key, value=not self.state)
        self.state = self.check(self.key)
        print(frame.winfo_children())
        if self.state:
            frame.winfo_children()[0].config(image=self.type['red']["buttons"]["normal"])
            frame.winfo_children()[1].config(bg=self.type['red']["colors"]["normal"], text="Disable")
            return
        else:
            frame.winfo_children()[0].config(image=self.type['blue']["buttons"]["normal"])
            frame.winfo_children()[1].config(bg=self.type['blue']["colors"]["normal"], text="Enable")
            return
    
    def buttonHighlight(self, frame, state, data):
        """Changes the highlight depending on the backgound color"""
        if self.state:
            data = data['red']
        else:
            data = data['blue']
        if state == "Enter":
            frame.winfo_children()[0].config(image=data["buttons"]["highlight"])
            if "colors" in data:
                frame.winfo_children()[1].config(bg=data["colors"]["highlight"])
        else:
            frame.winfo_children()[0].config(image=data["buttons"]["normal"])
            if "colors" in data:
                frame.winfo_children()[1].config(bg=data["colors"]["normal"])
        return True
    