import unittest
from color_utils import *

class TestColorUtils(unittest.TestCase):
    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex(255, 0, 0), '#ff0000')
        self.assertEqual(rgb_to_hex(0, 255, 0), '#00ff00')
        self.assertEqual(rgb_to_hex(0, 0, 255), '#0000ff')
        
    def test_hex_to_rgb(self):
        self.assertEqual(hex_to_rgb('#ff0000'), (255, 0, 0))
        self.assertEqual(hex_to_rgb('#00ff00'), (0, 255, 0))
        self.assertEqual(hex_to_rgb('#0000ff'), (0, 0, 255))
        
    def test_rgb_to_hsv(self):
        self.assertEqual(rgb_to_hsv(255, 0, 0), (0, 100, 100))
        self.assertEqual(rgb_to_hsv(0, 255, 0), (120, 100, 100))
        self.assertEqual(rgb_to_hsv(0, 0, 255), (240, 100, 100))
        
    def test_get_complementary_color(self):
        self.assertEqual(get_complementary_color(255, 0, 0), (0, 255, 255))
        self.assertEqual(get_complementary_color(0, 255, 0), (255, 0, 255))
        
    def test_get_color_name(self):
        self.assertEqual(get_color_name(255, 0, 0), 'красный')
        self.assertEqual(get_color_name(0, 255, 0), 'зеленый')
        self.assertEqual(get_color_name(0, 0, 255), 'синий')
        
    def test_get_color_temperature(self):
        self.assertEqual(get_color_temperature(255, 255, 255), 'теплый')
        self.assertEqual(get_color_temperature(0, 0, 0), 'холодный')
        self.assertEqual(get_color_temperature(128, 128, 128), 'нейтральный')

if __name__ == '__main__':
    unittest.main() 