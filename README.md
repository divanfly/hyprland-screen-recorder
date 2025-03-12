# Программа для записи экрана

Простая программа для записи экрана, оптимизированная для Arch Linux и Hyprland.

## Возможности

- Запись экрана в формате MP4
- Запись звука с микрофона
- Настройка качества записи и частоты кадров
- Включение/отключение отображения курсора
- Таймер записи

## Требования

- Arch Linux с Hyprland
- Python 3.10 или новее
- wf-recorder
- GTK 4

## Установка

1. Установите необходимые пакеты:

```bash
sudo pacman -S wf-recorder python-gobject python-cairo python-pip
```

2. Установите Python-зависимости:

```bash
pip install -r requirements.txt
```

## Использование

Запустите программу:

```bash
./run.sh
```

или

```bash
python screen_recorder.py
```

### Настройки в интерфейсе

- **Записывать звук микрофона** - включает запись звука
- **Показывать курсор мыши** - показывает указатель во время записи
- **Качество видео** - выбор между низким, средним и высоким качеством
- **Частота кадров** - выбор частоты кадров (15, 24, 30, 60 FPS)
- **Сохранить настройки** - сохраняет настройки для будущих запусков

### Папка сохранения

Все записи сохраняются в директорию `~/Videos`.

## Горячие клавиши

Для настройки горячих клавиш в Hyprland добавьте в файл `~/.config/hypr/hyprland.conf`:

```
# Запуск программы по Ctrl+Alt+R
bind = CTRL ALT, R, exec, /полный/путь/к/run.sh
```

## Устранение проблем

### Если не запускается

Убедитесь, что установлены все зависимости:

```bash
sudo pacman -S wf-recorder python-gobject python-cairo python-pip
pip install -r requirements.txt
```

### Если не работает запись

- Проверьте, что используете Wayland: `echo $XDG_SESSION_TYPE`
- Проверьте доступ к аудиоустройствам: `ls -la /dev/snd/`
- Проверьте настройки PulseAudio/PipeWire: `pactl info`

### Для настройки качества записи

Если запись слишком нагружает систему, выберите более низкое качество и частоту кадров. 