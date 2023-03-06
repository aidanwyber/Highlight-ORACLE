
#  20x4 RGB character LCD Test Script

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : EN (Enable or Strobe)
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight R ->  -> GND
# 17: LCD Backlight G -> random larger resistor -> GND
# 18: LCD Backlight B -> 100 Ohm -> GND

# datasheet: https://cdn-shop.adafruit.com/datasheets/WH2004A-CFH-JT%23.pdf

try:
    import RPi.GPIO as GPIO # contained in Adafruit lib
    from Adafruit_CharLCD import Adafruit_CharLCD as LCD
    # python code in ~/.local/lib/python3.9/site-packages/Adafruit_CharLCD
except:
    print('Exception! Run electronics.py on RPi.')

import time
import threading
import random
from math import sin, cos, pi

LCD_RS = 25 # -> pin GPIO25 (GPIO.BCM layout)
LCD_EN = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 7
LCD_D7 = 22

COLS = 20
ROWS = 4

# button and LED
BUTTON = 4 # GPIO4 + > 20K Ohm resistor in series
BUTTON_NOISE_DELAY = 0.2
button_state = 0
button_state_prev = 0

LED = 12 # GPIO12 PWM enabled (+ integrated resistor in LED)
PWM_FREQUENCY = 1000
MAX_BRIGHTNESS = 100

# public
button_pressed = False

max_msg_len = (COLS - 2) * (ROWS - 2) # (20-2) * (4-2), 18 * 2, 36

verbose = False

def get_button_state():
    return GPIO.input(BUTTON)

def start_noise_led(prob=0.05, dt=0.01):
    global led_event, led_thread
    led_event = threading.Event()
    led_thread = threading.Thread(
##        name='breathe-led',
        target=_noise_led,
        args=(led_event, prob, dt))
    led_thread.start()
    
def stop_noise_led():
    global led_event
    led_event.set()


def _noise_led(event, prob, dt):
    global led_t, MAX_BRIGHTNESS
    # stop thread by led_event.set()
    while not event.is_set():
        duty = random.randint(0, MAX_BRIGHTNESS) if random.random() < prob else 0
        led_pwm.ChangeDutyCycle(duty)
        event.wait(dt)
        
    if verbose:
        print('End of LED threading function')
    led_pwm.ChangeDutyCycle(0)


def display_msg(s, random_border=True, border_char_chance=0.2):
    # format messgage string s
    #######s = word_wrap_lcd(s, max_msg_len // 2)
    s = s.ljust(max_msg_len)
    if verbose:
        print(s)

    global lcd
    for x in range(20):
        for y in range(4):
            lcd.set_cursor(x, y)
            if x in [0, 19] or y in [0, 3]:
                # xy in border
                if random_border and random.random() < border_char_chance:
                    ch = chr(random.randint(0,255))
                else:
                    ch = ' '
            else:
                inside_index = (x - 1) + (y - 1) * 18
                ch = s[inside_index]
            lcd.message(ch)


def word_wrap_lcd(s, nchars):    
    s_lines = []
    for intentional_lines in s.split('\n'):
        s_lines.append([])
        for word in intentional_lines.split(' '):
            s_lines[-1].append(word) 
    
    n_lines = []
    for s_line in s_lines:
        n_lines.append([])
        for word in s_line:
            if len(' '.join(n_lines[-1]) + ' ' + word) > nchars:
                # word added on line > max line length
                n_lines.append([])
            n_lines[-1].append(word)

    ns = '\n'.join([
         ' '.join(n_line).ljust(max_msg_len // 2)
         for n_line in n_lines
         ])
    return ns


if True or __name__ == '__main__':

    ##def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(LED, GPIO.OUT)
    led_pwm = GPIO.PWM(LED, PWM_FREQUENCY)
    led_pwm.start(0) # 0 duty cycle, duty cycle in [0, 100]

    # make the LCD object
    global lcd
    lcd = LCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, COLS, ROWS)

    if verbose:
        display_msg('Initialised.')

    start_noise_led(prob=0.05)
    time.sleep(2)
    stop_noise_led()




##    GPIO.setup(LED, GPIO.OUT)
##    for x in range(5):
##        GPIO.output(LED, 1)
##        time.sleep(0.1)
##        GPIO.output(LED, 0)
##        time.sleep(0.1)


##t = 0
##def f(event):
##    global t
##    # stop thread by led_event.set()
##    while not event.is_set():
##        print(t)
##        t += 0.1
##        event.wait(1)
##        
##        if False:
##            event.set()
##            break
##    print('End of LED threading function')



# do_scroll_msg = len(msg) > max_msg_len




