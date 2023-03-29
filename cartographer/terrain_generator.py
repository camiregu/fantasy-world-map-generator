#camiregu
#2023-mar-27
import config
import cartographer.tile_manager as tm

import random
import numpy as np


#import rules here


#functions
def assign_terrain(coordinates: tuple) -> str: #move
    probability_list = []
    for vector in config.BASIS_VECTORS:
        pos_1 = tuple(coordinates + np.array(vector))
        if (pos_1 in list(tm.tiles.keys()) and tm.unfilled not in tm.tiles[pos_1].groups()):
            probability_list += [tm.tiles[pos_1].terrain] * 3
        else:
            i = random.randrange(len(tm.TERRAIN_IMAGES))
            possible_terrain = list(tm.TERRAIN_IMAGES.keys())[i]
            probability_list += [possible_terrain] * 2

        pos_2 = tuple(coordinates - np.array(vector))
        if (pos_2 in list(tm.tiles.keys()) and tm.unfilled not in tm.tiles[pos_2].groups()):
            probability_list += [tm.tiles[pos_2].terrain] * 3
        else:
            i = random.randrange(len(tm.TERRAIN_IMAGES))
            possible_terrain = list(tm.TERRAIN_IMAGES.keys())[i]
            probability_list += [possible_terrain] 
    return probability_list[random.randrange(len(probability_list))]