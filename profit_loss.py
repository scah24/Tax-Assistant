import re
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tkinter as tk
from tkinter import filedialog, messagebox


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Function to find credits and debits
def find_credit_debit(text):
    credit_pattern = r'Credit\s+([0-9,]+(?:\.\d{2})?)'
    debit_pattern = r'Debit\s+([0-9,]+(?:\.\d{2})?)'
    credits = re.findall(credit_pattern, text)
    debits = re.findall(debit_pattern, text)
    return credits, debits


# Function to calculate totals
def calculate_totals(credits, debits):
    total_credit = sum([float(c.replace(',', '')) for c in credits])
    total_debit = sum([float(d.replace(',', '')) for d in debits])
    return total_credit, total_debit


# Function to calculate net profit
def calculate_net_profit(total_credit, total_debit):
    return total_credit - total_debit


# Function to calculate tax
def calculate_tax(net_profit):
    if net_profit <= 1_00_00_000:
        tax = net_profit * 0.25
    elif net_profit <= 10_00_00_000:
        tax = net_profit * 0.30
    else:
        tax = net_profit * 0.30
        tax += tax * 0.10
    return tax


# Function to calculate Profit After Tax (PAT)
def calculate_pat(net_profit, tax):
    return net_profit - tax


# Function to generate report PDF
def create_totals_pdf(output_pdf, total_credit, total_debit, net_profit, tax, pat):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, "Financial Report")

    c.setFont("Helvetica", 12)
    y_position = 760
    c.drawString(100, y_position, f"Total Credit: {total_credit:.2f}")
    y_position -= 20
    c.drawString(100, y_position, f"Total Debit: {total_debit:.2f}")
    y_position -= 20
    c.drawString(100, y_position, f"Net Profit: {net_profit:.2f}")
    y_position -= 20
    c.drawString(100, y_position, f"Total Tax: {tax:.2f}")
    y_position -= 20
    c.drawString(100, y_position, f"Profit After Tax (PAT): {pat:.2f}")

    c.save()


# Function to process the bank statement
def process_bank_statement(pdf_path, output_pdf):
    text = extract_text_from_pdf(pdf_path)
    credits, debits = find_credit_debit(text)
    total_credit, total_debit = calculate_totals(credits, debits)
    net_profit = calculate_net_profit(total_credit, total_debit)
    tax = calculate_tax(net_profit)
    pat = calculate_pat(net_profit, tax)

    create_totals_pdf(output_pdf, total_credit, total_debit, net_profit, tax, pat)
    return f"Report saved as: {output_pdf}"


# Browse input PDF
def browse_pdf_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_pdf_var.set(filepath)


# Browse output PDF
def browse_output_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if filepath:
        output_pdf_var.set(filepath)


# Process and generate PDF
def process_and_generate_pdf():
    input_pdf = input_pdf_var.get()
    output_pdf = output_pdf_var.get()

    if not input_pdf or not output_pdf:
        messagebox.showerror("Error", "Please select both input and output files.")
        return

    try:
        result_message = process_bank_statement(input_pdf, output_pdf)
        messagebox.showinfo("Success", result_message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Setup
root = tk.Tk()
root.title("Bank Statement Processor")
root.geometry("500x350")
root.configure(bg="#1E3A5F")  # Blue Theme

input_pdf_var = tk.StringVar()
output_pdf_var = tk.StringVar()

# Labels
tk.Label(root, text="Input PDF File:", bg="#1E3A5F", fg="white", font=("Arial", 12)).pack(padx=10, pady=5)
tk.Entry(root, textvariable=input_pdf_var, width=40, bg="#D9E6F3").pack(padx=10, pady=5)
tk.Button(root, text="Browse", font=("Arial", 10), bg="#0073E6", fg="white", command=browse_pdf_file).pack(padx=10,
                                                                                                           pady=5)

tk.Label(root, text="Output PDF File:", bg="#1E3A5F", fg="white", font=("Arial", 12)).pack(padx=10, pady=5)
tk.Entry(root, textvariable=output_pdf_var, width=40, bg="#D9E6F3").pack(padx=10, pady=5)
tk.Button(root, text="Browse", font=("Arial", 10), bg="#0073E6", fg="white", command=browse_output_file).pack(padx=10,
                                                                                                              pady=5)

tk.Button(root, text="Process and Generate PDF", font=("Arial", 12, "bold"), bg="#0073E6", fg="white",
          command=process_and_generate_pdf).pack(padx=10, pady=20)


# Exit Button with Hover Effect (Red Default, Lighter Red on Hover)
def on_enter(e):
    exit_button.config(bg="#FF6666", fg="white")  # Lighter Red on Hover


def on_leave(e):
    exit_button.config(bg="#D32F2F", fg="white")  # Dark Red Default


exit_button = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="#D32F2F", fg="white", command=root.quit)
exit_button.pack(pady=10)
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

root.mainloop()
