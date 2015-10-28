__author__ = 'Kevin Ting'

from elevator import elevator as Elevator

def main():
    elevator = Elevator(10)
    print elevator
    elevator.get_request()
    print elevator

main()
