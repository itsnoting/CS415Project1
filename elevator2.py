from enum import Enum
import os
import sys
from time import sleep


class Direction(Enum):
    Idle = 0
    Up = 1
    Down = 2


class Request:

    def __init__(self, in_floor, out_floor):
        self.in_floor = in_floor
        self.out_floor = out_floor
        self.in_elevator = False


class Elevator:

    def __init__(self, num_floors=20, current_floor=1):
        self._current_floor = current_floor
        self._up = []
        self._down = []
        self._num_floors = num_floors
        self._direction = Direction.Up

    def __str__(self):
        if os.name == 'nt':
            os.system('CLS')
        else:
            os.system('clear')
        result = "Current Occupants:"
        for r in self._up:
            if r.in_elevator:
                result += ' '+ str(r.in_floor) + '=>' + str(r.out_floor)
        for r in self._down:
            if r.in_elevator:
                result += ' '+ str(r.in_floor) + '=>' + str(r.out_floor)
        result +='\n'
        floor_requests = self._in_elevator_floors()
        num_floor = len(floor_requests)
        if num_floor < 10:
            num_floor = '0' + str(num_floor)
        else:
            num_floor = str(num_floor)
        for i in range(self._num_floors, 0, -1):
            floor_requests = []
            for request in self._up:
                if request.in_floor == i:
                    floor_requests.append(request)
            for request in self._down:
                if request.in_floor == i:
                    floor_requests.append(request)
            if i == self._current_floor:
                result += str(i) + "\t||----[" + num_floor + "]----||\t"
                for request in floor_requests:
                    if not request.in_elevator:
                        result += ' ' + str(request.in_floor) + '=>' + str(request.out_floor)
            else:
                result += str(i) + "\t||------------||\t"
                for request in floor_requests:
                    if not request.in_elevator:
                        result += ' ' + str(request.in_floor) + '=>' + str(request.out_floor)
            result += '\n'
        return result

    def _in_elevator_floors(self):
        requests = []
        for request in self._up:
            if request.in_elevator:
                requests.append(request)
        for request in self._down:
            if request.in_elevator:
                requests.append(request)
        return requests

    def _find_bot_floor(self):
        botfloor = self._num_floors + 1
        for r in self._up:
            if r.in_floor < botfloor and not r.in_elevator:
                botfloor = r.in_floor
        if botfloor > self._num_floors:
            return self._current_floor
        else:
            return botfloor

    def _find_top_floor(self):
        topfloor = 0
        for r in self._down:
            if r.in_floor > topfloor:
                topfloor = r.in_floor
        return topfloor

    def visiting(self):
        if self._direction == Direction.Up:
            for r in self._up:
                if r.in_elevator:
                    if r.out_floor == self._current_floor:
                        self._up.remove(r)
                else:
                    # Not in elevator
                    if r.in_floor == self._current_floor:
                        r.in_elevator = True
            if not self._up and self._down:
                self._direction = Direction.Down

        elif self._direction == Direction.Down:
            for r in self._down:
                if r.in_elevator:
                    if r.out_floor == self._current_floor:
                        self._down.remove(r)
                else:
                    # Not in elevator
                    if r.in_floor == self._current_floor:
                        r.in_elevator = True
            if not self._down and self._up:
                self._direction = Direction.Up

    def _go_to(self, floor):
        print self._current_floor
        for i in range(abs(self._current_floor - floor)):
            if floor < self._current_floor:
                self._current_floor -= 1
            elif floor > self._current_floor:
                if self._find_bot_floor() == self._current_floor:
                    self.visiting()
                self._current_floor += 1
            print self
            sleep(.5)
        self.visiting()
        print self
        sleep(.5)

    def _any_occupants(self, direction):
        for r in direction:
            if r.in_elevator:
                return True

    def execute_request(self):
        while self._up or self._down:
            if self._direction == Direction.Up:
                self._go_to(self._find_bot_floor())
                if self._any_occupants(self._up):
                    for r in self._up:
                        self._go_to(r.out_floor)

            elif self._direction == Direction.Down:
                if not self._any_occupants(self._down):
                    self._go_to(self._find_top_floor())

    def get_request(self):
        try:
            while True:
                raw_request = raw_input("What is your request?: \n")
                request = [int(num.strip()) for num in raw_request.split(',')]

                for i in range(2):
                    if request[i] < 1 or request[i] > self._num_floors:
                        print "Invalid input"
                if not len(request) == 2:
                    print "Invalid input"
                else:
                    request = Request(request[0],request[1])
                    if request.in_floor < request.out_floor:
                        self._up.append(request)
                        self._up.sort(key=lambda x: x.out_floor)
                    elif request.in_floor > request.out_floor:
                        self._down.append(request)
                        self._down.sort(key=lambda x: x.out_floor, reverse=True)
        except ValueError:
            if raw_request == "reset":
                self._go_to_floor(1)