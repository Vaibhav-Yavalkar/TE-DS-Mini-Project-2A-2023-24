from tkinter import *
from PIL import ImageTk, Image
import subprocess

window = Tk()  # instantiate an instance of a window
window.geometry("1000x650")
window.title("Trendy Threads")

logo = PhotoImage(file='ttlogo.png')
window.config(background="#E7C6FF")

img = ImageTk.PhotoImage(Image.open("About.png"))
label = Label(window, image=img)
label.pack()
label.place(x=0, y=0)

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

window.mainloop()
