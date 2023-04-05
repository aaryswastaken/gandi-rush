"""
    Main orchestrator for gandi-rush

    Author: @aaryswastaken
    Creation Date: 04/04/2023
"""

from lib.event_pool_controller import EventPool
from lib.grid_controller import GridManager
from lib.window_controller import WindowController, MenuPrincipal

if __name__ == "__main__":
    event_pool = EventPool()

    grid_controller = GridManager(0.5, event_pool, None, animation_wait_time=150)
    grid_controller.start()

    window_controller = WindowController()
    menu = MenuPrincipal(window_controller)

    menu.root.main_loop()
