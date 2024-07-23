import abc
from datetime import datetime
from typing import List, Dict
import requests

class InputValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, inp: str) -> str:
        pass

class CurrencyValidator(InputValidator):
    def validate(self, inp: str) -> str:
        valid_currencies = ['usd', 'eur', 'gel', '1', '2', '3', '1usd', '2eur', '3gel']
        if inp not in valid_currencies:
            print('\nInvalid input, such currency does not exist')
            return self.validate(input('\n1. USD\n2. EUR\n3. GEL\nChoose a currency: ').lower().replace(' ', ''))
        try:
            return ['usd', 'eur', 'gel'][int(inp)-1]
        except:
            return inp

class AmountValidator(InputValidator):
    def validate(self, inp: str) -> int:
        try:
            return int(inp)
        except ValueError:
            print('\nInvalid input, enter a number')
            return self.validate(input('\nEnter the amount of income: '))

class YearValidator(InputValidator):
    def validate(self, inp: str) -> int:
        try:
            year = int(inp)
            current_year = datetime.now().year
            if not(2016 <= year <= current_year):
                print('\nInvalid input, such year is not supported')
                return self.validate(input('\nEnter the year for which you want to calculate the tax: '))
            return year
        except ValueError:
            print('\nInvalid input, enter a number')
            return self.validate(input('\nEnter the year for which you want to calculate the tax: '))

class MonthValidator(InputValidator):
    def validate(self, inp: str) -> str:
        months = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }
        if inp.isdigit() and 0 < int(inp) <= 12:
            return ('0' * (int(inp) < 10)) + inp
        elif inp in months:
            return months[inp]
        print('\nInvalid input, such month does not exist')
        return self.validate(input('\nEnter the month of income (example: \'09\' or \'september\'): ').lower())

class DayValidator(InputValidator):
    def validate(self, inp: str, month: str, year: int) -> str:
        try:
            day = int(inp)
            max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][int(month)-1]
            if month == '02' and year % 4 == 0:
                max_days += 1
            if not(0 < day <= max_days):
                print('\nInvalid input, such day does not exist')
                return self.validate(input('\nEnter the day of income (example: \'09\' or \'9\'): '), month, year)
            return ('0' * (day < 10)) + str(day)
        except ValueError:
            print('\nInvalid input, enter a number')
            return self.validate(input('\nEnter the day of income (example: \'09\' or \'9\'): '), month, year)

class Transaction:
    def __init__(self, currency: str, year: int, month: str, day: str, amount: float):
        self.currency = currency
        self.year = year
        self.month = month
        self.day = day
        self.amount = amount

class CurrencyConverter:
    def __init__(self):
        self.symbols = {'usd': '$', 'eur': '€', 'gel': '₾'}

    def convert_to_gel(self, transaction: Transaction) -> float:
        if transaction.currency == 'gel':
            return transaction.amount
        
        date = f"{transaction.year}-{transaction.month}-{transaction.day}"
        response = requests.get(f'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date={date}')
        currencies = response.json()

        if transaction.currency == 'usd':
            rate = currencies[0]['currencies'][40]['rate'] / currencies[0]['currencies'][40]['quantity']
        elif transaction.currency == 'eur':
            rate = currencies[0]['currencies'][13]['rate'] / currencies[0]['currencies'][13]['quantity']
        else:
            raise ValueError(f"Unsupported currency: {transaction.currency}")

        return transaction.amount * rate

    def format_amount(self, amount: float, currency: str) -> str:
        return f"{amount}{self.symbols[currency]}"

class TaxCalculator:
    def calculate(self, total_amount: float) -> float:
        if total_amount <= 140000:
            return round(total_amount / 100, 2)
        else:
            # Placeholder for more complex tax calculation
            return round(total_amount / 100, 2)  # This should be replaced with the actual calculation

class TransactionManager:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.currency_converter = CurrencyConverter()
        self.tax_calculator = TaxCalculator()

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def calculate_total_tax(self) -> float:
        total_amount = sum(self.currency_converter.convert_to_gel(t) for t in self.transactions)
        return self.tax_calculator.calculate(total_amount)

class UserInterface:
    def __init__(self):
        self.currency_validator = CurrencyValidator()
        self.amount_validator = AmountValidator()
        self.year_validator = YearValidator()
        self.month_validator = MonthValidator()
        self.day_validator = DayValidator()
        self.transaction_manager = TransactionManager()

    def run(self):
        print('\nHello, this program will help you calculate entrepreneur taxes')
        while True:
            currency = self.currency_validator.validate(input('\n1. USD\n2. EUR\n3. GEL\nChoose a currency: ').lower().replace(' ', ''))
            year = self.year_validator.validate(input('\nEnter the year for which you want to calculate the tax: '))
            
            while True:
                month = self.month_validator.validate(input('\nEnter the month of income (example: \'09\' or \'september\'): ').lower())
                day = self.day_validator.validate(input('\nEnter the day of income (example: \'09\' or \'9\'): '), month, year)
                amount = self.amount_validator.validate(input('\nEnter the amount of income: '))
                
                transaction = Transaction(currency, year, month, day, amount)
                self.transaction_manager.add_transaction(transaction)
                
                action = input('\n1. Calculate taxes\n2. Add more income\nChoose an action: ').lower().replace(' ', '').replace('.', '')
                if action in ['1', 'calculate_taxes', '1calculate_taxes']:
                    total_tax = self.transaction_manager.calculate_total_tax()
                    print(f'\nThis year you need to pay: {total_tax}₾')
                    break
            
            action = input('\n1. Restart\n2. Exit\nChoose an action: ').lower().replace(' ', '').replace('.', '')
            if action in ['2', 'exit', '2exit']:
                break

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
