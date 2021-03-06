# MPD_Pi_USBRF_Remote

Mpd remote controller example application.
You will need to modify based on your specific remote and configuration/needs.

### My Setup
- ReadOnly raspberry Pi w (16gb sd card, power supply)
- Usb Drive... Music folder for music, mpd folder for mpd library etc, mpd/playlists for mpd playlists
- Asus Usb Sound Card
- Usb RF remote

# Install Guide Steps from new Raspberry Pi which is accessible from ssh
```
sudo apt-get update
sudo apt-get upgrade
sudo rasp-config
```
### Expand filesystem, update, timezone, boot to autologin/console etc
```
sudo apt-get install mpd mpc python-pip python-mpd
sudo pip install evdev
```
### Add this line to /etc/fstab 
```
/dev/sda1	/mnt/sda1	auto	nofail,uid=109,gid=29,noatime	0	0	
```
### Set the following in /etc/mpd.conf for readonly setup
And any other things you may want to set like sound card/ mixer etc
```
music_directory		"/mnt/sda1/Music"
playlist_directory		"/mnt/sda1/mpd/playlists"
db_file			"/mnt/sda1/mpd/tag_cache"
pid_file			"/tmp/mpd.pid"
state_file			"/mnt/sda1/mpd/state"
sticker_file                   "/mnt/sda1/mpd/sticker.sql"
user				"mpd"
bind_to_address		"0.0.0.0"
port             "6600"
save_absolute_paths_in_playlists	"yes"
auto_update    "yes"
```
### Put this at the end of /etc/profile (or any way you want to start a sample script on login)
I chose this just because this is easy but I have to use a check in startup.sh to see if it is the default autologin tty
```
if [ -e /mnt/sda1/scripts/startup.sh ]
then
    echo "Start up file found... executing"
    sh /mnt/sda1/scripts/startup.sh
else
    echo "Start up file not found"
fi
```
### /mnt/sda1/scripts/startup.sh
This can be used to put login message and start up scripts.
This is in USB which is writable even after pi is readonly so you can use this to make other changes
Any installation will not be easy after readonly so make sure you install all you need to future development before making the pi readonly 
```
#!/bin/sh

echo "In Startup Script"
tty=$(tty)
case "$(tty)" in
  /dev/tty1) 
    echo "Starting BlitzMp3Player" > /tmp/start_"$(date +"%Y_%m_%d_%I_%M_%p").log"
    python /mnt/sda1/scripts/controller.py &
    ;;
  *) echo "Startup not required on this tty"
    ;;
esac
```
### Put controller.py in /mnt/sda1/scripts
In the controller.py change the controller device path, mpd connect settings according to your setup.
Also test whether the keys on your remote match ones in the code. 
Change according to what you need the keys to do and maybe add functionality.
### Make raspberry pi readonly
make sure you have tested every thing you need before this step
The link below is a clone of https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/read-only-fs.sh
I didn't want to loose the current version so I made a copy, you can use original too 
It will make it hard to install new libraries but I need a more stable sysem(SD corruption is a big problem)
Make a copy before and after this step... so you can revert if you want
```
wget https://raw.githubusercontent.com/blitzter/Raspberry-Pi-Installer-Scripts/master/read-only-fs.sh
sudo bash read-only-fs.sh
```
