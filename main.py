# camiregu
# 2023-mar-22
from file_manager import start_menu
from cartographer.map_manager import open_map


# main
while True:
    path = start_menu()
    open_map(path)