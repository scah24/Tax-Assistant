from tkinter import *
from tkinter import scrolledtext
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create ChatBot instance
chatbot = ChatBot(
    'TaxBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db',
)

# Define training data
training_data = [
    # Greetings
    "hi", "Hello! How can I assist you with your taxes today?",
    "hii", "Hello! How can I assist you with your taxes today?",
    "hello", "Hello! How can I assist you with your taxes today?",
    "hey", "Hello! How can I assist you with your taxes today?",
    "howdy", "Hello! How can I assist you with your taxes today?",

    # Income Tax and other sections
    "What is income tax?", "Income tax is a tax that the government imposes on earnings.",
    "What is income tax return?",
    "An income tax return is a form used to report income and taxes paid to the government.",
    "How do I file an income tax return?", "You can file it online through the Income Tax e-filing portal.",

    # Section 24(b) - Home Loan Interest Deduction
    "What is Section 24(b)?",
    "Section 24(b) allows you to claim a deduction on the interest paid on home loans. You can claim up to ₹2 lakh per year for a self-occupied property.",
    "What is the maximum limit under Section 24(b)?",
    "Under Section 24(b), you can claim a maximum deduction of ₹2 lakh on the interest paid on home loans for a self-occupied property.",
    "Can I claim Section 24(b) for rented property?",
    "Yes, you can claim a deduction on home loan interest for rented properties under Section 24(b), without any upper limit.",

    # Section 80C - Deductions
    "What is Section 80C?",
    "Section 80C of the Income Tax Act allows individuals and Hindu Undivided Families (HUF) to claim deductions for investments in specified financial instruments like PPF, ELSS, and life insurance premiums, up to ₹1.5 lakh.",
    "What are the eligible investments under Section 80C?",
    "Investments eligible for deduction under Section 80C include PPF, NSC, EPF, life insurance premiums, 5-year fixed deposits, and more.",
    "What is the maximum deduction under Section 80C?",
    "The maximum deduction you can claim under Section 80C is ₹1.5 lakh in a financial year.",
    "Can I claim tax deductions under Section 80C for tuition fees?",
    "Yes, tuition fees for children’s education are eligible for deductions under Section 80C, up to ₹1.5 lakh.",

    # TDS (Tax Deducted at Source)
    "What is TDS?",
    "TDS (Tax Deducted at Source) is the tax that is deducted by the payer from payments made to the payee, before making the payment. This tax is then submitted to the government.",
    "What is tds?",
    "TDS (Tax Deducted at Source) is the tax that is deducted by the payer from payments made to the payee, before making the payment. This tax is then submitted to the government.",
    "What is TDS on salary?",
    "TDS on salary is deducted by the employer based on the income tax slabs applicable to the employee's total income for the year.",
    "What is tds on salary?",
    "TDS on salary is deducted by the employer based on the income tax slabs applicable to the employee's total income for the year.",
    "What is the TDS rate on salary?",
    "The TDS rate on salary depends on the individual’s income tax slab. For example, 5% for income between ₹2.5 lakh and ₹5 lakh, 20% for income between ₹5 lakh and ₹10 lakh, and 30% for income above ₹10 lakh.",
    "What is the tds rate on salary?",
    "The TDS rate on salary depends on the individual’s income tax slab. For example, 5% for income between ₹2.5 lakh and ₹5 lakh, 20% for income between ₹5 lakh and ₹10 lakh, and 30% for income above ₹10 lakh.",
    "What is TDS on interest income?",
    "For interest income from a savings account, TDS is deducted at the rate of 10% if the interest exceeds ₹10,000 in a financial year.",
    "What is tds on interest income?",
    "For interest income from a savings account, TDS is deducted at the rate of 10% if the interest exceeds ₹10,000 in a financial year.",
    "How is TDS calculated?",
    "TDS is calculated as a percentage of the income received. For example, 10% of the interest income or salary, based on the applicable TDS rate for that income.",
    "How is tds calculated?",
    "TDS is calculated as a percentage of the income received. For example, 10% of the interest income or salary, based on the applicable TDS rate for that income.",
    "When is TDS deducted?", "TDS is deducted at the time of payment or credit to the payee, whichever occurs first.",
    "When is tds deducted?", "TDS is deducted at the time of payment or credit to the payee, whichever occurs first.",
    "What are TDS exemptions?",
    "Certain types of income, such as interest from savings accounts up to ₹10,000, are exempt from TDS. Also, senior citizens are exempt from TDS on interest income up to ₹50,000 in certain cases.",
    "What are tds exemptions?",
    "Certain types of income, such as interest from savings accounts up to ₹10,000, are exempt from TDS. Also, senior citizens are exempt from TDS on interest income up to ₹50,000 in certain cases.",
    "How can I check my TDS deductions?",
    "You can check your TDS deduction in your Form 26AS, which is available on the Income Tax e-filing portal.",
    "How can I check my tds deductions?",
    "You can check your TDS deduction in your Form 26AS, which is available on the Income Tax e-filing portal.",
    "What is the TDS return?",
    "TDS return is a form that needs to be filed by the deductor to report the amount of tax deducted and remitted to the government on behalf of the payee.",
    "What is the tds return?",
    "TDS return is a form that needs to be filed by the deductor to report the amount of tax deducted and remitted to the government on behalf of the payee.",

    # GST related queries
    "What is GST?",
    "GST (Goods and Services Tax) is a single tax that replaces multiple indirect taxes in India. It is levied on the supply of goods and services.",
    "What is gst?",
    "GST (Goods and Services Tax) is a single tax that replaces multiple indirect taxes in India. It is levied on the supply of goods and services.",
    "What are the GST rates in India?",
    "GST rates in India range from 0% to 28%, with 0% on essential goods, 5% on certain goods and services, and 28% on luxury goods and services.",
    "What is the GST rate for food items?",
    "Most food items fall under the 0% GST rate, but packaged food items can have a GST rate of 5% or more.",
    "What is GSTIN?",
    "GSTIN (Goods and Services Tax Identification Number) is a unique identifier assigned to businesses registered under GST.",
    "What is the GST rate for services?",
    "The GST rate for services generally ranges from 5% to 18%, with some services taxed at 28%.",
    "How is GST calculated?",
    "GST is calculated as a percentage of the sale value of goods and services, and varies depending on the type of goods or service. Example: For a good priced at ₹100 with 18% GST, GST = 18% of ₹100 = ₹18.",
    "What is the input tax credit (ITC)?",
    "Input Tax Credit (ITC) allows businesses to reduce the tax paid on inputs (goods and services) from the tax payable on output (sales).",
    "How do I calculate GST on a product?",
    "To calculate GST, multiply the cost of the product by the applicable GST rate (e.g., 18% for most products). Example: ₹100 * 18% = ₹18 GST.",
    "What is the threshold for GST registration?",
    "GST registration is mandatory if your annual turnover exceeds ₹20 lakh (₹10 lakh for special category states).",
    "Do I need to file GST returns?",
    "Yes, GST returns must be filed by businesses registered under GST. These are usually filed monthly or quarterly depending on the turnover.",
    "What is GST return?",
    "GST return is a form that businesses must file with the government to report the GST collected and paid on sales and purchases.",
    "What is the due date for GST return filing?",
    "GST returns are due by the 20th of the following month for regular taxpayers.",

    # Senior Citizen Taxation
    "What is the income tax exemption for senior citizens?",
    "For senior citizens (60 years and above), the exemption limit is ₹3 lakh for FY 2025-26.",
    "What is the tax exemption for very senior citizens?",
    "For very senior citizens (80 years and above), the exemption limit is ₹5 lakh for FY 2025-26.",
    "Do senior citizens need to file tax returns?",
    "Yes, senior citizens need to file income tax returns if their income exceeds the exemption limit.",

    # Tax Audit
    "Do I need a tax audit?",
    "A tax audit is required if your turnover exceeds ₹1 crore for businesses or ₹50 lakh for professionals under Section 44AB.",
    "What is Section 44AB?",
    "Section 44AB mandates a tax audit if the turnover of a business exceeds ₹1 crore (₹50 lakh for professionals).",

    # Capital Gains Tax
    "What is capital gains tax?",
    "Capital gains tax is levied on the profit earned from the sale of capital assets like property, shares, or bonds.",
    "What are the types of capital gains?",
    "There are two types of capital gains: short-term capital gains (STCG) and long-term capital gains (LTCG).",
    "What is the tax on long-term capital gains?",
    "Long-term capital gains are taxed at 20% with indexation benefits for most assets.",
    "What is the tax on short-term capital gains?",
    "Short-term capital gains are taxed at 15% on the sale of listed shares or equity mutual funds.",

    # Rebates and Exemptions
    "What is the income tax rebate for individuals?",
    "Under Section 87A, individuals with income up to ₹5 lakh can avail of a rebate of up to ₹12,500.",
    "What are exemptions for agricultural income?",
    "Agricultural income is generally exempt from income tax, subject to certain conditions.",
    "What is the HRA exemption?",
    "House Rent Allowance (HRA) is partially exempt from tax based on rent paid, salary, and city of residence.",

    # Other Exemptions
    "What are the exemptions for children’s education?",
    "You can claim exemptions for children’s education under Section 80C for tuition fees paid.",
    "Can I claim tax deductions for donations?",
    "Yes, donations to registered charitable organizations can be deducted under Section 80G.",
    "What is the exemption for interest on savings account?",
    "Interest on savings accounts is exempt up to ₹10,000 under Section 80TTA for individuals below 60 years.",

    # Miscellaneous
    "What is the deadline for filing GST returns?",
    "GST returns must be filed by the 20th of the following month for regular taxpayers.",
    "How is GST calculated?",
    "GST is calculated as a percentage of the sale value of goods and services, with rates varying by category.",
    "What is the income tax deduction for education loans?",
    "Under Section 80E, you can claim a deduction on interest paid on education loans for higher studies.",
    "What is Section 80E?", "Section 80E provides tax deductions on interest paid on loans taken for higher education.",

    # Special cases
    "What is the tax treatment of NRI income?",
    "Income earned by Non-Resident Indians (NRIs) in India is subject to Indian income tax laws.",
    "What is a tax haven?", "A tax haven is a jurisdiction that offers low or zero tax rates for foreign investors.",
    "Do I need to pay tax on cryptocurrency gains?",
    "Yes, cryptocurrency gains are considered taxable under capital gains tax, based on the holding period and amount.",

]

