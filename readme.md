# CloudflareWarpGUI

## Table of Content
- [What is this?](#what-is-this)
- [How it works](#how-it-works)
- [Using the program](#using-the-program)
- [Windows support](#windows-support)
- [Motivation](#motivation)
- [Requirements](#requirements)
- [Download](#download)
- [Note](#note)


# What is this?
Cloudflare WARP is a fast VPN service offered by Cloudflare. It unblocks websites and ports that has no limits or login credentials to manage. This project was originally made for Linux systems because there is no GUI for Linux users. The GUI that has been developed is user-friendly and intuitive, even for those who are new to VPNs. While the current GUI is simple and straightforward, I am continuously working to add more advanced settings and options that can be accessed through the command line interface (CLI).

# How it works
The program utilizes the `warp-cli` command line interface, which can be installed from the [Cloudflare website](https://cloudflarewarp.com) or for arch based systems use the AUR repo [cloudflare-warp-bin](https://aur.archlinux.org/packages/cloudflare-warp-bin). To install it on other systems please look it up. The GUI runs commands in the background via the CLI when the user interacts with it.

# Using the program
This program is a graphical user interface (GUI) for the Cloudflare Warp service, which provides a secure and fast connection for your internet traffic.

The main focus of this program is the Tkinter version, which is built into Python, and there are releases available in the [download](#download) section. The GUI is easy to use, with a connect and disconnect button and a tray icon. The tray icon on Linux runs the `Cloudflare Zero Trust` program, while on Windows, it runs the original `Cloudflare Warp` program. Currently, the program automatically disconnects on exit, but this feature will be configurable in the future.

![Preview of main.py using built-in Tkinter](https://raw.githubusercontent.com/DNAMcKnight/CloudflareWarpGUI/main/screenshots/tkinter.png "main.py")

![Preview of about section of the app](https://raw.githubusercontent.com/DNAMcKnight/CloudflareWarpGUI/main/screenshots/about.png "about")

## Windows support
The `warp cli` can be found on windows as well which means this program should work on windows with some modifications. However there is already a GUI provided by Cloudflare, but this project aims to make it more useful for both Windows and Linux platforms over time.

## Motivation
Recently, I made a complete transition from Windows to Linux (using Arch Linux) and encountered some challenges. One of the features I missed from Windows was the "Warp GUI" that allowed me to easily turn my VPN connection on or off and also minimize it into the system tray.

Although I am still working on finding a solution for the system tray aspect, I have developed a working GUI that allows you to connect and disconnect to your VPN and displays the current status right below the button.

# Requirements
- Cloudflare WARP
- Python 3.10 (*or above*)
- customTkinter (*if you're using the customTkinter version*)

In order to run the program, you need to update the permissions of the `launcher.sh` script by running `sudo chmod +x launcher.sh` in a terminal.

# Download
Make sure you meet the [requirements](#requirements) and download the program from the latest [release](https://github.com/DNAMcKnight/CloudflareWarpGUI/releases).

## Note
If you want to move the script to some other place make sure to update the path location in `launcher`

Time I spent on this project so far ↙️

[![CloudflareWarpGUI](https://wakatime.com/badge/user/fb640bef-8826-45d4-89a9-dc6e12cf9ebd/project/862a461a-4cb7-45b6-bbad-fa88e1d84a88.svg)](https://wakatime.com/badge/user/fb640bef-8826-45d4-89a9-dc6e12cf9ebd/project/862a461a-4cb7-45b6-bbad-fa88e1d84a88)
