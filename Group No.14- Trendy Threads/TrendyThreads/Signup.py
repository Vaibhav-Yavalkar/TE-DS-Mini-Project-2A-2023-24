import re
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess
import pymysql

window = Tk()  # instantiate an instance of a window
window.geometry("1000x650")
window.title("TrendyThreads- Sign Up")

logo = PhotoImage(file='ttlogo.png')
window.config(background="#E7C6FF")

img = ImageTk.PhotoImage(Image.open("SignupPage.png"))
label = Label(window, image=img)
label.pack()
label.place(x=0, y=0)

firstname_entry = Entry(window,
                        font=("Cambria", 10)
                        )
firstname_entry.pack(side=LEFT)
firstname_entry.place(x=595, y=240)

lastname_entry = Entry(window,
                       font=("Cambria", 10)
                       )
lastname_entry.pack(side=LEFT)
lastname_entry.place(x=780, y=240)

username_entry = Entry(window,
                       font=("Montserrat", 10)
                       )
username_entry.pack(side=LEFT)
username_entry.place(x=730, y=300)

email_entry = Entry(window,
                    font=("Montserrat", 10)
                    )
email_entry.pack(side=LEFT)
email_entry.place(x=730, y=355)

password_entry = Entry(window,
                       font=("Cambria", 10),
                       show='*')
password_entry.pack(side=LEFT)
password_entry.place(x=599, y=440)

cpassword_entry = Entry(window,
                               font=("Cambria", 10),
                               show='*')
cpassword_entry.pack(side=LEFT)
cpassword_entry.place(x=780, y=440)


db = pymysql.connect(
    host="localhost",
    user="root",
    password="aeioU#1904@",
    database="trendy"
)

# Create cursor object
cursor = db.cursor()

def validate_form():
    # Get user input from entry fields
    firstname = firstname_entry.get().strip()
    lastname = lastname_entry.get().strip()
    username = username_entry.get().strip()
    emailid = email_entry.get().strip()
    password = password_entry.get().strip()
    cpassword = cpassword_entry.get().strip()

    if not firstname or not lastname or not username or not emailid or not password or not cpassword:
        messagebox.showerror("Error", "Please fill all the fields")
        return

        # Validate first name and last name
    if not re.match(r"^[A-Za-z ]+$", firstname) or not re.match(r"^[A-Za-z ]+$", lastname):
        messagebox.showerror("Error", "Invalid first or last name")
        return

        # Validate username (allow only alphanumeric characters and underscores)
    if not re.match(r"^\w+$", username):
        messagebox.showerror("Error", "Invalid username")
        return

        # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", emailid):
        messagebox.showerror("Error", "Invalid email")
        return

        # Check if password and confirm password match
    if password != cpassword:
        messagebox.showerror("Error", "Passwords do not match")
    return True

def clear():
    # Function to clear entry fields
    firstname_entry.delete(0, END)
    lastname_entry.delete(0, END)
    username_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)
    cpassword_entry.delete(0, END)


def connect_database():
    if not validate_form():
        return
    # Get user input from entry fields
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    cpassword = cpassword_entry.get()

    # Check if username already exists in database
    cursor.execute("SELECT * FROM sign_up WHERE username=%s", (username,))
    user = cursor.fetchone()
    if user:
        messagebox.showerror("Error", "Username already exists")
    else:
        # Define the SQL INSERT query
        sql_insert = "INSERT INTO sign_up (firstname, lastname, username, email, password, cpassword) VALUES (%s, %s, %s, %s, %s, %s)"

        # Execute the INSERT query
        try:
            cursor.execute(sql_insert, (firstname, lastname, username, email, password, cpassword))
            db.commit()
            messagebox.showinfo("Success", "Account created Successfully")
            import main
            clear()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", "Database Error: " + str(e))

button = Button(window,
                text="Create Account",
                command=connect_database,
                font=("Montserrat Light", 12),
                fg="#e5b3fe",
                bg="#7b2cbf",
                activeforeground="#e5b3fe",
                activebackground="#7209B7",
                state=ACTIVE)
button.pack()
button.place(x=750, y=510)

#def on_button_click():
    # Close the current file
 #  window.destroy()
    # Open the new file
  #subprocess.Popen(["python", "Selfie.py"])


#button = Button(window,
 #               text=" ← ",
  #              command=on_button_click,
   #             font=("Montserrat", 15),
    #            fg="#E7C6FF",
     #           bg="#F72585",
      #          activeforeground="#E7C6FF",
       #         activebackground="#7209B7",
        #        state=ACTIVE)
#button.pack()
#button.place(x=950, y=10)

window.mainloop()
