import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import os

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing App")

        self.title_label = tk.Label(self.master, text="Draw waves in the space given below")
        self.title_label.pack()

        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<ButtonPress-3>", self.start_erase)
        self.canvas.bind("<B3-Motion>", self.erase)
        self.canvas.bind("<ButtonRelease-3>", self.end_erase)
        self.entry = tk.Entry(self.master)
        self.entry.pack(side=tk.TOP, fill=tk.X)
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.pack()
        
        self.draw_color = "blue"
        self.draw_size = 3
        self.erase_size = 10
        self.is_drawing = False
        self.is_erasing = False
        self.last_x, self.last_y = None, None
        self.lines = []

    def start_draw(self, event):
        self.is_drawing = True
        self.is_erasing = False
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.is_drawing:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.draw_size, fill=self.draw_color, capstyle=tk.ROUND, smooth=True)
            self.last_x, self.last_y = event.x, event.y
            self.lines.append((self.last_x, self.last_y))

    def end_draw(self, event):
        self.is_drawing = False
        self.last_x, self.last_y = None, None

    def start_erase(self, event):
        self.is_erasing = True
        self.is_drawing = False
        self.last_x, self.last_y = event.x, event.y

    def erase(self, event):
        if self.is_erasing:
            self.canvas.create_oval(event.x - self.erase_size, event.y - self.erase_size,
                                    event.x + self.erase_size, event.y + self.erase_size,
                                    fill="white", outline="white")
            self.last_x, self.last_y = event.x, event.y

    def end_erase(self, event):
        self.is_erasing = False
        self.last_x, self.last_y = None, None

    def submit(self):
        filename = "sample 2.png"
        save_path = "D:/college/sem 8/project/"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        full_path = os.path.join(save_path, filename)
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab().crop((x, y, x1, y1))
        drawing_area = (0, self.entry.winfo_height(), self.canvas.winfo_width(), self.canvas.winfo_height())
        drawing_image = image.crop(drawing_area)
        drawing_image.save(full_path)
        print(f"Saved drawing as {filename}")
        #print("Submitted drawing with lines:", self.lines)


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
