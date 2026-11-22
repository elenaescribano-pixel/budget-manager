# services.py — la LÓGICA del negocio. Aquí NO hay input(), print() ni archivos.
# Las funciones reciben la lista de transacciones y devuelven resultados.

from budget_manager.models import make_transaction


def next_id(transactions):
    # "T001", "T002", ... -> busca el número más alto y suma 1.
    highest = 0
    for t in transactions:
        number = int(t["id"][1:])
        if number > highest:
            highest = number
    return f"T{highest + 1:03d}"


def add_transaction(transactions, date, kind, category, amount, currency="EUR"):
    existing_ids = [t["id"] for t in transactions]
    new = make_transaction(next_id(transactions), date, kind, category, amount, currency, existing_ids)
    transactions.append(new)
    return new


def total_income(transactions):
    total = 0
    for t in transactions:
        if t["kind"] == "income":
            total += t["amount"]
    return round(total, 2)


def total_expenses(transactions):
    total = 0
    for t in transactions:
        if t["kind"] == "expense":
            total += t["amount"]
    return round(total, 2)


def balance(transactions):
    return round(total_income(transactions) - total_expenses(transactions), 2)


def expenses_by_category(transactions):
    # Devuelve un diccionario, ej. {"food": 18.5, "housing": 450.0}
    totals = {}
    for t in transactions:
        if t["kind"] == "expense":
            category = t["category"]
            totals[category] = round(totals.get(category, 0) + t["amount"], 2)
    return totals
