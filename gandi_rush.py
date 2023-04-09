"""
    Main orchestrator for gandi-rush

    Author: @aaryswastaken
    Creation Date: 04/04/2023
"""

from tkinter import Tk

from lib.event_pool_controller import EventPool
from lib.grid_controller import GridManager
from lib.window_controller import MenuPrincipal, configure_window
from lib.generator import GridGenerator

if __name__ == "__main__":
    event_pool = EventPool()
    generator = GridGenerator()

    grid_controller = GridManager(event_pool, generator, animation_wait_time=150)
    grid_controller.start()

    window = Tk()
    configure_window(window)
    menu = MenuPrincipal(window, sprite_home="./sprite/")

    menu.root.mainloop()
