from requests import get
from json import loads
from time import localtime

class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def check_month(input_value):
        months = {'january': '01', 'february': '02', 'march': '03', 'april': '04', 'may': '05', 'june': '06', 'july': '07', 'august': '08', 'september': '09', 'october': '10', 'november': '11', 'december': '12'}
        if input_value.isdigit() and 0 < int(input_value) <= 12:
            return ('0'*(int(input_value)<10)) + input_value
        elif input_value in list(months.keys()):
            return months[input_value]
        print('\nInvalid input, month not found')
        return Date.check_month(input('\nEnter income month (e.g., \'09\' or \'september\'): ').lower())

    @staticmethod
    def check_day(input_value, month, year):
        try:
            input_value = int(input_value)
            max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][int(month)-1]
            if (month == '02') and not (year % 4):
                max_days += 1
            if not (0 < input_value <= max_days):
                print('\nInvalid input, day does not exist')
                return Date.check_day(input('\nEnter income day (e.g., \'09\' or \'9\'): '), int(month), int(year))
            return ('0'*(input_value < 10)) + str(input_value)
        except:
            print('\nInvalid input, enter a number')
            return Date.check_day(input('\nEnter income day (e.g., \'09\' or \'9\'): '), int(month), int(year))

    @staticmethod
    def check_year(input_value):
        try:
            input_value = int(input_value)
            if not(2016 <= input_value <= localtime()[0]):
                print('\nInvalid input, year not supported')
                return Date.check_year(input('\nEnter the year for which you want to calculate taxes: '))
            return input_value
        except:
            print('\nInvalid input, enter a number')
            return Date.check_year(input('\nEnter the year for which you want to calculate taxes: '))

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    @staticmethod
    def check_amount(input_value):
        try:
            return int(input_value)
        except:
            print('\nInvalid input, enter a number')
            return Money.check_amount(input('\nEnter the income amount: '))

    @staticmethod
    def check_currency(input_value):
        valid_currencies = ['usd', 'eur', 'gel', '1', '2', '3', '1usd', '2eur', '3gel']
        if input_value not in valid_currencies:
            print('\nInvalid input, currency not found')
            input_value = Money.check_currency(input('\n1. USD\n2. EUR\n3. GEL\nChoose currency: ').lower().replace(' ', ''))
        try:
            return ['usd', 'eur', 'gel'][int(input_value)-1]
        except:
            return input_value

class Transaction:
    def __init__(self, date, money):
        self.date = date
        self.money = money

    def convert_to_gel(self):
        currencies = loads(get(f'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date={self.date.year}-{self.date.month}-{self.date.day}').text)
        amount = self.money.amount
        currency = self.money.currency
        rate = 1
        symbols = {'usd': '$', 'eur': '€', 'gel': '₾'}
        if currency == 'usd':
            rate = currencies[0]['currencies'][40]['rate'] / currencies[0]['currencies'][40]['quantity']
            amount *= rate
        elif currency == 'eur':
            rate = currencies[0]['currencies'][13]['rate'] / currencies[0]['currencies'][13]['quantity']
            amount *= rate
        print(f'\nCurrency: {currency}\nDate: {self.date.day}/{self.date.month}/{self.date.year}\nAmount: {self.money.amount}{symbols.get(currency, "")}'+ f' * {rate} = {round(amount, 2)}₾'*(currency in ['usd', 'eur']))
        return amount

def value_check(inp):
    valid_values = ['1', '2', 'calculatetaxes', 'addmoreincome', '1calculatetaxes', '2addmoreincome']
    if inp not in valid_values:
        print('\nInvalid input, such action does not exist')
        inp = value_check(input('\n1. Calculate taxes\n2. Add more income\nChoose action: ').lower().replace(' ', '').replace('.', ''))
    return inp

def check_action(input_value):
    valid_actions = ['1', '2', '3', 'addincome', 'restart', 'exit', '1addincome', '2restart', '3exit']
    if input_value not in valid_actions:
        print('\nInvalid input, action not found')
        input_value = check_action(input('\n1. Add income\n2. Restart\n3. Exit\nChoose action: ').lower().replace(' ', '').replace('.', ''))
    return input_value

def check_action2(input_value):
    valid_actions2 = ['1', '2', 'restart', 'exit', '1restart', '2exit']
    if input_value not in valid_actions2:
        print('\nInvalid input, action not found')
        return check_action2(input('\n1. Restart\n2. Exit\nChoose action: ').lower().replace(' ', '').replace('.', ''))
    return input_value

def process_transaction(currency, year, transactions):
    month = Date.check_month(input('\nEnter income month (e.g., \'09\' or \'september\'): ').lower())
    day = Date.check_day(input('\nEnter income day (e.g., \'09\' or \'9\'): '), month, year)
    amount = Money.check_amount(input('\nEnter the income amount: '))
    date = Date(day, month, year)
    money = Money(amount, currency)
    transaction = Transaction(date, money)
    amount_in_gel = transaction.convert_to_gel()
    transactions.append(amount_in_gel)
    action = value_check(input('\n1. Calculate taxes\n2. Add more income\nChoose action: ').lower().replace(' ', '').replace('.', ''))
    if action in ['1', 'calculatetaxes', '1calculatetaxes']:
        total_amount = sum(transactions)
        final_amount = round(total_amount / 100, 2)
        if total_amount <= 140000:
            print(f'\nThis year you need to pay: {round(total_amount, 2)}₾ * 1% = {final_amount}₾')
        else:
            print(f'\nThis year you need to pay: not sure how much GEL')
            #дописать
        action2 = check_action2(input('\n1. Restart\n2. Exit\nChoose action: ').lower().replace(' ', '').replace('.', ''))
        if action2 in ['2', 'exit', '2exit']:
            exit()
        elif action2 in ['1', 'restart', '1restart']:
            main()
    elif action in ['2', 'addmoreincome', '2addmoreincome']:
        process_transaction(currency, year, transactions)

def main():
    print('\nHello, this program will help you calculate entrepreneur taxes')
    currency = Money.check_currency(input('\n1. USD\n2. EUR\n3. GEL\nChoose currency: ').lower().replace(' ', '').replace('.', ''))
    year = Date.check_year(input('\nEnter the year for which you want to calculate taxes: '))
    action = check_action(input('\n1. Add income\n2. Restart\n3. Exit\nChoose action: ').lower().replace(' ', '').replace('.', ''))
    if action in ['3', 'exit', '3exit']:
        exit()
    elif action in ['2', 'restart', '2restart']:
        main()
    elif action in ['1', 'addincome', '1addincome']:
        transactions = []
        process_transaction(currency, year, transactions)

main()
