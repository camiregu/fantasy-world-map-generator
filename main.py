# camiregu
# 2023-mar-22
from config import Config
from map_launcher.start_menu import StartMenu
from cartographer.map_manager import open_map
import file_manager

Config.load_global_settings()

# main
while True:
    map = StartMenu().select()
    Config.load_local_settings(map)
    tilemap = open_map()
    file_manager.edit_map(map, {"tilemap": tilemap})