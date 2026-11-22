# Design rationale

The program is split into layers that each do one job: `cli.py` only reads commands and
prints results, `services.py` holds the budget rules (add, totals, balance) without any
`input()`, `print()` or files, and `storage.py` only reads and writes the CSV. All checks
live in `validation.py` and are applied at the two places where data enters the program:
when a transaction is created (`models.make_transaction`) and when the file is loaded.
Because of this, the business rules can be tested directly with plain lists, without
typing commands or touching real files. One edge case shaped the design: if the file has
an invalid row and the user adds a new transaction, saving would rewrite the file and the
bad row would disappear without warning. To avoid silently losing data, invalid rows are
reported as "Row N: ..." and `add` is blocked until the file is fixed.
