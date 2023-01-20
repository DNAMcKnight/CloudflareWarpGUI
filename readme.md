# CloudflareWarpGUI
There are two versions of GUI in this repo, but right now the main focus is on the tkinter version
1. `main.py` uses the old tkinter that comes built in with python, to run this you don't need anything else other than python.

![preview of customTkinter-app.py using builtin Tkinter](/images/tkinter.png "main.py")

2. `customTkinter-app.py` uses the customTkinter which is a module based on tkinter but looks far better.

![preview of main.py using builtin customTkinter](/images/customTkinter.png "customTkinter-app.py")

If you wish to use the `launcher.sh` script please make sure it's pointing to the correct script you wish to run

### This app now works on Windows.
Although it does work there's a GUI for Windows made by Cloudflare, however this app will give you more control than to just turn it on or off. All the options will be added as I update the app.

### As a Linux user you're probably thinking "why does this exist?"

I have recently moved completely over from windows to Arch Linux (*I use Arch BTW*) and cause of that transition I can't help but miss a few things from windows such as the Warp GUI that let me easily turn it on or off and also was able to minimize into tray.

While I haven't figured out the tray part yet, I have made a working GUI for now. you can connect and disconnect and it'll show the current status right below it.

# Requirements
- Python 3.10 (*or above*)
- customTkinter (*if you're using the better looking version*)

## You will also need to update the `launcher.sh` permissions to run the app directly
```sh
sudo chmod +x launcher.sh
```
## Note
If you want to move the script to some other place make sure to update the path location in `launcher`
