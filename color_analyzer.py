import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from color_utils import *

class ColorAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор цветов")
        self.root.geometry("800x600")
        
        style = ttk.Style()
        style.configure("Custom.TButton", padding=10, font=("Arial", 12))
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        self.img_label = ttk.Label(self.main_frame, text="Перетащите изображение\nили нажмите кнопку для выбора")
        self.img_label.pack(pady=20)
        
        self.select_btn = ttk.Button(self.main_frame, text="Выбрать изображение", 
                                   command=self.select_image, style="Custom.TButton")
        self.select_btn.pack(pady=10)
        
        self.preview_label = ttk.Label(self.main_frame)
        self.preview_label.pack(pady=10)
        
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill=X, pady=10)
        self.progress_label = ttk.Label(self.main_frame, text="")
        self.progress_label.pack()
        
        self.colors_frame = ttk.Frame(self.main_frame)
        self.colors_frame.pack(pady=10, fill=X)
        
        self.setup_drag_drop()

    def setup_drag_drop(self):
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_image)

    def drop_image(self, event):
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        self.process_image(file_path)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            self.process_image(file_path)

    def update_progress(self, current, total, message=""):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
        self.root.update_idletasks()

    def process_image(self, image_path):
        try:
            self.progress_var.set(0)
            self.progress_label.config(text="Загрузка изображения...")
            
            preview = Image.open(image_path)
            preview.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(preview)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
            
            self.update_progress(20, 100, "Обработка пикселей...")
            
            pil_image = Image.open(image_path)
            image = np.array(pil_image)
            pixels = image.reshape(-1, 3)
            total_pixels = len(pixels)
            
            self.update_progress(40, 100, "Подготовка отображения...")
            
            step = 1000
            colors = pixels[::step]
            
            for widget in self.colors_frame.winfo_children():
                widget.destroy()
            
            self.update_progress(60, 100, "Создание интерфейса...")
            
            canvas = Canvas(self.colors_frame)
            scrollbar = ttk.Scrollbar(self.colors_frame, orient="horizontal", command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)

            canvas.configure(xscrollcommand=scrollbar.set)
            
            scrollbar.pack(side="bottom", fill="x")
            canvas.pack(side="top", fill="both", expand=True)
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            ttk.Label(self.colors_frame, text=f"Всего пикселей: {total_pixels}, Показано цветов: {len(colors)}").pack(side="top", pady=5)
            
            self.update_progress(80, 100, "Отображение цветов...")
            
            batch_size = 100
            for i in range(0, len(colors), batch_size):
                batch = colors[i:i+batch_size]
                for color in batch:
                    frame = ttk.Frame(scrollable_frame)
                    frame.pack(side=LEFT, padx=5)
                    
                    r, g, b = color[0], color[1], color[2]
                    color_box = Canvas(frame, width=50, height=50, bg=rgb_to_hex(r, g, b))
                    color_box.pack()
                    
                    comp_r, comp_g, comp_b = get_complementary_color(r, g, b)
                    comp_color = Canvas(frame, width=25, height=25, bg=rgb_to_hex(comp_r, comp_g, comp_b))
                    comp_color.pack()
                    
                    rgb_text = f"RGB: {r}, {g}, {b}"
                    hsv = rgb_to_hsv(r, g, b)
                    hsv_text = f"HSV: {hsv[0]}, {hsv[1]}, {hsv[2]}"
                    name_text = f"Цвет: {get_color_name(r, g, b)}"
                    temp_text = f"Тип: {get_color_temperature(r, g, b)}"
                    
                    ttk.Label(frame, text=rgb_text).pack()
                    ttk.Label(frame, text=hsv_text).pack()
                    ttk.Label(frame, text=name_text).pack()
                    ttk.Label(frame, text=temp_text).pack()
                
                progress = 80 + (i / len(colors)) * 20
                self.update_progress(progress, 100, f"Отображение цветов... {i}/{len(colors)}")
                self.root.update_idletasks()
            
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            self.update_progress(100, 100, "Готово!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обработке изображения: {str(e)}")
            self.progress_label.config(text="Произошла ошибка!")

if __name__ == "__main__":
    from tkinterdnd2 import *
    root = TkinterDnD.Tk()
    app = ColorAnalyzer(root)
    root.mainloop() 