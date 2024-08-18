import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from datetime import datetime
import json
import numpy as np

# Initialize the main application window
root = tk.Tk()
root.title("Church Lot Purchase Progress")
root.geometry("400x500")

# Global variables
goal = 1000000  # 1 million pesos goal
current_progress = 0
min_increment = 0.0001  # Minimum progress increment per lot
lot_price = 5000
contributions = []  # List to store the contributions along with the dates

# Update the progress bar
def update_progress():
    global current_progress
    progress_percent = (current_progress / goal) * 100
    # Ensure the progress bar shows at least the minimum increment per lot
    if progress_percent > 0 and progress_percent < min_increment:
        progress_percent = min_increment
    progress_bar['value'] = progress_percent
    progress_label.config(text=f"Progress: {progress_percent:.4f}%")

# Function to handle lot purchase
def purchase_lot():
    def on_confirm():
        global current_progress
        try:
            num_lots = int(lot_entry.get())
            total_cost = num_lots * lot_price  # Calculate total cost
            if confirm_var.get() == 1:
                current_progress += total_cost  # Add the total cost to the current progress
                contributions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_cost))  # Log the contribution with the date
                update_progress()
                log_purchase(name_entry.get(), num_lots)  # Log the purchase
                purchase_window.destroy()
            else:
                messagebox.showinfo("Info", "You need to confirm the purchase.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of lots.")

    # Create a new window to get user details
    purchase_window = tk.Toplevel(root)
    purchase_window.title("Purchase Lot")
    purchase_window.geometry("350x200")

    tk.Label(purchase_window, text="Enter Your Name:").pack(pady=10)
    name_entry = tk.Entry(purchase_window)
    name_entry.pack(pady=5)

    tk.Label(purchase_window, text="How many lots do you want to purchase?").pack(pady=10)
    lot_entry = tk.Entry(purchase_window)
    lot_entry.pack(pady=5)

    confirm_var = tk.IntVar()
    confirm_check = tk.Checkbutton(
        purchase_window,
        text=f"Each lot costs {lot_price} Pesos. Do you want to proceed?",
        variable=confirm_var
    )
    confirm_check.pack(pady=10)

    confirm_button = tk.Button(purchase_window, text="Confirm Purchase", command=on_confirm)
    confirm_button.pack(pady=5)

# Function to log the purchase
def log_purchase(name, num_lots):
    log_text.insert(tk.END, f"{name} purchased {num_lots} lot(s).\n")
    log_text.see(tk.END)  # Scroll to the latest entry

# Function to display the contributions graph
def show_graph():
    dates = [datetime.strptime(contribution[0], "%Y-%m-%d %H:%M:%S") for contribution in contributions]
    amounts = [contribution[1] for contribution in contributions]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o')
    plt.title("Contributions Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount (Pesos)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to display the lot grid graph
def show_lot_grid():
    num_lots = goal // lot_price  # Total number of lots
    purchased_lots = int(current_progress / lot_price)  # Number of purchased lots

    grid_size = int(np.ceil(np.sqrt(num_lots)))  # Determine the grid size (grid_size x grid_size)

    grid = np.zeros((grid_size, grid_size))  # Initialize a grid of zeros
    grid.ravel()[:purchased_lots] = 1  # Mark purchased lots as 1

    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap="Greens", vmin=0, vmax=1, aspect='equal')
    plt.title("Lot Purchase Progress")
    plt.xticks([])
    plt.yticks([])

    # Add a legend
    plt.scatter([], [], color='green', label='Purchased')
    plt.scatter([], [], color='gray', label='Available')
    plt.legend(loc='upper right')

    plt.show()

# Function to handle "New"
def new_file():
    global current_progress, contributions
    current_progress = 0
    contributions = []
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Purchase History:\n")
    update_progress()

# Function to handle "Save"
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump({"progress": current_progress, "contributions": contributions}, file)

# Function to handle "Load"
def load_file():
    global current_progress, contributions
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            data = json.load(file)
            current_progress = data["progress"]
            contributions = data["contributions"]
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, "Purchase History:\n")
            for contribution in contributions:
                log_purchase(contribution[0], contribution[1] // lot_price)
            update_progress()

# Create a menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Load", command=load_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Configure the root window to display the menu bar
root.config(menu=menu_bar)

# Program name label
program_name_label = tk.Label(root, text="LCC Isabela Church Lot Progress App", font=("Arial", 16))
program_name_label.pack(pady=10)

# Progress bar widget
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

# Label to display progress percentage
progress_label = tk.Label(root, text="Progress: 0%")
progress_label.pack(pady=5)

# Button to open the purchase window
purchase_button = tk.Button(root, text="Add a Lot", command=purchase_lot)
purchase_button.pack(pady=20)

# Button to show the contributions graph
graph_button = tk.Button(root, text="Show Contributions Graph", command=show_graph)
graph_button.pack(pady=10)

# Button to show the lot grid graph
grid_button = tk.Button(root, text="Show Lot Grid", command=show_lot_grid)
grid_button.pack(pady=10)

# Log Text widget to display purchase history
log_text = tk.Text(root, height=10, width=45, state=tk.NORMAL)
log_text.pack(pady=10)
log_text.insert(tk.END, "Purchase History:\n")

# Start the Tkinter event loop
root.mainloop()
