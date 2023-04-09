"""
    This modules aims at testing the grid controller
"""

from time import time, sleep
import pytest

from lib.grid_controller import GridManager
from lib.event_pool_controller import EventPool, Event
from lib.generator import GridGenerator


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

def test_thread_exit_event():
    """
        Test the TYPE_EXIT_ALL
    """

    event_pool = EventPool()
    gen = GridGenerator()

    manager = GridManager(0.5, event_pool, gen)
    manager.start()

    threads.append(manager)

    event = Event(0, Event.TYPE_EXIT_ALL, None)
    event_pool.push(event)

    success = False
    end_epoch = time() + 5  # Wait for 5 seconds

    while (not success) and (time() < end_epoch):
        success = success or manager.thread_stop_flag
        sleep(0.05)

    assert success is True

def test_close_threads():
    """
        Closes all threads so that pytest can proceed
    """

    for thread in threads:
        thread.stop()
        thread.join()
