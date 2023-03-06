import pyperclip, re, json

country = 'Sweden'

with open('cities.json', encoding='utf-8') as f:
    cities_dict = json.load(f)

keys = list(cities_dict.keys())
key = ''
for k in keys:
    if k.find(country) > -1:
        key = k
        break
cities = cities_dict[key]

s = ''.join(f'\t\t\t\t\t"{c}",\n' for c in cities)
s = s[:-2]

##s = names.strip() + '\n'
##s = re.sub(r'List of.*\n', '', s)
##s = re.sub(r'\n\n', '\n', s)
##s = re.sub(r'^.\n', '', s)
##s = re.sub(r'\n.\n', '\n', s)
##s = re.sub(r' \(.*\)\n', '\n', s)
##s = re.sub(r'(.*)\n', r'\t\t\t\t\t\t"\1",\n', s)
##
##s = s.strip()
##s = s[:-1]

pyperclip.copy(s)
print(s[:100])
print(s[-100:])
