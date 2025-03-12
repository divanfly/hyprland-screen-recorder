import os
import json
from pathlib import Path

CONFIG_DIR = os.path.join(Path.home(), ".config", "screen-recorder")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "output_dir": str(Path.home() / "Videos"),
    "audio_enabled": True,
    "video_quality": "high",  
    "fps": 30,
    "show_cursor": True,
    "audio_source": "default",
}

def load_config():
    
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        
        return config
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
        return False
def get_recorder_args(config):
    args = []
    
    if config['video_quality'] == 'low':
        args.extend(['-c', 'h264_vaapi', '-b:v', '2M'])
    
    elif config['video_quality'] == 'medium':
        args.extend(['-c', 'h264_vaapi', '-b:v', '4M'])
    
    else:  
        args.extend(['-c', 'h264_vaapi', '-b:v', '8M'])
    args.extend(['-r', str(config['fps'])])
    
    if config['show_cursor']:
        args.append('--show-cursor')
    
    if config['audio_enabled']:
        if config['audio_source'] == 'default':
            args.append('-a')
        else:
            args.extend(['-a', config['audio_source']])
            
    return args 