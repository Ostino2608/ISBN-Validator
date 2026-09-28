"""
ISBN Validator

Validates ISBN-10 and ISBN-13 codes by recalculating the check digit
from the other digits and comparing it to the one provided.
"""


def validate_isbn(isbn, length):
    """
    Validate an ISBN-10 or ISBN-13 code and print the result.

    Hyphens and spaces are stripped first, since real-world ISBNs are
    almost always printed with them (e.g. "0-306-40615-2").
    """
    isbn = isbn.replace('-', '').replace(' ', '')

    if len(isbn) != length:
        print(f'ISBN-{length} code should be {length} digits long.')
        return

    main_digits = isbn[0:length - 1]
    given_check_digit = isbn[length - 1].upper()

    if not main_digits.isdigit():
        print(f'ISBN-{length} code should contain only digits (and, for '
              'ISBN-10, an "X" as the final check digit).')
        return

    main_digits_list = [int(digit) for digit in main_digits]

    # Calculate the check digit from other digits
    if length == 10:
        expected_check_digit = calculate_check_digit_10(main_digits_list)
    else:
        expected_check_digit = calculate_check_digit_13(main_digits_list)

    # Check if the given check digit matches with the calculated check digit
    if given_check_digit == expected_check_digit:
        print('Valid ISBN Code.')
    else:
        print('Invalid ISBN Code.')


def calculate_check_digit_10(main_digits_list):
    """Calculate the expected ISBN-10 check digit from the first 9 digits."""
    digits_sum = 0
    for index, digit in enumerate(main_digits_list):
        digits_sum += digit * (10 - index)

    result = 11 - digits_sum % 11
    if result == 11:
        expected_check_digit = '0'
    elif result == 10:
        expected_check_digit = 'X'
    else:
        expected_check_digit = str(result)
    return expected_check_digit


def calculate_check_digit_13(main_digits_list):
    """Calculate the expected ISBN-13 check digit from the first 12 digits."""
    digits_sum = 0
    for index, digit in enumerate(main_digits_list):
        if index % 2 == 0:
            digits_sum += digit * 1
        else:
            digits_sum += digit * 3

    result = 10 - digits_sum % 10
    if result == 10:
        expected_check_digit = '0'
    else:
        expected_check_digit = str(result)
    return expected_check_digit


def main():
    user_input = input('Enter ISBN and length: ')
    values = [val.strip() for val in user_input.split(',')]
    isbn = values[0]
    length = int(values[1])

    if length == 10 or length == 13:
        validate_isbn(isbn, length)
    else:
        print('Length should be 10 or 13.')


if __name__ == '__main__':
    main()
