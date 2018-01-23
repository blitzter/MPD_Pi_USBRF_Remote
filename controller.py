import evdev, mpd, sys, time
from subprocess import call
from evdev import ecodes, categorize

time.sleep(5)
dev = evdev.InputDevice('/dev/input/by-id/usb-AliTV_Remote_V1_Airmouse-event-kbd')
client = mpd.MPDClient(use_unicode=True)
client.connect('localhost', 6600)
status = client.status()
volume = int(status["volume"])

def handle_key_down(code):
    global volume, status, client
    try:
        client.ping()
        status = client.status()
        volume = int(status["volume"])
    except Exception as e:
        client.connect('localhost', 6600)
    if code == None:
        time.sleep(0.2)
    elif ecodes.ecodes['KEY_VOLUMEDOWN'] == code:
        print('KEY_VOLUMEDOWN key pressed')
        if volume > 0:
            volume -= 1
            client.setvol(volume)
        else:
            print("Volume Already Zero!!")
    elif ecodes.ecodes['KEY_VOLUMEUP'] == code:
        print('KEY_VOLUMEUP key pressed')
        if volume < 100:
            volume += 1
            client.setvol(volume)
        else:
            print("Volume Already Max!!")


def handle_key_up(code):
    global volume, status, client
    try:
        client.ping()
        status = client.status()
        volume = int(status["volume"])
    except Exception as e:
        client.connect('localhost', 6600)
    if code == None:
        time.sleep(0.2)
    elif ecodes.ecodes['KEY_MUTE'] == code:
        print('KEY_MUTE key pressed')
        status = client.status()
        if int(status["volume"]) == 0:
            client.setvol(volume)
        else:
            client.setvol(0)
    elif ecodes.ecodes['KEY_POWER'] == code:
        print('KEY_POWER key pressed..... Turning off')
        if sys.platform.startswith('linux'):
            call("sudo nohup shutdown -h now", shell=True)
        else:
            print("Can't PowerOff from remote")
    elif ecodes.ecodes['KEY_NEXTSONG'] == code:
        print('KEY_NEXTSONG key pressed')
        client.next()
    elif ecodes.ecodes['KEY_PLAYPAUSE'] == code:
        print('KEY_PLAYPAUSE key pressed')
        status = client.status()
        if status["state"] == "play":
            client.pause()
            print('Music Paused')
        else:
            client.play()
            print('Music Started')
    elif ecodes.ecodes['KEY_PREVIOUSSONG'] == code:
        print('KEY_PREVIOUSSONG key pressed')
        client.previous()
    elif ecodes.ecodes['KEY_PLAY'] == code:
        status = client.status()
        print('KEY_PLAY key pressed')
        if status["state"] == "play":
            client.pause()
            print('Music Paused')
        else:
            client.play()
            print('Music Started')
    elif ecodes.ecodes['KEY_PAGEUP'] == code:
        print('KEY_PAGEUP key pressed')
    elif ecodes.ecodes['KEY_PAGEDOWN'] == code:
        print('KEY_PAGEDOWN key pressed')

try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            print(categorize(event))
            print(event.value)
            if event.value == 1:  # key down
                handle_key_down(event.code)
            if event.value == 0:  # key up
                handle_key_up(event.code)
except KeyboardInterrupt:
    sys.exit()
