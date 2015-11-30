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
        self._direction = Direction.Idle

    def __str__(self):
        if os.name == 'nt':
            os.system('CLS')
        else:
            os.system('clear')
        result = ""
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
                    result += ' ' + str(request.out_floor)
            else:
                result += str(i) + "\t||------------||\t"
                for request in floor_requests:
                    result += ' ' + str(request.out_floor)
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
                    elif request.in_floor > request.out_floor:
                        self._down.append(request)
        except ValueError:
            if raw_request == "reset":
                self._go_to_floor(1)