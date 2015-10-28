__author__ = 'Kevin Ting'
import os
import time
from elevator import Elevator

def main():
    num_floors = input("How many floors would you like?\n")
    elevator = Elevator(num_floors)
    elevator.get_request()
    print elevator
    time.sleep(1)
    elevator.execute_request()

main()
