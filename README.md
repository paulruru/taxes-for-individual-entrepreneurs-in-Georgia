Program Specification - Entrepreneur Tax Calculator
This document outlines the functionalities and design of a program that assists Georgian entrepreneurs with calculating their annual income tax.

1. Functionality

The program helps users calculate their annual income tax based on user-provided income details. Here are the key functionalities:

User enters income details:
Income amount
Income currency (USD, EUR, or GEL)
Income date (day, month, year)
Program validates user input for data integrity (e.g., valid date format, currency code).
Program retrieves daily exchange rates for USD and EUR (if income currency is not GEL) using an external API.
Program converts income amount to GEL based on retrieved exchange rates.
Program simulates a basic tax calculation based on a pre-defined income threshold (currently set at 140,000 GEL). Note: This is a simplified calculation and may not reflect actual tax regulations.
Users can add multiple income entries throughout the year.
2. Technical Specifications

Programming Language: Python (v3.x recommended)
Libraries:
requests - for making API calls to external currency exchange service.
json - for parsing JSON data received from the API.
time (optional) - for functionalities related to current date/time.
3. Assumptions and Limitations

The program retrieves daily exchange rates. Fluctuations within the day are not considered.
The current tax calculation is a simplified example and may not reflect actual Georgian tax regulations. Users should consult with a tax professional for accurate tax calculations.
The program does not store user data or past calculations.
4. User Interface

The program uses a text-based command-line interface for user interaction.

5. Error Handling

The program implements basic input validation to ensure data integrity. Error messages are provided to guide users in case of invalid input.

6. Testing

The program should include unit tests to verify the functionality of individual components (e.g., input validation, currency conversion).

7. Deployment

This program is designed to be run locally on a user's machine.

8. Future Enhancements

Integrate with a more comprehensive tax calculation API to reflect actual tax regulations.
Implement a persistent storage mechanism to save user data and past calculations.
Develop a graphical user interface (GUI) for a more user-friendly experience.
This specification provides a high-level overview of the program's functionalities and design considerations.  More detailed technical specifications can be added based on the project's specific requirements.
