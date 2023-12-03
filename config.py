# camiregu
# 2023-mar-24
import json

class Config():
    """Holds configuration settings for various files."""
    MAPS_DIRECTORY: str
    STORAGE_FILENAME: str
    LOCAL_CONFIG_FILENAME: str
    TEXTURE_DIRECTORY: str
    BASIS_VECTORS: list[list[int]]
    INCIRCLE_RADIUS: int
    UNEXPLORED_IMAGE_PATH: str
    TERRAINS: dict[dict]

    @classmethod
    def load_global_settings(cls):
        with open("global_config.json","r") as global_config:
            # convert json to dict
            config: dict = json.load(global_config)
            # extract config
            cls.MAPS_DIRECTORY = config["maps_directory"]
            cls.STORAGE_FILENAME = config["storage_filename"]
            cls.LOCAL_CONFIG_FILENAME = config["local_config_filename"]
            cls.TILEMAP_FILENAME = config["tilemap_filename"]
            cls.TEXTURE_DIRECTORY = config["texture_directory"]
            cls.BASIS_VECTORS = config["basis_vectors"]

    @classmethod
    def load_local_settings(cls, local_path: str):
        with open(local_path, "r") as local_config:
            # convert json to dict
            config: dict = json.load(local_config)
            # extract config
            cls.INCIRCLE_RADIUS = config["incircle_radius"]
            cls.UNEXPLORED_IMAGE_PATH = config["unexplored_image"]
            cls.UNEXPLORED_ADJACENCIES = config["unexplored_adjacencies"]
            cls.TERRAINS = config["terrains"]