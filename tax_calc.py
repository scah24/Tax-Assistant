import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import webbrowser


# Class for Old Tax Regime
class OldTaxRegime:
    def __init__(self):
        self.income = Decimal(0)
        self.deductions = Decimal(0)
        self.deductions_80C = Decimal(0)
        self.deductions_80D = Decimal(0)
        self.standard_deduction = Decimal(50000)

    def input_data(self, income, deductions_80C, deductions_80D):
        self.income = Decimal(income)
        self.deductions_80C = Decimal(deductions_80C)
        self.deductions_80D = Decimal(deductions_80D)
        self.deductions = self.deductions_80C + self.deductions_80D + self.standard_deduction

    def calculate_taxable_income(self):
        return max(self.income - self.deductions, Decimal(0))

    def calculate_tax(self, taxable_income):
        if taxable_income <= 250000:
            return Decimal(0)
        elif taxable_income <= 500000:
            return (taxable_income - 250000) * Decimal(0.05)
        elif taxable_income <= 1000000:
            return 12500 + (taxable_income - 500000) * Decimal(0.20)
        else:
            return 12500 + 100000 + (taxable_income - 1000000) * Decimal(0.30)

    def tax_summary(self, tax, taxable_income):
        return f"\n=== Tax Summary (Old Regime) ===\nTotal Income: ₹{self.income:,.2f}\n" \
               f"Total Deductions: ₹{self.deductions:,.2f}\nTaxable Income: ₹{taxable_income:,.2f}\n" \
               f"Total Tax Owed: ₹{tax:,.2f}"


# Class for New Tax Regime
class NewTaxRegime:
    def __init__(self):
        self.income = Decimal(0)

    def calculate_taxable_income(self):
        return max(self.income, Decimal(0))

    def calculate_tax(self, taxable_income):
        if taxable_income <= 700000:
            return Decimal(0)
        elif taxable_income <= 900000:
            return (taxable_income - 700000) * Decimal(0.10)
        elif taxable_income <= 1200000:
            return 20000 + (taxable_income - 900000) * Decimal(0.15)
        elif taxable_income <= 1500000:
            return 65000 + (taxable_income - 1200000) * Decimal(0.20)
        else:
            return 125000 + (taxable_income - 1500000) * Decimal(0.30)

    def tax_summary(self, tax, taxable_income):
        return f"\n=== Tax Summary (New Regime) ===\nTotal Income: ₹{self.income:,.2f}\n" \
               f"Taxable Income: ₹{taxable_income:,.2f}\n" \
               f"Total Tax Owed: ₹{tax:,.2f}"


# Open Tax Guide Link
def open_link(event):
    webbrowser.open("https://cleartax.in/s/80c-80-deductions")


# Validate Deductions
def validate_deductions(*args):
    deductions_80C = deductions_80C_entry.get()
    deductions_80D = deductions_80D_entry.get()

    if deductions_80C and float(deductions_80C) > 150000:
        error_80C_label.config(text="⚠ Maximum allowed: ₹1,50,000", fg="red")
    else:
        error_80C_label.config(text="")  # Clear message if within limit

    if deductions_80D and float(deductions_80D) > 50000:
        error_80D_label.config(text="⚠ Maximum allowed: ₹50,000", fg="red")
    else:
        error_80D_label.config(text="")  # Clear message if within limit


# Tax Calculation Function
def calculate_tax():
    regime_choice = regime_var.get()
    try:
        income = float(income_entry.get())
        if regime_choice == 1:
            deductions_80C = float(deductions_80C_entry.get())
            deductions_80D = float(deductions_80D_entry.get())

            # Validate deductions
            if deductions_80C > 150000:
                messagebox.showerror("Invalid Input", "Deductions under Section 80C cannot exceed ₹1,50,000.")
                return

            if deductions_80D > 50000:
                messagebox.showerror("Invalid Input", "Deductions under Section 80D cannot exceed ₹50,000.")
                return

            tax_assistant = OldTaxRegime()
            tax_assistant.input_data(income, deductions_80C, deductions_80D)
            taxable_income = tax_assistant.calculate_taxable_income()
            tax = tax_assistant.calculate_tax(taxable_income)
            result = tax_assistant.tax_summary(tax, taxable_income)
        elif regime_choice == 2:
            tax_assistant = NewTaxRegime()
            tax_assistant.income = Decimal(income)
            taxable_income = tax_assistant.calculate_taxable_income()
            tax = tax_assistant.calculate_tax(taxable_income)
            result = tax_assistant.tax_summary(tax, taxable_income)
        else:
            result = "Please select a valid tax regime."

        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")


