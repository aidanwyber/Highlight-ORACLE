
import time
import random


class RandomPicker:
    '''
    pick a non-repeating random index of a given length
    e.g. 4-1-0-2-5-3 dynamically from list_length 6
    '''
    def __init__(self, list_length):
        if list_length == 0:
            raise Exception('List len 0')
        
        self.inds = list(range(list_length))
        self.picked = [False for x in self.inds]

    def get_index(self):
        r = 999999999
        while r >= len(self.inds) or self.picked[r]:
            r = random.randint(0, len(self.inds))
        self.picked[r] = True
        return self.inds[r]

    def is_available(self):
        return not all(self.picked)


def get_choice_list(in_n, out_n):
    '''
    get non-repeating random index list
    e.g. get_choice_list(9, 3) -> [2, 6, 1]
    '''
    if out_n > in_n: 
        raise Exception("Wrong use")

    rp = RandomPicker(in_n)
    return [rp.get_index() for x in range(out_n)]

def choice_weighted_dict(dictt):
    keys = [k for k in dictt.keys()]
    # items in dict need to be numeric weight values
    weights = [dictt[k] for k in dictt.keys()]
    choice = random_weighted_choice(keys, weights)
    return choice

def random_weighted_choice(listt, weights):
    normal_weights = normalise_list(weights)
    r = random.random()
    weight_integral = 0
    out = None
    for i in range(len(listt)):
        weight_integral += normal_weights[i]
        if r < weight_integral:
            out = listt[i]
            break
    return out

def normalise_list(listt):
    tot = sum(listt)
    return [x / tot for x in listt]


def vertical_bar_choice(s):
##    sep = s.split('|')
##    ri = random.randint(0, len(sep) - 1)
##    return (sep[ri], ri)
    return random.choice(s.split('|'))

def capitalise_str(s):
    if len(s) > 1:
        return s[0].upper() + s[1:]
    elif len(s) == 1:
        return s.upper()
    else:
        return s 


def is_vowel(char):
    return True if 'aiueoy'.find(char) > -1 else False
def a_an(noun):
    return 'an' if is_vowel(noun[0].lower()) else 'a'



def gen_timestamp():
    return time.time()


