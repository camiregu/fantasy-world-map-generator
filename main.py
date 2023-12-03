# camiregu
# 2023-mar-22
from config import Config
from map_launcher.start_menu import start_menu
from cartographer.map_manager import open_map

Config.load_global_settings()

# main
while True:
    path = start_menu()
    open_map(path)