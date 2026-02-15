from uasyncio import sleep_ms
from usys import print_exception
from uos import mount, umount, statvfs

mount("/sd", "/sdcard")