# Train the chatbot
trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Create GUI
root = Tk()
root.title("TaxBot - AI Tax Assistant")
root.geometry("500x600")
root.configure(bg="#1E3A5F")  # Dark Blue Background

# Header Label
header_label = Label(root, text="TaxBot - AI Tax Assistant", font=("Arial", 14, "bold"), bg="#1E3A5F", fg="white")
header_label.pack(pady=10)

# Chat Display Area (Scrollable)
chat_display = scrolledtext.ScrolledText(root, wrap=WORD, width=55, height=20, bg="#E0E8F0", fg="black",
                                         font=("Arial", 12))
chat_display.pack(padx=10, pady=5)
chat_display.insert(END, "TaxBot: Hello! How can I assist you with your taxes today?\n\n")
chat_display.config(state=DISABLED)

# User Input Box
user_input = Entry(root, font=("Arial", 12), width=40, bg="#D9E6F3")
user_input.pack(pady=5)

# Function to handle user input
def send_message():
    user_text = user_input.get()
    if user_text.strip():  # Check if input is not empty
        chat_display.config(state=NORMAL)
        chat_display.insert(END, f"You: {user_text}\n", "user")
        response = chatbot.get_response(user_text)
        chat_display.insert(END, f"TaxBot: {response}\n\n", "bot")
        chat_display.config(state=DISABLED)
        chat_display.yview(END)  # Scroll to the bottom
    user_input.delete(0, END)

# Send Button
send_button = Button(root, text="Send", font=("Arial", 12, "bold"), bg="#0073E6", fg="white", command=send_message)
send_button.pack(pady=5)

# Exit Button
def on_enter(e):
    exit_button.config(bg="#FF6666", fg="white")  # Lighter Red on Hover

def on_leave(e):
    exit_button.config(bg="#D32F2F", fg="white")

exit_button = Button(root, text="Exit", font=("Arial", 12, "bold"), bg="#D32F2F", fg="white", command=root.quit)
exit_button.pack(pady=5)

exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

# Run the chatbot GUI
root.mainloop()