from tkinter import Toplevel, Label

class Popup:
    def __init__(self, root, text, bind) -> None:
        self.frame = Toplevel(root)
        label = Label(self.frame, text=text)
        label.pack()
        self.frame.withdraw()
        self.bind(frame=bind)
    
    def on_hover(self, event):
        self.frame.geometry("+%d+%d" % (event.x_root, event.y_root))
        self.frame.overrideredirect(True)
        self.frame.deiconify()  # show the widget

    def on_leave(self, event):
        self.frame.withdraw()  # hide the widget
        return
        
    def bind(self, frame):
        frame.bind("<Enter>", self.on_hover)
        frame.bind("<Leave>", self.on_leave)