# storage.py — GUARDAR y CARGAR del archivo CSV. Nada más.
# (La misma idea que entries.json en el cli.py de clase, pero con CSV.)

import csv
from pathlib import Path

from budget_manager.models import FIELDS, make_transaction


def load_transactions(path):
    # Devuelve DOS cosas: (transacciones válidas, lista de errores).
    # Las filas malas NO se aceptan, pero tampoco se ignoran en silencio:
    # cada una genera un mensaje como "Row 4: amount must be > 0 (got -5.0)".
    file = Path(path)
    transactions = []
    errors = []
    if not file.exists():
        return transactions, errors

    with open(file, newline="") as f:
        reader = csv.DictReader(f)
        # start=2 porque la fila 1 del archivo es la cabecera.
        for row_number, row in enumerate(reader, start=2):
            existing_ids = [t["id"] for t in transactions]
            try:
                t = make_transaction(row["id"], row["date"], row["kind"],
                                     row["category"], row["amount"], row["currency"],
                                     existing_ids)
                transactions.append(t)
            except ValueError as error:
                errors.append(f"Row {row_number}: {error}")
    return transactions, errors


def save_transactions(path, transactions):
    # Reescribe el archivo entero con el estado actual.
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t)
