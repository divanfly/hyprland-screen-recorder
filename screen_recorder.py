import gi
import os
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path
import config

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib

class ScreenRecorderApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.github.screen_recorder")
        self.connect("activate", self.on_activate)
        self.recording_process = None
        self.is_recording = False
        self.config = config.load_config()
        
    def on_activate(self, app):
        self.window = Gtk.ApplicationWindow(application=app)
        self.window.set_title("Запись экрана")
        self.window.set_default_size(400, 250)
        self.window.set_resizable(False)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        self.window.set_child(main_box)
        
        title_label = Gtk.Label()
        title_label.set_markup("<span size='large' weight='bold'>Запись экрана</span>")
        main_box.append(title_label)
        
        settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        settings_box.set_margin_top(10)
        main_box.append(settings_box)
        
        self.audio_toggle = Gtk.CheckButton()
        self.audio_toggle.set_label("Записывать звук микрофона")
        self.audio_toggle.set_active(self.config['audio_enabled'])
        self.audio_toggle.connect("toggled", self.on_audio_toggle)
        settings_box.append(self.audio_toggle)
        
        self.cursor_toggle = Gtk.CheckButton()
        self.cursor_toggle.set_label("Показывать курсор мыши")
        self.cursor_toggle.set_active(self.config['show_cursor'])
        self.cursor_toggle.connect("toggled", self.on_cursor_toggle)
        settings_box.append(self.cursor_toggle)
        
        quality_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        quality_label = Gtk.Label(label="Качество видео:")
        quality_box.append(quality_label)
        
        self.quality_combo = Gtk.ComboBoxText()
        self.quality_combo.append("low", "Низкое")
        self.quality_combo.append("medium", "Среднее")
        self.quality_combo.append("high", "Высокое")
        self.quality_combo.set_active_id(self.config['video_quality'])
        self.quality_combo.connect("changed", self.on_quality_changed)
        quality_box.append(self.quality_combo)
        
        settings_box.append(quality_box)
        
        fps_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        fps_label = Gtk.Label(label="Частота кадров:")
        fps_box.append(fps_label)
        
        self.fps_combo = Gtk.ComboBoxText()
        for fps in ["15", "24", "30", "60"]:
            self.fps_combo.append(fps, f"{fps} FPS")
        self.fps_combo.set_active_id(str(self.config['fps']))
        self.fps_combo.connect("changed", self.on_fps_changed)
        fps_box.append(self.fps_combo)
        
        settings_box.append(fps_box)
        
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_margin_top(10)
        button_box.set_halign(Gtk.Align.CENTER)
        main_box.append(button_box)
        
        self.record_button = Gtk.Button(label="Начать запись")
        self.record_button.connect("clicked", self.on_record_clicked)
        self.record_button.set_hexpand(True)
        button_box.append(self.record_button)
        
        self.settings_button = Gtk.Button(label="Сохранить настройки")
        self.settings_button.connect("clicked", self.on_save_settings)
        button_box.append(self.settings_button)
        
        output_label = Gtk.Label()
        output_label.set_markup(f"<span size='small'>Папка сохранения: {self.config['output_dir']}</span>")
        output_label.set_margin_top(10)
        main_box.append(output_label)
        
        self.status_label = Gtk.Label(label="Готов к записи")
        self.status_label.set_margin_top(5)
        main_box.append(self.status_label)
        
        self.timer_label = Gtk.Label(label="00:00")
        self.timer_label.set_margin_top(5)
        main_box.append(self.timer_label)
        
        self.window.present()
    
    def on_audio_toggle(self, button):
        self.config['audio_enabled'] = button.get_active()
    
    def on_cursor_toggle(self, button):
        self.config['show_cursor'] = button.get_active()
    
    def on_quality_changed(self, combo):
        self.config['video_quality'] = combo.get_active_id()
    
    def on_fps_changed(self, combo):
        self.config['fps'] = int(combo.get_active_id())
    
    def on_save_settings(self, button):
        if config.save_config(self.config):
            self.status_label.set_text("Настройки сохранены")
        else:
            self.status_label.set_text("Ошибка при сохранении настроек")
    
    def on_record_clicked(self, button):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        if self.recording_process:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.config['output_dir'], f"запись_{timestamp}.mp4")
        
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        cmd = ["wf-recorder", "-f", output_file]
        cmd.extend(config.get_recorder_args(self.config))
        
        try:
            env = os.environ.copy()
            self.recording_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            self.is_recording = True
            self.record_button.set_label("Остановить запись")
            self.status_label.set_text("Идет запись...")
            self.audio_toggle.set_sensitive(False)
            self.cursor_toggle.set_sensitive(False)
            self.quality_combo.set_sensitive(False)
            self.fps_combo.set_sensitive(False)
            self.settings_button.set_sensitive(False)
            
            self.start_time = time.time()
            self.timer_id = GLib.timeout_add(1000, self.update_timer)
            
        except Exception as e:
            self.status_label.set_text(f"Ошибка: {str(e)}")
            self.recording_process = None
    
    def stop_recording(self):
        if not self.recording_process:
            return
        
        self.recording_process.send_signal(signal.SIGINT)
        self.recording_process.wait()
        
        self.is_recording = False
        self.record_button.set_label("Начать запись")
        self.status_label.set_text(f"Запись сохранена в папку {self.config['output_dir']}")
        self.audio_toggle.set_sensitive(True)
        self.cursor_toggle.set_sensitive(True)
        self.quality_combo.set_sensitive(True)
        self.fps_combo.set_sensitive(True)
        self.settings_button.set_sensitive(True)
        
        if hasattr(self, 'timer_id'):
            GLib.source_remove(self.timer_id)
        
        self.recording_process = None
    
    def update_timer(self):
        if not self.is_recording:
            return False
        
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.set_text(f"{minutes:02d}:{seconds:02d}")
        
        return True

if __name__ == "__main__":
    app = ScreenRecorderApp()
    app.run(None) 