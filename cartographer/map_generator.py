#camiregu
#2023-mar-27
import numpy as np

#functions
def assign_terrain():
    pass

#constants
BASIS_VECTORS = (
    np.array((1, -1, 0)),
    np.array((0, -1, 1)),
    np.array((-1, 0, 1)),
    np.array((-1, 1, 0)), #delete bottom 3
    np.array((0, 1, -1)),
    np.array((1, 0, -1))
)