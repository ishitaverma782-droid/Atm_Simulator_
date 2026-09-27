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
