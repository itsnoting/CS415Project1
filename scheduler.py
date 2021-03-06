import sys
from time import sleep

from elevator import Elevator
from elevator import Request
from elevator import Direction
import random
import os


class Scheduler:
    def __init__(self, num_elev, num_floors):
        self._ele_list = []
        self._up = []
        self._down = []
        self._num_floors = num_floors
        for i in range(num_elev):
            self._ele_list.append(Elevator(self._up, self._down, i, num_floors, random.randint(1, num_floors)))

    def __str__(self):
        if os.name == 'nt':
            os.system('CLS')
        else:
            os.system('clear')
        ele_info = []
        result = "Current Occupants:\n"
        for i, ele in enumerate(self._ele_list):
            result += "Elevator " + str(i) + ': \t\t'
            ele_req = ele._in_elevator_floors()

            if len(ele._in_elevator_floors()) < 10:
                num_floor = '0' + str(len(ele._in_elevator_floors()))
            else:
                num_floor = str(len(ele._in_elevator_floors()))

            ele_info.append([ele, num_floor])
            if ele._direction == Direction.Up:
                dir_string = "Up"
            elif ele._direction == Direction.Down:
                dir_string = "Down"
            else:
                dir_string = "Idle"
            for r in ele_req:
                result += ' ' + str(r.in_floor) + '=>' + str(r.out_floor)
            result += '|Current Floor: ' + str(ele._current_floor) + ' |Direction: ' + dir_string +'\n'
        for i in range(self._num_floors, 0, -1):
            result += str(i) + "\t||----"
            for ele in ele_info:
                if ele[0]._current_floor == i:
                    result += '[' + ele[1] + ']' + '---'
                else:
                    result += '-------'
            result += '-||\t'
            for r in self._up:
                if r.in_floor == i and r.elevNum == -1:
                    result += str(r.in_floor) + '=>' + str(r.out_floor) + ' '
            result += '\n'
        return result


        result += "Up:\t"
        for r in self._up:
            result += ' ' + str(r)
        result += '\n'
        result += 'Down:\t'
        for r in self._down:
            result += ' ' + str(r)
        result += '\n'
        return result

    def execute(self):
        while self._up or self._down:
            for elevator in self._ele_list:
                if elevator._direction == Direction.Up:
                    if not elevator._any_occupants(elevator._up):
                        #Up
                        next_floor = elevator._find_bot_floor()
                        if not next_floor == sys.maxsize:
                            if elevator._current_floor == next_floor:
                                elevator.visiting()
                            elif elevator._current_floor > next_floor:
                                elevator._current_floor -= 1
                            else:
                                elevator._current_floor += 1
                    else:
                        elevator.update_goal_floor(self._up)
                        if elevator.requested_floor():
                            elevator.visiting()
                            if not elevator._any_occupants(elevator._up):
                                elevator._direction = Direction.Idle
                        elif elevator._current_floor < elevator._goal_floor:
                            elevator._current_floor += 1


                elif elevator._direction == Direction.Down:
                    if not elevator._any_occupants(self._down):
                        #Down
                        next_floor = elevator._find_top_floor()
                        if not next_floor == sys.maxsize:
                            if elevator._current_floor == next_floor:
                                elevator.visiting()
                            elif elevator._current_floor > next_floor:
                                elevator._current_floor -= 1
                            else:
                                elevator._current_floor += 1
                    else:
                        elevator.update_goal_floor(self._down)
                        if elevator.requested_floor():
                            elevator.visiting()
                            if not elevator._any_occupants(self._down):
                                elevator._direction = Direction.Idle
                        elif elevator._current_floor > elevator._goal_floor:
                            elevator._current_floor -= 1

                elif elevator._direction == Direction.Idle:
                    #Idle
                    next_up_floor = elevator._find_bot_floor()
                    next_down_floor = elevator._find_top_floor()
                    if abs(next_up_floor - elevator._current_floor) < abs(elevator._current_floor - next_down_floor):
                        if next_up_floor <= self._num_floors:
                            elevator._direction = Direction.Up
                            if elevator._current_floor == next_up_floor:
                                elevator.visiting()
                            elif elevator._current_floor > next_up_floor:
                                elevator._current_floor -= 1
                            else:
                                elevator._current_floor += 1
                    else:
                        if next_down_floor <= self._num_floors:
                            elevator._direction = Direction.Down
                            if next_down_floor <= self._num_floors:
                                if elevator._current_floor == next_down_floor:
                                    elevator.visiting()
                                elif elevator._current_floor > next_down_floor:
                                    elevator._current_floor -= 1
                                else:
                                    elevator._current_floor += 1
            print self
            sleep(1)



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
            print "Bad input"
