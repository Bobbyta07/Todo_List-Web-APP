import math
import time


class Data:

    def __init__(self):
        self.task_list = []
        self.count = 0

    def add_task(self, task_date, task_name):

        self.task_list.append({"id": self.count, "task": task_name, "date": task_date})

        self.count += 1

    # def display_task(self):
    #     # set time_format empty
    #     self.time_format = []
    #     for task in self.task_list:
    #
    #         if task['time'] > 60:
    #             minute = task['time'] % 60
    #             hour = math.floor(task['time'] / 60)
    #             task_time = f"{hour}H : {minute}Min "
    #
    #         else:
    #             task_time = f"Min {task['time']}:00"
    #
    #         total_seconds = task['time'] * 60
    #
    #         self.time_format.append({"id": task['id'], "task": task['task'], "time": task_time})

    def remove_task(self, task_id):
        self.count = 0

        self.task_list.pop(task_id)

        for items in self.task_list:
            items['id'] = self.count

            self.count += 1





