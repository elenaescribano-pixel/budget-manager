# storage.py — GUARDAR y CARGAR del archivo CSV. Nada más.
#
# Contrato del archivo:
#   Formato:   CSV          Codificación: UTF-8
#   Columnas:  id,date,kind,category,amount,currency
#   Errores:   las filas malas NO se aceptan y se informa de cada una.

import csv
from pathlib import Path

from budget_manager.models import FIELDS, Transaction


def load_transactions(path):
    # Devuelve DOS cosas: (transacciones válidas, lista de errores).
    # Cada fila mala genera un mensaje como "Row 4: amount must be > 0 (got -5.0)".
    file = Path(path)
    transactions = []
    errors = []
    if not file.exists():
        return transactions, errors  # Primera vez: todavía no hay archivo.

    with open(file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        # 1. Primero comprobamos que están las columnas correctas.
        if reader.fieldnames != FIELDS:
            errors.append(f"Row 1: columns must be {FIELDS} (got {reader.fieldnames})")
            return transactions, errors

        # 2. Después validamos fila a fila.
        # start=2 porque la fila 1 del archivo es la cabecera.
        for row_number, row in enumerate(reader, start=2):
            existing_ids = [t.id for t in transactions]
            try:
                t = Transaction(row["id"], row["date"], row["kind"],
                                row["category"], row["amount"], row["currency"],
                                existing_ids)
                transactions.append(t)
            except ValueError as error:
                errors.append(f"Row {row_number}: {error}")
    return transactions, errors


def save_transactions(path, transactions):
    # Escritura segura (sesión 5): primero escribimos un archivo temporal
    # y solo cuando está completo lo cambiamos por el archivo real.
    # Así, si el programa se corta a mitad, el archivo bueno sigue intacto.
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = file.parent / (file.name + ".tmp")

    with open(temp_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t.to_dict())

    temp_file.replace(file)
