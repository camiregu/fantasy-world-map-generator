# camiregu
# 2023-mar-28
from cartographer.tile_manager import TileManager
from cartographer.display_controller import DisplayController
import pygame as pg

# functions
def process_user_input() -> bool:
    """Read user input this frame and call appropriate functions."""

    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                return True
            
            if event.key == pg.K_f:
                DisplayController.toggle_fullscreen()
                DisplayController.draw_screen()
            
        elif event.type == pg.MOUSEBUTTONDOWN:
            # convert mouse position to its equivalent position on the draw_screen
            relative_pos = (pg.mouse.get_pos() - DisplayController.get_blit_position()) * (DisplayController.draw_surface.get_height() // DisplayController.display_surface.get_height()) // DisplayController.scale
            hovered_tile = TileManager.find_tile_at(relative_pos)

            if event.button == 1:
                if hovered_tile and hovered_tile in TileManager.unexplored:
                    TileManager.randomize_terrain(hovered_tile)
                    DisplayController.draw_screen()

            if event.button == 3:
                if hovered_tile and hovered_tile in TileManager.explored:
                    TileManager.destroy_tile(hovered_tile)
                    DisplayController.draw_screen()

        elif event.type == pg.MOUSEWHEEL:
            DisplayController.scale_display(event.y)
            DisplayController.draw_screen()

        elif event.type == pg.MOUSEMOTION:
            if event.buttons[1]:
                DisplayController.pan_display(event.rel)
                DisplayController.draw_screen()
    
    return False