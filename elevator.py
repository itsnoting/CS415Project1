import sys
from enum import Enum
import os
from time import sleep


class Direction(Enum):
    Idle = 0
    Up = 1
    Down = 2


class Request:

    def __init__(self, in_floor, out_floor, ele_num = -1):
        self.in_floor = in_floor
        self.out_floor = out_floor
        self.elevNum = ele_num

    def __str__(self):
        return "<" + str(self.in_floor) + "=>" + str(self.out_floor) + ' ' + str(self.elevNum) + ">"


class Elevator:

    def __init__(self, up, down, elevator_num, num_floors=20, current_floor=1):
        self._current_floor = current_floor
        self._up = up
        self._down = down
        self._num_floors = num_floors
        self._direction = Direction.Idle
        self._goal_floor = 0
        self._elevator_num = elevator_num

    def update_goal_floor(self, direction):
        if self._direction == Direction.Up:
            self._goal_floor = 0
            for r in direction:
                if r.elevNum == self._elevator_num and r.out_floor > self._goal_floor:
                    self._goal_floor = r.out_floor
        elif self._direction == Direction.Down:
            self._goal_floor = self._num_floors + 1
            for r in direction:
                if r.elevNum == self._elevator_num and r.out_floor < self._goal_floor:
                    self._goal_floor = r.out_floor

    def requested_floor(self):
        if self._direction == Direction.Up:
            for r in self._up:
                if (r.elevNum == self._elevator_num and r.out_floor == self._current_floor) or (r.elevNum == -1 and r.in_floor == self._current_floor):
                    return True
        elif self._direction == Direction.Down:
            for r in self._down:
                if (r.elevNum == self._elevator_num and r.out_floor == self._current_floor) or (r.elevNum == -1 and r.in_floor == self._current_floor):
                    return True
        else:
            return False

    def _in_elevator_floors(self):
        requests = []
        for request in self._up:
            if request.elevNum == self._elevator_num:
                requests.append(request)
        for request in self._down:
            if request.elevNum == self._elevator_num:
                requests.append(request)
        return requests

    def _find_bot_floor(self):
        botfloor = self._num_floors + 1
        for r in self._up:
            if r.in_floor < botfloor and r.elevNum == -1:
                botfloor = r.in_floor
        if botfloor > self._num_floors:
            return sys.maxsize
        else:
            return botfloor

    def _find_top_floor(self):
        topfloor = 0
        for r in self._down:
            if r.in_floor > topfloor and r.elevNum == -1:
                topfloor = r.in_floor
        if topfloor > 0:
            return topfloor
        else:
            return sys.maxsize

    def visiting(self):
        if self._direction == Direction.Up:
            for r in self._up[:]:
                if r.elevNum == self._elevator_num:
                    if r.out_floor == self._current_floor:
                       self._up.remove(r)
                elif r.elevNum == -1:
                    # Not in elevator
                    if r.in_floor == self._current_floor:
                        r.elevNum = self._elevator_num

            if not self._up and self._down:
                self._direction = Direction.Down

        elif self._direction == Direction.Down:
            for r in self._down[:]:
                if not r.elevNum == -1:
                    if r.out_floor == self._current_floor:
                        self._down.remove(r)
                elif r.elevNum == -1:
                    # Not in elevator
                    if r.in_floor == self._current_floor:
                        r.elevNum = self._elevator_num
            if not self._down and self._up:
                self._direction = Direction.Up


    def _any_occupants(self, direction):
        for r in direction:
            if r.elevNum == self._elevator_num:
                return True
        return False

