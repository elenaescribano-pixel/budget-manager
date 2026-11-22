# cli.py — HABLAR con el usuario: argparse para leer comandos, print para mostrar.
# Aquí NO van cálculos: se llama a services.py y storage.py.
#
# Ejemplos (desde la carpeta budget-manager):
#   PYTHONPATH=src python3 -m budget_manager.cli add expense food 18.50
#   PYTHONPATH=src python3 -m budget_manager.cli list
#   PYTHONPATH=src python3 -m budget_manager.cli report
#   PYTHONPATH=src python3 -m budget_manager.cli --file data/sample_transactions.csv report
#
# Códigos de salida: 0 = todo bien, 1 = error (dato inválido o archivo con filas malas).

import argparse
import sys
from datetime import date

from budget_manager import services, storage

# Nombres de los comandos en constantes, para no escribirlos mal en dos sitios.
COMMAND_ADD = "add"
COMMAND_LIST = "list"
COMMAND_REPORT = "report"
DEFAULT_FILE = "data/transactions.csv"


def build_parser():
    parser = argparse.ArgumentParser(description="Personal budget manager")
    parser.add_argument("--file", default=DEFAULT_FILE, help="CSV file to use")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser(COMMAND_ADD, help="add a transaction")
    add.add_argument("kind", help="expense or income")
    add.add_argument("category", help="food, transport, housing, leisure, health, salary, other")
    add.add_argument("amount", help="positive number, e.g. 18.50")
    add.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD (default: today)")
    add.add_argument("--currency", default="EUR")

    commands.add_parser(COMMAND_LIST, help="show all transactions")
    commands.add_parser(COMMAND_REPORT, help="show totals and balance")
    return parser


def show_list(transactions):
    if not transactions:
        print("No transactions yet.")
    for t in transactions:
        print(t)  # Usa Transaction.__str__


def show_report(transactions):
    print(f"Income:   {services.total_income(transactions):>9.2f} EUR")
    print(f"Expenses: {services.total_expenses(transactions):>9.2f} EUR")
    print(f"Balance:  {services.balance(transactions):>9.2f} EUR")
    by_category = services.expenses_by_category(transactions)
    if by_category:
        print("Expenses by category:")
        for category, amount in by_category.items():
            print(f"  {category:<10} {amount:>9.2f}")


def main():
    args = build_parser().parse_args()

    transactions, errors = storage.load_transactions(args.file)

    # Avisar de las filas que no se han podido cargar (por el canal de errores).
    for error in errors:
        print(f"Skipped {error}", file=sys.stderr)

    if args.command == COMMAND_ADD:
        if errors:
            # Si guardáramos ahora, las filas malas desaparecerían del archivo sin avisar.
            print("Cannot add: fix the rows above in the file first.", file=sys.stderr)
            sys.exit(1)
        try:
            new = services.add_transaction(transactions, args.date, args.kind,
                                           args.category, args.amount, args.currency)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        storage.save_transactions(args.file, transactions)
        print(f"Added {new}")

    elif args.command == COMMAND_LIST:
        show_list(transactions)

    elif args.command == COMMAND_REPORT:
        show_report(transactions)


if __name__ == "__main__":
    main()
