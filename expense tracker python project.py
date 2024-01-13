import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

BACKGROUND_COLOR = "#87CEEB"
FOREGROUND_COLOR = "#FFFFFF"

def record_expense(category, item_name, price, date_of_purchase):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expense_entry = {
        "timestamp": timestamp,
        "category": category,
        "item_name": item_name,
        "price": price,
        "date_of_purchase": date_of_purchase
    }

    with open('expenses.json', 'a') as file:
        json.dump(expense_entry, file)
        file.write('\n')

def insert_values(category, item_name, price, date_of_purchase, expenses_display):
    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the price.")
        return

    record_expense(category, item_name, price, date_of_purchase)
    messagebox.showinfo("Expense Recorded", "Expense recorded successfully!")

    # Display added expenses below the entry fields
    expenses_display.config(state=tk.NORMAL)
    expenses_display.insert(tk.END, f"Category: {category}, Item Name: {item_name}, Price: ${price}, Date: {date_of_purchase}\n")
    expenses_display.config(state=tk.DISABLED)

def display_expenses(category, expenses_listbox):
    category_window = tk.Toplevel(root)
    category_window.title(f"{category} Expenses")
    category_window.configure(bg=BACKGROUND_COLOR)

    with open('expenses.json', 'r') as file:
        expenses = [json.loads(line) for line in file if json.loads(line).get("category") == category]

    expenses_listbox = tk.Listbox(category_window, selectmode=tk.MULTIPLE, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    expenses_listbox.pack()

    for expense in expenses:
        timestamp = expense.get('timestamp', 'N/A')
        item_name = expense.get('item_name', 'N/A')
        price = expense.get('price', 'N/A')
        date_of_purchase = expense.get('date_of_purchase', 'N/A')

        expense_info = f"{timestamp} - {item_name} - ${price} - {date_of_purchase}"
        expenses_listbox.insert(tk.END, expense_info)

    delete_button = tk.Button(category_window, text="Delete Selected", command=lambda: delete_selected_expenses(category, expenses_listbox),
                              bg='#FF0000', fg=FOREGROUND_COLOR)
    delete_button.pack()

def delete_selected_expenses(category, expenses_listbox):
    selected_indices = expenses_listbox.curselection()
    if not selected_indices:
        messagebox.showwarning("No Selection", "Please select items to delete.")
        return

    with open('expenses.json', 'r') as file:
        expenses = [json.loads(line) for line in file]

    new_expenses = [expense for index, expense in enumerate(expenses) if index not in selected_indices]

    with open('expenses.json', 'w') as file:
        for expense in new_expenses:
            json.dump(expense, file)
            file.write('\n')

    messagebox.showinfo("Deletion Successful", "Selected items deleted successfully.")

def delete_expense(category, item_name):
    with open('expenses.json', 'r') as file:
        expenses = [json.loads(line) for line in file]

    new_expenses = [expense for expense in expenses if expense.get("category") == category and expense.get("item_name") == item_name]

    with open('expenses.json', 'w') as file:
        for expense in new_expenses:
            json.dump(expense, file)
            file.write('\n')

    messagebox.showinfo("Deletion Successful", f"{item_name} in {category} deleted successfully.")

def calculate_total_expense(category):
    with open('expenses.json', 'r') as file:
        expenses = [json.loads(line) for line in file if json.loads(line).get("category") == category]

    total_expense = sum(expense.get('price', 0) for expense in expenses)
    messagebox.showinfo(f"Total {category} Expense", f"Total Expense: ${total_expense}")

def show_recorded_items_count():
    with open('expenses.json', 'r') as file:
        items_count = sum(1 for line in file)

    messagebox.showinfo("Recorded Items Count", f"Number of recorded items: {items_count}")

def category_button_click(category, expenses_display):
    category_window = tk.Toplevel(root)
    category_window.title(f"{category} Expenses")
    category_window.configure(bg=BACKGROUND_COLOR)

    item_name_label = tk.Label(category_window, text="Item Name:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    item_name_label.grid(row=0, column=0)
    entry_item_name = tk.Entry(category_window)
    entry_item_name.grid(row=0, column=1)

    price_label = tk.Label(category_window, text="Price ($):", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    price_label.grid(row=1, column=0)
    entry_price = tk.Entry(category_window)
    entry_price.grid(row=1, column=1)

    date_label = tk.Label(category_window, text="Date of Purchase:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    date_label.grid(row=2, column=0)
    entry_date = tk.Entry(category_window)
    entry_date.grid(row=2, column=1)

    expenses_listbox = tk.Listbox(category_window, selectmode=tk.MULTIPLE, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    expenses_listbox.grid(row=3, columnspan=2, pady=5)

    # Added text widget to display added expenses dynamically
    expenses_display = tk.Text(category_window, height=8, width=40, state=tk.DISABLED, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    expenses_display.grid(row=4, columnspan=2, pady=5)

    insert_button = tk.Button(category_window, text="Insert Values",
                              command=lambda: insert_values(category, entry_item_name.get(), entry_price.get(), entry_date.get(), expenses_display),
                              bg='#4CAF50', fg=FOREGROUND_COLOR)
    insert_button.grid(row=5, columnspan=2, pady=5)

    select_all_button = tk.Button(category_window, text="Select All",
                                  command=lambda: display_expenses(category, expenses_listbox), bg='#2196F3', fg=FOREGROUND_COLOR)
    select_all_button.grid(row=6, columnspan=2, pady=5)

    delete_button = tk.Button(category_window, text="Delete Expense",
                              command=lambda: delete_expense(category, entry_item_name.get()), bg='#FF5722', fg=FOREGROUND_COLOR)
    delete_button.grid(row=7, columnspan=2, pady=5)

    delete_selected_button = tk.Button(category_window, text="Delete Selected",
                                       command=lambda: delete_selected_expenses(category, expenses_listbox), bg='#FF0000', fg=FOREGROUND_COLOR)
    delete_selected_button.grid(row=8, columnspan=2, pady=5)

    find_button = tk.Button(category_window, text="Find Value",
                            command=lambda: display_expenses(category, expenses_listbox), bg='#FFC107', fg=FOREGROUND_COLOR)
    find_button.grid(row=9, columnspan=2, pady=5)

    total_expense_button = tk.Button(category_window, text="Total Expense",
                                     command=lambda: calculate_total_expense(category), bg='#607D8B', fg=FOREGROUND_COLOR)
    total_expense_button.grid(row=10, columnspan=2, pady=5)

    exit_button = tk.Button(category_window, text="Exit", command=category_window.destroy, bg='#9E9E9E', fg=FOREGROUND_COLOR)
    exit_button.grid(row=11, columnspan=2, pady=5)

def home_page_button_click(expenses_display):
    home_page_window = tk.Toplevel(root)
    home_page_window.title("Home Page")
    home_page_window.configure(bg=BACKGROUND_COLOR)

    grocery_button = tk.Button(home_page_window, text="Grocery", command=lambda: category_button_click("Grocery", expenses_display),
                               bg='#4CAF50', fg=FOREGROUND_COLOR)
    grocery_button.pack(pady=10)

    household_button = tk.Button(home_page_window, text="Household", command=lambda: category_button_click("Household", expenses_display),
                                 bg='#2196F3', fg=FOREGROUND_COLOR)
    household_button.pack(pady=10)

    other_button = tk.Button(home_page_window, text="Other", command=lambda: category_button_click("Other", expenses_display),
                             bg='#FF5722', fg=FOREGROUND_COLOR)
    other_button.pack(pady=10)

    exit_button = tk.Button(home_page_window, text="Exit", command=home_page_window.destroy, bg='#9E9E9E', fg=FOREGROUND_COLOR)
    exit_button.pack(pady=10)

# Create the welcome page window
welcome_page = tk.Tk()
welcome_page.title("Welcome to Expense Tracker")
welcome_page.geometry("400x300")
welcome_page.configure(bg=BACKGROUND_COLOR)

# Create a Label for the welcome message
welcome_label = tk.Label(welcome_page, text="Welcome to Expense Tracker!", font=("Helvetica", 16), pady=20, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
welcome_label.pack()

# Create a button to enter the main application
enter_button_welcome = tk.Button(welcome_page, text="Enter Expense Tracker", command=lambda: welcome_page.destroy(), bg='#4CAF50', fg=FOREGROUND_COLOR)
enter_button_welcome.pack(pady=10)

welcome_page.mainloop()

# Now, create the main expense tracker window
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg=BACKGROUND_COLOR)

expenses_display = tk.Text(root, height=5, width=40, state=tk.DISABLED, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
expenses_display.pack(pady=10)

home_page_button = tk.Button(root, text="Home Page", command=lambda: home_page_button_click(expenses_display), bg='#4CAF50', fg=FOREGROUND_COLOR)
home_page_button.pack(pady=10)

find_value_button = tk.Button(root, text="Find Value", command=lambda: display_expenses("All", None), bg='#2196F3', fg=FOREGROUND_COLOR)
find_value_button.pack(pady=10)

delete_expense_button = tk.Button(root, text="Delete Expense", command=lambda: display_expenses("All", None), bg='#FF5722', fg=FOREGROUND_COLOR)
delete_expense_button.pack(pady=10)

total_expense_button = tk.Button(root, text="Total Expense", command=lambda: calculate_total_expense("All"), bg='#607D8B', fg=FOREGROUND_COLOR)
total_expense_button.pack(pady=10)

show_items_count_button = tk.Button(root, text="Show Items Count", command=show_recorded_items_count, bg='#FFC107', fg=FOREGROUND_COLOR)
show_items_count_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy, bg='#9E9E9E', fg=FOREGROUND_COLOR)
exit_button.pack(pady=10)

root.mainloop()
