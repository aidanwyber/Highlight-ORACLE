import threading, time
from random import randint


##t = 0
##dt = 0.3
##
##def flashLed(e, dur):
##    """flash the specified led every second"""
##    while not e.is_set():
##        global t
##        print(t)
##        time.sleep(dt)
##        t += dt
##        event_is_set = e.wait(dt)
##        if event_is_set:
##            print('stop led from flashing')
##        else:
##            print('leds off')
##            time.sleep(dt)
##            t += dt
##            
##colour = "red"
##e = threading.Event()
##th = threading.Thread(name='non-block', target=flashLed, args=(e, 2))
##th.start()
##
##for i in range(0, 10):
##    # Randomly assign red or green every 10 seconds
##    randomNumber = randint(0,10)
##    print(randomNumber, '/////////')
##    time.sleep(1)
##
##e.set()

t = 0
def f(event):
    global t
    # stop thread by led_event.set()
    while not event.is_set():
        print(t)
        t += 0.1
        event.wait(1)
        
        if False:
            event.set()
            break
    print('End of LED threading function')

led_event = threading.Event()
x = threading.Thread(name='breathe-led', target=f, args=(led_event,))
x.start()

