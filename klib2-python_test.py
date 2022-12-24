import socketio
import time
import threading
import random


footValue =  [
'0 0 1 1 0 0 1 1 0 0 0 0 1 2 2 0 0 3 3 3 0 0 0 1 4 4 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
'0 0 1 1 0 0 1 2 0 0 0 0 1 2 3 0 0 1 2 3 0 0 0 1 1 1 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
'0 0 1 1 0 0 1 1 0 0 0 0 3 3 3 0 0 2 3 3 0 0 0 1 1 1 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
'0 0 1 1 0 0 1 1 0 0 0 0 1 2 2 0 0 1 2 3 0 0 0 1 1 1 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
'0 0 1 1 0 0 1 1 0 0 0 0 1 1 2 0 0 1 1 1 0 0 0 1 1 1 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
]

def worker():
    # print(time.time())
    regist = random.choice(footValue)
    foot = 'foot'
    sio.emit('send_footStatus', {foot: regist})
    time.sleep(.01)


def schedule(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

# standard Python
sio = socketio.Client()

sio.connect('http://localhost:3001')

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data):
    print('I received a message!')

@sio.on('send_footStatus')
def on_message(data):
    print('I received a message!2')
    # schedule(5,worker)

schedule(.1,worker)