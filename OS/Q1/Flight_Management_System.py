import tkinter as tk

from tkinter import messagebox

class Flight:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Management System")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        mainTitle = tk.Label(self.root, text="SkyWays AirLine", bd=5, relief="groove", font=("Times New Roman", 40, "bold"), bg="#229799", fg="white")
        mainTitle.pack(side="top", fill="x")



root = tk.Tk()
obj = Flight(root)  # Changed from Hotel to Flight
root.mainloop()
