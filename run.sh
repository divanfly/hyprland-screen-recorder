if ! command -v wf-recorder >/dev/null 2>&1; then
    echo "Ошибка: wf-recorder не установлен."
    echo "Установите его командой: sudo pacman -S wf-recorder"
    exit 1
fi

if ! command -v python >/dev/null 2>&1; then
    echo "Ошибка: Python не установлен."
    echo "Установите его командой: sudo pacman -S python"
    exit 1
fi


if [ -z "$WAYLAND_DISPLAY" ]; then
    echo "Предупреждение: WAYLAND_DISPLAY не определен. Возможно, вы не используете Wayland."
    echo "Программа может работать неправильно."
fi


if ! ps -e | grep -q "Hyprland"; then
    echo "Предупреждение: Hyprland не обнаружен. Программа оптимизирована для Hyprland."
    echo "Некоторые функции могут работать неправильно."
fi

if [ ! -f "requirements.txt" ]; then
    echo "Ошибка: Файл requirements.txt не найден."
    exit 1
fi

mkdir -p ~/Videos

echo "Запуск программы записи экрана..."
python screen_recorder.py 