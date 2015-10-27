__author__ = 'Kevin Ting'

import os
from time import sleep

class elevator:
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
    # go up:            Increments the elevator by one floor
    # go down:          Decrements the elevator by one floor
    # animate:          Animates the elevator's execution
    # ========================================================================
    def __init__(self, num_floors = 20, current_floor = 1):
        self._current_floor = current_floor
        self._requests = []
        self._num_floors = num_floors

    def __str__(self):
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

    def _add_request(self, request):
        if len(request) == 2:
            self._requests.append(request)

    def _go_up(self):
        self._current_floor += 1

    def _go_down(self):
        self._current_floor -= 1

    def _animate(self):
        print self
        sleep(.5)


    # PUBLIC FUNCTIONS
    # =========================================================================
    # set requests:         Sets the list of request for the elevator
    # get requests:         Returns the list of requests
    # set current floor:    Sets the current floor the elevator is on
    # get current floor;    Returns the current floor the elevator is located
    # go to floor:          Implements the go up, go down and animate functions
    #                       to display what the elevator is doing
    # =========================================================================
    def set_requests(self, requests):
        self._requests = requests

    def get_requests(self):
        return self._requests

    def set_current_floor(self, current_floor):
        self._current_floor = current_floor

    def get_current_floor(self):
        return self._current_floor

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
            return requests


    def go_to_floor(self, floor):
        if isinstance(floor, int):
            if floor > self._current_floor:
                for i in range(floor - self._current_floor):
                    self._go_up()
                    self._animate()
            elif floor < self._current_floor:
                for i in range(self._current_floor - floor):
                    self._go_down()
                    self._animate()


