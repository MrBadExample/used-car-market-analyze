import requests
import csv
from bs4 import BeautifulSoup
import re
import datetime

date_time = datetime.datetime.now()

make = 'fiat'
model = '500'
from_date = '2010'
to_date = '2010'

base_url = 'https://www.otomoto.pl/osobowe/{}/{}/od-{}/?search%5Bfilter_float_year%3Ato%5D={}&search%' \
           '5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=' \
    .format(make, model, from_date, to_date)


def find_last_page():
    r = requests.get(base_url).text
    soup = BeautifulSoup(r, 'lxml')
    last_page = int(soup.select('.page')[-1].text)
    return last_page


def generate_objects():
    object_map = []
    for page_number in range(1, find_last_page()) :
        page_url = base_url + '&page={}'.format(page_number)
        r = requests.get(page_url).text
        soup = BeautifulSoup(r, 'lxml')
        car_list = soup.select('article.offer-item')
        for car in car_list:
            oto_id = car.find('a', class_='offer-title__link')['data-ad-id']
            if oto_id not in build_index_list():
                link = car.find('a', class_='offer-title__link')['href']
                price_str = car.find('span', class_='offer-price__number').text.replace(' ', '')
                price = re.findall(r'\d+', price_str)[0]
                location = car.find('span', {'ds-location-city'}).text
                parameters = ["mileage", "year", "engine_capacity", "fuel_type"]
                values = [oto_id, price, location, link, date_time]
                for parameter in parameters:
                    try:
                        value = car.find('li', {"data-code" : parameter}).text.strip()
                        values.append(value)
                    except AttributeError:
                        values.append('')

                object_map.append(values)
        return object_map


def build_csv_report():
    with open(make + "_" + model + '_report.csv', 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in generate_objects():
            csv_writer.writerow(row)


def build_index_list():
    index_list = []
    with open('fiat_500_report.csv', 'r', newline='') as csv_file :
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)
    for value in data:
        index = value[0]
        index_list.append(index)
    return index_list


build_csv_report()