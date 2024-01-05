import threading
import queue
import asyncio
from enum import Enum

buttons_characteristic_uuid = '1A270002-C2ED-4D11-AD1E-FC06D8A02D37'

device_name_map = {
    "beep": "WAC-2463",
    "boop": "WAC-7F36",
    "buzz": "WAC-98CE",
    "bzzt": "WAC-D329",
    "chirp": "WAC-1A74",
    "click": "WAC-27B7",
    "clonk": "WAC-9776",
    "clunk": "WAC-7740",
    "crash": "WAC-22F2",
    "dink": "WAC-6BC7",
    "doot": "WAC-47F1",
    "fizz": "WAC-121A",
    "honk": "WAC-5613",
    "hoot": "WAC-9717",
    "jolt": "WAC-A466",
    "noot": "WAC-EC1C",
    "oink": "",
    "pew": "",
    "ping": "",
    "pong": "",
    "pop": "",
    "pow": "",
    "purr": "",
    "quark": "",
    "ring": "",
    "roar": "",
    "sigh": "",
    "snip": "",
    "sput": "",
    "swsh": "",
    "tape": "",
    "thud": "",
    "thum": "",
    "tik": "",
    "tok": "",
    "tong": "",
    "vroom": "",
    "whim": "",
    "whir": "",
    "whiz": "",
    "whoop": "",
    "whum": "",
    "wizz": "",
    "wow": "",
    "yip": "",
    "zap": "",
    "zip": "",
    "zot": "",
}

class DynamicObject:
    def __init__(self):
        pass

    def __setattr__(self, name, value):
        self.__dict__[name] = value

class RobotState(Enum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED_IDLE = 2
    RUNNING = 3
    DONE = 4

def copy_queue(original_queue):
    new_queue = queue.Queue(maxsize=original_queue.qsize())
    temp_list = []

    # Lock to ensure thread-safe access to the queue
    with threading.Lock():
        while not original_queue.empty():
            try:
                # Try to get an item without blocking
                item = original_queue.get_nowait()
                new_queue.put_nowait(item)
                temp_list.append(item)
            except queue.Empty:
                # The queue is empty, break the loop
                break

    # Put items back into the original queue
    for item in temp_list:
        original_queue.put(item)

    return new_queue

async def copy_asyncio_queue(original_queue: asyncio.Queue) -> asyncio.Queue:
    new_queue = asyncio.Queue(maxsize=original_queue.maxsize)
    temp_list = []

    # Transfer items from the original queue to the new queue
    while not original_queue.empty():
        item = await original_queue.get()
        await new_queue.put(item)
        temp_list.append(item)

    # Restore items to the original queue
    for item in temp_list:
        await original_queue.put(item)

    return new_queue

async def empty_asyncio_queue(queue: asyncio.Queue):
    while not queue.empty():
        await queue.get()
        queue.task_done()