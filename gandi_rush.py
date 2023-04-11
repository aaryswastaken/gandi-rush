"""
    Main orchestrator for gandi-rush

    Author: @aaryswastaken
    Creation Date: 04/04/2023
"""

from tkinter import Tk

from lib.event_pool_controller import EventPool
from lib.grid_controller import GridManager
from lib.window_controller import main_loop , genere_alea
from lib.generator import GridGenerator

if __name__ == "__main__":
    event_pool = EventPool()
    generator = GridGenerator()

    grid_controller = GridManager(event_pool, generator, animation_wait_time=150)
    grid_controller.start()

    main_loop(event_pool,"./sprite/",genere_alea(3))