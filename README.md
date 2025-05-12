# Color Analyzer

Приложение для анализа цветов в изображениях с графическим интерфейсом. Программа показывает все цвета, присутствующие в изображении, их RGB и HSV значения.

## Возможности

- Загрузка изображений через диалог выбора файла или drag-and-drop
- Отображение превью изображения
- Анализ всех цветов в изображении
- Отображение RGB и HSV значений для каждого цвета
- Индикатор прогресса обработки
- Поддержка различных форматов изображений (PNG, JPG, JPEG, BMP, GIF, TIFF)

## Требования

- Python 3.8 или выше
- Установленные зависимости из requirements.txt

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/YALOKGARua/color-analyzer.git
cd color-analyzer
```

2. Создайте виртуальное окружение (рекомендуется):
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

Запустите программу:
```bash
python color_analyzer.py
```

После запуска вы можете:
1. Перетащить изображение в окно программы
2. Или нажать кнопку "Выбрать изображение" и выбрать файл через диалог

## Структура проекта

```
color-analyzer/
├── color_analyzer.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Лицензия

MIT License 