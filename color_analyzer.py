import numpy as np
from sklearn.cluster import KMeans
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from color_utils import *
from constants import *
import threading

class ColorAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор цветов")
        self.root.geometry(WINDOW_SIZE)
        
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
        self.colors_frame.pack(pady=10, fill=BOTH, expand=True)
        
        self.canvas = Canvas(self.colors_frame)
        self.scrollbar_y = ttk.Scrollbar(self.colors_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.colors_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.load_more_btn = ttk.Button(self.main_frame, text="Загрузить еще цвета", 
                                      command=self.load_more_colors, style="Custom.TButton")
        self.load_more_btn.pack(pady=10)
        self.load_more_btn.pack_forget()
        
        self.current_color_index = 0
        self.all_colors = None
        self.setup_drag_drop()

    def setup_drag_drop(self):
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_image)

    def drop_image(self, event):
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"): file_path = file_path[1:-1]
        self.process_image(file_path)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path: self.process_image(file_path)

    def update_progress(self, current, total, message=""):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
        self.root.update_idletasks()

    def create_color_frame(self, color_data):
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(side=LEFT, padx=5, pady=5)
        
        color_box = Canvas(frame, width=COLOR_BOX_SIZE, height=COLOR_BOX_SIZE, bg=color_data['hex'])
        color_box.pack()
        
        comp_color = Canvas(frame, width=COMP_COLOR_BOX_SIZE, height=COMP_COLOR_BOX_SIZE, bg=color_data['comp_hex'])
        comp_color.pack()
        
        rgb_text = f"RGB: {color_data['rgb'][0]}, {color_data['rgb'][1]}, {color_data['rgb'][2]}"
        hsv_text = f"HSV: {color_data['hsv'][0]}, {color_data['hsv'][1]}, {color_data['hsv'][2]}"
        name_text = f"Цвет: {color_data['name']}"
        temp_text = f"Тип: {color_data['temp']}"
        
        ttk.Label(frame, text=rgb_text).pack()
        ttk.Label(frame, text=hsv_text).pack()
        ttk.Label(frame, text=name_text).pack()
        ttk.Label(frame, text=temp_text).pack()

    def load_more_colors(self):
        if self.all_colors is None or self.current_color_index >= len(self.all_colors):
            self.load_more_btn.pack_forget()
            return
            
        end_idx = min(self.current_color_index + MAX_COLORS, len(self.all_colors))
        colors_to_show = self.all_colors[self.current_color_index:end_idx]
        
        for color in colors_to_show:
            color_data = {
                'rgb': tuple(color),
                'hex': rgb_to_hex(*color),
                'comp': get_complementary_color(*color),
                'comp_hex': rgb_to_hex(*get_complementary_color(*color)),
                'hsv': rgb_to_hsv(*color),
                'name': get_color_name(*color),
                'temp': get_color_temperature(*color)
            }
            self.create_color_frame(color_data)
        
        self.current_color_index = end_idx
        if self.current_color_index >= len(self.all_colors):
            self.load_more_btn.pack_forget()
        
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def process_colors(self, pixels):
        kmeans = KMeans(n_clusters=min(len(pixels), 500), n_init=1)
        kmeans.fit(pixels)
        self.all_colors = kmeans.cluster_centers_.astype(int)
        self.current_color_index = 0
        
        self.load_more_colors()
        if self.current_color_index < len(self.all_colors):
            self.load_more_btn.pack(pady=10)
        
        self.update_progress(100, 100, "Готово!")

    def process_image(self, image_path):
        try:
            self.progress_var.set(0)
            self.progress_label.config(text="Загрузка изображения...")
            
            preview = Image.open(image_path)
            preview.thumbnail(PREVIEW_SIZE)
            photo = ImageTk.PhotoImage(preview)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
            
            self.update_progress(20, 100, "Обработка пикселей...")
            
            image = np.array(Image.open(image_path))
            pixels = image.reshape(-1, 3)[::COLOR_SAMPLE_STEP]
            total_pixels = len(image.reshape(-1, 3))
            
            self.update_progress(40, 100, "Подготовка отображения...")
            
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            ttk.Label(self.main_frame, text=f"Всего пикселей: {total_pixels}, Анализируемых цветов: {len(pixels)}").pack(side="top", pady=5)
            
            self.update_progress(60, 100, "Кластеризация цветов...")
            
            thread = threading.Thread(target=self.process_colors, args=(pixels,))
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обработке изображения: {str(e)}")
            self.progress_label.config(text="Произошла ошибка!")

if __name__ == "__main__":
    from tkinterdnd2 import *
    root = TkinterDnD.Tk()
    app = ColorAnalyzer(root)
    root.mainloop() 