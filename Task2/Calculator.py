import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        # Remove fixed size to allow resizing
        # self.root.geometry("320x400")
        self.root.minsize(320, 400)
        self.root.resizable(True, True)

        self.expression = ""

        # Display frame
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            root,
            textvariable=self.display_var,
            font=("Helvetica Neue", 30, "bold"),
            bg="#1C1C1E",  # Dark display like Apple calculator
            fg="white",
            insertbackground="white",  # Cursor color
            bd=0,
            highlightthickness=2,
            highlightbackground="#3A3A3C",
            relief=tk.FLAT,
            justify='right'
        )
        self.display.pack(fill='both', ipadx=8, ipady=15, padx=10, pady=10, expand=True)

        # Buttons frame
        btns_frame = tk.Frame(root, bg="#2F2F2F")  # Light blue background for button frame
        btns_frame.pack(fill='both', expand=True)

        # Configure grid weights for responsiveness
        for i in range(5):
            btns_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btns_frame.columnconfigure(j, weight=1)

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('×', 3, 3),
            ('CL', 4, 0), ('0', 4, 1), ('=', 4, 2), ('÷', 4, 3),
        ]

        for (text, row, col) in buttons:
            canvas = tk.Canvas(btns_frame, width=100, height=100, bg=btns_frame['bg'], highlightthickness=0)
            if text == '=':
                fill_color = '#FFD700'  # Yellow
                text_color = 'black'
            elif text in {'+', '-', '÷', '×'}:
                fill_color = "#565656"  # Red
                text_color = 'white'
            elif text == 'CL':
                fill_color = "#DF5324"  # Green
                text_color = 'white'
            else:
                fill_color = "#000000"  # Purple
                text_color = 'white'

            canvas.create_oval(10, 10, 90, 90, fill=fill_color, outline="")
            canvas.create_text(50, 50, text=text, font=("Arial", 27), fill=text_color)
            canvas.grid(row=row, column=col, padx=8, pady=10, sticky='nsew')
            canvas.bind("<Button-1>", lambda e, t=text: self.on_button_click(t))

    def on_button_click(self, char):
        if char == 'CL':
            self.expression = ""
            self.display_var.set("")
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.display_var.set(result)
                self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot divide by zero")
                self.expression = ""
                self.display_var.set("")
            except Exception:
                messagebox.showerror("Error", "Invalid input")
                self.expression = ""
                self.display_var.set("")
        else:
            if char == '×':
                self.expression += '*'
            elif char == '÷':
                self.expression += '/'
            else:
                self.expression += str(char)
        self.display_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()