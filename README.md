# ISBN Validator

A Python tool that validates ISBN-10 and ISBN-13 codes by recalculating
the official check digit from the rest of the number and comparing it
to the one provided.

## How ISBN validation works

Both ISBN-10 and ISBN-13 end in a **check digit** — a digit
mathematically derived from all the digits before it. If a single digit
is mistyped or two digits get swapped, the check digit won't match,
catching the error. This tool recomputes that check digit and compares
it to the one given.

- **ISBN-10**: each of the first 9 digits is multiplied by a weight
  counting down from 10 to 2, summed, and checked against `11 - (sum
  mod 11)`. The result can be `0`–`9` or the letter `X` (representing
  10).
- **ISBN-13**: each of the first 12 digits is multiplied alternately by
  1 and 3, summed, and checked against `10 - (sum mod 10)`.

## Project structure

```
isbn-validator/
├── isbn_validator.py         # Core validation logic
├── example.py                  # Demo script
├── tests/
│   └── test_isbn_validator.py    # Test suite (pytest)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/isbn-validator.git
cd isbn-validator
pip install -r requirements.txt   # only needed to run the tests
```

No external libraries are required to run the tool itself — it only
uses Python's standard library.

## Usage

```python
from isbn_validator import validate_isbn

validate_isbn('0-306-40615-2', 10)   # Valid ISBN Code.
validate_isbn('978-0-13-235088-4', 13)  # Valid ISBN Code.
```

Or run it interactively:

```bash
python isbn_validator.py
```

```
Enter ISBN and length: 0-306-40615-2, 10
Valid ISBN Code.
```

Or run the included demo:

```bash
python example.py
```

## Running the tests

```bash
pytest
```

12 tests cover the check-digit math for both formats (including the
`X` check digit case), hyphen/space handling, wrong-length input, and
non-digit input.

## Bug fixed from the original version

The check-digit **math** was already correct — verified by fuzz-testing
both `calculate_check_digit_10()` and `calculate_check_digit_13()`
against independently-derived reference formulas across 20,000 random
inputs each, with zero mismatches.

The actual bug was in how the ISBN string was handled: **real-world
ISBNs are almost always written with hyphens** (e.g. the one printed on
the back of any book, `0-306-40615-2`). The original code checked the
raw string length directly, so any hyphenated ISBN — including
perfectly valid ones — was rejected outright as "the wrong length,"
without even getting to the check-digit math. Since basically nobody
types an ISBN *without* the hyphens, this made the tool unusable for
its actual intended purpose.

The fix strips hyphens and spaces from the input before validating, and
also adds a friendly error message if the remaining characters aren't
all digits (e.g. letters other than a trailing `X`).

## Known limitations / next steps

This is a learning project, so it's intentionally simple. Ideas for
extending it:

- Auto-detect the ISBN length from the input instead of requiring the
  user to specify it separately.
- Add a function to *generate* a valid check digit for a given set of
  main digits, not just validate an existing one.
- Support converting an ISBN-10 to its equivalent ISBN-13 (and back).

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE)
for details.
