import random
import time
import string

import id_counter
import printer

from util import *
from artist import Artist
from artwork import Artwork
from lcd_messages import LCD_Messages

class Prophecy:
    verbose = None
    
    OD = None
    lines = None
    c_id = None

    artist = None
    artwork = None
    lcd_msgs = None

    output_folder = 'prophecy_output'

    def __init__(self, OD, verbose=False):
        self.verbose = verbose
        if self.verbose:
            print('Prophecy.__init__')
        
        self.OD = OD
        self.lines = []

        if self.verbose:
            print('Updating ID counter file...')
        self.get_update_id()
        
        if self.verbose:
            print('Generating prophecy...')
        self.generate_prophecy()


    def get_update_id(self):
        # get counter from file
        n = id_counter.get_id()
        # increment counter file with 1
        id_counter.set_id(n + 1)
        # pad to an 8-char string
        self.c_id = str(n).zfill(8)


    def generate_prophecy(self):
        random_artist = random.random() > self.OD.getval('artist/historical-artist-chance')

        if self.verbose:
            print('Generating Artist()...')
        self.artist = Artist(self.OD, gen_random=random_artist)
        if self.verbose:
            print('Generating Artwork()...')
        self.artwork = Artwork(self.OD, self.artist)
        if self.verbose:
            print('Generating LCD_Messages()...')
        self.lcd_msgs = LCD_Messages(self.OD, verbose=self.verbose)
        
        self.lines.append(self.artwork)
        self.lines.append(self.artist)
        
        if self.verbose:
            print('self.lines:\n\n', self.lines)

    def display_loading_messages(self):
        self.lcd_msgs.run()

    def print_receipt(self):
        m = 4
        
        printer.print_esoteric_line()
        printer.print_esoteric_line()
        printer.print_esoteric_line()
        
        printer.p.set(align='center')
        printer.p.text(f'\nHighlight ORACLE\nProphecy id.: {self.c_id}\n')
        
        printer.print_esoteric_line()
        
        printer.p.text('\n')
        
        # print_margined('', padding_n=m)
        printer.print_title(self.artwork.title,
        2, fontab='a')
        printer.p.text('\n')
        printer.print_title(f'By {self.artist.fname} {self.artist.lname} ' +
        f'({self.artist.nationality_abbr})',
        2, fontab='b')
        
        # printer.p.text('\n')
        
        printer.print_esoteric_line()
        printer.print_margined(printer.word_wrapped_lines(
            f'\n{self.artwork.description}\n', margin=m),
            padding_n=m)
        printer.print_esoteric_line()
        
        printer.p.text('\n')
        
        printer.print_title('Where and when',
        2, fontab='b')
        
        
        printer.print_margined(printer.word_wrapped_lines(
            f'\n{self.artwork.address_line_1}\n' + 
            f'{self.artwork.address_line_2}\n' +
            f'{self.artwork.future_date}\n'
            , margin=m),
            padding_n=m, esoteric=False)
        
        printer.print_esoteric_line()
        printer.p.text('\n')
        
        printer.print_title('About the artist',
        2, fontab='b')
        
        printer.print_margined(printer.word_wrapped_lines(
            f'\n{self.artist.description}\n' +
            f'Tel.:     {self.artist.phonenumber}\nEmail:     {self.artist.email}\n'
            , margin=m),
            padding_n=m, esoteric=False)
        
        printer.print_esoteric_line()
        
        printer.p.set()
        printer.print_margined(printer.word_wrapped_lines(
            f'\n{self.artwork.funding}\n', margin=m),
            padding_n=m, esoteric=False)
                
        printer.print_esoteric_line()
        printer.print_esoteric_line()
        printer.print_esoteric_line()
        
        printer.p.text('\n\n\n')
        
        # cut receipt
        #printer.p.text('\n\n\n\n')
        printer.p.cut()

    def __str__(self):
        s = '======================PROPHECY:======================\n'
        # for l in self.lines:
        #     s += str(l) + '\n\n'

        s += f'[Highlight ORACLE id.: {self.c_id}]'
        s += '\n\n'
        s += f'\t-> {self.artwork.title.upper()}\n'
        s += f'\t-> By {self.artist.fname} {self.artist.lname} ({self.artist.nationality_abbr})'
        s += '\n\n'
        s += f'{self.artwork.description}'
        s += '\n\n'
        s += f'— Where and when —\n'
        s += f'{self.artwork.address_line_1}\n{self.artwork.address_line_2}\n'
        s += f'{self.artwork.future_date}'
        s += '\n\n'
        s += f'— About the artist —\n{self.artist.description}\n'
        s += f'Tel.:\t{self.artist.phonenumber}\nEmail:\t{self.artist.email}'
        s += '\n\n'
        s += f'{self.artwork.funding}'
        return s

    def output_prophecy_markdown(self):
        # save in MarkDown style
        s = f'*Highlight ORACLE id.: {self.c_id}*'
        s += '\n\n'
        s += f'# {self.artwork.title.upper()}\n'
        s += f'### By {self.artist.fname} {self.artist.lname} ({self.artist.nationality_abbr})\n'
        s += '\n'
        s += f'{self.artwork.description}'
        s += '\n\n'
        s += f'## Where and when\n'
        s += f'{self.artwork.address_line_1}\n{self.artwork.address_line_2}\n'
        s += f'{self.artwork.future_date}'
        s += '\n\n'
        s += f'## About the artist\n{self.artist.description}\n'
        s += f'Tel.:\t{self.artist.phonenumber}\nEmail:\t{self.artist.email}'
        s += '\n\n'
        s += f'{self.artwork.funding}\n'

        with open(f'{self.output_folder}/{self.c_id}.md', mode='w') as f:
            f.write(s)
            f.close()
        return s




if __name__ == '__main__':
    from ORACLE_Dictionary import ORACLE_Dictionary

    od = ORACLE_Dictionary('ORACLE_Dictionary_Dummy.jsonc')
    while True:
        p = Prophecy(od)
        print(p)
        input()
    
