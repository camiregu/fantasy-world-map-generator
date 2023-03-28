#camiregu
#2023-mar-27
import config
import os

#functions
def open_map(local_directory: str):
    tilemap_path = os.path.join(local_directory,config.TILEMAP_FILENAME)
    local_config_path = os.path.join(local_directory,config.LOCAL_CONFIG_FILENAME)

    config.load_local_settings(local_config_path)
    import cartographer.tilemap as tilemap
    import cartographer.map_drawer as map_drawer
    
    map = tilemap.load_map(tilemap_path)
    map_drawer.download_map(map)

    done = False
    while not done:
        done = map_drawer.process_user_input()
    map = map_drawer.upload_map()
    tilemap.save_map(map,tilemap_path)