# camiregu
# 2023-mar-28
from config import Config
from cartographer.tile import Tile

import pygame as pg
import numpy as np
import random

class TileManager():
    """Singleton class holds data for and modifies all tiles, explored and unexplored, currently on the board."""
    unexplored: 'pg.sprite.Group[Tile]'
    explored: 'pg.sprite.Group[Tile]'
    tiles: 'dict[tuple[int, int, int], Tile]'

    surface: pg.Surface
    origin: 'tuple[int, int]'
    blit_offset: float
    rect_size: 'tuple[float, float]'
    axis_vectors: 'tuple[tuple[float, float], tuple[float, float], tuple[float, float]]'

    loading: bool


    @classmethod
    def start(cls, surface: pg.Surface):
        """Reset all class variables."""
        cls.unexplored = pg.sprite.Group()    
        cls.explored = pg.sprite.Group()
        cls.tiles = {}

        cls.surface = surface
        cls.origin = np.array((cls.surface.get_width() // 2, cls.surface.get_height() // 2))
        cls.blit_offset = ((-2 / np.sqrt(3)) * Config.INCIRCLE_RADIUS)
        cls.rect_size = -2*cls.blit_offset, -2*cls.blit_offset
        cls.axis_vectors = (
            np.array((-1/2, -np.sqrt(3)/2)) * (2/np.sqrt(3)) * Config.INCIRCLE_RADIUS,
            np.array((-1/2, np.sqrt(3)/2)) * (2/np.sqrt(3)) * Config.INCIRCLE_RADIUS,
            np.array((1,0)) * (2/np.sqrt(3)) * Config.INCIRCLE_RADIUS
        )


    @classmethod
    def load(cls, tilemap: dict):
        """Load a set of tiles onto the board."""
        cls.loading = True
        for coordinates, terrain in tilemap.items():
            if coordinates in cls.tiles:
                tile = cls.tiles[coordinates]
            else:
                tile = cls.create_tile(coordinates)
            cls.update_terrain(tile, terrain)
        cls.explored.draw(cls.surface)
        cls.unexplored.draw(cls.surface)
        cls.loading = False


    @classmethod
    def save(cls) -> dict:
        """Create a dict object containing explored tile data."""
        tilemap = {}
        for tile in cls.tiles.values():
            if cls.explored in tile.groups():
                tilemap.update({tile.coordinates: tile.terrain})
        return tilemap
    

    @classmethod
    def create_tile(cls, coordinates: tuple[int, int, int]) -> Tile:
        """Instantiate a Tile object at coordinates and add it to the appropriate groups. Create neighbours if necessary. Return new Tile object."""
        tile = Tile(coordinates)
        cls.tiles.update({tile.coordinates: tile})
        cls.unexplored.add(tile)
        tile.rect = pg.Rect(cls.get_screen_pos(tile.coordinates) + cls.blit_offset, cls.rect_size)
        tile.mask = pg.mask.from_surface(tile.image)

        return tile


    @classmethod 
    def destroy_tile(cls, tile: Tile):
        """Delete tile and neighbours if necessary. Recreate tile if necessary."""
        cls.tiles.pop(tile.coordinates)
        tile.kill()

        if not cls.is_isolated(tile):
            cls.create_tile(tile.coordinates)

        for vector in Config.BASIS_VECTORS:
            tile_1 = cls.tiles[tuple(tile.coordinates + np.array(vector))]
            if cls.is_isolated(tile_1):
                cls.tiles.pop(tile_1.coordinates)
                tile_1.kill()
            tile_2 = cls.tiles[tuple(tile.coordinates - np.array(vector))]
            if cls.is_isolated(tile_2):
                cls.tiles.pop(tile_2.coordinates)
                tile_2.kill()

        cls.surface.fill((0,0,0))
        cls.explored.draw(cls.surface)
        cls.unexplored.draw(cls.surface)
        

    @classmethod
    def update_terrain(cls, tile: Tile, terrain: str):
        """Update a Tile's terrain and adjacencies."""
        if tile in cls.unexplored:
            cls.unexplored.remove(tile)
            cls.explored.add(tile)

        tile.terrain = terrain 
        tile.adjacency_bonuses = Config.TERRAINS[terrain]["adjacency_bonuses"]
        tile.adjacency_vetoes = Config.TERRAINS[terrain]["adjacency_vetoes"]
        tile.image = pg.image.load(Config.TERRAINS[terrain]["image"])
        tile.rect = pg.Rect(cls.get_screen_pos(tile.coordinates) + cls.blit_offset, cls.rect_size)
        tile.mask = pg.mask.from_surface(tile.image)

        for vector in Config.BASIS_VECTORS:
            pos_1 = tuple(tile.coordinates + np.array(vector))
            if pos_1 not in cls.tiles:
                cls.create_tile(pos_1)
            pos_2 = tuple(tile.coordinates - np.array(vector))
            if pos_2 not in cls.tiles:
                cls.create_tile(pos_2)
        
        if not cls.loading:
            cls.surface.fill((0,0,0))
            cls.explored.draw(cls.surface)
            cls.unexplored.draw(cls.surface)
    

    @classmethod
    def find_tile_at(cls, position) -> Tile:
        """If mouse is over a tile, return that tile. Otherwise return None."""
        for tile in cls.tiles.values():
            if tile.rect.collidepoint(position):
                position_in_mask = position[0] - tile.rect.x, position[1] - tile.rect.y
                if tile.mask.get_at(position_in_mask):
                    return tile
                
    
    @classmethod
    def get_screen_pos(cls, coordinates: tuple[int,int,int]) -> np.ndarray:
        return coordinates[0] * cls.axis_vectors[0] + coordinates[1] * cls.axis_vectors[1] + coordinates[2] * cls.axis_vectors[2] + cls.origin


    @classmethod
    def is_isolated(cls, tile: Tile) -> bool:
        """Return True if there are no explored Tiles adjacent to tile and tile is not explored."""
        if cls.explored in tile.groups():
            return False
        
        for vector in Config.BASIS_VECTORS:
            pos_1 = tuple(tile.coordinates + np.array(vector))
            if (pos_1 in cls.tiles and cls.tiles[pos_1] in cls.explored):
                return False
            pos_2 = tuple(tile.coordinates - np.array(vector))
            if (pos_2 in cls.tiles and cls.tiles[pos_2] in cls.explored):
                return False

        return True
    

    @classmethod
    def randomize_terrain(cls, tile: Tile):
        """Randomly select a new terrain type for tile with weights based on adjacent tiles."""
        terrain_bag = []
        vetoes = []

        for vector in Config.BASIS_VECTORS:
            pos_1 = tuple(tile.coordinates + np.array(vector))
            if pos_1 in cls.tiles:
                vetoes += cls.tiles[pos_1].adjacency_vetoes
            pos_2 = tuple(tile.coordinates - np.array(vector))
            if pos_2 in cls.tiles:
                vetoes += cls.tiles[pos_2].adjacency_vetoes

        for vector in Config.BASIS_VECTORS:

            pos_1 = tuple(tile.coordinates + np.array(vector))
            if pos_1 in cls.tiles:
                for terrain, weight in cls.tiles[pos_1].adjacency_bonuses.items():
                    if terrain not in vetoes:
                        terrain_bag += [terrain] * weight

            pos_2 = tuple(tile.coordinates - np.array(vector))
            if pos_2 in cls.tiles:
                for terrain, weight in cls.tiles[pos_2].adjacency_bonuses.items():
                    if terrain not in vetoes:
                        terrain_bag += [terrain] * weight
        
        cls.update_terrain(tile, terrain_bag[random.randrange(len(terrain_bag))])