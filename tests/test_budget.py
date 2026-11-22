# test_budget.py — 1 caso normal + casos límite, cada uno con su resultado esperado.
# Ejecutar desde la carpeta budget-manager:
#   PYTHONPATH=src python3 tests/test_budget.py

from pathlib import Path

from budget_manager import services, storage

PROJECT = Path(__file__).parent.parent
SAMPLE = PROJECT / "data" / "sample_transactions.csv"
TEST_FILE = PROJECT / "tests" / "roundtrip_test.csv"


# --- Caso normal ---
def test_balance_income_minus_expenses():
    transactions = []
    services.add_transaction(transactions, "2026-09-01", "income", "salary", "1200")
    services.add_transaction(transactions, "2026-09-02", "expense", "food", "18.50")
    assert services.total_income(transactions) == 1200.0
    assert services.total_expenses(transactions) == 18.5
    assert services.balance(transactions) == 1181.5
    assert transactions[1].id == "T002"


# --- Casos límite ---
def test_negative_amount_is_rejected():
    try:
        services.add_transaction([], "2026-09-01", "expense", "food", "-5")
        assert False, "a negative amount should be rejected"
    except ValueError as error:
        assert str(error) == "amount must be > 0 (got -5.0)"


def test_zero_amount_is_rejected():
    try:
        services.add_transaction([], "2026-09-01", "expense", "food", "0")
        assert False, "amount 0 should be rejected"
    except ValueError as error:
        assert str(error) == "amount must be > 0 (got 0.0)"


def test_unknown_kind_is_rejected():
    try:
        services.add_transaction([], "2026-09-01", "gift", "food", "10")
        assert False, "kind 'gift' should be rejected"
    except ValueError as error:
        assert "kind must be one of" in str(error)


def test_unknown_category_is_rejected():
    try:
        services.add_transaction([], "2026-09-01", "expense", "unicorns", "3")
        assert False, "category 'unicorns' should be rejected"
    except ValueError as error:
        assert "category must be one of" in str(error)


def test_failed_add_does_not_change_the_list():
    transactions = []
    try:
        services.add_transaction(transactions, "2026-09-01", "expense", "food", "-5")
    except ValueError:
        pass
    assert transactions == []


# --- Archivos ---
def test_save_and_load_round_trip():
    transactions = []
    services.add_transaction(transactions, "2026-09-01", "income", "salary", "1200")
    services.add_transaction(transactions, "2026-09-02", "expense", "food", "18.50")
    storage.save_transactions(TEST_FILE, transactions)
    loaded, errors = storage.load_transactions(TEST_FILE)
    assert errors == []
    assert [t.to_dict() for t in loaded] == [t.to_dict() for t in transactions]


def test_missing_file_gives_empty_list():
    loaded, errors = storage.load_transactions(PROJECT / "this_file_does_not_exist.csv")
    assert loaded == []
    assert errors == []


def test_sample_file_reports_bad_rows():
    loaded, errors = storage.load_transactions(SAMPLE)
    assert [t.id for t in loaded] == ["T001", "T002", "T008"]
    assert len(errors) == 7
    assert errors[0] == "Row 4: amount must be > 0 (got -5.0)"


if __name__ == "__main__":
    test_balance_income_minus_expenses()
    test_negative_amount_is_rejected()
    test_zero_amount_is_rejected()
    test_unknown_kind_is_rejected()
    test_unknown_category_is_rejected()
    test_failed_add_does_not_change_the_list()
    test_save_and_load_round_trip()
    test_missing_file_gives_empty_list()
    test_sample_file_reports_bad_rows()
    print("All 9 tests passed")
