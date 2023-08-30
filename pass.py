import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string
from ttkthemes import ThemedStyle

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
def show_password():
	custom_style = ThemedStyle()
	custom_style.set_theme("arc")  # You can choose from other available themes
	custom_style.configure("TLabel",foreground="green", font=("Helvetica", 12, "bold"))
	custom_style.configure("TLabel.Message", background="white", foreground="white", font=("Helvetica", 10))
	application_name = app_entry.get()
	conn = sqlite3.connect('passwords.db')
	cursor = conn.cursor()
	cursor.execute("SELECT password FROM passwords WHERE application=?", (application_name,))
	password = cursor.fetchone()
	conn.close()
	messagebox.showinfo("Password ", f"Password found for \n'{application_name}'  is : {password[0]}")
def on_generate_and_store():
    application_name = app_entry.get()
    password_length = int(length_entry.get() or 12)
    generated_password = generate_password(password_length)

    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            application TEXT,
            password TEXT
        )
    ''')
    cursor.execute("SELECT password FROM passwords WHERE application=?", (application_name,))
    existing_password = cursor.fetchone()

    if existing_password:
        cursor.execute("UPDATE passwords SET password=? WHERE application=?", (generated_password, application_name))
        conn.commit()
        messagebox.showinfo("Success", f"Password for '{application_name}' Updated and stored in the database.")
    else:
    	cursor.execute('INSERT INTO passwords (application, password) VALUES (?, ?)', (application_name, generated_password))
    	conn.commit()
    	messagebox.showinfo("Success", f"Password for '{application_name}' generated and stored in the database.")
    

def on_add_or_update_manual_password():
    application_name = app_entry.get()
    manual_password = manual_password_entry.get()

    if not manual_password:
        messagebox.showwarning("Empty Password", "Please enter a password.")
        return

    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            application TEXT,
            password TEXT
        )
    ''')

    cursor.execute("SELECT password FROM passwords WHERE application=?", (application_name,))
    existing_password = cursor.fetchone()

    if existing_password:
        cursor.execute("UPDATE passwords SET password=? WHERE application=?", (manual_password, application_name))
        conn.commit()
        messagebox.showinfo("Success", f"Manually entered password for '{application_name}' updated in the database.")
    else:
        cursor.execute('INSERT INTO passwords (application, password) VALUES (?, ?)', (application_name, manual_password))
        conn.commit()
        messagebox.showinfo("Success", f"Manually entered password for '{application_name}' stored in the database.")

    conn.close()

# Create the tkinter application
app = tk.Tk()
app.title("Password Generator and Storage")

# Apply the "arc" theme to the application
style = ThemedStyle(app)
style.set_theme("arc")

# Rest of the GUI layout (same as before)

# Labels
app_label = tk.Label(app, text="Enter app/site name :")
app_label.grid(row=0, column=0, padx=5, pady=5)

length_label = tk.Label(app, text="Enter password length / 12 :")
length_label.grid(row=1, column=0, padx=5, pady=5)

manual_password_label = tk.Label(app, text="Enter Manual Password:")
manual_password_label.grid(row=2, column=0, padx=5, pady=5)

# Entry widgets
app_entry = tk.Entry(app)
app_entry.grid(row=0, column=1, padx=5, pady=5)

length_entry = tk.Entry(app)
length_entry.grid(row=1, column=1, padx=5, pady=5)

manual_password_entry = tk.Entry(app)
manual_password_entry.grid(row=2, column=1, padx=5, pady=5)

# Generate and store / Change password button
generate_button = tk.Button(app, text="Generate / Change Password",bg="white",fg="purple",font=("Helvetica", 10, "bold"), command=on_generate_and_store)
generate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Show password button
show_password_button = tk.Button(app, text="Show Password for given app",bg="white",fg="purple",font=("Helvetica", 10, "bold"), command=show_password)
show_password_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Add or Update manually entered password button
add_or_update_manual_password_button = tk.Button(app, text="Add / Update manual Password",bg="white",fg="purple",font=("Helvetica", 10, "bold"), command=on_add_or_update_manual_password)
add_or_update_manual_password_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

app.mainloop()

