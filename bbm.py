import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk

class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank")

        # Create database connection
        self.conn = sqlite3.connect('blood_bank.db')
        self.c = self.conn.cursor()

        # Create tables if not exist
        self.create_tables()

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        # Title label
        self.title_label = tk.Label(self.main_frame, text="Blood Bank", font=("Helvetica", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Donate button
        self.donate_button = tk.Button(self.main_frame, text="Donate", command=self.donate, bg="lightblue")
        self.donate_button.grid(row=1, column=0, padx=5)

        # Receive button
        self.receive_button = tk.Button(self.main_frame, text="Receive", command=self.receive, bg="lightgreen")
        self.receive_button.grid(row=1, column=1, padx=5)

        # Blood group table
        self.blood_group_table = ttk.Treeview(self.main_frame, columns=('Can Donate To',))
        self.blood_group_table.heading('#0', text='Blood Group')
        self.blood_group_table.heading('#1', text='Can Donate To')
        self.blood_group_table.grid(row=2, column=0, columnspan=2, pady=10)

        # Populate blood group table
        self.populate_blood_group_table()

        # Transactions button
        self.transactions_button = tk.Button(self.main_frame, text="Transactions", command=self.show_transactions, bg="orange")
        self.transactions_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Receive window
        self.receive_window = None

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS donors (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            blood_group TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            gender TEXT NOT NULL
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            blood_group TEXT,
                            type TEXT NOT NULL
                        )''')

        self.conn.commit()


    def populate_blood_group_table(self):
        # Data for blood group table
        blood_groups = {
            'A+': ['A+', 'AB+'],
            'A-': ['A+', 'A-', 'AB+', 'AB-'],
            'B+': ['B+', 'AB+'],
            'B-': ['B+', 'B-', 'AB+', 'AB-'],
            'AB+': ['AB+'],
            'AB-': ['AB+', 'AB-'],
            'O+': ['A+', 'B+', 'AB+', 'O+'],
            'O-': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        }

        for blood_group, can_donate_to in blood_groups.items():
            self.blood_group_table.insert('', 'end', text=blood_group, values=(", ".join(can_donate_to)))

    def donate(self):
        # Create donate window
        donate_window = tk.Toplevel(self.root)
        donate_window.title("Donate")

        # Create form fields
        tk.Label(donate_window, text="Name:").grid(row=0, column=0)
        tk.Label(donate_window, text="Age:").grid(row=1, column=0)
        tk.Label(donate_window, text="Blood Group:").grid(row=2, column=0)
        tk.Label(donate_window, text="Phone:").grid(row=3, column=0)
        tk.Label(donate_window, text="Gender:").grid(row=4, column=0)

        name_entry = tk.Entry(donate_window)
        name_entry.grid(row=0, column=1)
        age_entry = tk.Entry(donate_window)
        age_entry.grid(row=1, column=1)
        blood_group_entry = tk.Entry(donate_window)
        blood_group_entry.grid(row=2, column=1)
        phone_entry = tk.Entry(donate_window)
        phone_entry.grid(row=3, column=1)
        gender_entry = tk.Entry(donate_window)
        gender_entry.grid(row=4, column=1)

        # Submit button
        submit_button = tk.Button(donate_window, text="Submit", command=lambda: self.save_donation(
            name_entry.get(), age_entry.get(), blood_group_entry.get(), phone_entry.get(), gender_entry.get()))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_donation(self, name, age, blood_group, phone, gender):
        # Save donor data to the database
        self.c.execute('''INSERT INTO donors (name, age, blood_group, phone, gender) 
                        VALUES (?, ?, ?, ?, ?)''', (name, age, blood_group, phone, gender))
        self.conn.commit()

        # Save donation transaction to the database
        self.c.execute('''INSERT INTO transactions (name, blood_group, type) VALUES (?, ?, ?)''', 
                        (name, blood_group, 'donate'))
        self.conn.commit()
        messagebox.showinfo("Success", "Donation saved successfully.")

    def receive(self):
        # Create receive window
        self.receive_window = tk.Toplevel(self.root)
        self.receive_window.title("Receive")

        # Create form fields
        tk.Label(self.receive_window, text="Name:").grid(row=0, column=0)
        tk.Label(self.receive_window, text="Age:").grid(row=1, column=0)
        tk.Label(self.receive_window, text="Blood Group:").grid(row=2, column=0)
        tk.Label(self.receive_window, text="Phone:").grid(row=3, column=0)
        tk.Label(self.receive_window, text="Gender:").grid(row=4, column=0)

        name_entry = tk.Entry(self.receive_window)
        name_entry.grid(row=0, column=1)
        age_entry = tk.Entry(self.receive_window)
        age_entry.grid(row=1, column=1)
        blood_group_entry = tk.Entry(self.receive_window)
        blood_group_entry.grid(row=2, column=1)
        phone_entry = tk.Entry(self.receive_window)
        phone_entry.grid(row=3, column=1)
        gender_entry = tk.Entry(self.receive_window)
        gender_entry.grid(row=4, column=1)

        # Submit button
        submit_button = tk.Button(self.receive_window, text="Submit", command=lambda: self.check_and_save_receive(
            name_entry.get(), age_entry.get(), blood_group_entry.get(), phone_entry.get(), gender_entry.get()))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def check_and_save_receive(self, name, age, blood_group, phone, gender):
        # Check if the requested blood group is available for reception
        self.c.execute('''SELECT COUNT(*) FROM transactions WHERE blood_group = ? AND type = ?''',
                       (blood_group, 'donate'))
        donations_count = self.c.fetchone()[0]

        self.c.execute('''SELECT COUNT(*) FROM transactions WHERE blood_group = ? AND type = ?''',
                       (blood_group, 'receive'))
        receive_count = self.c.fetchone()[0]

        if receive_count < donations_count:
            # Save receiver data to the database
            self.c.execute('''INSERT INTO transactions (name, blood_group, type) VALUES (?, ?, ?)''',
                            (name, blood_group, 'receive'))
            self.conn.commit()
            messagebox.showinfo("Success", "Reception saved successfully.")
            # Close receive window after submission
            self.receive_window.destroy()
        else:
            messagebox.showerror("Error", "Requested blood group is not available for reception.")
            # Close receive window after error message
            self.receive_window.destroy()

    def show_transactions(self):
        # Show transactions window
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transactions")

        # Fetch transactions from the database
        self.c.execute('''SELECT * FROM transactions''')
        transactions = self.c.fetchall()

        # Display transactions
        for i, transaction in enumerate(transactions):
            tk.Label(transactions_window, text=f"Transaction {i+1}:").grid(row=i, column=0, sticky="w")
            tk.Label(transactions_window, text=f"Name: {transaction[1]}").grid(row=i, column=1, sticky="w")
            tk.Label(transactions_window, text=f"Blood Group: {transaction[2]}").grid(row=i, column=2, sticky="w")
            tk.Label(transactions_window, text=f"Type: {transaction[3]}").grid(row=i, column=3, sticky="w")

    def __del__(self):
        # Close database connection when the app is closed
        self.conn.close()

# Create Tkinter application
root = tk.Tk()
app = BloodBankApp(root)
root.mainloop()
