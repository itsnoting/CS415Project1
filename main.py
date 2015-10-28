__author__ = 'Kevin Ting'
import os
import time
from elevator import Elevator

def main():
    elevator = Elevator(10)
    elevator.get_request()
    print elevator
    time.sleep(1)
    elevator.execute_request()

main()
