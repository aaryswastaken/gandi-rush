"""
    Main orchestrator for gandi-rush

    Author: @aaryswastaken
    Creation Date: 04/04/2023
"""

# Otherwise there is a conflict with Final newline missing
# pylint: disable=trailing-newlines

from lib.event_pool_controller import EventPool
from lib.grid_controller import GridManager
import lib.window_controller
from lib.generator import GridGenerator


if __name__ == "__main__":
    event_pool = EventPool()
    generator = GridGenerator()
    grid_controller = GridManager(event_pool, generator, animation_wait_time=100)
    grid_controller.start()

    lib.window_controller.main_loop(event_pool,"./sprite/",grid_controller)

