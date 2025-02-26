from tkinter import *
import subprocess

# Initialize Main Window
root = Tk()
root.title("Tax Assistant")
root.geometry("600x400")
root.configure(bg="#1E3A5F")  # Home Page Background Color

header_label = Label(root, text="Tax Assistant", font=("Arial", 16, "bold"), bg="#1E3A5F", fg="white")
header_label.pack(pady=10)

# Function to open Smart Audit System
def open_smart_audit():
    subprocess.Popen(["python", "profit_loss.py"])

# Function to open Indian Tax Assistant
def open_tax_assistant():
    subprocess.Popen(["python", "tax_calc.py"])

# Function to open Tax Assistant Chatbot
def open_chatbot():
    subprocess.Popen(["python", "bot.py"])

# Buttons for features
audit_button = Button(root, text="Financial Analysis", font=("Arial", 12, "bold"), bg="#0073E6", fg="white", command=open_smart_audit)
audit_button.pack(pady=10)

filing_button = Button(root, text="Tax Calculation", font=("Arial", 12, "bold"), bg="#0073E6", fg="white", command=open_tax_assistant)
filing_button.pack(pady=10)

chatbot_button = Button(root, text="Tax Assistant Chatbot", font=("Arial", 12, "bold"), bg="#0073E6", fg="white", command=open_chatbot)
chatbot_button.pack(pady=10)

# Exit Button with Hover Effect (Red Default, Lighter Red on Hover)
def on_enter(e):
    exit_button.config(bg="#FF6666", fg="white")  # Lighter Red on Hover

def on_leave(e):
    exit_button.config(bg="#D32F2F", fg="white")  # Dark Red Default

exit_button = Button(root, text="Exit", font=("Arial", 12, "bold"), bg="#D32F2F", fg="white", command=root.quit)
exit_button.pack(pady=10)
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

# Run the Home Page
root.mainloop()
