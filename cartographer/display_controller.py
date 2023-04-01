# camiregu
# 2023-mar-28
import numpy as np
import pygame as pg


# functions
def start_display():
    global max_display, default_display, scale, fullscreen, draw_surface, scale_surface, display_surface, zoom_offset, pan_offset

    pg.init()   
    max_display = np.array((pg.display.Info().current_w, pg.display.Info().current_h))
    default_display = max_display / 2
    fullscreen = False

    draw_surface = pg.Surface(max_display * 10)
    scale_surface = pg.Surface(default_display)
    display_surface = pg.display.set_mode(default_display)

    scale = 1
    zoom_offset = np.array((0.0, 0.0))
    pan_offset = np.array((0.0, 0.0))
    return


def draw_screen():
    pg.transform.scale(draw_surface, get_resolution(), scale_surface)
    display_surface.blit(scale_surface, get_blit_position())
    pg.display.flip()
    return


def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    set_display()
    return


def scale_display(increment: int):
    global scale, zoom_offset
    increment = increment / abs(increment) # normalize increment for easier math
    new_scale = scale * (2**increment) # half or double scale
    if new_scale <= 16:
        scale = new_scale    
        scale_pos = np.array(pg.mouse.get_pos()) 
        zoom_offset = zoom_offset - increment * (2/(3-increment)) * (scale_pos-zoom_offset) # zooms while keeping the position under the cursor constant
    set_display()


def set_display():
    global display_surface, scale_surface, draw_surface
    scale_surface = pg.Surface(get_resolution())
    if fullscreen:
        display_surface = pg.display.set_mode(max_display, pg.FULLSCREEN)
    else:
        display_surface = pg.display.set_mode(default_display)
    return


def get_resolution():
    if fullscreen:
        return max_display * scale
    else:
        return default_display * scale


def get_blit_position():
    return zoom_offset + pan_offset