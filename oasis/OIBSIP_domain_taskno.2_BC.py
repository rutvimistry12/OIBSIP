import tkinter as tk
from tkinter import messagebox
import datetime
import matplotlib.pyplot as plt

DATA_FILE = "bmi_data.txt"

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = weight / (height ** 2)
        category = bmi_category(bmi)

        result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")

        save_data(weight, height, bmi)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid positive numbers.")

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def save_data(weight, height, bmi):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(DATA_FILE, "a") as file:
        file.write(f"{date},{weight},{height},{bmi}\n")

def show_graph():
    dates = []
    bmis = []

    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                dates.append(data[0])
                bmis.append(float(data[3]))

        plt.figure()
        plt.plot(dates, bmis, marker='o')
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI Trend Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showinfo("No Data", "No BMI data found.")

# GUI Window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("350x300")

tk.Label(root, text="Weight (kg):").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (m):").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack()

tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)
tk.Button(root, text="Show BMI Graph", command=show_graph).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
