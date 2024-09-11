from typing import List
from expense import Expense


def main():
    print("Running Expense Tracker!")
    expense_file_path = "expense.csv"
    budget_file_path = "budget.txt"

    # Load or set the budget
    user_budget = get_or_set_budget(budget_file_path)

    while True:
        choice = display_menu_and_get_choice()

        if choice == '1':
            add_expense(expense_file_path)
            summarize_expense(expense_file_path)
            financial_summary(expense_file_path, user_budget)
        elif choice == '2':
            user_budget = update_budget(budget_file_path)
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")


def display_menu_and_get_choice():
    print("\n--- Expense Tracker Menu ---")
    print("1. Add a new expense")
    print("2. Update monthly budget")
    print("3. Exit")
    return input("Select an option (1/2/3): ")


def add_expense(expense_file_path):
    # Get user to input an expense
    expense = get_user_expense()

    # Write it to a file
    save_expense_to_file(expense, expense_file_path)


def get_or_set_budget(budget_file_path):
    try:
        with open(budget_file_path, "r") as f:
            budget = float(f.read().strip())
            print(f"Your budget is: ${budget:.2f}")
    except FileNotFoundError:
        budget = float(input("Enter Monthly Budget: "))
        with open(budget_file_path, "w") as f:
            f.write(str(budget))
        print(f"Budget of ${budget:.2f} has been saved.")

    return budget


def update_budget(budget_file_path):
    new_budget = float(input("Enter new monthly budget: "))
    with open(budget_file_path, "w") as f:
        f.write(str(new_budget))
    print(f"Budget updated to ${new_budget:.2f}")
    return new_budget


def get_user_expense():
    print("Getting user Expense")
    expense_name = input("Enter Expense: ")
    expense_amount = float(input("Enter Expense Amount: "))

    expense_categories = [
        "Food", "Housing", "Transportation", "Utilities", "Personal Spending", "Entertainment"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid Category: Please try again!")


def save_expense_to_file(expense, expense_file_path):
    print(f"Saving Expense to File: {expense}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")


def summarize_expense(expense_file_path):
    print("Summarizing Expenses")
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_category, expense_amount = line.strip().split(",")
            line_expense = Expense(
                name=expense_name, category=expense_category, amount=float(expense_amount)
            )
            print(line_expense)

    summarize_expense_by_category(expense_file_path)


def summarize_expense_by_category(expense_file_path):
    print("Expenses by Category:")
    category_totals = {}

    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            _, expense_category, expense_amount = line.strip().split(",")
            expense_amount = float(expense_amount)

            if expense_category in category_totals:
                category_totals[expense_category] += expense_amount
            else:
                category_totals[expense_category] = expense_amount

    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")

    return category_totals


def financial_summary(expense_file_path, user_budget):
    total_spent = 0.0

    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            _, _, expense_amount = line.strip().split(",")
            total_spent += float(expense_amount)

    budget_remaining = user_budget - total_spent

    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Budget Remaining: ${budget_remaining:.2f}")


if __name__ == "__main__":
    main()
