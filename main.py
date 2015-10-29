__author__ = 'Kevin Ting'
import os
import time
from elevator import Elevator

def main():
    floor_num = input("Please enter the number of floors:")
    elevator = Elevator(floor_num)
    try:
        while True:
            elevator.get_request()
            print elevator
            time.sleep(1)
            elevator.execute_request()
            print elevator
    except KeyboardInterrupt:
        print "Exiting elevator simulator...."

main()
