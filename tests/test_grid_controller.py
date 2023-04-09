"""
    This modules aims at testing the grid controller
"""

import pytest

from lib.grid_controller import GridManager
from lib.event_pool_controller import EventPool, Event
from lib.generator import GridGenerator

# from time import sleep

threads = []

@pytest.fixture(name="event_pool_from_manager")
def fixture_grid_manager():
    """
        Automates the grid manager creation
    """

    event_pool = EventPool()
    gen = GridGenerator()

    manager = GridManager(0.5, event_pool, gen)
    manager.start()

    threads.append(manager)

    return event_pool

def test_run(event_pool_from_manager):
    """
        Tests if the file is valid
    """

    event = Event(10, 10, True) # Dummy event
    event_pool_from_manager.push(event)

def test_generation():
    """
        Test the grid generation through events
    """

    # Not implemented yet lol
    assert True

def test_close_threads():
    """
        Closes all threads so that pytest can proceed
    """

    for thread in threads:
        thread.stop()
