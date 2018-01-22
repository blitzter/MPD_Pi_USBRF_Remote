import asyncio, evdev, mpd, sys, time
from subprocess import call
from evdev import ecodes

client = mpd.MPDClient(use_unicode=True)
client.connect('localhost', 6600)
status = client.status()
volume = int(status["volume"])

@asyncio.coroutine
def print_events(device):
    global volume, status, client
    while True:
        events = yield from device.async_read()
        for event in events:
            if ecodes.ecodes['KEY_MUTE'] == event.code:
                print('KEY_MUTE key pressed')
                status = client.status()
                if int(status["volume"]) == 0:
                    client.setvol(volume)
                else:
                    client.setvol(0)
            elif ecodes.ecodes['KEY_VOLUMEDOWN'] == event.code:
                print('KEY_VOLUMEDOWN key pressed')
                if volume > 0:
                    volume -= 1
                    client.setvol(volume)
                else:
                    print("Volume Already Zero!!")
            elif ecodes.ecodes['KEY_VOLUMEUP'] == event.code:
                print('KEY_VOLUMEUP key pressed')
                if volume < 100:
                    volume += 1
                    client.setvol(volume)
                else:
                    print("Volume Already Max!!")
            elif ecodes.ecodes['KEY_POWER'] == event.code:
                print('KEY_POWER key pressed..... Turning off')
                if sys.platform.startswith('linux'):
                    call("sudo nohup shutdown -h now", shell=True)
                else:
                    print("Can't PowerOff from remote")
            elif ecodes.ecodes['KEY_NEXTSONG'] == event.code:
                print('KEY_NEXTSONG key pressed')
                client.next()
            elif ecodes.ecodes['KEY_PLAYPAUSE'] == event.code:
                print('KEY_PLAYPAUSE key pressed')
                status = client.status()
                if status["state"] == "play":
                    client.pause()
                    print('Music Paused')
                else:
                    client.play()
                    print('Music Started')
            elif ecodes.ecodes['KEY_PREVIOUSSONG'] == event.code:
                print('KEY_PREVIOUSSONG key pressed')
                client.previous()
            elif ecodes.ecodes['KEY_PLAY'] == event.code:
                status = client.status()
                print('KEY_PLAY key pressed')
                if status["state"] == "play":
                    client.pause()
                    print('Music Paused')
                else:
                    client.play()
                    print('Music Started')
            elif ecodes.ecodes['KEY_PAGEUP'] == event.code:
                print('KEY_PAGEUP key pressed')
            elif ecodes.ecodes['KEY_PAGEDOWN'] == event.code:
                print('KEY_PAGEDOWN key pressed')
        time.sleep(1)



keybd = evdev.InputDevice('/dev/input/by-id/usb-AliTV_Remote_V1_Airmouse-event-kbd')

asyncio.async(print_events(keybd))

loop = asyncio.get_event_loop()
loop.run_forever()
