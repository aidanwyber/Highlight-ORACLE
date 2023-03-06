
import random

from util import *

class Artist:
    verbose = None
    MALE = 0
    FEMALE = 1
    middle_name_skew_fac = 3
    
    def __init__(self, OD, gen_random=True, verbose=False):
        self.verbose = verbose
        
        if self.verbose:
            print('Generating ARTIST...')
            print('\t__init__...')
        
        self.OD = OD

        real_historical_person_chance = self.OD.getval('artist/historical-artist-chance')
        self.real_historical_person = random.random() < real_historical_person_chance

        self.real_historical_person = False #######################

        if self.real_historical_person:
            # get historical Highlight artist
            if self.verbose:
                print('Constructing historical person...')
                
            self.get_random_hist_name()
            self.gen_pronouns_gender(use_they=True)

            ## replace following funcs with real data????
            self.gen_origin()
            self.gen_email()
            self.gen_phonenumber()
            
        else:
             # generate random artist
            if self.verbose:
                print('Generating random artist...')
                
            self.gen_pronouns_gender()
            self.gen_origin()
            self.gen_name()
            self.gen_email()
            self.gen_phonenumber()

            self.gen_description()
            #gen_contact2()
            

    def gen_pronouns_gender(self, use_they=False):
        if self.verbose:
            print('\tgen_pronouns...')

        if use_they:
            # they/them/their
            pronouns = 'they/them/their'
        else:
            pns_dict = self.OD.D['artist']['pronouns']
           # if self.verbose:
           #     print(pns_dict)
            pronouns = choice_weighted_dict(pns_dict)

        if self.verbose:
            print(pronouns)
        
        pn_types = pronouns.split('/')
        self.pronouns = {
            'string': pronouns, # original string
            'subj': pn_types[0], # subject
            'obj': pn_types[1], # object
            'poss': pn_types[2] # possessive
            }
        
        if self.pronouns['subj'] == 'he':
            self.name_gender_type = self.MALE
        elif self.pronouns['subj'] == 'she':
            self.name_gender_type = self.FEMALE
        else:
            self.name_gender_type = random.choice([self.MALE, self.FEMALE])

        if self.verbose:
            print(self.pronouns, self.name_gender_type)


    def gen_origin(self):
        if self.verbose:
            print('\tgen_nationality...')

        self.OD.nav('artist/nationality')
        #self.OD.dir()

        nationality_keys = list(self.OD.navD.keys())
        nationality_weights = [self.OD.navD[k]['chance'] for k in nationality_keys]

        if self.verbose:
            print('nationality data:')
            print(nationality_keys)
            print(nationality_weights)
            
        nationality = random_weighted_choice(nationality_keys, nationality_weights)
        if self.verbose:
            print(nationality)
        
       # nationality, bar_ind = vertical_bar_choice(nationality)
        
        
        self.nationality = nationality

        self.nationality_abbr = self.OD.navD[nationality]['abbreviation']
        self.nationality_abbr = vertical_bar_choice(self.nationality_abbr)

        self.nationality_country = self.OD.navD[nationality]['country-name']
        self.nationality_country = self.nationality_country.replace('The', 'the')

        self.phone_code = self.OD.navD[nationality]['phone-ext']

        self.city = random.choice(self.OD.navD[nationality]['cities'])
        
        if self.verbose:
            print(self.nationality, self.nationality_abbr, self.nationality_country)


    def gen_name(self):
        if self.verbose:
            print('\tgen_name...')
        
        names_dict = self.OD.D['artist']['nationality'][self.nationality]['names']
       # names_dict = self.OD.D['artist']['nationality']['Dutch']['names']

        if self.name_gender_type == self.MALE:
            fnames = names_dict['male-first-names']
        else: # FEMALE
            fnames = names_dict['female-first-names']

        lnames = names_dict['surnames']

        if self.verbose:
            print(f'Number of {self.name_gender_type} fnames:', len(fnames))
            print('Number of lnames:', len(lnames))

        # picker
        fn_rp = RandomPicker(len(fnames))
        self.fname = fnames[fn_rp.get_index()]

        ln_rp = RandomPicker(len(lnames))
        self.lname = lnames[ln_rp.get_index()]
    
        mid_name_strat = names_dict['middle-names-strategy']
        max_middle_names = self.OD.D['artist']['max-middle-names']
        if self.verbose:
            print('max_middle_names', max_middle_names)
        
        ## skew towards 0 middle names
        n_middle_names = round((random.random() ** self.middle_name_skew_fac) * max_middle_names)
        self.mnames = ''
        if mid_name_strat == 'first-names':
            for i in range(n_middle_names):
                self.mnames += fnames[fn_rp.get_index()] + ' '
                
        elif mid_name_strat == 'last-names':
            for i in range(n_middle_names):
                self.mnames += lnames[ln_rp.get_index()] + ' '

        else:
            if self.verbose:
                print(f'No middle name strategy: "{mid_name_strat}"')
            self.mnames = ''
        
        self.mnames = self.mnames.strip()

        # final name form
        if self.mnames == '':
            self.fullname = self.fname + ' ' + self.lname
        else:
             self.fullname = self.fname + ' ' + self.mnames + ' ' + self.lname

        self.fletter = self.fname[0].lower()
        self.lletter = ''.join([x[0].lower() for x in self.lname.split(' ')])

        if self.verbose:
            print(self.fullname)


    def get_random_hist_name(self):
        if self.verbose:
            print('\tget_random_hist_name...')

        self.fname = 'Arthur'.capitalize()
        self.lname = 'Historia'.capitalize()

        self.phone_code = '+31'
        
    
    def gen_email(self):
        if self.verbose:
            print('\tgen_email...')
            
        self.OD.nav('artist/contact-info')
        if random.random() > self.OD.navD['lame-pseudonym-chance']:
            #self.OD.dir()

            email_format_dict = self.OD.navD['email-name-formats']
            email_format = choice_weighted_dict(email_format_dict)
            user = email_format

            if self.verbose:
                print(user)
        else:
            user = random.choice(self.OD.navD['lame-pseudonyms'])
            if self.verbose:
                print(user)

        user = user.replace('{fname}', self.fname.lower())
        user = user.replace('{lname}', self.lname.lower().replace(' ', ''))
        user = user.replace('{fletter}', self.fletter)
        user = user.replace('{lletter}', self.lletter)

        ext_dict = self.OD.navD['email-domains']
        ext = choice_weighted_dict(ext_dict)
        
        email = user + '@' + ext
        self.email = email
        
        if self.verbose:
            print(self.email)
        

    def gen_phonenumber(self):
        if self.verbose:
            print('\tgen_phonenumber...')
        
        self.phonenumber = self.phone_code + ' '

        # nederlands mobiel nummer
        if self.nationality_abbr.lower() == 'nl':
            self.phonenumber += '6 '

        
        phn = str(random.randint(0, 99999999)).zfill(8)
        self.phonenumber += random.choice([
            phn[0:2] + ' ' + phn[2:4] + ' ' + phn[4:6] + ' ' + phn[6:8],
            phn[0:4] + ' ' + phn[4:8],
            phn[0:3] + ' ' + phn[3:6] + ' ' + phn[6:8]
            ])
        
        if self.verbose:
            print(self.phonenumber)


    def describe_origin(self):
        return random.choice([
            f' from {self.nationality_country}',
            f' ({self.nationality_abbr})',
            f', a {self.nationality} artist from {self.city}',
            f' ({self.city}, {self.nationality_abbr})'
            ])


    def gen_description(self):
        pns = '{0}/{1}'.format(self.pronouns['subj'], self.pronouns['obj'])
        desc = random.choice([
            f'{self.fullname} ({pns}) is {a_an(self.nationality)} {self.nationality} artist from {self.city}',
            f'{self.fullname} ({pns}) is {a_an(self.nationality)} {self.nationality} artist from {self.city}',
            f'{self.fullname} attended the art academy of {self.city} ({self.nationality_abbr}). {self.pronouns["poss"].capitalize()} pronouns are {pns}'

            ])

        self.description = capitalise_str(desc) + '.'


    def __str__(self):
        if self.verbose:
            print('\t__str__...')
            
        if self.real_historical_person:
            s = 'Historical artist: {0} {1}'.format(self.fname, self.lname)
        
        else:
            s = 'Artist:\n{}\nEmail: {}\nPhone: {}'.format(
                self.description,
                self.email,
                self.phonenumber
                )
        
        return s


