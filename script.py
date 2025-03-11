#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

relayPin = 11    # GPIO17
delay = 3


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relayPin, GPIO.OUT)
    GPIO.output(relayPin, GPIO.HIGH)


def open_valve():
    GPIO.output(relayPin, GPIO.HIGH)


def close_valve():
    GPIO.output(relayPin, GPIO.LOW)


def destroy():
    GPIO.output(relayPin, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        open_valve()
        time.sleep(delay)
        close_valve()
    except KeyboardInterrupt:
        destroy()

