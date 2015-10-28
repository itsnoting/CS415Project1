__author__ = 'Kevin Ting'
import os
from elevator import Elevator

def main():
    elevator = Elevator(10)
    elevator.get_request()
    print elevator

main()
