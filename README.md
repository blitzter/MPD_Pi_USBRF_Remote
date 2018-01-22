# MPD_Pi_USBRF_Remote

Mpd remote controller example application.
You will need to modify based on your specific remote and configuration/needs.

## My Setup
### ReadOnly raspberry Pi w
### Usb Drive... Music folder for music, mpd folder for mpd library etc, mpd/playlists for mpd playlists
### Asus Usb Sound Card
### Usb RF remote

# Install Guide Steps from new Raspberry Pi which is accessible from ssh
```
sudo apt-get update
sudo apt-get upgrade
sudo rasp-config
```
>expand filesystem, update, timezone etc
```
sudo apt-get install mpd mpc
```
>add this line to /etc/fstab 
```
/dev/sda1	/mnt/sda1	auto	nofail,uid=109,gid=29,noatime	0	0	
```
>set the following in /etc/mpd.conf for readonly setup
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
