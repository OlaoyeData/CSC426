import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        self.expression = ""       
        self.last_result = None    
        self.just_calculated = False  

        self.display_var = tk.StringVar()
        self.display_var.set("0")

        display_frame = tk.Frame(root, bg="#2c3e50")
        display_frame.pack(pady=20, padx=10, fill="both")

        self.display_entry = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            justify="right",
            bd=10,
            relief="ridge",
            bg="#ecf0f1",
            fg="#2c3e50",
            state="readonly",
            readonlybackground="#ecf0f1"
        )
        self.display_entry.pack(fill="both", expand=True, ipady=10)

        
        button_frame = tk.Frame(root, bg="#2c3e50")
        button_frame.pack(pady=10, padx=10, fill="both", expand=True)

        
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3), ("\\", 0, 4),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3), ("^", 1, 4),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3), ("%", 2, 4),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3), ("C", 3, 4)
        ]

        
        btn_bg = "#34495e"
        btn_fg = "white"
        operator_bg = "#e67e22"
        special_bg = "#e74c3c"
        equal_bg = "#27ae60"

        for (text, row, col) in buttons:
            if text in ("="):
                bg_color = equal_bg
            elif text in ("C",):
                bg_color = special_bg
            elif text in ("+", "-", "*", "/", "\\", "^", "%"):
                bg_color = operator_bg
            else:
                bg_color = btn_bg

            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 18, "bold"),
                bg=bg_color,
                fg=btn_fg,
                activebackground="#2c3e50",
                activeforeground="white",
                bd=0,
                padx=20,
                pady=15,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        
        for i in range(4):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        """Handle button clicks"""
        if char == "C":
            self.clear()
        elif char == "=":
            self.evaluate()
        else:
            if self.just_calculated:
                if char.isdigit() or char == ".":
                    self.expression = char
                    self.just_calculated = False
                elif char in "+-*/\\^%":
                    if self.last_result is not None:
                        self.expression = str(self.last_result) + char
                        self.just_calculated = False
                self.update_display()
            else:
                current = self.expression

                if current == "0" and char.isdigit():
                    self.expression = char
                else:
                    operators = "+-*/\\^%"
                    if current and current[-1] in operators and char in operators:
                        self.expression = current[:-1] + char
                    else:
                        self.expression += char

                self.update_display()

    def clear(self):
        """Reset calculator"""
        self.expression = ""
        self.last_result = None
        self.just_calculated = False
        self.display_var.set("0")

    def evaluate(self):
        """Evaluate the current expression"""
        if not self.expression.strip():
            return

        expr = self.expression
        expr = expr.replace("^", "**")
        expr = expr.replace("\\", "//")

        try:
            result = eval(expr, {"__builtins__": None}, {})

            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 10)

            self.last_result = result
            result_str = str(result)

            self.display_var.set(result_str)
            self.expression = result_str
            self.just_calculated = True

        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero is not allowed")
            self.clear()
        except Exception:
            messagebox.showerror("Syntax Error", "Invalid expression")
            self.clear()

    def update_display(self):
        """Update the display with current expression"""
        if not self.expression:
            self.display_var.set("0")
        else:
            self.display_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()