# Function to Exit the Application
def exit_app():
    root.quit()


# GUI Implementation
root = tk.Tk()
root.title("Indian Tax Assistant")
root.geometry("600x600")
root.configure(bg="#E3F2FD")

regime_var = tk.IntVar()

# Heading
tk.Label(root, text="Indian Tax Calculator", font=("Arial", 16, "bold"), bg="#1565C0", fg="white", padx=10,
         pady=10).pack(fill="x")

# Regime Selection
frame = tk.Frame(root, bg="#E3F2FD")
frame.pack(pady=10)

old_regime_radio = tk.Radiobutton(frame, text="Old Tax Regime", variable=regime_var, value=1, font=("Arial", 12),
                                  bg="#E3F2FD")
old_regime_radio.grid(row=0, column=0, padx=20)

new_regime_radio = tk.Radiobutton(frame, text="New Tax Regime", variable=regime_var, value=2, font=("Arial", 12),
                                  bg="#E3F2FD")
new_regime_radio.grid(row=0, column=1, padx=20)

# Income Input
tk.Label(root, text="Enter your total income (in ₹):", font=("Arial", 12), bg="#E3F2FD").pack(pady=5)
income_entry = tk.Entry(root, font=("Arial", 12), width=25)
income_entry.pack()

# Deduction 80C
tk.Label(root, text="Deductions under Section 80C (PPF, ELSS, LIC) ₹:", font=("Arial", 12), bg="#E3F2FD").pack(pady=5)
deductions_80C_entry = tk.Entry(root, font=("Arial", 12), width=25)
deductions_80C_entry.pack()

# Error Label for 80C
error_80C_label = tk.Label(root, text="", font=("Arial", 10), bg="#E3F2FD", fg="red")
error_80C_label.pack()

# Deduction 80D
tk.Label(root, text="Deductions under Section 80D (Health Insurance) ₹:", font=("Arial", 12), bg="#E3F2FD").pack(pady=5)
deductions_80D_entry = tk.Entry(root, font=("Arial", 12), width=25)
deductions_80D_entry.pack()

# Error Label for 80D
error_80D_label = tk.Label(root, text="", font=("Arial", 10), bg="#E3F2FD", fg="red")
error_80D_label.pack()

# Link for More Info
link_label = tk.Label(root, text="Click here to know about 80C & 80D deductions", fg="blue", cursor="hand2",
                      font=("Arial", 11), bg="#E3F2FD")
link_label.pack(pady=5)
link_label.bind("<Button-1>", open_link)

# Bind validation to entry changes
deductions_80C_entry.bind("<KeyRelease>", validate_deductions)
deductions_80D_entry.bind("<KeyRelease>", validate_deductions)

# Calculate Button
calculate_button = tk.Button(root, text="Calculate Tax", command=calculate_tax, font=("Arial", 14), bg="#0288D1",
                             fg="white", width=15)
calculate_button.pack(pady=15)

def on_enter(c):
    calculate_button.config(bg="#81D4FA")

def on_leave(c):
    calculate_button.config(bg="#0288D1")

calculate_button.bind("<Enter>", on_enter)
calculate_button.bind("<Leave>", on_leave)

# Result Display
result_text = tk.Text(root, height=6, width=55, font=("Arial", 12), state=tk.DISABLED)
result_text.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=exit_app, font=("Arial", 14, "bold"), bg="#B71C1C", fg="white",
                        width=15)
exit_button.pack(pady=10)

# Add Hover Effect on Exit Button
def on_enter(e):
    exit_button.config(bg="#D32F2F")

def on_leave(e):
    exit_button.config(bg="#B71C1C")

exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

root.mainloop()