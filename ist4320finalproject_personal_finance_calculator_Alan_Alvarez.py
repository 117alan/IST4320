#Completed By Alan Alvarez

import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from itertools import groupby

#Creating a class for all functions to be initilized and defined
class PersonalFinanceApp:
    def __init__(self, master):
        self.master = master
        master.title("Personal Finance Tracker & Calculator")

        self.user_name()
        self.date_selector()
        self.monthly_balance()
        self.monthly_earnings()
        self.monthly_expenses()
        self.initialize_db()
        
        #The main heading for the app:
        self.heading_label = tk.Label(self.master, relief = tk.RAISED, bg = 'lightblue', text="Welcome to The Personal Finance Calculator.\n"
                                     "Please fill out all entries with an appropriate value.\n"
                                     "If any financials are zero, just enter 0.0 and submit")
        
        #The name title label, entry box, and output label:
        self.nametitle_label = tk.Label(self.master, bg = 'lightblue',text="Enter Your Name Here: ")
        self.submit_name_button = tk.Button(self.master, text = "Set Name", bg = 'blue', command = self.set_name)
        self.submit_name_label = tk.Label(self.master, bg = 'Lightblue', text="Name: ")

        #The date title label, month selector and year entry box and output label:
        self.datetitle_label = tk.Label(self.master, bg = 'lightblue', text="Enter the month and year you want to calcuate your personal finaces: ")
        self.submit_date_button = tk.Button(self.master, text="Set Month and Year", bg = 'blue', command=self.set_date)
        self.selected_date_label = tk.Label(self.master, bg = 'lightblue', text ="Selected Date: ")
        
        #The account balance title, entry box, and output label
        self.balancetitle_label = tk.Label(self.master, bg = 'lightblue', text="Enter your current account balance if so desired: ")
        self.submit_balance_button = tk.Button(self.master, text = "Set Current Account Balance", bg ='blue', command = self.set_balance)
        self.submit_balance_label = tk.Label(self.master, bg = 'lightblue', text="Current Balance: 0")
        
        #The earnings balance title, entry box, and output label
        self.earntitle_label = tk.Label(self.master, bg = 'lightblue', text="Enter your estimated monthly earnings you'll recieve/recieved by the end of the month: ")
        self.sumbit_earnings_button = tk.Button(self.master, text = "Submit Earnings", bg = 'blue', command = self.set_earnings)
        self.submit_earnings_label = tk.Label(self.master, bg = 'lightblue', text="Current earnings with account balance: 0")

        #The expenses balance title, entry box, and output label
        self.expetitle_label = tk.Label(self.master, bg = 'lightblue', text="Enter your estimated monthly expesnses you'll spend/spent by the end of the month: ")
        self.submit_expenses_button = tk.Button(self.master, text = "Submit Expenses",bg = 'blue', command = self.set_expenses)
        self.submit_expenses_label = tk.Label(self.master, bg = 'lightblue',text="Remaining Budget: 0")
        
        #The Save/Update data button, view the saved records button, and delete records from database button
        self.save_button = tk.Button(master, text="Save/Update Data", bg = 'Yellow', command=self.on_save_clicked)
        self.view_button = tk.Button(master, text="View Records", bg = 'pink', command=self.on_view_clicked)
        self.delete_all_button = tk.Button(self.master, text="Delete All Records", bg = 'red', command=self.delete_all_records)

        #Finacial advice and the remaining budget button
        self.finacial_advice_button = tk.Button(self.master, text="Financial Advice", fg = 'white', bg = 'darkblue',command=self.show_financial_advice)
        self.remain_budget_button = tk.Button(self.master, text="Remaining Budget By Date and Name", fg = 'white', bg = 'darkblue', command=self.show_remain_budget) 
        
        #The graph button
        self.plot_button = tk.Button(self.master, text="Show Graph", bg = 'lime', command=self.plot_data) 



    #User input for the name
    def user_name(self):
        self.name_var = tk.StringVar(self.master)
        self.name_entry = tk.Entry(self.master, textvariable= self.name_var)
    
    def set_name(self):
        name = self.name_var.get()
        self.submit_name_label.config(text=f"Name: {name}")
   
    def set_date(self):
        month = self.month_var.get()
        year = self.year_var.get()
        if month == 'Select Month' or not 1900 <= year <= 2030:
            messagebox.showwarning("Warning", "Please select both a valid month and year.")
            return
        self.selected_date_label.config(text=f"Selected Date: {month} {year}")
    
    #User Input for the month and year
    def date_selector(self):
        # Month Selector
        self.month_var = tk.StringVar(self.master)
        self.month_selector = ttk.Combobox(self.master, textvariable=self.month_var)
        self.month_selector['values'] = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        self.month_selector.set('Select Month')

        # Year Selector
        self.year_var = tk.IntVar(self.master)
        self.year_entry = tk.Entry(self.master, textvariable = self.year_var)
    
    #User input for the current account balance
    def set_balance(self):
        balance = self.balance_var.get()
        self.submit_balance_label.config(text=f"Current Balance: {balance}")
    
    def monthly_balance(self):
        self.balance_var = tk.DoubleVar(self.master)
        self.balance_entry = tk.Entry(self.master, textvariable= self.balance_var)

    #User input for the estimated monthly earnings
    def set_earnings(self):
        try:
            balance = self.balance_var.get()  
        except ValueError:
            balance = 0.0  # If the balance entry is empty or invalid, default to 0.0
    
        try:
            earnings = self.earn_var.get()  
        except ValueError:
            earnings = 0.0 

        # Adding the balance and earnings to get the new balance
        new_balance = balance + earnings

        # Update the balance label with the new balance
        self.submit_earnings_label.config(text=f"Current earnings with account balance: {new_balance:.2f}")

    def monthly_earnings(self):
        self.earn_var = tk.DoubleVar(self.master)
        self.earn_entry = tk.Entry(self.master, textvariable = self.earn_var)

    #User input for their estimated monthly expenses
    def set_expenses(self):
        try:
            balance = float(self.balance_var.get())
        except ValueError:
            balance = 0.0  # Default to 0 if not entered

        try:
            earnings = float(self.earn_var.get())
        except ValueError:
            earnings = 0.0  # Default to 0 if not entered

        try:
            expenses = float(self.expe_var.get())
        except ValueError:
            expenses = 0.0  # Default to 0 if not entered
        
    # Calculate the remaining budget
        remaining_budget = balance + earnings - expenses

        self.submit_expenses_label.config(text=f"Remaining Budget: {remaining_budget:.2f}")
   
    def monthly_expenses(self):
        #User inputs their earnings for the month
        self.expe_var = tk.DoubleVar(self.master)
        self.expe_entry = tk.Entry(self.master, textvariable = self.expe_var)
    
    def initialize_db(self):
        # Connect to SQLite database, if file does not exist it will be created
        self.conn = sqlite3.connect('personal_finance.db')
    
        # Create a cursor object using the cursor() method
        cursor = self.conn.cursor()
    
        # Creating the table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            balance REAL NOT NULL,
            earnings REAL NOT NULL,
            expenses REAL NOT NULL,
            UNIQUE(name, date)
        )
        ''')
    
    #Getting value from the GUI elements
    def on_save_clicked(self):
         
        name = self.name_entry.get()
        month = self.month_var.get()  
        year = self.year_var.get()    

        # Validate the month and year fields
        try:
            year = int(self.year_var.get())  
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid year (numbers only).")
            return

        if not name or month == 'Select Month': 
            messagebox.showerror("Input Error", "Please enter your name, select a valid month, and enter a valid year.")
            return
    
        date = f"{month} {year}"  
        
        #Validate and convert numeric fields
        try:
            balance = float(self.balance_entry.get()) if self.balance_entry.get() else 0.0
            earnings = float(self.earn_entry.get()) if self.earn_entry.get() else 0.0
            expenses = float(self.expe_entry.get()) if self.expe_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for balance, earnings, and expenses.")
            return

    # Insert data into the database
        self.insert_update_data(name, date, balance, earnings, expenses)
        messagebox.showinfo("Success", "Data saved successfully!")

    def insert_update_data(self, name, date, balance, earnings, expenses):
        cursor = self.conn.cursor()
    
        # Check if an entry for this name and date already exists
        cursor.execute('SELECT id FROM finances WHERE name = ? AND date = ?', (name, date))
        existing_entry = cursor.fetchone()
    
        if existing_entry:
            #Update entry
            cursor.execute('''
                UPDATE finances
                SET balance = ?, earnings = ?, expenses = ?
                WHERE id = ?
            ''', (balance, earnings, expenses, existing_entry[0]))
        else:
             #insert a new one
            cursor.execute('''
                INSERT INTO finances (name, date, balance, earnings, expenses)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, date, balance, earnings, expenses))
    
        self.conn.commit()
    
    #Allows user to view the records stored in the database based on user input
    def on_view_clicked(self):
        records = self.retrieve_data()
        records_str = "\n".join([str(record) for record in records])
        messagebox.showinfo("Records", records_str)

    #Makes it so the when the button is clicked, the data is retrieved
    def retrieve_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM finances')
        records = cursor.fetchall()
        return records
    
    #User is able to delete all records from the database if so desired
    def delete_all_records(self):
        # Confirm with the user that they want to delete all records
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all records? This action cannot be undone.")
        if confirm:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM finances')
            self.conn.commit()
            messagebox.showinfo("Records Deleted", "All records have been successfully deleted.")
    
    #Aloows user to view finacial advice based on the ratio of their monthly expenses and earnings + balance
    def show_financial_advice(self):
        balance_str = self.balance_entry.get()
        earnings_str = self.earn_entry.get()
        expenses_str = self.expe_entry.get()

        # Check if any of the fields are empty 
        if not balance_str or not earnings_str or not expenses_str:
            tk.messagebox.showinfo("Input Needed", "Please input your financial information first")
            return  

        balance = float(balance_str)
        earnings = float(earnings_str)
        expenses = float(expenses_str)

        # Ensure the user has inputted non-zero earnings or balance to avoid division by zero
        if balance + earnings <= 0:
            tk.messagebox.showinfo("Input Error", "Balance and earnings can't both be zero.")
            return

        # Calculate the spending percentage
        spending_percentage = (expenses / (balance + earnings)) * 100 if balance + earnings else 0

        # Determine financial advice based on spending percentage
        if spending_percentage < 30:
            advice = "Your spending is well-managed at {:.2f}% of your total funds. Consider saving or investing the surplus."
        elif 30 <= spending_percentage <= 70:
            advice = "You're spending a moderate amount at {:.2f}%. It's a good balance, but consider saving more."
        else:
            advice = "Your spending is high at {:.2f}%. Try to cut back on unnecessary expenses to improve your budget."

        #Format the calulations
        advice = advice.format(spending_percentage)
    
        # Display the advice in a messagebox
        tk.messagebox.showinfo("Financial Advice", advice)

    #Get the remaining balance by name in the database
    def get_totals_by_name(self):
        conn = sqlite3.connect('personal_finance.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, date, SUM(balance + earnings - expenses) AS total_remaining_budget
            FROM finances
            GROUP BY name, date
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    #Allows the remainin budget information to be displayed by name and date (month + year)
    def show_remain_budget(self):
        data = self.get_totals_by_name()
        message = "Total Remaining Budget by Name:\n"
        for name, date, total in data:
            message += f"{name} {date}: {total:.2f}\n"
        messagebox.showinfo("Total Remaining Budget", message)
        
    #Getting the necessary inforamtion from the database to be displayed on the graph
    def get_graph_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, date, balance, earnings, expenses FROM finances ORDER BY date')
        records = cursor.fetchall()
        return records
    
    #Creating the bar graph when prompted by clicking the button
    def create_graph(self, data):
        data.sort(key=lambda x: (x[0], x[1]))  # x[0] is name, x[1] is date
    
        # Group data by name
        for name, group in groupby(data, lambda x: x[0]):
            grouped_data = list(group)
            dates = [item[1] for item in grouped_data]  # Get dates
            remaining_balances = [(item[2] + item[3] - item[4]) for item in grouped_data]  # Calculate remaining balances
        
            plt.figure(figsize=(10, 5))
            plt.bar(dates, remaining_balances)
            plt.title(f'Remaining Balance Across Different Dates for {name}')
            plt.xlabel('Date')
            plt.ylabel('Remaining Balance')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            plt.show(block = False)
        input("Press Enter to close all graphs.")
        plt.close('all')
    
    def plot_data(self):
        data = self.get_graph_data()
        plt = self.create_graph(data)
        window = Toplevel(self.master)
        window.title("Graph of Balance Over Time")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        window.mainloop()
       
    #Defines the layout of the application. Utilized grid to map out all the labels, buttons, and entry boxes
    def layout(self):
        self.heading_label.grid(row = 0, column= 1)
        
        self.nametitle_label.grid(row=1, column=0, pady=10, stick = 'e')
        self.name_entry.grid(row=1, column=1, pady=10)
        self.submit_name_button.grid(row=1, column=2, pady=10)
        self.submit_name_label.grid(row=1, column=3, pady=10)

        self.datetitle_label.grid(row=2, column=0, pady=5, stick = 'e')
        self.month_selector.grid(row=2, column=1, padx=5, pady=5)
        self.year_entry.grid(row=3, column=1, padx=5)
        self.submit_date_button.grid(row=2, column=2 )
        self.selected_date_label.grid(row=2, column = 3)

        self.balancetitle_label.grid(row=4, column=0, pady=10, sticky='e')
        self.balance_entry.grid(row = 4, column= 1, padx=5, pady=10 )
        self.submit_balance_button.grid(row=4, column=2, padx=5)
        self.submit_balance_label.grid(row=4, column=3)

        self.earntitle_label.grid(row=5, column=0, pady=10, sticky='e')
        self.earn_entry.grid(row=5, column=1, padx =5, pady=10)
        self.sumbit_earnings_button.grid(row=5, column=2, padx=5)
        self.submit_earnings_label.grid(row=5, column=3)

        self.expetitle_label.grid(row=6, column=0, pady=10, sticky='e')
        self.expe_entry.grid(row=6, column=1, padx=5, pady=10)
        self.submit_expenses_button.grid(row=6, column=2, padx=5)
        self.submit_expenses_label.grid(row=6, column=3)

        self.save_button.grid(row=7, column=1, padx=5, pady=10)
        self.view_button.grid(row=8, column=0, padx=5, pady=10)
        self.delete_all_button.grid(row=7, column=0, padx=5, pady=10)

        self.finacial_advice_button.grid(row=8, column=2, padx=5, pady=5)
        self.remain_budget_button.grid(row=7, column=2, padx=5, pady=5)
        
        self.plot_button.grid(row=8, column=1, padx=5, pady=5)
    
def main():
    root = tk.Tk()
    root.configure()
    app = PersonalFinanceApp(root)
    app.layout()
    root.mainloop()

if __name__ == "__main__":
    main()