import json

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import requests

url = 'https://store.epicgames.com/ru/browse?sortBy=releaseDate&sortDir=DESC&category=Game&count=40'


def get_source_code():
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome()
    driver.get(url)

    source_code = driver.page_source
    with open("source_code.html", 'w', encoding='utf-8') as file:
        file.write(source_code)
    print('[INFO] Writing complite!')


def get_links(file):
    with open(file, encoding='utf-8') as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    count = 1
    with open('game-links.txt', 'w', encoding='utf-8') as file:
        for link in soup.findAll('a', class_='css-15fmxgh'):
            file.writelines(link.get('href') + '\n')
            print(f'[INFO] Link write: {count}')
            count += 1


def get_data(file):
    base_url = 'https://store.epicgames.com'

    with open(file, encoding='utf-8') as f:
        links = f.readlines()
        count = 1
        for link in links:

            driver = webdriver.Chrome()
            driver.get(base_url + link)
            src = driver.page_source

            soup = BeautifulSoup(src, "lxml")

            try:
                title = soup.find('span', class_='css-inhi4e').text
            except:
                title = 'None'
            try:
                price = soup.findAll('span', class_='css-119zqif')[11].text
            except:
                price = 'None'
            try:
                game_type = soup.findAll('div', class_='css-u4p24i')[1].text
            except:
                game_type = 'None'
            try:
                time_to_sale = soup.find('span', class_='css-iqno47').text
            except:
                time_to_sale = 'None'
            try:
                developer = soup.findAll('span', class_='css-119zqif')[13].text
            except:
                developer = 'None'
            try:
                release_date = soup.findAll('span', class_='css-119zqif')[15].text
            except:
                release_date = 'None'
            try:
                description = soup.find('div', class_='css-1myreog').text
            except:
                description = 'None'

            result = {}
            result["№"] = count
            result["Title"] = title
            result["Price"] = price[:-2]
            result["Game type"] = game_type
            result['Sale time'] = time_to_sale
            result["Developer"] = developer
            result["Release date"] = release_date
            result["Descrition"] = description

            with open('data.txt', 'a', encoding='utf-8') as outfile:
                json.dump(result, outfile, ensure_ascii=False, indent=4)

            print(f'[INFO] Game №{count}:{title} successfully recorded')

            count += 1


def main():
    # get_source_code()
    # get_links('source_code.html')
    get_data('game-links.txt')


if __name__ == '__main__':
    main()
