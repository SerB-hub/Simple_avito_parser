import csv
from time import sleep
from bs4 import BeautifulSoup
import math


def get_pages_amount(required_html):  # получает количество страниц с объявлениями
    soup = BeautifulSoup(required_html, 'lxml')
    all_pages_for_parse = soup.find('span', attrs={'data-marker': 'page-title/count'}).text
    # logging.info(f"row_all_pages_for_parse: {all_pages_for_parse}")
    print(all_pages_for_parse)
    all_pages_for_parse = math.ceil(int(all_pages_for_parse) / 50)
    # logging.info(f"Количество объявлений: {all_pages_for_parse}")
    array_all_pages = [i for i in range(1, (all_pages_for_parse + 1))]
    # logging.info(f"Массив номеров всех страниц с объявлениями: {array_all_pages}")
    return array_all_pages


def parse_pages(browser, array_all_pages):  # парсит объявления со всех страниц
    map = {}
    id = 0
    id_map = 1

    for page in array_all_pages:
        requiredHtml = browser.page_source

        soup = BeautifulSoup(requiredHtml, 'lxml')  # html5lib

        ads = soup.find_all('div',
                            class_='iva-item-root-G3n7v photo-slider-slider-3tEix iva-item-list-2_PpT iva-item-redesign-1OBTh items-item-1Hoqq items-listItem-11orH js-catalog-item-enum')

        for i in range(len(ads)):
            ad = ads[i]
            id += 1
            map[id] = {}

            # находим цену
            price = ad.find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').text
            price = price.replace('\xa0', ' ')
            # находим название, год
            name = ad.find('h3',
                           class_="title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc text-text-1PdBw text-size-s-1PUdo text-bold-3R9dt").text
            name_year = str(name).split(', ')
            name = name_year[0]
            year = name_year[1]
            map[id]["name"] = name
            map[id]["year"] = year
            map[id]["price"] = price

        for i in range(len(ads)):
            # logging.info(f" Объявление №{id_map}: {map[id_map]}")
            print(map[id_map])
            id_map += 1

        sleep(3)
        try:
            browser.find_element_by_xpath("//span[@data-marker='pagination-button/next']").click()

        except Exception as ex:
            print(ex)
    return map


def csv_dump(map, path):  # записывает данные в csv файл для дольнейшей обработки в pandas
    with open(path, 'w', encoding="utf-16", newline='') as csv_file:
        fieldnames = ['name', 'year', 'price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in map.items():
            writer.writerow(value)
