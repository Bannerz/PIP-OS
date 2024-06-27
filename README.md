This is my entry into the PIP-BOY python world...

It's written for Python 3.11

You need:
numpy
scipy
requests
pygame
pillow
mutagen

I'm running it on a Raspberry Pi 4B 8GB, on Bookworm, with the WaveShare 4 Inch 480x320 RPiLCD (A). I used their ready made IMG (32bit) for the OS.

It seems to need to boot to desktop before it will run.

I made it run at boot using lxsession. Here are the commands:

sudo nano /home/pi/.config/autostart/pip-os.desktop (I had to make the directory manually)

[Desktop Entry]
Type=Application
Name=PIP-OS
Exec=/home/pi/PIP-OS/start_pip_os.sh

chmod +x /home/pi/PIP-OS/start_pip_os.sh
chmod +x /home/pi/PIP-OS/main.py

I set the desktop BG to black and hid the TaskBar, I also disabled notifications in Panel Settings.

I used this to hide the mouse:
sudo apt-get update
sudo apt-get install unclutter

sudo nano ~/.xsessionrc

unclutter -idle 0.01 &

This minimised the Pi desktop so it looks like a black screen until it boots. You can use a Fallout themed background I guess to make it look better.

Some mentions:
I took heavy inspiration from: https://github.com/zapwizard/pypboy - Thank you!
Although I ended up remaking everything from scratch anyway, this project was invaluable for assets for testing and functionality 

The Atomic Command game is based off of code from this git page: https://github.com/SeijiNoda/Python-Missile-Command/tree/main - Thank you!


