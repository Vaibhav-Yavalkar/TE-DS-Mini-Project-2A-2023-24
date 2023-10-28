import re
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
import pymysql

window = Tk()  # instantiate an instance of a window
window.geometry("1000x650")
window.title("Trendy Threads- Sign In")

logo = PhotoImage(file='ttlogo.png')
window.config(background="#E7C6FF")

window.geometry("1000x650")
img = ImageTk.PhotoImage(Image.open("SignInPage.png"))
label = Label(window, image=img)
label.pack()
label.place(x=0, y=0)


db = pymysql.connect(
    host="localhost",
    user="root",
    password="aeioU#1904@",
    database="trendy"
)

# Create cursor object
cursor = db.cursor()

def clear():
    username_entry.delete(0, END)
    emailid_entry.delete(0, END)
    password_entry.delete(0, END)


def validate_form():
    # Perform account creation logic here
    # Show a message box to indicate that the account was created successfully
    username = username_entry.get().strip()
    emailid = emailid_entry.get().strip()
    password = password_entry.get().strip()

    # Check if all fields are filled
    if not username or not emailid or not password:
        messagebox.showerror("Error", "Please fill all the fields")
        return

    # Check if the username is valid
    if not username.isalnum():
        messagebox.showerror("Error", "Invalid username")
        return

    # Check if the email is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", emailid):
        messagebox.showerror("Error", "Invalid email")
        return

    # Perform account creation logic here
    # Show a message box to indicate that the account was created successfully
    messagebox.showinfo("Success", "Signed in Successfully")
    window.destroy()
    #subprocess.Popen(["python", "Selfie.py"])

def connect_database():
    if not validate_form():
        return
    # Get user input from entry fields
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if username already exists in database
    cursor.execute("SELECT * FROM sign_in WHERE username=%s", (username,))
    user = cursor.fetchone()
    if user:
        messagebox.showerror("Error", "Username already exists")
    else:
        # Define the SQL INSERT query
        sql_insert = "INSERT INTO sign_in (username, email, password) VALUES (%s, %s, %s)"

        # Execute the INSERT query
        try:
            cursor.execute(sql_insert, (username, email, password))
            db.commit()
            messagebox.showinfo("Success", "Signed in Successfully")
            import main
            clear()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", "Database Error: " + str(e))



def on_button_click():
    # Close the current file
    window.destroy()
    # Open the new file
    subprocess.Popen(["python", "Landing page.py"])


button = Button(window,
                   text=" ← ",
               command=on_button_click,
               font=("Montserrat", 15),
               fg="#E7C6FF",
               bg="#F72585",
               activeforeground="#E7C6FF",
               activebackground="#7209B7",
           state=ACTIVE)
button.pack()
button.place(x=950, y=10)

username_entry = Entry()
username_entry.config(font=('Montserrat Light', 10))  # change font
username_entry.config(bg='white')  # background
username_entry.config(fg='#7209B7')  # foreground
username_entry.config(width=10)  # width displayed in characters
username_entry.pack()
username_entry.place(x=691, y=266)

# for Email ID
emailid_entry = Entry()
emailid_entry.config(font=('Montserrat Light', 10))  # change font
emailid_entry.config(bg='white')  # background
emailid_entry.config(fg='#7209B7')  # foreground
emailid_entry.config(width=10)  # width displayed in characters

emailid_entry.pack()
emailid_entry.place(x=691, y=321)

# for password
password_entry = Entry()
password_entry.config(font=('Montserrat Light', 10))  # change font
password_entry.config(bg='white')  # background
password_entry.config(fg='#7209B7')  # foreground
password_entry.config(width=10)  # width displayed in characters
password_entry.config(show='*')  # replace characters shown with x character
password_entry.pack()
password_entry.place(x=691, y=383)

button = Button(window,
                text="LOGIN",
                command=connect_database,
                font=("Montserrat", 13),
                fg="#E7C6FF",
                bg="#F72585",
                activeforeground="#E7C6FF",
                activebackground="#7209B7",
                state=ACTIVE)
button.pack()
button.place(x=760, y=470)



window.mainloop()  # place window on computer screen, lister for events