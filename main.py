__author__ = 'Kevin Ting'

from elevator import elevator as Elevator

def main():
    elevator = Elevator(10)
    print elevator
    elevator.go_to_floor(5)

main()
