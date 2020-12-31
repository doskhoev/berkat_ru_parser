import requests
from bs4 import BeautifulSoup
import json

baseUrl = 'https://berkat.ru'
result = []

def parse_item(result, item):
    prices = [e for e in item.find('div', {'class': 'board_list_footer_left'}).find_all('span') if e.text.startswith('Цена:')]
    photos = list(map(lambda item: baseUrl + item.get('href'), item.find('div', {'class': 'photos'}).find_all('a')))    
    obj = {
        'title': item.find('a').text,
        'link': baseUrl + item.find('a').get('href'),
        'text': item.find('p').text,
        'tel': item.find('a', {'class': 'get_phone_style'}).text,
        'price': prices[0].text if len(prices) > 0 else '',
        'photos': photos
    }
    result.append(obj)

for i in range(1, 11):
    url = 'https://berkat.ru/board?page=' + str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    items = soup.find_all('div', {'class': 'board_list_item'})
    for item in items:
        parse_item(result, item)

print(json.dumps(result, indent = 4, ensure_ascii = False).encode('utf8').decode())


