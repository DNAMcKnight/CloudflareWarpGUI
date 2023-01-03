# CloudflareWarpGUI
There are two versions of GUI in this repo
1. `old_app.py` uses the old tkinter that comes built in with python, to run this you don't need anything else other than python.
![preview of old_app.py using builtin Tkinter](/images/tkinter.png "old_app.py")
2. `app.py` uses the customTkinter which is a module based on tkinter but looks far better.
![preview of app.py using builtin customTkinter](/images/customTkinter.png "app.py")
If you wish to use the `launcher.sh` script please make sure it's pointing to the correct script you wish to run

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