
import time
import random

from util import *

import electronics as e

class LCD_Messages:
    verbose = None

    lines = None
    sleep_times = None
    total_sleep_duration = None
    
    lcd = None

    max_n_messages = 2

    def __init__(self, OD, verbose=False):
        self.verbose = verbose
        if self.verbose:
            print('LCD_Messages.__init__')
            
        self.OD = OD
        
        self.lines = []
        self.sleep_times = []
##        self.total_sleep_duration = abs(
##            random.gauss(
##            mu=self.OD.D['loading-messages']['max-loading-duration-ms'] / 1000.0,
##            sigma=1.5
##            ))
        # 15
        json_max_dur = self.OD.D['loading-messages']['max-loading-duration-ms'] / 1000.0
        if self.verbose:
            print('json_max_dur', json_max_dur)
        # [15, 17]
        self.total_sleep_duration = json_max_dur * (1 + 0.2 * random.random())
        if self.verbose:
            print('self.total_sleep_duration', self.total_sleep_duration)

        if self.verbose:
            print('Generating message lines...')
        self.gen_lines()

        if self.verbose:
            print('Normalising sleep_times...')
        # normalise sleep times
        self.sleep_times = [t / sum(self.sleep_times) * self.total_sleep_duration
                            for t in self.sleep_times]

        
    def run(self):
        if self.verbose:
            print('LCD_Messages.run')
        
        t0 = time.time()

        disp_time = 0.40 if e.verbose else 0.284 # from measurement
        
        if self.verbose:
            print('Running LCD_Messages')
        
        for line_ind in range(len(self.lines)):
            if self.verbose:
                print('\n\t\t', self.lines[line_ind])

            n = random.randint(2, 10)

            for _i in range(n):
                # cause a blinking of noisy characters
                e.display_msg(self.lines[line_ind])
                
                sleep_time_i = self.sleep_times[line_ind] / n - disp_time
                sleep_time_i = sleep_time_i if sleep_time_i > 0 else 0

                time.sleep(sleep_time_i)

        if True or self.verbose:
            print('\n\t\ttime diff (meas, self.sleep_times):',
                  time.time()-t0, sum(self.sleep_times))

        end_msg = random.choice(self.OD.D['loading-messages']['end-messages'])
        # end_msg = 'end-message'
        if self.verbose:
            print(end_msg)
        e.display_msg(end_msg.center(e.COLS-2), random_border=False)

    def lcd_clear(self):
        e.lcd.clear()

    def lcd_display_waiting_for_button_press(self):
        e.display_msg('Press the button to beget a prophecy')


    def gen_lines(self):
        if self.verbose:
            print('LCD_Messages.gen_lines')
        
        n_lines = random.randint(1, 2)
        self.OD.nav('loading-messages')

        actions = self.OD.navD['actions']
        objects = self.OD.navD['objects']
        adjectives = self.OD.navD['adjectives']

        max_n = self.max_n_messages
        max_n_past =        min(max_n, len(actions['past']), len(objects['past']), len(adjectives['past']))
        max_n_present =     min(max_n, len(actions['present']), len(objects['present']), len(adjectives['present']))
        max_n_future =      min(max_n, len(actions['future']), len(objects['future']), len(adjectives['future']))
        # print(max_n_past, max_n_present, max_n_future)
        
        n_past =            random.randint(1, max_n_past)
        n_present =         random.randint(1, max_n_present)
        n_future =          random.randint(1, max_n_future)

        post_waiting_str = '...'
        max_len = (e.COLS - 2) * (e.ROWS - 2) - len(post_waiting_str)
        
        # looking into the past
        if self.verbose:
            print('Past...')
        for i in range(n_past):
            line = 'x' * (max_len + 1)
            while len(line) > max_len:
                past_actions = get_choice_list(len(actions['past']), n_past)
                past_adjectives = get_choice_list(len(adjectives['past']), len(past_actions))
                past_objects = get_choice_list(len(objects['past']), len(past_actions))
        
                line = actions['past'][past_actions[i]] + ' '
                if random.random() < adjectives['past-chance']:
                    line += adjectives['past'][past_adjectives[i]] + ' '
                line += objects['past'][past_objects[i]]

            line = capitalise_str(line) + post_waiting_str
            if self.verbose:
                print(line)
            self.lines.append(line)

            # add sleeping time
            self.sleep_times.append(self.random_sleeping_time())
        
        # looking into the present
        if self.verbose:
            print('Present...')
        for i in range(n_present):
            line = 'x' * (max_len + 1)
            while len(line) > max_len:
                present_actions = get_choice_list(len(actions['present']), n_present)
                present_adjectives = get_choice_list(len(adjectives['present']), len(present_actions))
                present_objects = get_choice_list(len(objects['present']), len(present_actions))

                line = actions['present'][present_actions[i]] + ' '
                if random.random() < adjectives['present-chance']:
                    line += adjectives['present'][present_adjectives[i]] + ' '
                line += objects['present'][present_objects[i]]

            line = capitalise_str(line) + post_waiting_str
            if self.verbose:
                print(line)
            self.lines.append(line)

            # add sleeping time
            self.sleep_times.append(self.random_sleeping_time())

        # looking into the future
        if self.verbose:
            print('Future...')
        for i in range(n_future):
            line = 'x' * (max_len + 1)
            while len(line) > max_len:
                future_actions = get_choice_list(len(actions['future']), n_future)
                future_adjectives = get_choice_list(len(adjectives['future']), len(future_actions))
                future_objects = get_choice_list(len(objects['future']), len(future_actions))
        
                line = actions['future'][future_actions[i]] + ' '
                if random.random() < adjectives['future-chance']:
                    line += adjectives['future'][future_adjectives[i]] + ' '
                line += objects['future'][future_objects[i]]

            line = capitalise_str(line) + post_waiting_str
            if self.verbose:
                print(line)
            self.lines.append(line)

            # add sleeping time
            self.sleep_times.append(self.random_sleeping_time())



    def random_sleeping_time(self):
        if self.verbose:
            print('\trandom_sleeping_time...')        
        return random.random() ** 2 + 0.8



if __name__ == '__main__':
    import ORACLE_Dictionary as od

    m = LCD_Messages(od.ORACLE_Dictionary('ORACLE_Dictionary_Dummy.jsonc'))

    m.run()






