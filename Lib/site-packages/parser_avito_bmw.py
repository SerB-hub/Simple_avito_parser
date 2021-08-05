from selenium import webdriver
from all_funcs import get_pages_amount, parse_pages, csv_dump

firefoxdriver = 'D:\\Downloads\\IT-courses\\Python_courses\\geckodriver.exe'
options = webdriver.FirefoxOptions()
# options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Firefox(executable_path=firefoxdriver)  # можно указать options в качестве аргумента chrome_options
browser.implicitly_wait(10)  # устанавливаем десятисекундную задержку
# Переход на первую страницу выдачи
url = 'https://www.avito.ru/sankt_peterburg_i_lo/avtomobili/bmw/x5-ASgBAgICAkTgtg3klyjitg22tCg?p=1'

browser.get(url)
requiredHtml = browser.page_source

array_all_pages = get_pages_amount(requiredHtml)

map = parse_pages(browser, array_all_pages)

csv_dump(map, 'C:\\Users\\user\\Desktop\\dict.csv')

browser.close()
browser.quit()

