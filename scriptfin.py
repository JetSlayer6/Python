import datetime
import os
import json

# Initialise global variables
transactions = []
categories = ["Food", "Transportation", "Housing", "Entertainment", "Utilities", "Applications", "Other"]


def main():
    # Load existing data if available
    load_data()
    
    print("\n===== PERSONAL FINANCE TRACKER =====")
    print("Track your income and expenses to better manage your finances!")
    
    # Main program loop
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new transaction")
        print("2. View all transactions")
        print("3. View spending by category")
        print("4. View monthly summary")
        print("5. Add a new category")
        print("6. Search transactions")
        print("7. Save and exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            view_by_category()
        elif choice == '4':
            view_monthly_summary()
        elif choice == '5':
            add_category()
        elif choice == '6':
            search_transactions()
        elif choice == '7':
            save_data()
            print("\nData saved. Thank you for using the Personal Finance Tracker!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


def load_data():
    global transactions, categories
    
    # Check if data file exists
    if os.path.exists("finance_data.json"):
        try:
            with open("finance_data.json", "r") as file:
                data = json.load(file)
                transactions = data.get("transactions", [])
                loaded_categories = data.get("categories", [])
                
                # Update categories list with any saved categories
                if loaded_categories:
                    categories = loaded_categories
                    
            print("Existing data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
    else:
        print("No existing data found. Starting with a new database.")


def save_data():
    try:
        data = {
            "transactions": transactions,
            "categories": categories
        }
        
        with open("finance_data.json", "w") as file:
            json.dump(data, file, indent=4)
            
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")


def add_transaction():
    print("\n----- Add New Transaction -----")
    
    # Get transaction date
    while True:
        date_str = input("Enter date (YYYY-MM-DD), or leave blank for today: ")
        
        if not date_str:  # Use today's date if blank
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            break
            
        try:
            # Validate date format
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            date = date_str
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
    
    # Get transaction description
    description = input("Enter description: ")
    
    # Get transaction amount and type
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    # Determine if it's income or expense
    while True:
        trans_type = input("Is this income or expense? (i/e): ").lower()
        if trans_type in ['i', 'e']:
            trans_type = "Income" if trans_type == 'i' else "Expense"
            break
        else:
            print("Please enter 'i' for income or 'e' for expense.")
    
    # Get category for expenses
    category = "Income"  # Default for income transactions
    if trans_type == "Expense":
        # Display available categories
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
            
        while True:
            try:
                cat_choice = int(input(f"Select category (1-{len(categories)}): "))
                if 1 <= cat_choice <= len(categories):
                    category = categories[cat_choice-1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(categories)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    # Create and add the transaction
    transaction = {
        "date": date,
        "description": description,
        "amount": amount,
        "type": trans_type,
        "category": category
    }
    
    transactions.append(transaction)
    print("Transaction added successfully!")


def view_transactions():
    if not transactions:
        print("\nNo transactions to display.")
        return
    
    # Sort options
    print("\n----- View Transactions -----")
    print("Sort by:")
    print("1. Date (newest first)")
    print("2. Date (oldest first)")
    print("3. Amount (highest first)")
    print("4. Amount (lowest first)")
    print("5. Type (income/expense)")
    
    # Get sorting choice
    sort_choice = input("Enter sorting option (1-5), or press Enter for default (newest first): ")
    
    # Create a copy of transactions for sorting
    sorted_transactions = transactions.copy()
    
    # Apply sorting based on user choice
    if sort_choice == '2':
        sorted_transactions.sort(key=lambda x: x["date"])
    elif sort_choice == '3':
        sorted_transactions.sort(key=lambda x: x["amount"], reverse=True)
    elif sort_choice == '4':
        sorted_transactions.sort(key=lambda x: x["amount"])
    elif sort_choice == '5':
        sorted_transactions.sort(key=lambda x: x["type"])
    else:  # Default or option 1
        sorted_transactions.sort(key=lambda x: x["date"], reverse=True)
    
    # Display transactions in table format
    print("\n" + "-" * 80)
    print(f"{'Date':<12} {'Description':<25} {'Amount':>10} {'Type':<10} {'Category':<15}")
    print("-" * 80)
    
    for transaction in sorted_transactions:
        amount_str = f"${transaction['amount']:.2f}"
        print(f"{transaction['date']:<12} {transaction['description'][:25]:<25} {amount_str:>10} "
              f"{transaction['type']:<10} {transaction['category']:<15}")
    
    print("-" * 80)
    
    # Calculate and display summary
    income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = income - expenses
    
    print(f"\nTotal Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Current Balance: ${balance:.2f}")


def view_by_category():
    # Filter for expense transactions only
    expense_transactions = [t for t in transactions if t["type"] == "Expense"]
    
    if not expense_transactions:
        print("\nNo expense transactions to analyze.")
        return
    
    # Calculate spending by category
    category_totals = {}
    for transaction in expense_transactions:
        category = transaction["category"]
        amount = transaction["amount"]
        
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    # Calculate total expenses
    total_expenses = sum(category_totals.values())
    
    # Display results in descending order
    print("\n----- Spending by Category -----")
    print(f"{'Category':<15} {'Amount':>10} {'Percentage':>12}")
    print("-" * 40)
    
    # Sort categories by amount
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_categories:
        percentage = (amount / total_expenses) * 100
        amount_str = f"${amount:.2f}"
        percentage_str = f"{percentage:.1f}%"
        
        print(f"{category:<15} {amount_str:>10} {percentage_str:>12}")
    
    print("-" * 40)
    print(f"{'Total':<15} ${total_expenses:.2f}")
    
    # Visual representation (simple text-based bar chart)
    print("\n----- Spending Distribution -----")
    max_width = 40  # Maximum bar width
    
    for category, amount in sorted_categories:
        percentage = (amount / total_expenses) * 100
        bar_width = int((amount / total_expenses) * max_width)
        bar = "#" * bar_width
        
        print(f"{category:<15} {bar} {percentage:.1f}%")


def view_monthly_summary():
    if not transactions:
        print("\nNo transactions to analyze.")
        return
    
    # Get all distinct year-month combinations
    months = set()
    for transaction in transactions:
        date = transaction["date"]
        year_month = date[:7]  # Extract YYYY-MM
        months.add(year_month)
    
    # Sort months chronologically
    months = sorted(list(months))
    
    # Calculate totals for each month
    print("\n----- Monthly Summary -----")
    print(f"{'Month':<10} {'Income':>12} {'Expenses':>12} {'Balance':>12}")
    print("-" * 50)
    
    for year_month in months:
        # Filter transactions for this month
        month_transactions = [t for t in transactions if t["date"].startswith(year_month)]
        
        # Calculate income and expenses
        income = sum(t["amount"] for t in month_transactions if t["type"] == "Income")
        expenses = sum(t["amount"] for t in month_transactions if t["type"] == "Expense")
        balance = income - expenses
        
        # Format strings
        income_str = f"${income:.2f}"
        expenses_str = f"${expenses:.2f}"
        balance_str = f"${balance:.2f}"
        
        # Determine balance color indicator (just using text)
        balance_indicator = " (profit)" if balance >= 0 else " (loss)"
        
        print(f"{year_month:<10} {income_str:>12} {expenses_str:>12} {balance_str:>12}{balance_indicator}")
    
    print("-" * 50)


def add_category():
    print("\n----- Add New Category -----")
    
    # Show current categories
    print("Current categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    # Get new category name
    new_category = input("\nEnter new category name: ").strip()
    
    # Validate input
    if not new_category:
        print("Category name cannot be empty.")
        return
    
    if new_category in categories:
        print(f"Category '{new_category}' already exists.")
        return
    
    # Add the new category
    categories.append(new_category)
    print(f"Category '{new_category}' added successfully.")


def search_transactions():
    if not transactions:
        print("\nNo transactions to search.")
        return
    
    print("\n----- Search Transactions -----")
    print("Search by:")
    print("1. Description")
    print("2. Date range")
    print("3. Amount range")
    print("4. Category")
    
    search_choice = input("Enter search option (1-4): ")
    
    if search_choice == '1':
        # Search by description
        search_term = input("Enter search term: ").lower()
        results = [t for t in transactions if search_term in t["description"].lower()]
        
    elif search_choice == '2':
        # Search by date range
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        
        try:
            # Validate dates
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
            
            results = [t for t in transactions if start_date <= t["date"] <= end_date]
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            return
        
    elif search_choice == '3':
        # Search by amount range
        try:
            min_amount = float(input("Enter minimum amount: "))
            max_amount = float(input("Enter maximum amount: "))
            
            results = [t for t in transactions if min_amount <= t["amount"] <= max_amount]
        except ValueError:
            print("Invalid amount. Please enter numbers.")
            return
        
    elif search_choice == '4':
        # Search by category
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
            
        try:
            cat_choice = int(input(f"Select category (1-{len(categories)}): "))
            if 1 <= cat_choice <= len(categories):
                category = categories[cat_choice-1]
                results = [t for t in transactions if t["category"] == category]
            else:
                print(f"Please enter a number between 1 and {len(categories)}.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
    else:
        print("Invalid choice.")
        return
    
    # Display search results
    if not results:
        print("\nNo matching transactions found.")
        return
    
    print(f"\nFound {len(results)} matching transactions:")
    print("-" * 80)
    print(f"{'Date':<12} {'Description':<25} {'Amount':>10} {'Type':<10} {'Category':<15}")
    print("-" * 80)
    
    for transaction in results:
        amount_str = f"${transaction['amount']:.2f}"
        print(f"{transaction['date']:<12} {transaction['description'][:25]:<25} {amount_str:>10} "
              f"{transaction['type']:<10} {transaction['category']:<15}")
    
    print("-" * 80)


# Run the program when the script is executed
if __name__ == "__main__":
    main()
