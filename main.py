import requests
import re
from fake_headers import Headers
from bs4 import BeautifulSoup
import json
import unicodedata

host = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

page = requests.get(host, headers=Headers(browser='Mozilla', os='win').generate()).text

bs = BeautifulSoup(page, parser='lxml', features="lxml")

vacancy_list = bs.find(class_='sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg')

vacancies = vacancy_list.find_all(class_='serp-item')

#Основное задание
parsed_data = []
for vacancy in vacancies:
    tag_a = vacancy.find('a')
    a = tag_a.string
    django = re.search('[Dd]jango', a)
    flask = re.search('[Ff]lask', a)
    if django!= None or flask != None:
        link = tag_a.attrs['href']
        salary_txt = vacancy.find('span', class_='bloko-header-section-3').text
        salary = unicodedata.normalize('NFKD', salary_txt)
        company_txt = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        company_name = unicodedata.normalize('NFKD', company_txt)
        city = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy-address'}).text
        parsed_data.append({'link': link, 'salary': salary, 'company_name': company_name, 'city': city})

with open('file.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)

#Дополнительное задание
parsed_data_1 = []
for vacancy in vacancies:
    tag_a = vacancy.find('a')
    a = tag_a.string
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}, class_='bloko-header-section-3')
    if salary != None:
        salary_txt = salary.text
    else:
        continue

    usd = re.search('[Uu][Ss][Dd]', salary_txt)
    if usd != None:
         link = tag_a.attrs['href']
         salary_usd = unicodedata.normalize('NFKD', salary_txt)
         company_txt = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
         company_name = unicodedata.normalize('NFKD', company_txt)
         city = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy-address'}).text
         parsed_data_1.append({'link': link, 'salary': salary_usd, 'company_name': company_name, 'city': city})

with open('file_usd.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data_1, f, indent=2, ensure_ascii=False)