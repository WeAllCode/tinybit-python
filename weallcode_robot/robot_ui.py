import tkinter as tk

from .commands import *
from .utils import RobotState

class RobotUI(tk.Tk):
    def __init__(self, robot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.robot = robot
        self.title(f'{robot.display_name}')
        self.geometry('200x100')
        self.resizable(False, False)

        self.main_label = tk.Label(self, text="")
        self.main_label.pack()

        self.cancel_button = tk.Button(self, text='Cancel', command=self.clear_robot)
        self.cancel_button.pack()
        self.redo_button = tk.Button(self, text='Redo', command=self.redo)
        self.redo_button.pack()

    def update(self):
        
        if self.robot.state == RobotState.DISCONNECTED:
            self.main_label['text'] = 'disconnected'
            self.cancel_button['state'] = tk.DISABLED
            self.redo_button['state'] = tk.DISABLED
        elif self.robot.state == RobotState.CONNECTING:
            self.main_label['text'] = 'connecting ...'
            self.cancel_button['state'] = tk.DISABLED
            self.redo_button['state'] = tk.DISABLED
        elif self.robot.state == RobotState.CONNECTED_IDLE:
            self.main_label['text'] = 'idle'
            self.cancel_button['state'] = tk.DISABLED
            self.redo_button['state'] = tk.NORMAL
        elif self.robot.state == RobotState.RUNNING or self.robot.state == RobotState.DONE:
            self.main_label['text'] = 'running ...'
            self.cancel_button['state'] = tk.NORMAL
            self.redo_button['state'] = tk.DISABLED

        super().update()

    def clear_robot(self):
        print('clearing')
        asyncio.create_task(self.robot.commands.clear_immediate())

    def redo(self):
        if self.robot.state == RobotState.CONNECTED_IDLE:
            print('redoing')
            asyncio.create_task(self.robot.commands.restore())
        