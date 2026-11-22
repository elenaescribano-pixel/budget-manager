# cli.py — HABLAR con el usuario: argparse para leer comandos, print para mostrar.
# Aquí NO van cálculos: se llama a services.py y storage.py.
#
# Ejemplos (desde la carpeta budget-manager):
#   PYTHONPATH=src python3 -m budget_manager.cli add expense food 18.50
#   PYTHONPATH=src python3 -m budget_manager.cli list
#   PYTHONPATH=src python3 -m budget_manager.cli report
#   PYTHONPATH=src python3 -m budget_manager.cli --file data/sample_transactions.csv report

import argparse
from datetime import date

from budget_manager import services, storage

parser = argparse.ArgumentParser(description="Personal budget manager")
parser.add_argument("--file", default="data/transactions.csv", help="CSV file to use")
commands = parser.add_subparsers(dest="command", required=True)

add = commands.add_parser("add", help="add a transaction")
add.add_argument("kind", help="expense or income")
add.add_argument("category", help="food, transport, housing, leisure, health, salary, other")
add.add_argument("amount", help="positive number, e.g. 18.50")
add.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD (default: today)")
add.add_argument("--currency", default="EUR")

commands.add_parser("list", help="show all transactions")
commands.add_parser("report", help="show totals and balance")

args = parser.parse_args()

transactions, errors = storage.load_transactions(args.file)

# Avisar de las filas que no se han podido cargar.
for error in errors:
    print(f"Skipped {error}")

if args.command == "add":
    if errors:
        # Si guardáramos ahora, las filas malas desaparecerían del archivo sin avisar.
        print("Cannot add: fix the rows above in the file first.")
    else:
        try:
            new = services.add_transaction(transactions, args.date, args.kind,
                                           args.category, args.amount, args.currency)
            storage.save_transactions(args.file, transactions)
            print(f"Added {new['id']}: {new['kind']} {new['category']} {new['amount']:.2f} {new['currency']}")
        except ValueError as error:
            print(f"Error: {error}")

elif args.command == "list":
    if not transactions:
        print("No transactions yet.")
    for t in transactions:
        print(f"{t['id']}  {t['date']}  {t['kind']:<8} {t['category']:<10} {t['amount']:>9.2f} {t['currency']}")

elif args.command == "report":
    print(f"Income:   {services.total_income(transactions):>9.2f} EUR")
    print(f"Expenses: {services.total_expenses(transactions):>9.2f} EUR")
    print(f"Balance:  {services.balance(transactions):>9.2f} EUR")
    by_category = services.expenses_by_category(transactions)
    if by_category:
        print("Expenses by category:")
        for category, amount in by_category.items():
            print(f"  {category:<10} {amount:>9.2f}")
