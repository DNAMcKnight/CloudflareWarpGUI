# CloudflareWarpGUI

## Table of Content
- [What is this?](#what-is-this)
- [How it works](#how-it-works)
- [Using the program](#using-the-program)
- [Windows support](#windows-support)
- [Why does this exist?](#why-does-this-exist)
- [Requirements](#requirements)
- [Downlaod](#downlaod)
- [Note](#note)
- 
# What is this?
Cloudflare WARP created by Cloudflare is a VPN that can be used to unblock websites and ports. Unlike other free VPNs on the internet WARP is a lot faster and as far as I'm aware it has no limits or ID/Passwords to keep up to date. This project was originally made for Linux systems because there is no GUI for Linux users. The GUI is pretty simple and nothing too complicated but I'll eventually add more settings that's available through the CLI.

# How it works
This project uses the command line interface of warp known as `warp-cli`. So in order to run the program you must first install Cloudflare Warp from their website directly https://cloudflarewarp.com or for arch based systems use the AUR repo [cloudflare-warp-bin](https://aur.archlinux.org/packages/cloudflare-warp-bin). To install it on other systems please look it up. The program uses the CLI for you and runs the commands in the background when you interact with the GUI.

# Using the program
Originally when I started I focused on a modern GUI that used customTkinter and a basic one using Tkinter that's built into python. However now the main focus have shifted to the tkinter version and based upon that we've created [releases](https://github.com/DNAMcKnight/CloudflareWarpGUI/releases). The GUI is pretty self explanatory, connect and disconnect button and a tray icon that basically runs the program `Cloudflare Zero Trust` on Linux and the original Cloudflare Warp progam on Windows. The program auto disconnects on exit, this will be configuable in the future.

`main.py` uses the old tkinter that comes built in with python, to run this you don't need anything else other than python.

![preview of main.py using builtin Tkinter](https://raw.githubusercontent.com/DNAMcKnight/CloudflareWarpGUI/main/assets/tkinter.png "main.py")

If you wish to use the `launcher.sh` script please make sure it's pointing to the correct script you wish to run

## Windows support
The `warp cli` can be found on windows as well which means this program should work on windows with some modifications. However there is a GUI for Windows made by Cloudflare. The GUI for windows doesn't give you much control either so over time we'll try to make the program more useful for both Windows and Linux platforms.

## Why does this exist?

I have recently moved completely over from windows to Linux (*I use Arch BTW*) and cause of that transition I can't help but miss a few things from windows such as the Warp GUI that let me easily turn it on or off and also was able to minimize into tray.

While I haven't figured out the tray part yet, I have made a working GUI for now. you can connect and disconnect and it'll show the current status right below it.

# Requirements
- Cloudflare WARP
- Python 3.10 (*or above*)
- customTkinter (*if you're using the customTkinter version*)

You will also need to update the `launcher.sh` permissions to run the app directly
```sh
sudo chmod +x launcher.sh
```
# Downlaod
Make sure you meet the [requirements](#requirements) and download the program from the latest [release](https://github.com/DNAMcKnight/CloudflareWarpGUI/releases)

## Note
If you want to move the script to some other place make sure to update the path location in `launcher`
