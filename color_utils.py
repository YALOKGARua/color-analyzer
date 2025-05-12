import colorsys
import numpy as np
from constants import BASIC_COLORS

def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return int(h*360), int(s*100), int(v*100)

def get_complementary_color(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    h = (h + 0.5) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r*255), int(g*255), int(b*255))

def get_color_name(r, g, b):
    color_array = np.array([r, g, b])
    distances = {name: np.sqrt(np.sum((color_array - np.array(value)) ** 2)) 
                for name, value in BASIC_COLORS.items()}
    return min(distances.items(), key=lambda x: x[1])[0]

def get_color_temperature(r, g, b):
    temperature = (r * 0.299 + g * 0.587 + b * 0.114)
    if temperature > 190: return "теплый"
    if temperature < 64: return "холодный"
    return "нейтральный"

def process_colors_batch(pixels, start_idx, batch_size):
    batch = pixels[start_idx:start_idx + batch_size]
    results = []
    for color in batch:
        r, g, b = color[0], color[1], color[2]
        comp_r, comp_g, comp_b = get_complementary_color(r, g, b)
        hsv = rgb_to_hsv(r, g, b)
        results.append({
            'rgb': (r, g, b),
            'hex': rgb_to_hex(r, g, b),
            'comp': (comp_r, comp_g, comp_b),
            'comp_hex': rgb_to_hex(comp_r, comp_g, comp_b),
            'hsv': hsv,
            'name': get_color_name(r, g, b),
            'temp': get_color_temperature(r, g, b)
        })
    return results 