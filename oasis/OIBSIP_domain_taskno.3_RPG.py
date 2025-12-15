import random
import string
import tkinter as tk
from tkinter import messagebox

# ---------------- PASSWORD GENERATION LOGIC ----------------
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 6:
            messagebox.showerror("Error", "Password length must be at least 6")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return

    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()

    if not (use_letters or use_numbers or use_symbols):
        messagebox.showerror("Error", "Select at least one character type")
        return

    exclude_chars = exclude_entry.get()

    letters = string.ascii_letters if use_letters else ""
    numbers = string.digits if use_numbers else ""
    symbols = string.punctuation if use_symbols else ""

    all_chars = letters + numbers + symbols

    # Remove excluded characters
    for char in exclude_chars:
        all_chars = all_chars.replace(char, "")

    if not all_chars:
        messagebox.showerror("Error", "No characters left after exclusion")
        return

    password = []

    # Security rules
    if use_letters:
        password.append(random.choice(string.ascii_lowercase))
        password.append(random.choice(string.ascii_uppercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))

    while len(password) < length:
        password.append(random.choice(all_chars))

    random.shuffle(password)
    final_password = "".join(password[:length])

    result_entry.delete(0, tk.END)
    result_entry.insert(0, final_password)

# ---------------- COPY TO CLIPBOARD ----------------
def copy_to_clipboard():
    password = result_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")

# ---------------- GUI DESIGN ----------------
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x450")
root.resizable(False, False)

tk.Label(root, text="🔐 Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

# Length
tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()
length_entry.insert(0, "12")

# Character Options
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=letters_var).pack()
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).pack()
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack()

# Exclude Characters
tk.Label(root, text="Exclude Characters (optional):").pack(pady=5)
exclude_entry = tk.Entry(root)
exclude_entry.pack()

# Generate Button
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=15)

# Result
tk.Label(root, text="Generated Password:").pack()
result_entry = tk.Entry(root, width=35, font=("Arial", 10))
result_entry.pack(pady=5)

# Copy Button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=10)

# Footer
tk.Label(root, text="Secure • Random • Customizable", font=("Arial", 9)).pack(side="bottom", pady=10)

root.mainloop()
