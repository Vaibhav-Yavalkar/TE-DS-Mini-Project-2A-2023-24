from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import subprocess

root = tk.Tk()
root.geometry("1000x650")
root.title("TrendyThreads")

logo = PhotoImage(file='ttlogo.png')
root.config(background="#E7C6FF")

img = ImageTk.PhotoImage(Image.open("Landing.png"))
label = Label(root, image=img)
label.pack()
label.place(x=0, y=0)

def on_button_click():
    # Close the current file
    root.destroy()
    # Open the new file
    subprocess.Popen(["python", "Signup.py"])

button = Button(root,
                text="Get Started",
                command=on_button_click,
                font=("Jacques Francois", 20),
                fg="#E7C6FF",
                bg="#F72585",
                activeforeground="#7209B7",
                activebackground="#E7C6FF",
                state=ACTIVE)
button.pack()
button.place(x=620, y=340)

def on_about_click():
    # Close the current file
    root.destroy()
    # Open the new file
    subprocess.Popen(["python", "About.py"])

button1 = Button(root,
                 text="ABOUT",
                 command=on_about_click,
                 font=("Jacques Francois", 10),
                 fg="#3A0CA3",
                 bg="#E7C6FF",
                 activeforeground="#3A0CA3",
                 activebackground="#E7C6FF",
                 state=ACTIVE)
button1.pack()
button1.place(x=930, y=11)

def onbuttonclick():
    # Close the current file
    root.destroy()
    # Open the new file
    subprocess.Popen(["python","Contact us.py"])


button2 = Button(root,
                 text="CONTACT US",
                 command=onbuttonclick,
                 font=("Jacques Francois", 10),
                 fg="#3A0CA3",
                 bg="#E7C6FF",
                 activeforeground="#3A0CA3",
                 activebackground="#E7C6FF",
                 state=ACTIVE)
button2.pack()
button2.place(x=818, y=11)


def on_button_click():
    # Close the current file
    root.destroy()
    # Open the new file
    subprocess.Popen(["python", "Signin.py"])


button3 = Button(root,
                 text="SIGN IN",
                 command=on_button_click,
                 font=("Jacques Francois", 10),
                 fg="#3A0CA3",
                 bg="#E7C6FF",
                 activeforeground="#3A0CA3",
                 activebackground="#E7C6FF",
                 state=ACTIVE)
button3.pack()
button3.place(x=730, y=11)



root.mainloop()
