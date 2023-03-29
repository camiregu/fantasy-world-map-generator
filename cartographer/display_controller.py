#camiregu
#2023-mar-28
import config
import pygame as pg


#functions
def start_display():
    global max_display, default_display, scale, fullscreen, draw_surface, scale_surface, display_surface

    pg.init()   
    max_display = pg.display.Info().current_w, pg.display.Info().current_h
    default_display = max_display[0] / 2, max_display[1] / 2
    scale = 1
    fullscreen = False

    draw_surface = pg.Surface((max_display[0] * 10, max_display[1] * 10))
    scale_surface = pg.Surface(default_display)
    display_surface = pg.display.set_mode(default_display)
    return


def draw_screen():
    pg.transform.scale(draw_surface, get_resolution(), scale_surface)
    display_surface.blit(scale_surface, get_blit_position())
    pg.display.flip()
    return


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
        return max_display[0] * scale, max_display[1] * scale
    else:
        return default_display[0] * scale, default_display[1] * scale


def get_blit_position():
    zoom_offset = -display_surface.get_width() / 2 * (scale - 1), -display_surface.get_height() / 2 * (scale - 1), 
    return zoom_offset


def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    set_display()
    return


def change_scale(increment: int):
    global scale
    if (increment > 0 and scale * 2 <= 16):
        scale *= 2
    elif increment < 0:
        scale *= 1/2
    print(scale)
    set_display()