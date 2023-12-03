# camiregu
# 2023-mar-28
import numpy as np
import pygame as pg

class DisplayController():
    """Singleton class keeps track of pan and zoom and displays accordingly."""
    max_display: 'tuple[int, int]'
    default_display: 'tuple[int, int]'
    scale: int
    fullscreen: bool
    draw_surface: pg.Surface
    scale_surface: pg.Surface
    display_surface: pg.Surface
    zoom_offset: 'tuple[float, float]'
    pan_offset: 'tuple[float, float]'


    @classmethod
    def start(cls):
        """Initialize pygame, set surfaces, and default values for pan/zoom/fullscreen."""
        pg.init()   
        cls.max_display = np.array((pg.display.Info().current_w, pg.display.Info().current_h))
        cls.default_display = cls.max_display / 2
        cls.fullscreen = False

        cls.draw_surface = pg.Surface(cls.max_display * 10)
        cls.scale_surface = pg.Surface(cls.default_display)
        cls.display_surface = pg.display.set_mode(cls.default_display)

        cls.scale = 1
        cls.zoom_offset = np.array((0.0, 0.0))
        cls.pan_offset = np.array((0.0, 0.0))


    @classmethod
    def draw_screen(cls):
        """Translate and draw game board to screen."""
        pg.transform.scale(cls.draw_surface, cls.get_resolution(), cls.scale_surface)
        cls.display_surface.blit(cls.scale_surface, cls.get_blit_position())
        pg.display.flip()


    @classmethod
    def toggle_fullscreen(cls):
        """Toggle fullscreen."""
        cls.fullscreen = not cls.fullscreen
        cls.set_display()


    @classmethod
    def scale_display(cls, increment: int):
        """Multiply display scale by 2^increment"""
        if increment != 0:
            increment = increment / abs(increment) # normalize increment for easier math
            new_scale = cls.scale * (2**increment) # half or double scale
            if new_scale <= 16:
                cls.scale = new_scale    
                scale_pos = np.array(pg.mouse.get_pos()) 
                cls.zoom_offset = cls.zoom_offset - increment * (2/(3-increment)) * (scale_pos-cls.zoom_offset) # zooms while keeping the position under the cursor constant
            cls.set_display()


    @classmethod
    def pan_display(cls, motion: tuple[int, int]):
        """Pan display by motion."""
        cls.pan_offset += np.array(motion) / cls.scale


    @classmethod
    def set_display(cls):
        cls.scale_surface = pg.Surface(cls.get_resolution())
        if cls.fullscreen:
            cls.display_surface = pg.display.set_mode(cls.max_display, pg.FULLSCREEN)
        else:
            cls.display_surface = pg.display.set_mode(cls.default_display)


    @classmethod
    def get_resolution(cls):
        if cls.fullscreen:
            return cls.max_display * cls.scale
        else:
            return cls.default_display * cls.scale


    @classmethod
    def get_blit_position(cls):
        return cls.zoom_offset + cls.scale * cls.pan_offset