"""
    This modules aims at testing the grid controller
"""

from time import time, sleep
import pytest

from lib.grid_controller import GridManager
from lib.event_pool_controller import EventPool, Event
from lib.generator import GridGenerator


threads = []

@pytest.fixture(name="manager_and_event_pool")
def fixture_grid_manager():
    """
        Automates the grid manager creation
    """

    event_pool = EventPool()
    gen = GridGenerator()

    manager = GridManager(event_pool, gen)
    manager.start()

    threads.append(manager)

    return (manager, event_pool)

def decompose(manager_tuple):
    """
        Decomposes the tuple returned by the fixture
        for easier use
    """
    return manager_tuple[0], manager_tuple[1]

def test_run(manager_and_event_pool):
    """
        Tests if the file is valid
    """

    _manager, event_pool = decompose(manager_and_event_pool)

    event = Event(10, 10, True) # Dummy event
    event_pool.push(event)

def test_generation(manager_and_event_pool):
    """
        Test the grid generation through events
    """

    manager, event_pool = decompose(manager_and_event_pool)

    dimensions = (11, 17)

    gen_event = Event(0, Event.TYPE_GEN_TRIGGER, {"grid_size": dimensions})
    event_pool.push(gen_event)

    success = False
    stop = False
    end_epoch = time() + 15

    while (not success) and (time() < end_epoch) and (not stop):
        if len(manager.grid) != 0:
            if len(manager.grid) != dimensions[1]:
                assert False, f"Grid height was supposed to be {dimensions[1]}, "+\
                        "is {len(manager.grid)}"
                stop = True  # Because breaks aren't allowed
            else:
                if len(manager.grid[0]) != dimensions[0]:
                    assert False, f"Grid width supposed to be {dimensions[0]}, "+\
                            "is {len(manager.grid[0])}"
                    stop = True
                else:
                    success = True

    if not stop:
        assert success

def test_thread_exit_event(manager_and_event_pool):
    """
        Test the TYPE_EXIT_ALL
    """

    manager, event_pool = decompose(manager_and_event_pool)

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
