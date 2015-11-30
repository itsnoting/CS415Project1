__author__ = 'Kevin Ting'
from enum import Enum
import os
import sys
from time import sleep


class Direction(Enum):
    Idle = 0
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
    def __init__(self, num_floors=20, current_floor=1):
        self._current_floor = current_floor
        self._requests = []
        self._up = []
        self._down = []
        self._num_floors = num_floors
        self._direction = Direction.Idle

    def __str__(self):
        if os.name == 'nt':
            os.system('CLS')
        else:
            os.system('clear')
        result = ""
        num_floor = len(self._up) + len(self._down)
        if num_floor < 10:
            num_floor = '0' + str(num_floor)
        else:
            num_floor = str(num_floor)
        for i in range(self._num_floors, 0, -1):
            floor_requests = []
            for request in self._requests:
                if request[0] == i:
                    floor_requests.append(request)
            if i == self._current_floor:
                result += str(i) + "\t||----[" + num_floor + "]----||\t"
                for request in floor_requests:
                    result += ' ' + str(request[1])
            else:
                result += str(i) + "\t||------------||\t"
                for request in floor_requests:
                    result += ' ' + str(request[1])
            result += '\n'
        return result

    def _closest_request(self):
        closest = None
        closest_requests = []
        if self._direction == Direction.Up:
            closest = sys.maxsize
            for request in self._requests:
                diff = request[0] - self._current_floor
                print 0 < diff < (closest - self._current_floor)
                if 0 <= diff <= (closest - self._current_floor):
                    closest = request[0]
                    closest_requests.append(request)
        elif self._direction == Direction.Down:
            closest = -sys.maxsize
            for request in self._requests:
                diff = self._current_floor - request[0]
                if 0 <= diff <= (self._current_floor - closest):
                    closest = request[0]
                    closest_requests.append(request)
        elif self._direction == Direction.Idle:
            closest = sys.maxsize
            for request in self._requests:
                diff = abs(request[0] - self._current_floor)
                if 0 <= diff <= (closest - self._current_floor):
                    closest = request[0]
                    closest_requests.append(request)
            if closest_requests[0][0] > closest_requests[0][1]:
                self._direction = Direction.Down
            if closest_requests[0][0] < closest_requests[0][1]:
                self._direction = Direction.Up

        for closest_request in closest_requests:
            if closest_request[0] == self._current_floor:
                self._requests.remove(closest_request)
                if self._direction == Direction.Up:
                    self._up.append(closest_request[1])
                elif self._direction == Direction.Down:
                    self._down.append(closest_request[1])
        return closest

    def _highest_down(self):
        highest = 0
        for request in self._requests:
            if request[0] - request[1] > 0:
                if request[0] > highest:
                    highest = request[0]
        return highest

    def _go_to_floor(self, floor):
        self._up.sort()
        self._down.sort(reverse=True)
        if isinstance(floor, int):
            if floor > self._current_floor:
                for i in range(floor - self._current_floor):
                    self._go_up()
                    self._animate()
                self._up = filter(lambda a: a != floor, self._up)
            elif floor < self._current_floor:
                for i in range(self._current_floor - floor):
                    self._go_down()
                    self._animate()
                self._down = filter(lambda a: a != floor, self._down)

    def _add_request(self, request):
        if len(request) == 2:
            self._requests.append(request)

    def _go_up(self):
        for request in self._requests:
            if request[0] == self._current_floor and request[0] < request[1]:
                self._up.append(request[1])
                self._up.sort()
                self._requests.remove(request)
        if self._up:
            if self._up[0] == self._current_floor:
                self._up = filter(lambda a: a != self._current_floor, self._up)
        self._current_floor += 1

    def _go_down(self):
        for request in self._requests:
            if request[0] == self._current_floor and request[0] > request[1]:
                self._down.append(request[1])
                self._down.sort(reverse=True)
                self._requests.remove(request)
        if self._down:
            if self._down[0] == self._current_floor:
                self._down = filter(lambda a: a != self._current_floor, self._down)
        self._current_floor -= 1

    def _animate(self):
        print self._requests
        print self._up
        print self._down
        print self
        sleep(1)



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
                for i in range(2):
                    if request[i] < 1 or request[i] > self._num_floors:
                        print "Invalid input"
                if not len(request) == 2:
                    print "Invalid input"
                else:
                    requests.append(request)
        except ValueError:
            self._requests = requests
            if raw_request == "reset":
                self._go_to_floor(1)
            return requests

    def execute_request(self):
        while self._requests or self._up or self._down:
            if self._current_floor == 9:
                print 9
            # Initial request
            if self._direction == Direction.Up:
                if self._up:
                    for request in self._up:
                        self._go_to_floor(request)
                else:
                    if self._down:
                        self._direction = Direction.Down
                        for request in self._down:
                            self._go_to_floor(request)
                    else:
                        self._direction = Direction.Idle

            elif self._direction == Direction.Down:
                if self._down:
                    for request in self._down:
                        self._go_to_floor(request)
                else:
                    if self._up:
                        self._direction = Direction.Up
                        for request in self._up:
                            self._go_to_floor(request)
                    else:
                        self._direction = Direction.Idle
            else:
                closest = self._closest_request()
                if closest > self._current_floor:
                    self._direction = Direction.Up
                elif closest < self._current_floor:
                    self._direction = Direction.Down
                    closest = self._highest_down()
                else:
                    if self._up:
                        self._direction = Direction.Up
                    if self._down:
                        self._direction = Direction.Down
                    continue
                self._go_to_floor(closest)

            # if not self._up and not self._down:
            #     self._direction = Direction.Idle
            #     self._go_to_floor(self._closest_request())
            # # If there are no more up requests, then switch to satisfy down requests
            # elif self._up and not self._down and not self._direction == Direction.Up:
            #     print "Going up!"
            #     self._direction = Direction.Up
            #
            # elif self._up and self._direction == Direction.Up:
            #     for request in self._up:
            #         self._go_to_floor(request)
            # elif self._down and not self._up and not self._direction == Direction.Down:
            #     print "Going down!"
            #     self._direction = Direction.Down
            # elif self._down and self._direction == Direction.Down:
            #     for request in self._down:
            #         self._go_to_floor(request)



