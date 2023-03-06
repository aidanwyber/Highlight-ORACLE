
import time
import printer

from util import *

from ORACLE_Dictionary import ORACLE_Dictionary
import electronics as e
from prophecy import Prophecy

dictionary_name = 'ORACLE_Dictionary.jsonc'

# states of state machine
INITIALISE = 0
WAITING_FOR_BUTTONPRESS = 1
GENERATE_PROPHECY = 2

LED_WAITING_BRIGHTNESS = 100
LED_PROCESSING_BRIGHTNESS = 25

# consts
LCD_WAITING_STR = 'Waiting for button|press...' # no space
LCD_WAITING_STR = 'Push the button torequest a prophecy.' # no space
WAIT_TIME_AFTER_RECEIPT_PRINT = 7 # s

# TESTING
DO_PRINT = True
VERBOSE = not True

prophecy_count = 0

##OD = None
##p = None

if __name__ == "__main__":
    global OD
    global p

    p = None    
    OD = ORACLE_Dictionary(dictionary_name)
    # OD.show_dictionary_structure(2, file_output=True)
    
##    while True:
##        print('\n\n\n\n')
##        p = Prophecy(OD)
##        
##        #p.display_loading_text()
##        
##        print(p)
####        p.output_prophecy_markdown()
####        
##        p.print_receipt()
##
##        input()
##        

    # state machine
    cur_state = INITIALISE
    while True:
        if cur_state is INITIALISE:
            e.lcd.clear()
            e.display_msg('Initialising...', random_border=False)
            
            OD = ORACLE_Dictionary(dictionary_name)

            if DO_PRINT:
                printer.init_test()
            
            e.lcd.clear()
            e.display_msg(LCD_WAITING_STR, random_border=False)
            print('\n' + LCD_WAITING_STR)

            time.sleep(1)

            cur_state = WAITING_FOR_BUTTONPRESS
            e.MAX_BRIGHTNESS = LED_WAITING_BRIGHTNESS
            e.start_noise_led(prob=0.05, dt=0.05)
        
        elif cur_state is WAITING_FOR_BUTTONPRESS:
            if e.get_button_state() == 1:
                print('Button pressed.')
                time.sleep(0.5)
                
                cur_state = GENERATE_PROPHECY
                e.MAX_BRIGHTNESS = LED_PROCESSING_BRIGHTNESS
                e.start_noise_led(prob=0.2, dt=0.0125)
                continue
            if random.random() < 0.01:
                e.display_msg(LCD_WAITING_STR, random_border=True,
                              border_char_chance=0.025)
                
            time.sleep(0.005)
        
        elif cur_state is GENERATE_PROPHECY:
            if VERBOSE:
                print('Generating new prophecy...')
            new_prophecy = Prophecy(OD, verbose=VERBOSE)
            if VERBOSE:
                print('Saving Markdown...')
            new_prophecy.output_prophecy_markdown()
            prophecy_count += 1

            # draw on lcd
            if VERBOSE:
                print('Drawing LCD...')
            new_prophecy.display_loading_messages()

            # print the receipt
            if DO_PRINT:
                new_prophecy.print_receipt()
            # print to terminal at the same time
            print(new_prophecy)
            
            e.stop_noise_led()

            time.sleep(WAIT_TIME_AFTER_RECEIPT_PRINT)

            e.lcd.clear()
            e.display_msg(LCD_WAITING_STR, random_border=False)
            print('\n' + LCD_WAITING_STR)
            
            cur_state = WAITING_FOR_BUTTONPRESS
            e.MAX_BRIGHTNESS = LED_WAITING_BRIGHTNESS
            e.start_noise_led(prob=0.05, dt=0.05)

            time.sleep(0.1)
        else:
            # ?
            print('The ELSE clause was triggered for "cur_state". What happened?')
            cur_state = WAITING_FOR_BUTTONPRESS
            e.MAX_BRIGHTNESS = LED_WAITING_BRIGHTNESS
            e.start_noise_led(prob=0.05, dt=0.05)

