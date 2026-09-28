"""
Basic tests for isbn_validator.py.

Run with:
    pytest
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from isbn_validator import (  # noqa: E402
    validate_isbn,
    calculate_check_digit_10,
    calculate_check_digit_13,
)


# --- calculate_check_digit_10 ---

def test_calculate_check_digit_10_known_value():
    # 0-306-40615-2 is a well-known valid ISBN-10 example.
    digits = [int(d) for d in '030640615']
    assert calculate_check_digit_10(digits) == '2'


def test_calculate_check_digit_10_returns_x_when_needed():
    # 0-439-42089-X (Harry Potter) — the check digit is 'X'.
    digits = [int(d) for d in '043942089']
    assert calculate_check_digit_10(digits) == 'X'


# --- calculate_check_digit_13 ---

def test_calculate_check_digit_13_known_value():
    digits = [int(d) for d in '978013235088']
    assert calculate_check_digit_13(digits) == '4'


# --- validate_isbn: hyphen handling (the fixed bug) ---

def test_validate_isbn_10_accepts_hyphens(capsys):
    # Regression test: previously, hyphens made the length check fail
    # even for a genuinely valid ISBN.
    validate_isbn('0-306-40615-2', 10)
    assert 'Valid ISBN Code.' in capsys.readouterr().out


def test_validate_isbn_13_accepts_hyphens(capsys):
    validate_isbn('978-0-13-235088-4', 13)
    assert 'Valid ISBN Code.' in capsys.readouterr().out


def test_validate_isbn_10_accepts_spaces(capsys):
    validate_isbn('0 306 40615 2', 10)
    assert 'Valid ISBN Code.' in capsys.readouterr().out


# --- validate_isbn: normal cases ---

def test_validate_isbn_10_without_separators(capsys):
    validate_isbn('0306406152', 10)
    assert 'Valid ISBN Code.' in capsys.readouterr().out


def test_validate_isbn_10_with_x_check_digit(capsys):
    validate_isbn('043942089X', 10)
    assert 'Valid ISBN Code.' in capsys.readouterr().out


def test_validate_isbn_13_without_separators(capsys):
    validate_isbn('9780132350884', 13)
    assert 'Valid ISBN Code.' in capsys.readouterr().out


def test_validate_isbn_rejects_wrong_check_digit(capsys):
    # Same ISBN as a valid test above, but with the last digit changed.
    validate_isbn('0-306-40615-3', 10)
    assert 'Invalid ISBN Code.' in capsys.readouterr().out


def test_validate_isbn_rejects_wrong_length(capsys):
    validate_isbn('12345', 10)
    assert 'should be 10 digits long' in capsys.readouterr().out


def test_validate_isbn_rejects_non_digit_input(capsys):
    validate_isbn('abcdefghij', 10)
    assert 'should contain only digits' in capsys.readouterr().out
