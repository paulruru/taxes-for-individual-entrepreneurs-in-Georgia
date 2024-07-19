Program Specification
Overview
This program assists users in calculating taxes for entrepreneurial income by converting amounts from various currencies to Georgian Lari (GEL) and determining the tax owed based on the total income for a specified year. The program allows users to input multiple transactions, convert them to GEL, and calculate the applicable taxes.

Components
Classes

Date

Handles date validation and formatting.
Methods:
__init__(self, day, month, year): Initializes the date with day, month, and year.
check_month(input_value): Validates and formats the month input.
check_day(input_value, month, year): Validates and formats the day input considering month and leap years.
check_year(input_value): Validates the year input within a supported range.
Money

Manages currency and amount validation.
Methods:
__init__(self, amount, currency): Initializes the amount and currency.
check_amount(input_value): Validates and formats the amount input.
check_currency(input_value): Validates the currency input against a list of accepted values.
Transaction

Handles conversion of different currencies to GEL and displays conversion details.
Methods:
__init__(self, date, money): Initializes the transaction with date and money.
convert_to_gel(self): Converts the transaction amount to GEL based on current exchange rates and prints the conversion details.
Functions

get_valid_input(prompt, valid_options): Prompts the user for input and validates it against a list of acceptable options. Continues prompting until a valid input is received.

process_transaction(currency, year, transactions): Handles the input of transaction details (month, day, amount), creates a Transaction object, converts the amount to GEL, and updates the transaction list. Also manages the calculation of taxes and subsequent actions (calculate taxes, add more income, restart, or exit).

main(): The main entry point of the program. Handles initial user setup (currency and year), and manages user actions (add income, restart, exit). Calls process_transaction() to handle income data and tax calculations.

User Interaction
Input Validation

Prompts the user to enter valid months, days, years, amounts, and currencies.
Ensures input is correctly formatted and falls within acceptable ranges.
Actions

Add Income: Allows the user to enter additional income transactions and calculates taxes based on the accumulated income.
Calculate Taxes: Computes the taxes due based on the total income and displays the result.
Restart: Restarts the program, allowing the user to change currency or year.
Exit: Terminates the program.
Error Handling
The program includes error handling for invalid input and network issues during currency conversion.
Prompts the user to correct any invalid inputs and re-enter data as needed.
External Dependencies
Currency Conversion: Uses the National Bank of Georgia's API to obtain current exchange rates.
Assumptions
The API endpoint used for currency conversion is accessible and returns valid JSON data.
The user provides valid and sensible inputs for all prompts.
