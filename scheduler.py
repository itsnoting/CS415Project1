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
        for i in range(num_elev):
            self._ele_list.append(Elevator(self._up, self._down, num_floors, random.randint(1, num_floors)))

    # def __str__(self):
    #     if os.name == 'nt':
    #         os.system('CLS')
    #     else:
    #         os.system('clear')
    #     result = "Current Occupants:\n"
    #     for i, ele in self._ele_list:
    #         result += "Elevator " + str(i) + ' '
    #         ele_req = ele._in_elevator_floors()
    #         for r in ele_req:
    #             result += ' ' + str(r.in_floor) + '=>' + str(r.out_floor)


    def execute(self):
        for elevator in self._ele_list:
            if elevator._direction == Direction.Up:
                #Up
                next_floor = elevator._find_bot_floor()
                if elevator._current_floor == next_floor:
                    elevator.visiting()
                elif elevator._current_floor > next_floor:
                    elevator._current_floor -= 1
                else:
                    elevator._current_floor += 1

            elif elevator._direction == Direction.Down:
                #Down
                next_floor = elevator._find_top_floor()
                if elevator._current_floor == next_floor:
                    elevator.visiting()
                elif elevator._current_floor > next_floor:
                    elevator._current_floor -= 1
                else:
                    elevator._current_floor += 1

            else:
                #Idle
                next_up_floor = elevator._find_bot_floor()
                next_down_floor = elevator._find_bot_floor()
                if abs(next_up_floor - elevator._current_floor) < abs(elevator._current_floor - next_down_floor):
                    elevator._direction = Direction.Up
                    if elevator._current_floor == next_up_floor:
                        elevator.visiting()
                    elif elevator._current_floor > next_up_floor:
                        elevator._current_floor -= 1
                    else:
                        elevator._current_floor += 1
                else:
                    elevator._direction = Direction.Down
                    if elevator._current_floor == next_down_floor:
                        elevator.visiting()
                    elif elevator._current_floor > next_down_floor:
                        elevator._current_floor -= 1
                    else:
                        elevator._current_floor += 1



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
