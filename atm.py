"""
atm.py
------
Core logic for the ATM Simulation System.

This module contains all the "business logic" of the ATM: loading and
saving account data, verifying the PIN, and performing balance inquiry,
deposit, withdrawal, transaction history, and PIN change operations.

The account data (hashed PIN, balance, transaction history, lock status)
is persisted to a local JSON file so that it survives between program
runs. This is purely for educational/demo purposes and does NOT
represent real banking security practices.
"""

import json
import os
import hashlib
import getpass
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DATA_FILE = "data.json"          # File used to persist account data
MAX_PIN_ATTEMPTS = 3             # Maximum allowed incorrect PIN attempts
DEFAULT_PIN = "1234"             # Default PIN used only when creating a new account
DEFAULT_BALANCE = 5000.00        # Starting balance for a brand-new account


# ---------------------------------------------------------------------------
# Helper: PIN hashing
# ---------------------------------------------------------------------------

def hash_pin(pin: str) -> str:
    """
    Return a SHA-256 hash of the given PIN.

    We never store the raw PIN on disk -- only its hash. This is a simple
    educational demonstration of "don't store secrets in plain text",
    not a production-grade security mechanism.
    """
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Data persistence (JSON file handling)
# ---------------------------------------------------------------------------

def load_account(filepath: str = DATA_FILE) -> dict:
    """
    Load account data from the JSON file.

    If the file does not exist or is corrupted/unreadable, a brand-new
    account is created with default values and immediately saved.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                # Basic structure validation -- if keys are missing,
                # fall back to defaults for those keys.
                data.setdefault("pin_hash", hash_pin(DEFAULT_PIN))
                data.setdefault("balance", DEFAULT_BALANCE)
                data.setdefault("transactions", [])
                data.setdefault("locked", False)
                return data
        except (json.JSONDecodeError, OSError) as error:
            print(f"[Warning] Could not read existing data file ({error}).")
            print("A new account will be created with default values.\n")

    # No valid file found -- create a fresh account.
    new_account = {
        "pin_hash": hash_pin(DEFAULT_PIN),
        "balance": DEFAULT_BALANCE,
        "transactions": [],
        "locked": False,
    }
    save_account(new_account, filepath)
    return new_account


def save_account(account: dict, filepath: str = DATA_FILE) -> None:
    """Persist the account dictionary to the JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(account, file, indent=4)
    except OSError as error:
        print(f"[Error] Could not save account data: {error}")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_currency(amount: float) -> str:
    """Format a numeric amount as a currency string, e.g. 1234.5 -> '$1,234.50'."""
    return f"${amount:,.2f}"


def current_timestamp() -> str:
    """Return the current date/time as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def get_hidden_pin(prompt: str) -> str:
    """
    Prompt the user for a PIN without echoing it to the screen, using the
    standard-library 'getpass' module. Falls back to normal input() if the
    terminal does not support hidden input (e.g. some IDE consoles).
    """
    try:
        return getpass.getpass(prompt)
    except Exception:
        # getpass can fail in some non-interactive terminals; fall back
        # gracefully so the program still works everywhere.
        print("[Note] Hidden input not supported in this terminal.")
        return input(prompt)


def get_valid_pin(prompt: str) -> str:
    """Keep prompting until the user enters a valid 4-digit numeric PIN."""
    while True:
        pin = get_hidden_pin(prompt).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("Invalid PIN format. Please enter exactly 4 digits.\n")


def get_positive_amount(prompt: str) -> float:
    """
    Keep prompting until the user enters a valid positive number.
    Handles non-numeric input and negative/zero values gracefully.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            amount = float(raw_value)
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.\n")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid input. Please enter a numeric amount (e.g. 250.00).\n")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def authenticate(account: dict) -> bool:
    """
    Verify the user's PIN, allowing up to MAX_PIN_ATTEMPTS attempts.

    Returns True if authentication succeeds, False if the account becomes
    locked. The 'locked' status is persisted so the lock survives restarts.
    """
    if account.get("locked", False):
        print("\nThis account is LOCKED due to too many failed PIN attempts.")
        print("Please contact the bank administrator to unlock it.\n")
        return False

    attempts_left = MAX_PIN_ATTEMPTS
    while attempts_left > 0:
        entered_pin = get_hidden_pin("Enter your 4-digit PIN: ").strip()

        if not entered_pin.isdigit() or len(entered_pin) != 4:
            print("PIN must be exactly 4 digits.\n")
            attempts_left -= 1
            print(f"Attempts remaining: {attempts_left}\n")
            continue

        if hash_pin(entered_pin) == account["pin_hash"]:
            print("\nPIN verified successfully. Access granted.\n")
            return True

        attempts_left -= 1
        if attempts_left > 0:
            print(f"Incorrect PIN. Attempts remaining: {attempts_left}\n")
        else:
            print("\nIncorrect PIN. No attempts remaining.")
            account["locked"] = True
            save_account(account)
            print("Account has been LOCKED for security reasons.\n")

    return False


