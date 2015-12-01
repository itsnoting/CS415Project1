__author__ = 'Kevin Ting'
import os
import time
from elevator2 import Elevator

from scheduler import Scheduler

def main():
    floor_num = input("Please enter the number of floors:")
    ele_num = input("Please enter the number of elevators:")
    scheduler = Scheduler(ele_num, floor_num)
    # elevator = Elevator(floor_num)
    try:
        while True:
            scheduler.get_request()
            print scheduler
            scheduler.execute()
    except KeyboardInterrupt:
        print "Exiting elevator simulator...."

main()
