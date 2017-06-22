import time

import subprocess
import yeelight
#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pytest


bulbs_json = yeelight.discover_bulbs()
bulbs = []
for b in bulbs_json:
    bulbs.append(yeelight.Bulb(b['ip'], b['port']))


def green():
    for bulb in bulbs:
        bulb.turn_on()
        bulb.set_brightness(100)
        bulb.set_rgb(0, 255, 0)


def red():
    for bulb in bulbs:
        bulb.turn_on()
        bulb.set_brightness(100)
        bulb.set_rgb(255, 0, 0)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == './dojo/dojo.py':
            try:
                subprocess.run(['/usr/bin/python', '-m pytest', './dojo/dojo.py'], check=True)
                green()
            except Exception as e:
                red()

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./dojo', recursive=False)
    observer.start()
    print('starting watching:')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

