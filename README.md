# ATM Simulation System

A terminal-based ATM simulator in Python (standard library only). Educational project. No real money or banking is involved.

## Quick Start

**Requirements:** Python 3.7+. No packages to install.

```bash
cd ATM-Simulation-System
python main.py        # use python3 on macOS/Linux if needed
```

**Demo login:** PIN `1234` (starting balance $5,000.00). The PIN is hidden as you type.

## Features

| Menu Option | What it does |
|---|---|
| 1. Balance Inquiry | Shows the balance as currency |
| 2. Deposit Cash | Accepts positive amounts only |
| 3. Withdraw Cash | Positive amounts only; blocked if above balance |
| 4. Transaction History | Type, amount, date/time, balance after each transaction |
| 5. Change PIN | Verifies current PIN, then confirms the new 4-digit PIN |
| 6. Exit | Safe logout with confirmation message |

Also: 3 wrong PIN attempts lock the account, and all data persists between runs.

## Suggested 5-Minute Evaluation

| # | Test | Expected result |
|---|---|---|
| 1 | Enter `1234` | Access granted, menu appears |
| 2 | Option 2, deposit `250` | Balance becomes $5,250.00 |
| 3 | Option 2, deposit `-50` or `abc` | Rejected, asks again |
| 4 | Option 3, withdraw `100` | Balance becomes $5,150.00 |
| 5 | Option 3, withdraw `99999` | "Insufficient balance", balance unchanged |
| 6 | Option 4 | Both transactions listed with timestamps |
| 7 | Option 5, change PIN | Works only with correct current PIN and matching confirmation |
| 8 | Option 6, then rerun `python main.py` | Balance, history, and new PIN are all preserved |
| 9 | Restart, enter 3 wrong PINs | Account locks, and stays locked on the next run |

## Resetting Between Tests

Delete `data.json` and run the program again. It is recreated automatically with PIN `1234` and a $5,000.00 balance. This also clears a locked account.

## Files

```
ATM-Simulation-System/
├── main.py            # Menu loop and user interaction
├── atm.py             # Core logic: PIN check, transactions, file handling
├── data.json          # Saved account data (auto-created if missing)
├── requirements.txt   # States that no external packages are needed
└── .gitignore
```

## Data Storage

`data.json` holds the balance, transaction history, lock status, and a SHA-256 **hash** of the PIN (never the plain PIN). This is for demonstration only and is not production-grade security.

## Input Validation

- PIN must be exactly 4 digits.
- Amounts must be numeric and greater than zero.
- Invalid menu choices are rejected without crashing.
- A missing or corrupted `data.json` is replaced with a fresh default account.
- Ctrl+C exits cleanly.

## Limitations

- Single account only.
- Unsalted PIN hash and unencrypted data file (demo purposes).
- No admin unlock flow. Reset by deleting `data.json`.

## Author

*Ishita Verma , 26BCE11056,python essential,