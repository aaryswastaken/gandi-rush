"""
    Main orchestrator for gandi-rush

    Author: @aaryswastaken, @Byllie
    Creation Date: 04/04/2023
"""

# Otherwise there is a conflict with Final newline missing
# pylint: disable=trailing-newlines,redefined-builtin,invalid-name

from sys import argv, exit

from lib.event_pool_controller import EventPool
from lib.grid_controller import GridManager
import lib.window_controller
from lib.generator import GridGenerator


if __name__ == "__main__":
    try:
        animation_wait_time = 50
        debug = False

        i = 1
        while i < len(argv):
            arg = argv[i]

            if arg in ["-d", "--debug", "--god-help-me"]:
                debug = True
            elif arg in ["-t", "--animation-delay"]:
                animation_wait_time = int(argv[i+1])
                i += 1

            i += 1
    except ValueError:
        print("Parsing failed, exiting")
        exit(1)

    event_pool = EventPool()
    generator = GridGenerator()
    grid_controller = GridManager(event_pool, generator,
                                  animation_wait_time=animation_wait_time, debug=debug)
    grid_controller.start()

    lib.window_controller.main_loop(event_pool, "./sprite/",
                                    grid_controller, debug=debug)

