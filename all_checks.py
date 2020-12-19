
import shutil
import sys
import os
import psutil
import socket

def check_reboot():
    """Return True if the computer has a pending reboot."""
    return os.path.exists ("/run/reboot-required")

def check_disk_full(disk,min_gb,min_percent):
    """Return True if there isn't enough disk space, false otherwise."""
    du = shutil.disk_usage(disk)
    #Calcuate the percentage of gree space
    percent_free = 100 * du.free / du.total
    #Calcuate how many gree gigabytes
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free< min_gb:
        return True
    return False

def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full(disk= "/", min_gb=2, min_percent=10)

def check_no_network():
    """Return True if it fails to resolve Google's URL, False otherwise."""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    check = [
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root Partition full"),
        (check_no_network,"No working network"),
    ]
    everything_ok = True

    for check, msg in check:
        if check():
            print (msg)
            everything_ok = False

    if not everything_ok:
        sys.exit(1)

    print("Everything OK.")
    sys.exit(0)

main()
