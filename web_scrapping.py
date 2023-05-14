import json
import requests

from bs4 import BeautifulSoup

if __name__ == '__main__':
        
    headers = {
    'authority': 'www.yeezysupply.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

    session = requests.session()

    response = session.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    FOUND = "Python"
    FOUND_1 = "Москва" 
    FOUND_2 = "Санкт-Петербург"
    FOUND_3 = "Django"
    FOUND_4 = "Flask"

    d = {}
    a = []

# 1. Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург". Эти параметры задаются по ссылке

    for element in soup.find_all(class_='serp-item'):
        title = element.find('h3', class_="bloko-header-section-3").text.strip()
        city = element.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
        
        link = element.find('a').get('href')
                
        if FOUND in title or FOUND_1 in city or FOUND_2 in city:
            print('Success')

# 2. Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".

        link_2 = session.get(link, headers=headers)
        soup_2 = BeautifulSoup(link_2.text, 'html.parser')
        find_element_1 = soup_2.find_all(class_='bloko-tag-list')
        find_element_2 = soup_2.find(class_="wrapper-flat--H4DVL_qLjKLCo1sytcNI")
        find_city = find_element_2.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite").text.strip()
        find_element_3 = soup_2.find("span", class_="vacancy-company-name")
        find_title = find_element_3.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite").text.strip()

        for element_2 in find_element_1:
            name_2 = element_2.find_all(class_="bloko-tag bloko-tag_inline")      
            for elem in name_2:
                keeeey = elem.find('span', class_= "bloko-tag__section bloko-tag__section_text").text.strip()

                if FOUND_3 in keeeey or FOUND_4 in keeeey:
                    d = {'ссылка':link,'зп':find_city,'название':find_title,'город':city}
                    a.append(d)

# 3. Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.               
                
    with open('sw_templates.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(a, ensure_ascii=False, indent=1))