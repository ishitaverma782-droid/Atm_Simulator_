"""
main.py
-------
Entry point for the ATM Simulation System.

Run this file to start the program:
    python main.py

This module is intentionally kept small -- it only handles the menu
loop and user interaction. All the actual banking logic lives in atm.py.
"""

from atm import (
    DATA_FILE,
    load_account,
    authenticate,
    check_balance,
    deposit_cash,
    withdraw_cash,
    view_transaction_history,
    change_pin,
)

MENU_TEXT = """
===== ATM SIMULATION SYSTEM =====
1. Balance Inquiry
2. Deposit Cash
3. Withdraw Cash
4. Transaction History
5. Change PIN
6. Exit
==================================