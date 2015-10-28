__author__ = 'Kevin Ting'
from enum import Enum
import os
import sys
from time import sleep


class Direction(Enum):
    Up = 1
    Down = 2


class Elevator:
    # PRIVATE VARIABLES
    # =======================================================================
    # current_floor:    Represents the current floor
    #                   Defaults to floor 1
    # requests:         Contains all the requests
    #                   Defaults to an empty array
    # number of floors: Represents the total number of floors in the building
    #                   Defaults to a 20 story building
    # ========================================================================
    # PRIVATE FUNCTIONS
    # ========================================================================
    # closest floor:    Returns the closest floor based on elevator direction
    # go to floor:      Moves to elevator to the specified floor
    # *add request:      Add a request to the array of requests
    # go up:            Increments the elevator by one floor
    # go down:          Decrements the elevator by one floor
    # animate:          Animates the elevator's execution
    # ========================================================================
    def __init__(self, num_floors = 20, current_floor = 1):
        self._current_floor = current_floor
        self._requests = []
        self._up = []
        self._down = []
        self._num_floors = num_floors
        self._direction = Direction.Up

    def __str__(self):
        if os.name == 'nt':
            os.system('CLS')
        else:
            os.system('clear')
        result = ""
        for i in range(self._num_floors, 0, -1):
            floor_requests = []
            for request in self._requests:
                if request[0] == i:
                    floor_requests.append(request)
            if i == self._current_floor:
                result += str(i) + "\t||----[0]----||\t"
                for request in floor_requests:
                    result += ' ' + str(request[1])
            else:
                result += str(i) + "\t||-----------||\t"
                for request in floor_requests:
                    result += ' ' + str(request[1])
            result += '\n'
        return result

    def _closest_request(self):
        closest = sys.maxsize

        if self._direction == Direction.Up:
            for request in self._requests:
                diff = request[0] - self._current_floor
                if 0 < diff <= (closest - self._current_floor):
                    closest = request[0]

        elif self._direction == Direction.Down:
            for request in self._requests:
                diff = self._current_floor - request[0]
                if 0 < diff <= (self._current_floor - closest):
                    closest = request[0]

        return closest

    def _go_to_floor(self, floor):
        if isinstance(floor, int):
            if floor > self._current_floor:
                for i in range(floor - self._current_floor):
                    self._go_up()
                    self._animate()
                self._up.remove(floor)
            elif floor < self._current_floor:
                for i in range(self._current_floor - floor):
                    self._go_down()
                    self._animate()
                self._down.remove(floor)

    def _add_request(self, request):
        if len(request) == 2:
            self._requests.append(request)

    def _go_up(self):
        self._current_floor += 1
        self._up.sort()

    def _go_down(self):
        self._current_floor -= 1
        self._down.sort(reverse=True)

    def _animate(self):
        print self
        sleep(.5)



    # PUBLIC FUNCTIONS
    # =========================================================================
    # get requests:         Returns the list of requests
    # =========================================================================
    def get_request(self):
        try:
            requests = []
            while True:
                raw_request = raw_input("What is your request?: \n")
                request = [int(num.strip()) for num in raw_request.split(',')]
                if not len(request) == 2:
                    print "Invalid input"
                else:
                    requests.append(request)
        except ValueError:
            self._requests = requests
            return requests


