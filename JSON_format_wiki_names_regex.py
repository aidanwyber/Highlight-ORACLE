import pyperclip, re

'''
util

////////////// ^(?!//)^(?!\n)(.*)
////////////// "$1",

RM single char lines ('A\n'):
^.$\n

 (.*)
'''

names = '''
A
Aaberg
Aalberg
Aberg
Abrahamsson
Adelsköld
Af Forselles (surname)
Af Jochnick
Af Klintberg
Afzelius
Ågren
Ahlgren
Ahlm
Ahlqvist
Åhlund
Ahnlund
Ahrén
Åkerberg
Åkerblom
Åkerlund
Åkerman
Åkermark
Åkerström
Alenius
Alexandersson
Alfredsson
Alm (surname)
Almgren
Almlöf
Almqvist
Alström
Alströmer
Ålund
Amundson
Anderberg
Andersdotter
Anderson (surname)
Andersson
Andrae
Ångström (disambiguation)
Antonsson
Appelqvist
Arneson
Artursson
Arvidsson
Arwidsson
Åsbrink
Åslund
Aspegren
Aspelund
Asplund
Åström
Augustsson
Axelsson
B
Bäck
Backlund
Bäcklund (surname)
Backman
Backstrom
Bengtsson
Berggren
Bergh (surname)
Berghult
Bergius
Bergkvist
Bergling
Berglund
Bergman
Bergmann
Bergquist
Bergqvist
Bergroth
Bergsten
Bergstrom
Bergvall
Berndtsson
Bertilsson
Bexell (surname)
Billberg
Birgersson
Bjellqvist
Björk (name)
Björklund
Bjorkman
Björling
Björnstjerna
Blix
Blom (surname)
Blomgren
Blomquist
Blomqvist
Blomstedt
Bodin (surname)
Bok (surname)
Bolander
Bong (surname)
Borg (surname)
Borgström
Börjesson
Botvid
Boustedt
Bovin
Brahe
Brännström
Brask
Brate
Bratt
Brattström
Brink (surname)
Brodd
Brorsson
Brundin
Brunnberg
Brunström
Bruun
Bruzelius
Brydolf
Bucht
Bure (surname)
Bye (surname)
Byström
C
Carlen (surname)
Carlgren
Carlsdotter
Carlsson
Casparsson
Ceder
Cederblom
Cedergren (surname)
Cederqvist
Cederschiöld
Cederström
Collberg
Crona
Cronholm
D
Dahl (surname)
Dahlberg (surname)
Dahlgren (surname)
Dahlin
Dahlquist
Dahlström (surname)
Dahlvig
Dalin (surname)
Danielsson
Davidsson
Degerlund
Degermark
Djerf
Djoos
Drakenberg
Dyrssen
E
Edgren
Edling (surname)
Edlund
Edström
Edvinsson
Egnell
Ehrling
Ekberg
Ekblad
Ekbom
Ekdahl
Ekdal
Ekenberg
Ekerot
Ekfeldt
Ekholm
Eklund
Ekman
Ekstrand
Ekström
Elfsberg
Elfström
Ellefson
Elmsäter
Enckell
Engberg
Engdahl
Englund
Engström
Enlund
Enquist
Ericsson (surname)
Eriksson
Erlandson
Erlandsson
Ernman
F
Fältskog
Fagerholm (surname)
Fagerudd
Fahlén
Fällman
Farnerud
Faxén
Fernholm
Fingerroos (surname)
Fjellner
Flodqvist
Flygare
Fogelklou
F
Forsberg
Forsell
Forslund
Forsman
Forsström
Fougstedt
Fransson
Franzén
Fredholm
Fredin
Fredriksson
Friberg
Frisk (surname)
Frumerie
Frykberg
G
Gabrielsson
Gårdinger
Gauffin
Geijer
Gentzel
Gerhardsson
Göransson
Göthberg
Grafström
Granath
Grandelius
Granholm
Granqvist
Grönberg
Grönblom
Grönroos
Grönvall
Gunderson
Gunnarsson
Gustafson
Gyllenhaal family
Gyllenstierna
Gylling
H
Hafström
Hagelin
Hagerstrom
Hägg
Hägglund
Haglund
Hagman
Hagnell
Hagström (disambiguation)
Håkansson
Hallberg
Hallnäs
Hallström
Halvarsson
Hammarberg
Hammarlund (surname)
Hammarström
Hansdotter
Hansson (surname)
Haraldsson
Hartman
Hassel (surname)
Hasselgren
Hedberg
Hedin (surname)
Hedlund
Hedman
Hedqvist
Hedstrom
Heidenstam
Helgerson
Helgesson
Hellberg
Hellgren
Hellquist
Hellqvist
Hellstedt
Hellsten
Hellström (surname)
Henriksson
Herlitz (surname)
Hermansson
Heurlin
Hildebrand (surname)
Hirdman (surname)
Hjalmarsson
Hjertsson
Hjortsberg
Hjulström
Högberg
Höglund
Holgersson
Holm (surname)
Holmberg
Holmdahl
Holmgren
Holmlund
Holmquist
Holmqvist
Holmström
Hugosson
Hult (surname)
Hultgren
Hultin
Hultman
Hurtig
Hwasser
Hylander
Hysén
I
Igelström
Ingelow
Ingesson
Ingvardsson
Isaksson
Isberg
Israelsson
J
Jacobson (surname)
Jacobsson
Jäderholm
Jakobsson
Jansson
Jarlskog
Järnefelt
Jernberg
Johannesson
Johansson
Johnson
Johnsson
Jonsson
Jönsson
Josefsson
Juhlin
K
Källström
Kamprad
Karlen
Karlsdotter
Karlsson
Karlström
Kinberg
Kjellström
Kling
Klingspor
Knape (surname)
Knutsson
Kreuger
Kristensson
Kristoffersson
Kroon
Kugelberg
Kullander
Kulldorff
L
Lagerfeld
Lagergren (surname)
Lagerhjelm
Lagerkvist
Lagerlöf
Landberg
Lantz (surname)
Larsson
Laxman (Scandinavian surname)
Leijonhufvud
Lejon
Lennartsson
Lestander
Leuhusen
Lidholm
Lilja (surname)
Liljeroth
Liljeström
Lind
Lindahl
Lindberg (surname)
Lindbergh
Lindblad
Lindblom
Lindegren
Lindell (surname)
Lindelöf (surname)
Lindeman
Lindén
Linden (surname)
Linderoth
Lindfors
Lindgren
Lindholm (surname)
Lindquist
Lindqvist
Lindroos
Lindroth
Lindskog
Lindström
Linroth
Ljung (surname)
Ljungberg
Ljungdahl
Ljunggren
Ljungkvist
Ljungqvist
Lötvall
Löfgren
Löwenadler
Löwenberg (surname)
L
Ludvigsson
Lugn
Lund (surname)
Lundbäck
Lundberg
Lundblad
Lundeberg
Lundell
Lundgren
Lundin
Lundmark
Lundquist
Lundqvist
Lundström
Lundvall
Lundvik
M
Magnell
Magnuson
Magnusson
Malmberg
Malmborg
Malmgren
Malmkvist
Malmquist
Malmqvist
Malmsten
Malmstrom
Månsdotter
Marklund
Markström
Mårtensson
Martinsson
Mattisson
Mattson
Mattsson
Mellgren
Mikaelsson
Molander
Moller
Morberg
Mörner
Mosander
N
Näslund
Nätterqvist
Nicklasson
Nilsson
Norberg (disambiguation)
Nordahl
Nordenfalk
Nordengrip
Nordgren
Nordin (surname)
Nordlander (name)
Nordling
Nordlund
Nordquist
Nordstrom (disambiguation)
Nordwall
Norelius
Noren (surname)
Norin
Norling
Norström
Nyberg (surname)
Nygaard (surname)
Nykvist
Nyquist (surname)
Nystrom
O
Öberg
Odenberg
Odhner
Ohlin
Ohlson
Ohlsson
Ohly
Olander
Olderman
Olofsson
Olsson
Ortmark
Oskarsson
Ossler
Östberg
Österberg
Östergren
Osterlund
Österman
Ostlund
Östman
Ostrom
Ottosson
P
Påhlson
Påhlsson
Palm (surname)
Palmberg
Palmcrantz
Palmgreen
Palmgren
Palmquist
Palmroth
Palmstierna
Palmstruch
Pålson
Pålsson
Paulsson
Persson
Petersen
Petersson
Pettersson
Pihl
Posse (surname)
Pousette
Q
Quicklund
Quist
Qvist
R
Råberg
Rådström
Rakell
Rask (surname)
Rathsman
Regnell
Rehn
Rehnquist (surname)
Renlund
Rheborg
Richardsson
Rickardsson
Rindborg
Risberg
Rönnberg
Rönnlund
Rönström
Roos (surname)
Rosander (surname)
Rosén
Rosenberg (surname)
Rosenblad
Rosengren
Rosenius
Rosenquist
Rosenqvist
S
Säfström
Sahlberg
Sahlin
Samuelsson
Sandahl
Sandberg (surname)
Sandborg
Sandelin
Sandell
Sandgren
Sandqvist
Sandström
Segerström (surname)
Selander
Silfverstolpe
Siljeström
Simonsson
Sjöberg
Sjöblom
Sjödin
Sjögren
Sjöholm
Sjölin
Sjölund
Sjöqvist
Sjöstedt
Sjöström
Skiöld
Skog (surname)
Skoglund
Sköld
Sköldberg
Skoog (surname)
Snellman (surname)
Söderberg
Södergren
Söderlund
Söderman
Söderström
Söderholm
Sohlman
Sollander
Sörenstam
Sparre
Sparv
Stading
Ståhlberg (surname)
Stahre
Stenbeck
Stenbock
Stenmark
Stenström
Stiernspetz
Stjernberg
Strandberg
Strandlund
Strindlund
Ström (surname)
Strömbäck
S
Strömberg (surname)
Stromberg (surname)
Strömstedt
Sundberg
Sundblad
Sundborg
Sundelin
Sundin (surname)
Sundqvist
Sundstrand
Sundström
Svanström
Svärd
Svedberg (surname)
Svedin
Svenonius
Svens
Svensson
Swartz (surname)
Swedberg
Swedlund
Syrén
T
Tånnander
Taube
Tedenby
Tegnér
Tegstedt
Tenggren
Theorin
Thofelt
Thollander
Thoresson
Thormahlen
Thörnell
Thornquist
Thörnqvist
Thorsell
Thunberg
Thunman
Tingsten
Tjernberg
Tobiasson
Tornquist
Törnros
Torvalds
Trolle (name)
Tunberg
Turesson
U
Uggla
Ulf
Ulvaeus
V
Vidgren (surname)
Viklund
Viksten
Vikström
Viktorsson
Vingqvist
Von Bahr
W
Waering
Wahlberg (surname)
Wahlbom
Wahlgren
Wahlin
Wahlqvist
Wahlström
Walgren
Wallenberg
Wallerstedt
Wallin
Wallmark
Wallquist
Weibull
Wennberg
Wennerberg
Wermelin
Wersäll
Westberg
Westergren
Westerholm
Westermark
Westin (surname)
Westlund
Wicksell
Wickström
Widegren
Widforss
Widing
Widlund
Wieslander
Wiklöf
Wikström
Wilhelmsson
Winblad
Wollter
Wranå
Z
Zachrisson
Zakrisson
'''


s = names.strip() + '\n'
s = re.sub(r'\n.+ \(.\)\n', '\n', s)
s = re.sub(r'List of.*\n', '', s)
s = re.sub(r'^\n', '', s)
s = re.sub(r'^.\n', '', s)
s = re.sub(r'\n.\n', '\n', s)
s = re.sub(r' \(.*\)\n', '\n', s)
s = re.sub(r'\n\n', '\n', s)

# remove duplicates
ss = list(set(s.split('\n')))
ss.sort()
s = '\n'.join(ss)
s = s[1:] if s[0] == '\n' else s

s = re.sub(r'(.*)\n', r'\t\t\t\t\t\t"\1",\n', s)
s = re.sub(r'\n(.*)$', r'\n\t\t\t\t\t\t"\1"', s) # end of str

s = s.strip()
##s = s[:-1]

pyperclip.copy(s)
print(s[:100])
print(s[-100:])

