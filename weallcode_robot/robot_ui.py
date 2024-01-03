import tkinter as tk

from weallcode_robot.commands import *

class RobotUI(tk.Tk):
    def __init__(self, robot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.robot = robot
        self.title(f'{robot.display_name}')
        self.geometry('800x600')
        # self.resizable(False, False)

        self.main_label = tk.Label(self, text="")
        self.main_label.pack()

        self.cancel_button = tk.Button(self, text='Cancel', command=self.clear_robot)
        self.cancel_button.pack()
        self.redo_button = tk.Button(self, text='Redo', command=self.redo)
        self.redo_button.pack()


    def update(self):
        if self.main_label.winfo_exists():
            self.main_label['text'] = self.robot.status_message

        super().update()

    def clear_robot(self):
        self.robot.clear()

    def redo(self):
        print(self.robot.last_command)
        for command in self.robot.last_command:
            self.robot.commands.put(command)
        