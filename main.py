__author__ = 'Kevin Ting'
import os
import time
from elevator import Elevator

def main():
<<<<<<< HEAD
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
=======
    num_floors = input("How many floors would you like?\n")
    elevator = Elevator(num_floors)
    elevator.get_request()
    print elevator
    time.sleep(1)
    elevator.execute_request()
>>>>>>> fced8cf16bbae1de4c3d943d44bdb9cb1b47446e

main()