# ---------------------------------------------------------------------------
# Core banking operations
# ---------------------------------------------------------------------------

def add_transaction(account: dict, transaction_type: str, amount: float) -> None:
    """Append a transaction record with type, amount, timestamp, and resulting balance."""
    transaction = {
        "type": transaction_type,
        "amount": round(amount, 2),
        "timestamp": current_timestamp(),
        "balance_after": round(account["balance"], 2),
    }
    account["transactions"].append(transaction)


def check_balance(account: dict) -> None:
    """Display the current account balance."""
    print("\n----- Balance Inquiry -----")
    print(f"Current Balance: {format_currency(account['balance'])}")
    print("---------------------------\n")


def deposit_cash(account: dict) -> None:
    """Ask for a deposit amount, validate it, update balance, and record it."""
    print("\n----- Cash Deposit -----")
    amount = get_positive_amount("Enter amount to deposit: ")
    account["balance"] += amount
    add_transaction(account, "Deposit", amount)
    save_account(account)
    print(f"Deposit successful! New balance: {format_currency(account['balance'])}")
    print("-------------------------\n")


def withdraw_cash(account: dict) -> None:
    """Ask for a withdrawal amount, validate against balance, update, and record it."""
    print("\n----- Cash Withdrawal -----")
    amount = get_positive_amount("Enter amount to withdraw: ")

    if amount > account["balance"]:
        print("Insufficient balance for this withdrawal.")
        print(f"Available balance: {format_currency(account['balance'])}")
        print("----------------------------\n")
        return

    account["balance"] -= amount
    add_transaction(account, "Withdrawal", amount)
    save_account(account)
    print(f"Withdrawal successful! New balance: {format_currency(account['balance'])}")
    print("----------------------------\n")


def view_transaction_history(account: dict) -> None:
    """Display all recorded transactions, most recent last."""
    print("\n----- Transaction History -----")
    transactions = account.get("transactions", [])

    if not transactions:
        print("No transactions have been recorded yet.")
    else:
        print(f"{'Date/Time':<20} {'Type':<12} {'Amount':>12} {'Balance After':>15}")
        print("-" * 61)
        for entry in transactions:
            print(
                f"{entry['timestamp']:<20} "
                f"{entry['type']:<12} "
                f"{format_currency(entry['amount']):>12} "
                f"{format_currency(entry['balance_after']):>15}"
            )
    print("--------------------------------\n")


def change_pin(account: dict) -> None:
    """Verify the current PIN, then set and confirm a new 4-digit PIN."""
    print("\n----- Change PIN -----")
    current_pin = get_hidden_pin("Enter your current PIN: ").strip()

    if hash_pin(current_pin) != account["pin_hash"]:
        print("Current PIN is incorrect. PIN change cancelled.")
        print("-----------------------\n")
        return

    new_pin = get_valid_pin("Enter your new 4-digit PIN: ")
    confirm_pin = get_valid_pin("Confirm your new PIN: ")

    if new_pin != confirm_pin:
        print("The new PIN and confirmation do not match. PIN change cancelled.")
        print("-----------------------\n")
        return

    account["pin_hash"] = hash_pin(new_pin)
    save_account(account)
    print("PIN changed successfully!")
    print("-----------------------\n")
