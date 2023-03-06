
import random
import string

from util import *

class Artwork:
    verbose = False

    # available fields
    id = None
    title = None
    description = None
    funding = None
    address_line_1 = None
    address_line_2 = None
    future_date = None
    year = None

    max_title_len = 42

    # to implement
    # nothing yet


    # id, title, year, address(postcode address city number)
    # cont/intent desc, funding desc
    def __init__(self, OD, artist):
        if self.verbose:
            print('Generating ARTWORK...')
            print('\t__init__...')
            
        self.OD = OD
        self.artist = artist

        self.gen_id()

        # get title len to be < self.max_title_len
        self.title = 'x' * (self.max_title_len + 1)
        while len(self.title) > self.max_title_len:
            self.gen_title()
        
        self.gen_future_date()
        self.gen_description()
        self.gen_funding()
        self.gen_address()

    def gen_id(self):
        if self.verbose:
            print('\tgen_id...')
        self.id = str(random.randint(1000, 9999)).zfill(8)
        if self.verbose:
            print(self.id)

    
    def gen_title(self):
        if self.verbose:
            print('\tgen_title...')

        self.OD.nav('artwork/title-gen')
       # self.OD.dir()
        title_dict = self.OD.navD

        if random.random() < title_dict['capitalise-random-word-as-title-chance']:
            # title is one random word
            all_words = title_dict['pre-adjectives'] + title_dict['nouns'] + title_dict['post-words']
            title = random.choice(all_words)
            title = title.upper()
            
        else:
            # construct compound title
            title = ''

            # "pre-word"
            if random.random() < title_dict['pre-words-chance']:
                title += random.choice(title_dict['pre-words']) + ' '

            # prefix
            if random.random() < title_dict['prefix-chance']:
                title += random.choice(title_dict['prefixes']) + '-'

            # adjective
            if random.random() < title_dict['pre-adjective-chance']:
                rp_adj = RandomPicker(len(title_dict['pre-adjectives']))
                title += capitalise_str(title_dict['pre-adjectives'][rp_adj.get_index()])
                # second adjective
                if random.random() < title_dict['second-pre-adjective-chance']:
                    title += random.choice(' s s, s, s, s, s: s/s-'.split('s'))
                    sec_adj = capitalise_str(title_dict['pre-adjectives'][rp_adj.get_index()])
                    title += sec_adj + ' '
                else:
                    title += ' '

            # (first) noun
            plural = random.random() < title_dict['plural-nouns-chance']
            do_sec_noun = random.random() < title_dict['second-noun-chance']
            
            rp = RandomPicker(len(title_dict['nouns']))
            noun = title_dict['nouns'][rp.get_index()]

            # cause "laptop chargers", not "laptops chargers" or "laptops charger"
            # only pluralise when plural and no second noun exists
            plural_first_noun = plural and not do_sec_noun 
            noun = self.process_noun(noun, plural_first_noun)
            
            title += noun

            # second noun
            if do_sec_noun:
                title += random.choice(' s s s s s s s-s-s-s and s and the s | s|s & s & '.split('s'))
                sec_noun = title_dict['nouns'][rp.get_index()]
                sec_noun = self.process_noun(sec_noun, plural)
                if len(sec_noun) > 1:
                    sec_noun = capitalise_str(sec_noun)
                title += sec_noun + ' '
            else:
                title += ' '
                
            # "post-word"
            if random.random() < title_dict['post-word-chance']:
                title += random.choice(title_dict['post-words']) + ' '

            title = title.strip()
        
        # capitalize each word
        title = ' '.join([capitalise_str(x) for x in title.split(' ')])

        self.title = title
        
        if self.verbose:
            print(self.title)

    def process_noun(self, noun, plural):
        if noun.find('/') > -1:
            # case "mycolog/y/ies" (specified plural)
            noun_parts = noun.split('/') 
            if plural:
                noun = noun_parts[0] + noun_parts[2]
            else:
                noun = noun_parts[0] + noun_parts[1]
        elif noun.find('+') > -1:
            # case "DNA+" (don't multiply)
            noun = noun.replace('+', '')
        elif noun[-1] == 's':
            # case "species" or "Barbados" (no need to do anything)
            pass
        else:
            # case "vector" -> vectors
            if plural:
                noun += 's'
        return noun


    def gen_description(self):
        if self.verbose:
            print('\tgen_description...')
        
        hist_insp_chance = self.OD.getval('artwork/description/inspired-by-hl-historical-work-chance')
        was_inspired = random.random() < hist_insp_chance
        inspiration_desc = self.gen_inspiration_desc(was_inspired)

        intent_desc = self.gen_intent_desc()
        
        description = f'{intent_desc}{inspiration_desc}'
        self.description = description.strip()

        if self.verbose:
            print(self.description)


    def gen_inspiration_desc(self, do):
        if not do:
            return ''

        self.OD.nav('highlight-history')
        year_strs = [k for k in self.OD.navD.keys()]
        year_weights = [len(self.OD.navD[k]) for k in year_strs]
        h_year = random_weighted_choice(year_strs, year_weights)

        h_select = random.choice(self.OD.navD[h_year])
        h_artist = h_select[0]
        h_artwork = h_select[1]

        cap_lname = capitalise_str(self.artist.lname)

        inspiration = random.choice([
            f'{self.artist.fname} was inspired by {h_artist}\'s work "{h_artwork}", which was presented during Highlight {h_year}',
            f'{cap_lname} was heavily influenced by Highlight {h_year} work "{h_artwork}" by {h_artist}',
            f'{cap_lname} based much of {self.artist.pronouns["poss"]} exploration on inspiration from "{h_artwork}" by Highlight {h_year} featured artist {h_artist}',
            f'The idea behind the work was sparked after {cap_lname} was introduced to the "{h_artwork}" project by {h_artist} during Highlight in {h_year}'
            ])
        return capitalise_str(inspiration) + '. '
                   
    
    def gen_intent_desc(self):
        self.OD.nav('artwork/description')

        # tech-means
        means_list = self.OD.navD['tech-means']
        rp_m = RandomPicker(len(means_list))
        means_1 = means_list[rp_m.get_index()].strip()
        means_2 = means_list[rp_m.get_index()].strip()

        if random.random() < self.OD.navD['second-tech-means-chance']:
            means = means_1 + ' and ' + means_2
        else:
            means = means_1

        means = means.replace('{poss}', self.artist.pronouns['poss'])
        
        # goals
        goal_list = self.OD.navD['intended-goals']
        rp_g = RandomPicker(len(goal_list))
        goal_1 = goal_list[rp_g.get_index()].strip()
        goal_2 = goal_list[rp_g.get_index()].strip()

        if random.random() < self.OD.navD['second-tech-means-chance']:
            goal = goal_1 + ' and to ' + goal_2
        else:
            goal = goal_1

        goal = goal.replace('{poss}', self.artist.pronouns['poss'])

        # intent
        subj = self.artist.pronouns["subj"]
        subj_pl = '' if subj == 'they' else 's'
        intent = random.choice([
            f'{self.artist.lname} uses {means} in this project to {goal}',
            f'in this radical work, the artist uses {means} to {goal}',
            f'in {self.artist.fname} {self.artist.lname}\'s work, {subj} strive{subj_pl} to {goal} by means of {means}',
            f'{self.artist.fname} seeks to {goal} in this work by means of {means}',
            f'{self.artist.lname} attempts to {goal}. {subj.capitalize()} make{subj_pl} use of {means}',
            f'in this work for Highlight {self.year}, {capitalise_str(self.artist.lname)} aims to {goal} by using {means}',
            f'this project scheduled for {self.year} by {self.artist.fname} {self.artist.lname} aims to {goal} by using {means}'
            ])
        return capitalise_str(intent) + '. '
        

    def gen_funding(self):
        self.OD.nav('artwork/description')

        rp = RandomPicker(len(self.OD.navD['funds-names']))
        source = self.OD.navD['funds-names'][rp.get_index()]
        
        if random.random() < 0.25:
            source += ' and '
            source += self.OD.navD['funds-names'][rp.get_index()]

        r = random.randint(3, 8)
        grant_n = str(random.randint(10**(r), 10**(r+1)))

        funding = random.choice([
            f'this project was enabled by {source}',
            f'{self.artist.lname}\'s project was made possible by {source}',
            f'the resources for this project were made available by {source}',
            f'{self.title} was made possible by {source} [grant number {grant_n}]',
            f'this work was supported by {source} [grant number {grant_n}]'
            ])

        funding = capitalise_str(funding) + '.'

        self.funding = funding

    
    def gen_address(self):
        if self.verbose:
            print('\tgen_address...')
        
        self.OD.nav('artwork/location')

        street = random.choice(self.OD.navD['streets-delft'])

        max_hn = self.OD.navD['max-street-number']
        house_number = str(int((random.random() ** 3) * max_hn) + 1)
        if random.random() < 0.25:
            letters_len = len(self.OD.navD['street-number-letter'])
            letter_ind = int((random.random() ** 4) * letters_len)
            house_number += self.OD.navD['street-number-letter'][letter_ind]
        
        minmax_pc = self.OD.navD['postcode-range-delft']
        postcode = str(random.randint(minmax_pc[0], minmax_pc[1]))
        postcode += ' ' + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)

        city = 'Delft'

        self.address_line_1 = f'{street} {house_number}'
        self.address_line_2 = f'{postcode} {city}'

        if self.verbose:
            print(self.address_line_1)
            print(self.address_line_2)


    def gen_future_date(self):
        if self.verbose:
            print('\tgen_future_date...')
        
        this_year = int(time.ctime().split(' ')[-1])
        max_year = self.OD.D['artwork']['max-future-year']

        skew = 4
    
        if self.verbose:
            print('Min and max years:', this_year, max_year)
            print('Skew:', skew)
        
        year = round((random.random() ** skew) * (max_year - 1 - this_year) + this_year) + 1 ## minimum +1 year ahead
        self.future_date = 'February ' + str(year)
        self.year = str(year)
        if self.verbose:
            print(self.future_date)


    def __str__(self):
        if self.verbose:
            print('\t__str__...')

        s = f'[Project id.: {self.id}]\n\n'
        s += f'Title:\n{self.title}\n\n'
        s += f'Description:\n{self.description}\n\n'
        s += 'Where and when:\n{}\n{}\n{}\n\n{}'.format(
            self.address_line_1, self.address_line_2, self.future_date,
            self.funding)
        return s

