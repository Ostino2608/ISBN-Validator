"""
Demo script: run a handful of ISBNs (valid, invalid, and hyphenated)
through the validator.

Usage:
    python example.py
"""

from isbn_validator import validate_isbn

if __name__ == '__main__':
    print('A real, hyphenated ISBN-10 (as printed on a book):')
    validate_isbn('0-306-40615-2', 10)

    print('\nThe same ISBN, but with a typo in the check digit:')
    validate_isbn('0-306-40615-3', 10)

    print('\nA real, hyphenated ISBN-13:')
    validate_isbn('978-0-13-235088-4', 13)

    print('\nAn ISBN-10 whose check digit is "X":')
    validate_isbn('0-439-42089-X', 10)
