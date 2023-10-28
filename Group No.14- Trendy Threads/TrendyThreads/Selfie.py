from tkinter import *
from tkinter import ttk
import subprocess
from PIL import ImageTk, Image

def on_selfie_click():
    # Open the second GUI for webcam and skin tone analysis
    subprocess.Popen(["python", "Webcam.py"])

# Create the first Tkinter window
window = Tk()
window.geometry("1000x650")
window.title("Trendy Threads-Selfie")

img = ImageTk.PhotoImage(Image.open("Skinanalysis.png"))
label = Label(window, image=img)
label.pack()
label.place(x=0, y=0)


button_selfie = Button(window,
                      text="Take a Selfie",
                      command=on_selfie_click,
                      font=("Jacques Francois", 30))
button_selfie.pack()
button_selfie.place(x=90,y=453)

window.mainloop()
