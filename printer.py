
import random
import time
from escpos.printer import Usb

# following https://python-escpos.readthedocs.io/en/v2.2.0/user/usage.html
# "lsusb" cmd gives: "0fe6:811e" = vendorId:productId
p = Usb(0x0fe6, 0x811e) # WORKS
# lsusb iInterface & bEndpointAddress gave 0 & 0x01 (last two args)
#p_generic = printer.Usb(0x1a2b, 0x1a2b, 0, 0x00, 0x01)
#p_file = printer.File("/dev/usb/lp1") # lp0 is default

CHAR_WIDTH_A = 48
CHAR_WIDTH_B = 64

p.charcode('USA')

# charcode "PC437: USA, Standard Europe", send with p._raw()
tall_black_box = b'\xDB'
black_square = b'\xDC'
gradient0 = b'\xB0'
gradient1 = b'\xB1'
gradient2 = b'\xB2'

esoteric_chars = list(range(166, 255))


def byte_from_char_code(n):
    return n.to_bytes(1, 'big')

def encode_cp437(s):
    return s.encode(encoding='cp437', errors='replace')

def init_test():
    p.set(align='center', font='b', height=2, width=3)
    p.text(f'PRINTER OPERATIONAL\n\n')
    p.set(align='center', font='b', height=1, width=2)
    p.text(f'{time.ctime()}' + '\n' * 5)
    p.cut()


def print_esoteric_line(char_width=1, fontab='a'):
    max_line_width = CHAR_WIDTH_B if fontab == 'b' else CHAR_WIDTH_A

    p.set(width=char_width, font=fontab)
    
    n = int(max_line_width / char_width)
    eso_line = [random.choice(esoteric_chars) for x in range(n)]

    p.text('\n') # needed for some reason
    p._raw(eso_line)
    p.text('\n') # also


def print_prophecy(pr):
    # p set args: (X doesn't do anything)
    # str align: left/center/right
    # X str font: 'a' or 'b'
    # X str text_type: 'normal'
    # int width: [1,8]
    # int height: [1,8]
    # int density: [1,9]
    # boolean flip, invert
    p.set()
    p.text(s)
    

def word_wrapped_lines(s, char_width=1, margin=0, fontab='a', verbose=False):
    max_line_width = CHAR_WIDTH_A if fontab == 'a' else CHAR_WIDTH_B

    norm_mlw = max_line_width / char_width
    margined_mlw = norm_mlw - margin * 2

    if verbose:
        print(s[:60])
    
    s_lines = []
    for intentional_lines in s.split('\n'):
        s_lines.append([])
        for word in intentional_lines.split(' '):
            s_lines[-1].append(word) 

    if verbose:
        print('S_LINES')
        for s_line in s_lines[:12]:
            print(s_line)
    
    n_lines = []
    for s_line in s_lines:
        n_lines.append([])
        for word in s_line:
            if len(' '.join(n_lines[-1]) + ' ' + word) > margined_mlw:
                # word added on line > max line length
                n_lines.append([])
            n_lines[-1].append(word)

    if verbose:
        print('N_LINES')
        for n_line in n_lines[:12]:
            print(n_line)

    ns = '\n'.join([' '.join(n_line) for n_line in n_lines])

    if verbose:
        print(ns)
    
    return ns


def print_margined(s, padding_n, max_line_width=CHAR_WIDTH_A, esoteric=True):
    p.set() #reset formatting
    if padding_n < 1:
        raise Exception('Padding < 1')
    for line in s.split('\n'):
        p._raw(byte_from_char_code(random.choice(esoteric_chars)) if esoteric else b' ')
        if padding_n > 1 > 0:
            p.text(' ' * (padding_n-1))
        if len(line) > 0:
            p._raw(encode_cp437(line))
        n_padding_right = max_line_width - padding_n * 2 - len(line)
        if n_padding_right > 0:
            p.text(' ' * n_padding_right)
        if padding_n > 1 > 0:
            p.text(' ' * (padding_n-1))
        p._raw(byte_from_char_code(random.choice(esoteric_chars)) if esoteric else b' ')
##    m_lines = [[random.choice(esoteric_chars).to_bytes(1, 'big') if esoteric else b' ',
##               (b' ' * (padding_n-1) if padding_n > 1 else b''),
##               line,
##               (' ' * (padding_n-1) if padding_n > 1 else ''),
##               random.choice(esoteric_chars).to_bytes(1, 'big') if esoteric else ' ']
##               for line in s.split('\n')
##               ]
    #p._raw(m_lines)
##    return m_lines

def print_title(title, size, fontab='a'):
    p.set(font=fontab, width=size, height=size, align='center')
    p._raw(encode_cp437(word_wrapped_lines(title + '\n', margin=0, 
    char_width=size, fontab=fontab)))
    p.set()



S = '''
[Highlight ORACLE id.: 00000022]

=============== LIBERATION DINGLISH ==========================
###           By René Timmermans (NL)

In this work for Highlight 2026, In this work for Highlight 2026, Timmermans aims to play Timmermans aims to play In this work for Highlight 2026, Timmermans aims to play In this work for Highlight 2026, Timmermans aims to play with your salience machinery and to create a conflicting paradigm by using future soft robotics research and a suggestively shaped solid-state battery.

## Where and when
Van Walsumhof 3E
2613 TH Delft
February 2026

## About the artist
René Richardus Minne Timmermans (co/co) is a Dutch artist from Nieuwegein.
Tel.:    +31 6 46 79 35 15
Email:   r.t@msn.com

The resources for this project were made available by Stimuleringsfonds Oproep Wegen naar Welzijn.
'''
m = 4
cont = word_wrapped_lines(S, margin=m)

def test():
    print_esoteric_line()
    print_margined('', padding_n=m)
    print_title('This Is The Title')
    print_margined('', padding_n=m)
    print_esoteric_line()
    print_margined(cont, padding_n=m)
    print_esoteric_line()
    p.cut()








