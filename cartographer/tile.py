# camiregu 2023-nov-24
from config import Config
import pygame as pg

class Tile(pg.sprite.Sprite):
    """Object stores sprite, coordinates, and adjacencies."""
    coordinates: 'tuple[int, int, int]'
    image: pg.Surface
    terrain: str
    adjacency_bonuses: 'dict[str, int]'
    adjacency_vetoes: 'list[str]'


    def __init__(self, coordinates: tuple[int,int,int]) -> None:
        """Instantiate a Tile object."""
        super().__init__()
        self.terrain = None
        self.image = pg.image.load(Config.UNEXPLORED_IMAGE_PATH)
        self.adjacency_bonuses = Config.UNEXPLORED_ADJACENCIES
        self.adjacency_vetoes = []
        self.coordinates = coordinates    