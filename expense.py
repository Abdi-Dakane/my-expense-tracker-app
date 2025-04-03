import tkinter as tk
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime

# Set up the main window
root = tk.Tk()
root.geometry("900x600")
root.title("Expense Tracker App")
root.configure(background="#1E1E2E")  # Dark background

item_list = []
total_cost_var = tk.StringVar(value="Total: $0.00")

# Function to add an item


def Add_item():
    item = item_text.get()
    category = category_text.get()
    quantity = quantity_text.get()
    cost = cost_text.get()

    if not item or not category or not quantity or not cost:
        return  # Prevent adding empty fields

    try:
        quantity = int(quantity)
        cost = int(cost)
        total_cost = quantity * cost
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get current row count for proper alignment
        row_count = len(item_list) + 1

        # Insert data in the grid
        item_data = [item, category, quantity, cost, total_cost, date]
        for col, value in enumerate(item_data):
            tk.Label(frame2, text=value, bg="#1E1E2E", fg="#FFD700", font=(
                "Arial", 14), padx=10, pady=5).grid(row=row_count, column=col)

        # Append to list
        item_list.append({
            "item": item,
            "category": category,
            "quantity": quantity,
            "cost": cost,
            "total": total_cost,
            "date": date
        })

        # Update total cost display
        update_total_cost()

    except ValueError:
        return  # Ignore invalid input

# Function to update total cost


def update_total_cost():
    total = sum(item["total"] for item in item_list)
    total_cost_var.set(f"Total: ${total:.2f}")

# Function to clear input fields


def Clear_item():
    item_text.delete(0, "end")
    category_text.delete(0, "end")
    quantity_text.delete(0, "end")
    cost_text.delete(0, "end")

# Function to analyze expenses


def Analyse():
    if not item_list:
        return  # Prevent analyzing empty data

    data_frame = pd.DataFrame(item_list)
    grouped_data = data_frame.groupby("category")["total"].sum()

    plt.figure(figsize=(10, 5))
    plt.bar(grouped_data.index, grouped_data.values,
            color='#FF4500', width=0.4)
    plt.ylabel("Total Cost")
    plt.xlabel("Item Categories")
    plt.title("Expense Analysis by Category")
    plt.show()


# Title
title_label = tk.Label(root, text="Expense Tracker",
                       bg="#1E1E2E", fg="#00FF7F", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

# Input Fields
input_fields = {}
for label_text in ["Item", "Category", "Quantity", "Cost Per Unit"]:
    tk.Label(root, text=label_text, bg="#1E1E2E",
             fg="#FFFFFF", font=("Arial", 15)).pack()
    entry = tk.Entry(root, font=("Arial", 15))
    entry.pack()
    input_fields[label_text.lower().replace(" ", "_")] = entry

item_text = input_fields["item"]
category_text = input_fields["category"]
quantity_text = input_fields["quantity"]
cost_text = input_fields["cost_per_unit"]

# Buttons Frame
frame1 = tk.Frame(root, bg="#1E1E2E")
frame1.pack(pady=10)

add_button = tk.Button(frame1, text="Add Item", bg="#FF6347",
                       fg="#FFFFFF", font=("Arial", 15), command=Add_item)
add_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(frame1, text="Clear", bg="#4682B4",
                         fg="#FFFFFF", font=("Arial", 15), command=Clear_item)
clear_button.pack(side=tk.RIGHT, padx=10)

# Expense List Header
display_label = tk.Label(root, text="Expense List",
                         bg="#1E1E2E", fg="#FFD700", font=("Arial", 18, "bold"))
display_label.pack(pady=10)

# Expense List Display Frame
frame2 = tk.Frame(root, bg="#1E1E2E")
frame2.pack()

# Header row for the table
header_labels = ["Item", "Category", "Quantity",
                 "Cost Per Unit", "Total Cost", "Date"]
for col, text in enumerate(header_labels):
    tk.Label(frame2, text=text, bg="#1E1E2E", fg="#00FFFF", font=(
        "Arial", 14, "bold"), padx=10, pady=5).grid(row=0, column=col)

# Overall Total Cost Label
total_label = tk.Label(root, textvariable=total_cost_var,
                       bg="#1E1E2E", fg="#FF4500", font=("Arial", 18, "bold"))
total_label.pack(pady=10)

# Analyse Button
analyse_button = tk.Button(root, text="Analyse", bg="#32CD32",
                           fg="#FFFFFF", font=("Arial", 15), command=Analyse)
analyse_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
