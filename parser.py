import requests
from bs4 import BeautifulSoup
import pandas as pd
#from time import sleep
#from selenium import  webdriver
#driver = webdriver.Chrome()
user_login = input('Введите ID пользователя: ')
url = f'https://www.kinopoisk.ru/user/{user_login}/votes/'

r = requests.get(url)
#driver.get(url)
#sleep(30)
html_content = requests.get(url).text
with open('kinopoisk.html', 'w', encoding='utf-8') as output_file:
   output_file.write(r.text)
def collect_user_rates(user_login):
    page_num = 1
    data = []

    url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}/#list'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'lxml')
    entries = soup.find_all('div', {'class':{'item', 'item even'}})
    while True:
        if len(entries) == 0:  # Признак остановки
            break
        for entry in entries:
            nameRus = entry.find('div', class_='nameRus')
            film_name = nameRus.find('a').text
            div_rating = entry.find('div', class_='rating')
            rating = div_rating.find('b').text
            data.append({'film name': film_name, 'rating': rating})
        page_num += 1  #Переходим на следующую страницу
    print(len(entries))
    return data
user_rates = collect_user_rates(user_login)
df = pd.DataFrame(user_rates)

df.to_excel('user_rates.xlsx')
print(len(user_rates))
