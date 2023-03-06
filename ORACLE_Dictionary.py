
import json
import re

do_pyperclip = False
if do_pyperclip:
    import pyperclip

from util import *

class ORACLE_Dictionary:
    verbose = None
    
    D = {}
    navD = {}

    _dict_structure = None

    def __init__(self, file_name, verbose=False):
        self.verbose = verbose
        
        if self.verbose:
            print('Generating ORACLE_Dictionary...')
            print('\t__init__...')
        self.D = self.read_dictionary(file_name)
        self.reset_nav()

    
    def read_dictionary(self, file_name):
        if self.verbose:
            print('\tread_dictionary...')
            print('Opening file...')
        f = open(file_name, encoding='utf-8')
        commented_cont = f.read()
        f.close()

        if self.verbose:
            print('Removing comments...')
        cont = self.remove_comments(commented_cont)

        if self.verbose and do_pyperclip:
            print('Copying to clipboard...')
            pyperclip.copy(cont)
            print('Loading JSON into dictionary...')
        d = json.loads(cont)
        return d


    def remove_comments(self, string):
        # code from https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
        
        # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", string)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        string = re.sub(re.compile(r"//.*?\n" ), "", string)
        string = re.sub(re.compile(r"//.*?$" ), "", string) # $ end of string
        return string

    def show_dictionary_structure(self, max_level, file_output=False, file_name='dict_structure.txt'):
        if self.verbose:
            print('Showing dictionary key structure:')
            print('type:', type(self.D))
        global _dict_structure
        _dict_structure = ''
        self._show_dictionary_structure(self.D, 0, max_level)
        
        if file_output:
            with open(file_name, mode='w', encoding='utf-8') as f:
                f.write(_dict_structure)
        else:
            print(_dict_structure)
        return

    def _show_dictionary_structure(self, d, level, max_level):
        if type(d) != type(dict()) or level > max_level - 1:
            return
        global _dict_structure
        for k in d.keys():
            _dict_structure += (level * '\t') + k + '\n'
            self._show_dictionary_structure(d[k], level + 1, max_level)
        return


    def getkeys(self, string):
        '''
        access(d, 'artist/nationality/German')
        '''
        ks = string.split('/')
        if self.verbose:
            print(ks, type(self.D))
        return self.get_path_key_list(self.D, 0, ks)

    def get_path_key_list(self, d, level, ks):
        if level >= len(ks) - 1:
            return list(d.keys())
        return self.get_path_key_list(dict(d[ks[level]]), level + 1, ks)

    def reset_nav(self):
        self.path = ''
        self.navD = self.D
    
    def nav(self, path):
        self.reset_nav()
        
        self.path = path
        for sub in path.split('/'):
            self.navD = self.navD[sub]

    def dir(self):
        print()
        print('PATH ' + str(self.path) + ':')
        keys = list(self.navD.keys())
        for i in range(len(keys)):
            print('\tKey', i, '->', keys[i])
            print('\tItem', i, '->', self.navD[keys[i]])
        print()
        
    def getval(self, path):
        self.reset_nav()
        
        p = path.split('/')
        path = '/'.join(p[:-1]) # rm last key to get nav path
        key = p[-1]
        self.nav(path)
        if self.verbose:
            print(self.navD[key])
        return self.navD[key]



if __name__ == '__main__':
    from artist import Artist
    from artwork import Artwork

    verbose = False
    
    global od
    od = ORACLE_Dictionary('ORACLE_Dictionary.jsonc', verbose=verbose)
    od.show_dictionary_structure(2)

    while True:
        atst = Artist(od, verbose=verbose)
        awk = Artwork(od, atst)
##        if len(awk.title) > awk.max_title_len-1:
##        if awk.title.lower().find('communist') > -1:
        if True:
            print(atst)
            print(awk)
            print('\n\n' + awk.title)
            input()

