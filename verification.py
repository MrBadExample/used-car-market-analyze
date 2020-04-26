import requests
import csv


with open('fiat_500_report.csv', 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = list(csv_reader)

for element in data:
    link = element[2]
    r = requests.get(link)
    if r.status_code != 200:
        print(link + ' is probably sold.')

