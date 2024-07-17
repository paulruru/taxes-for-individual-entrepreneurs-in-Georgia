#https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date=2024-07-12
from requests import get
from json import loads
from time import localtime




def currencycheck(inp):
    if inp not in ['usd', 'eur', 'gel', '1', '2', '3', '1usd', '2eur', '3gel']:
        print('\nНекоректный ввод, такой валюты нет')
        inp = currencycheck(input('\n1. USD\n2. EUR\n3. GEL\nВыберите валюту: ').lower().replace(' ', ''))
    try:
        return ['usd', 'eur', 'gel'][int(inp)-1]
    except:
        return inp


def amountcheck(inp):
    try:
        inp = int(inp)
        return inp
    except:
        print('\nНекоректный ввод, введите число')
        inp = amountcheck(input('\nВведите сумму дохода: '))


def yearcheck(inp):
    try:
        inp = int(inp)
        if not(2016 <= inp <= localtime()[0]):
            print('\nНекоректный ввод, такой год не поддерживается')
            inp = yearcheck(input('\nВведите год за который вы хотите рассчитать налог: '))
        return inp
    except:
        print('\nНекоректный ввод, введите число')
        inp = yearcheck(input('\nВведите год за который вы хотите рассчитать налог: '))


def valuecheck(inp):
    if inp not in ['1', '2', '3', 'добавитьдоход', 'перезапустить', 'выйти', '1добавитьдоход', '2перезапустить', '3выйти']:
        print('\nНекоректный ввод, такого действия нет')
        inp = valuecheck(input('\n1. Добавить доход\n2. Перезапустить\n3. Выйти\nВыберите действие: ').lower().replace(' ', '').replace('.', ''))
    return inp


def actioncheck(inp):
    if inp not in ['1', '2', 'рассчитатьналоги', 'добавитьещёдоход', '1рассчитатьналоги', '2добавитьещёдоход']:
        print('\nНекоректный ввод, такого действия нет')
        inp = actioncheck(input('\n1. Рассчитать\n2. Добавить ещё доход\nВыберите действие: ').lower().replace(' ', '').replace('.', ''))
    return inp


def monthcheck(inp):
    try:
        inp = int(inp)
        months = {1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12'}
    except:
        months = {'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04', 'май': '05', 'июнь': '06', 'июль': '07', 'август': '08', 'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'}
    if inp not in list(months.keys()):
        print('\nНекоректный ввод, такого месяца нет')
        inp = monthcheck(input('\nВведите месяц дохода(пример: \'09\' или \'сентябрь\'): ').lower())
    return months[inp]


def daycheck(inp, month, year):
    try:
        inp = int(inp)
        maximum = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
        if (month == '02') and not(year%4):
            maximum += 1
        if not(0 < inp <= maximum): 
            print('\nНекоректный ввод, такого дня не существует')
            inp = daycheck(input('\nВведите день дохода(пример: \'9\'): '), int(month), int(year))
        return ('0'*(inp<10)) + str(inp)
    except:
        print('\nНекоректный ввод, введите число')
        inp = daycheck(input('\nВведите день дохода(пример: \'9\'): '), int(month), int(year))
    

def action2check(inp):
    if inp not in ['1', '2', 'перезапустить', 'выйти', '1перезапустить', '2выйти']:
        print('\nНекоректный ввод, такого действия нет')
        inp = action2check(input('\n1. Перезапустить\n2. Выйти\nВыберите действие: ').lower().replace(' ', '').replace('.', ''))
    else:
        return inp


def transaction(currency, year, transactions):
    month = monthcheck(input('\nВведите месяц дохода(пример: \'09\' или \'сентябрь\'): ').lower())
    day = daycheck(input('\nВведите день дохода(пример: \'09\'): '), int(month), int(year))
    amount = amountcheck(input('\nВведите сумму дохода: '))
    amountcopy = amount 
    currencies = loads(get(f'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date={year}-{month}-{day}').text)
    cur, simb = 1, {'usd': '$', 'eur': '€'}
    if currency == 'usd':
        cur = currencies[0]['currencies'][40]['rate'] / currencies[0]['currencies'][40]['quantity']
        amount *= cur
    elif currency == 'eur':
        cur = currencies[0]['currencies'][13]['rate'] / currencies[0]['currencies'][13]['quantity']
        amount *= cur
    print(f'\nВалюта: {currency}\nДата: {day}/{month}/{year}\nСумма: {amountcopy}{simb[currency]}'+ f' * {cur} = {round(amount, 2)}₾'*(currency in ['usd', 'eur']))
    transactions.append([currency, year, month, day, amount])
    action = actioncheck(input('\n1. Рассчитать налоги\n2. Добавить ещё доход\nВыберите действие: ').lower().replace(' ', '').replace('.', ''))
    if action in ['1', 'рассчитатьналоги', '1.рассчитатьналоги']:
        allamount = sum([transaction[4] for transaction in transactions])
        overallamount = round(allamount/100, 2)
        if allamount <= 140000:
           print(f'\nВ этом году вам нужно заплатить: {round(allamount, 2)} * 1% = {overallamount}₾')
        else:
            print(f'\nВ этом году вам нужно заплатить: не знаю сколько лари')
        action2 = action2check(input('\n1. Перезапустить\n2. Выйти\nВыберите действие: ').lower().replace(' ', '').replace('.', ''))
        if action2 in ['2', 'выйти', '3выйти']:
            exit()
        elif action2 in ['1', 'перезапустить', '1перезапустить']:
            main()
    elif action in ['2', 'добавитьещёдоход', '2.добавитьещёдоход']:
        transaction(currency, year, transactions)
    

def main():
    #try:
    print('\nЗдравствуйте, эта программа поможет вам рассчитать налоги предпринимателя')
    currency = currencycheck(input('\n1. USD\n2. EUR\n3. GEL\nВыберите валюту: ').lower().replace(' ', '').replace('.', ''))
    year = yearcheck(input('\nВведите год за который вы хотите рассчитать налог: '))
    value = valuecheck(input('\n1. Добавить доход\n2. Перезапустить\n3. Выйти\nВыберите действие: ').lower().replace(' ', '').replace('.', ''))
    if value in ['3', 'выйти', '3выйти']:
        exit()
    elif value in ['2', 'перезапустить', '2перезапустить']:
         main()
    elif value in ['1', 'добавитьдоход', '1добавитьдоход']:
        transactions = []
        transaction(currency, year, transactions)
    '''except:
        print('Что-то пошло не так, попрубуйте снова')
        main()'''


main()
