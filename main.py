from bs4 import BeautifulSoup
import requests

url_base = 'https://datasets.freesound.org/fsd/explore/%252Fm%252F04szw/'

r = requests.get(url_base)
s = BeautifulSoup(r.text, 'html.parser')

page_numbers = s.find('div', {'class': ['ui pagination menu']})
max_page_number = page_numbers.find_all('a')[-2]['href'].split('=')[-1]

hierarchy = 'Root'
tree = s.find('tr').find_all('a')
for h in tree:
    hierarchy += '>' + h.text

audio_urls = []
for p in range(int(max_page_number)):

    page_number = p + 1
    url = url_base + '?page=' + str(page_number)

    print('Processing', page_number)

    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')

    players = s.find_all('div', {'class':'player_container'})
    for c in players:
        url = 'http:' + c.script.text.split('sound_url:')[-1].split('"')[1]
        audio_urls.append(url)

fname = hierarchy + '.txt'
with open('urls/' + fname, 'w') as f:
    for url in audio_urls:
        f.write(url + '\n')
