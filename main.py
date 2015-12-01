__author__ = 'Kevin Ting'
import os
import time
from elevator2 import Elevator

from scheduler import Scheduler

def main():
    # floor_num = input("Please enter the number of floors:")
    # elevator = Elevator(floor_num)
    # try:
    #     while True:
    #         elevator.get_request()
    #         print elevator
    #         time.sleep(1)
    #         elevator.execute_request()
    #         #print elevator
    # except KeyboardInterrupt:
    #     print "Exiting elevator simulator...."
    scheduler = Scheduler(3, 10)
    scheduler.get_request()
    scheduler.execute()

main()
