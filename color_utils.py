import colorsys
import numpy as np

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
    color_dict = {
        'красный': (255, 0, 0),
        'зеленый': (0, 255, 0),
        'синий': (0, 0, 255),
        'желтый': (255, 255, 0),
        'пурпурный': (255, 0, 255),
        'голубой': (0, 255, 255),
        'белый': (255, 255, 255),
        'черный': (0, 0, 0),
        'серый': (128, 128, 128),
        'оранжевый': (255, 165, 0),
        'коричневый': (165, 42, 42),
        'розовый': (255, 192, 203)
    }
    
    min_distance = float('inf')
    closest_color = 'неизвестный'
    
    for name, value in color_dict.items():
        distance = np.sqrt(sum((np.array([r, g, b]) - np.array(value)) ** 2))
        if distance < min_distance:
            min_distance = distance
            closest_color = name
            
    return closest_color

def get_color_temperature(r, g, b):
    temperature = (r * 0.299 + g * 0.587 + b * 0.114)
    if temperature > 190:
        return "теплый"
    elif temperature < 64:
        return "холодный"
    else:
        return "нейтральный" 