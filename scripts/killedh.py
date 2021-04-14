#!/usr/bin/env python3
import time

def main():
    while True:
        f = open("/home/pi/script/killedh.txt", "r")
        killed=f.read()
        f.close()
        killed=killed.split("text")
        killed=killed[1].split(":")
        killed=killed[1].split(",")
        killed=str(killed[0])
        chk='"killed"'
        if killed==chk:
            state="Off"
            f = open("/home/pi/script/On Humi.txt", "w")
            f.write(state)
            f.close()
            print("killed")
        else:
            state="On"
            f = open("/home/pi/script/On Humi.txt", "w")
            f.write(state)
            f.close()
            print("Running")
        time.sleep(1)


if __name__ == '__main__':
    main()