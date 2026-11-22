# Personal Budget Manager — Release 1

Command-line app to add, list and report personal transactions (income and expenses),
saved to a CSV file and validated at entry.

## Setup
- Python 3.10 or newer. No extra packages needed (only the standard library).
- Open a terminal in the `budget-manager` folder.

## Run
All commands are run from the `budget-manager` folder:

```bash
PYTHONPATH=src python3 -m budget_manager.cli add expense food 18.50
PYTHONPATH=src python3 -m budget_manager.cli add income salary 1200 --date 2026-09-01
PYTHONPATH=src python3 -m budget_manager.cli list
PYTHONPATH=src python3 -m budget_manager.cli report
PYTHONPATH=src python3 -m budget_manager.cli --help
```

On Windows (PowerShell) set the path first: `$env:PYTHONPATH="src"`, then `python -m budget_manager.cli ...`

Data is saved in `data/transactions.csv` (created automatically).
Use `--file` to choose another file, e.g. `--file data/sample_transactions.csv`.

Exit codes: `0` = success, `1` = invalid input or the file has invalid rows (errors are printed to stderr).

Allowed values:
- kind: `expense`, `income`
- category: `food`, `transport`, `housing`, `leisure`, `health`, `salary`, `other`
- amount: a number greater than 0
- date: `YYYY-MM-DD` (default: today)
- currency: `EUR`

## Example

```
$ PYTHONPATH=src python3 -m budget_manager.cli add income salary 1200 --date 2026-09-01
Added T001  2026-09-01  income   salary       1200.00 EUR
$ PYTHONPATH=src python3 -m budget_manager.cli add expense food 18.50 --date 2026-09-04
Added T002  2026-09-04  expense  food           18.50 EUR
$ PYTHONPATH=src python3 -m budget_manager.cli add expense food -5
Error: amount must be > 0 (got -5.0)
$ PYTHONPATH=src python3 -m budget_manager.cli report
Income:     1200.00 EUR
Expenses:     18.50 EUR
Balance:    1181.50 EUR
Expenses by category:
  food           18.50
```

Loading the sample file shows how invalid rows are reported:

```
$ PYTHONPATH=src python3 -m budget_manager.cli --file data/sample_transactions.csv report
Skipped Row 4: amount must be > 0 (got -5.0)
Skipped Row 5: kind must be one of ['expense', 'income'] (got 'gift')
Skipped Row 6: category must be one of [...] (got 'unicorns')
Skipped Row 7: date must be YYYY-MM-DD (got '2026-13-45')
Skipped Row 8: amount must be a number (got 'abc')
Skipped Row 10: amount must be > 0 (got 0.0)
Skipped Row 11: id must be unique ('T001' is repeated)
Income:     1200.00 EUR
Expenses:    468.50 EUR
Balance:     731.50 EUR
```

## Test

```bash
PYTHONPATH=src python3 tests/test_budget.py
```

Expected: `All 9 tests passed` (1 normal case, boundary cases for amount/kind/category,
and save/load round-trip). If an assertion fails, Python shows an `AssertionError`.

## Known limitations
- Only one currency (EUR). Mixing currencies would make the balance wrong.
- No way to edit or delete a transaction yet (no undo).
- If the data file contains invalid rows, `add` is blocked until the file is fixed,
  so that bad rows are never deleted silently when the file is saved again.
- Categories are a fixed list in `validation.py`; new ones need a code change.
