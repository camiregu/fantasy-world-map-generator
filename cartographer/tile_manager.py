# camiregu
# 2023-mar-28
import config
import pygame as pg
import numpy as np


# tile class
class Tile(pg.sprite.Sprite):
    def __init__(self, coordinates: tuple[int,int,int]) -> None:
        """Instantiate a Tile object."""
        super().__init__(unexplored)
        self.image = UNEXPLORED_IMAGE
        self.mask = pg.mask.from_surface(self.image)
        self.coordinates = coordinates
        tiles.update({self.coordinates: self})
        return
        
    def update_terrain(self, terrain: str):
        """Update a Tile's terrain and its associated image."""
        self.terrain = terrain
        self.image = TERRAIN_IMAGES[terrain]
        self.mask = pg.mask.from_surface(self.image)
        return

    def set_explored(self, is_explored: bool):
        """Move the Tile to the appropriate sprite group."""
        if is_explored:
            unexplored.remove(self)
            explored.add(self)
        else:
            unexplored.add(self)
            explored.remove(self)
        return

    def mouse_is_over(self, position) -> bool:
        """Return True if position collides with Tile sprite"""
        position_in_mask = position[0] - self.rect.x, position[1] - self.rect.y
        return self.rect.collidepoint(position) and self.mask.get_at(position_in_mask)
    
    def is_isolated(self) -> bool:
        """Return True if there are no explored Tiles adjacent to this one and this one is not explored."""
        if explored in self.groups():
            return False
        
        isolated = True
        for vector in config.BASIS_VECTORS:
            pos_1 = tuple(self.coordinates + np.array(vector))
            if (pos_1 in tiles and explored in tiles[pos_1].groups()):
                isolated = False
            pos_2 = tuple(self.coordinates - np.array(vector))
            if (pos_2 in tiles and explored in tiles[pos_2].groups()):
                isolated = False

        return isolated

    def reset(self):
        """Reset the Tile as if it was never explored."""
        self.set_explored(False)
        self.terrain = None
        self.image = UNEXPLORED_IMAGE
        self.mask = pg.mask.from_surface(self.image)
        for vector in config.BASIS_VECTORS:
            tile_1 = tiles[tuple(self.coordinates + np.array(vector))]
            if tile_1.is_isolated():
                tiles.pop(tile_1.coordinates)
                unexplored.remove(tile_1)
                del tile_1
            tile_2 = tiles[tuple(self.coordinates - np.array(vector))]
            if tile_2.is_isolated():
                tiles.pop(tile_2.coordinates)
                unexplored.remove(tile_2)
                del tile_2
        if self.is_isolated():
            tiles.pop(self.coordinates)
            unexplored.remove(self)
            del self
    

# functions
def start_tiles():
    # constants
    global TERRAIN_IMAGES, UNEXPLORED_IMAGE

    # global variables
    global unexplored, explored, tiles

    TERRAIN_IMAGES = {}
    for terrain_name, image_path in config.TERRAINS.items():
        TERRAIN_IMAGES.update({terrain_name: pg.image.load(image_path)})
    UNEXPLORED_IMAGE = pg.image.load(config.UNEXPLORED_IMAGE_PATH)

    unexplored = pg.sprite.Group()    
    explored = pg.sprite.Group()
    tiles = {}
    return


def download_map(tilemap: dict):
    for coordinates, terrain in tilemap.items():
        tile = Tile(coordinates)
        tile.update_terrain(terrain)
        tile.set_explored(True)
    return


def upload_map() -> dict:
    tilemap = {}
    for tile in tiles.values():
        if explored in tile.groups():
            tilemap.update({tile.coordinates: tile.terrain})
    return tilemap