#Create a Scentific Calculator in using python 
import tkinter as tk
from tkinter import messagebox
import math
import cmath

# Function to set the operation and clear entry for input
def set_operation(operation):
    global selected_operation
    selected_operation = operation
    entry.delete(0, tk.END)
    entry.insert(0, f"{operation}(")
    entry.config(state=tk.NORMAL)

# Function to evaluate the selected operation
def evaluate_operation():
    global selected_operation
    try:
        expression = entry.get()
        if selected_operation:
            value = expression.replace(f"{selected_operation}(", "").rstrip(")")
            
            # Check if value is complex or float
            if "j" in value:
                value = complex(value)
            else:
                value = float(value)

            if selected_operation == "sqrt":
                result = cmath.sqrt(value)
            elif selected_operation == "log":
                result = cmath.log10(value)
            elif selected_operation == "ln":
                result = cmath.log(value)
            elif selected_operation == "sin":
                result = cmath.sin(math.radians(value.real) if degree_mode.get() else value.real)
            elif selected_operation == "cos":
                result = cmath.cos(math.radians(value.real) if degree_mode.get() else value.real)
            elif selected_operation == "tan":
                result = cmath.tan(math.radians(value.real) if degree_mode.get() else value.real)
            elif selected_operation == "deg":
                result = math.degrees(value.real)
            elif selected_operation == "rad":
                result = math.radians(value.real)
            elif selected_operation == "square":
                result = value ** 2
            elif selected_operation == "cube_root":
                result = value ** (1/3)  # Cube root
            elif selected_operation == "root":
                # Handle input like root(x, n)
                if "," in value:
                    parts = value.split(',')
                    if len(parts) == 2:
                        x = float(parts[0])
                        n = int(parts[1])
                        result = x ** (1/n)
                    else:
                        raise ValueError("Invalid root input format")
                else:
                    raise ValueError("Invalid root input format")
                
            # Check if the result has no imaginary part, if so, return as real number
            if isinstance(result, complex) and result.imag == 0:
                result = result.real

            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
            selected_operation = None
        else:
            messagebox.showerror("Error", "No operation selected")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Input for Operation: {str(e)}")

# Function to clear the entry field
def clear_entry():
    global selected_operation
    selected_operation = None
    entry.delete(0, tk.END)

# Function to append a character to the entry field
def append_to_entry(character):
    entry.insert(tk.END, character)

# Function to toggle between Degree and Radian mode
def toggle_mode():
    if degree_mode.get():
        mode_label.config(text="Degree Mode")
    else:
        mode_label.config(text="Radian Mode")

# Create the main window
root = tk.Tk()
root.title("Advanced Scientific Calculator")
root.geometry("480x800")
root.configure(bg="#121212")  # Dark theme

# Create an entry widget for user input
entry = tk.Entry(root, font=("Courier", 24, "bold"), borderwidth=5, relief=tk.RIDGE, bg="#1f1f1f", fg="#ffffff", justify="right")
entry.grid(row=0, column=0, columnspan=5, padx=15, pady=20, sticky="nsew")

# Label for Degree/Radian Mode
mode_label = tk.Label(root, text="Degree Mode", font=("Courier", 16, "bold"), bg="#121212", fg="#ffffff")
mode_label.grid(row=1, column=0, columnspan=5, pady=10)

# Create the degree_mode variable after the root window has been initialized
degree_mode = tk.BooleanVar(value=True)  # Default mode: Degree

# Radio buttons to switch between Degree and Radian mode
degree_rb = tk.Radiobutton(root, text="Degree", font=("Courier", 16), bg="#121212", fg="#ffffff", variable=degree_mode, value=True, command=toggle_mode)
degree_rb.grid(row=2, column=0, pady=5, padx=20, sticky="nsew")

radian_rb = tk.Radiobutton(root, text="Radian", font=("Courier", 16), bg="#121212", fg="#ffffff", variable=degree_mode, value=False, command=toggle_mode)
radian_rb.grid(row=2, column=1, pady=5, padx=20, sticky="nsew")

# Button specifications
buttons = [
    ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("sqrt", 3, 4),
    ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3), ("log", 4, 4),
    ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3), ("ln", 5, 4),
    ("0", 6, 0), (".", 6, 1), ("=", 6, 2), ("+", 6, 3), ("sin", 6, 4),
    ("cos", 7, 3), ("tan", 7, 4), ("deg", 7, 0), ("rad", 7, 1),
    ("²", 7, 2), ("³√", 8, 0), ("root", 8, 1)
]

# Add buttons to the grid
for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(root, text=text, font=("Courier", 18, "bold"), bg="#4caf50", fg="white", activebackground="#66bb6a", command=evaluate_operation)
    elif text in ["sqrt", "log", "ln", "sin", "cos", "tan", "deg", "rad", "square", "cube_root", "root"]:
        button = tk.Button(root, text=text, font=("Courier", 16, "bold"), bg="#673ab7", fg="white", activebackground="#9575cd", command=lambda t=text: set_operation(t))
    else:
        button = tk.Button(root, text=text, font=("Courier", 18, "bold"), bg="#eceff1", fg="#37474f", activebackground="#cfd8dc", command=lambda t=text: append_to_entry(t))
    button.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

# Add a clear button
clear_button = tk.Button(root, text="C", font=("Courier", 18, "bold"), bg="#e53935", fg="white", activebackground="#ef5350", command=clear_entry)
clear_button.grid(row=8, column=2, columnspan=3, padx=15, pady=20, sticky="nsew")

# Configure row and column weights for responsiveness
for i in range(9):  # Adjusted for 9 rows
    root.grid_rowconfigure(i, weight=1, uniform="equal")
for j in range(5):  # Adjusted for 5 columns
    root.grid_columnconfigure(j, weight=1, uniform="equal")

# Add hover effects for buttons
def hover_effect(widget, color_on_hover, color_on_leave):
    widget.bind("<Enter>", lambda e: widget.configure(bg=color_on_hover))
    widget.bind("<Leave>", lambda e: widget.configure(bg=color_on_leave))

for widget in root.winfo_children():
    if isinstance(widget, tk.Button):
        if widget["bg"] == "#4caf50":
            hover_effect(widget, "#66bb6a", "#4caf50")
        elif widget["bg"] == "#e53935":
            hover_effect(widget, "#ef5350", "#e53935")
        elif widget["bg"] == "#673ab7":
            hover_effect(widget, "#9575cd", "#673ab7")
        elif widget["bg"] == "#eceff1":
            hover_effect(widget, "#cfd8dc", "#eceff1")

# Start the main event loop
root.mainloop()
