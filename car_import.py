import requests

r = requests.get(url='https://api.exchangeratesapi.io/latest?base=EUR')
data = r.json()
exchange_rate = data['rates']['PLN']

price_in_eur = 9000
price_in_pln = price_in_eur * exchange_rate
car_capacity = 1800

if car_capacity > 2000:
    tax_percentage = 0.186
else:
    tax_percentage = 0.031

tax_confirmation = 17
technical_inspection = 98
translations = 200
registration = 256
tax = price_in_pln * tax_percentage

total_price_in_pln = price_in_pln + tax_confirmation + technical_inspection + translations + registration + tax

print(price_in_pln)
print(total_price_in_pln)



