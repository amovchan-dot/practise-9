import math
import tkinter as tk
from tkinter import messagebox


class FunctionPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Побудова графіка функції — Варіант 13")
        self.root.geometry("680x520")
        self.root.resizable(False, False)


        ctrl_frame = tk.Frame(self.root, pady=8)
        ctrl_frame.pack(fill="x", padx=15)

        tk.Label(ctrl_frame, text="Відрізок [a; b]:", font=("Arial", 9, "bold")).pack(side="left")

        tk.Label(ctrl_frame, text="a =").pack(side="left", padx=(10, 2))
        self.entry_a = tk.Entry(ctrl_frame, width=7)
        self.entry_a.insert(0, "0.01")
        self.entry_a.pack(side="left")

        tk.Label(ctrl_frame, text="b =").pack(side="left", padx=(10, 2))
        self.entry_b = tk.Entry(ctrl_frame, width=7)
        self.entry_b.insert(0, "5.0")
        self.entry_b.pack(side="left")

        tk.Button(
            ctrl_frame, text="Побудувати графік", bg="#d9ead3", font=("Arial", 9, "bold"),
            command=self.draw_plot
        ).pack(side="left", padx=15)

        tk.Button(
            ctrl_frame, text="Вихід", bg="#f4cccc",
            command=self.root.quit
        ).pack(side="right")


        tk.Label(
            self.root,
            text="Функція: y = arccos((x - lg(x)) / (1 + cos(3x)) + 1)",
            font=("Arial", 10, "italic"), fg="#1c4587"
        ).pack()


        self.width = 640
        self.height = 420
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white", bd=2, relief="groove")
        self.canvas.pack(pady=8)

        self.draw_plot()

    def calculate_y(self, x):

        if x <= 0:
            return None
        denom = 1.0 + math.cos(3.0 * x)
        if abs(denom) < 1e-9:
            return None
        arg = ((x - math.log10(x)) / denom) + 1.0
        if -1.0 <= arg <= 1.0:
            return math.acos(arg)
        return None

    def draw_plot(self):
        try:
            a = float(self.entry_a.get().replace(",", "."))
            b = float(self.entry_b.get().replace(",", "."))
            if a >= b:
                raise ValueError("Межа 'a' має бути меншою за 'b'.")
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))
            return

        self.canvas.delete("all")
        margin = 45
        plot_w = self.width - 2 * margin
        plot_h = self.height - 2 * margin


        y_min, y_max = -0.2, math.pi + 0.2

        def to_screen(x, y):
            sx = margin + (x - a) / (b - a) * plot_w
            sy = self.height - margin - (y - y_min) / (y_max - y_min) * plot_h
            return sx, sy


        self.canvas.create_rectangle(margin, margin, self.width - margin, self.height - margin, outline="#cccccc")
        _, y0 = to_screen(a, 0)
        self.canvas.create_line(margin, y0, self.width - margin, y0, fill="black", arrow=tk.LAST)
        self.canvas.create_text(self.width - margin + 12, y0, text="X", font=("Arial", 9, "bold"))

        if a <= 0 <= b:
            x0, _ = to_screen(0, 0)
        else:
            x0 = margin
        self.canvas.create_line(x0, self.height - margin, x0, margin, fill="black", arrow=tk.LAST)
        self.canvas.create_text(x0, margin - 12, text="Y", font=("Arial", 9, "bold"))


        steps = 2000
        dx = (b - a) / steps
        prev_point = None
        has_points = False

        for i in range(steps + 1):
            x = a + i * dx
            y = self.calculate_y(x)
            if y is not None:
                has_points = True
                curr_point = to_screen(x, y)
                if prev_point is not None:
                    self.canvas.create_line(prev_point[0], prev_point[1], curr_point[0], curr_point[1], fill="#cc0000", width=2)
                else:
                    self.canvas.create_oval(curr_point[0]-2, curr_point[1]-2, curr_point[0]+2, curr_point[1]+2, fill="#cc0000", outline="#cc0000")
                prev_point = curr_point
            else:
                prev_point = None

        if not has_points:
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text="На заданому відрізку функція не має дійсних значень\n(вираз під arccos виходить за межі [-1; 1])",
                fill="#666666", font=("Arial", 10), justify="center"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionPlotterApp(root)
    root.mainloop()