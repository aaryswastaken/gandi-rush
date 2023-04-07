"""
    This test is about EventPool
"""

# pytest: disable=refedine-from-outer-scope

import pytest
from lib.event_pool_controller import EventPool, Event


@pytest.fixture(name="event_pool")
def fixture_event_pool():
    """
        Just a fixture to return a new event pool
    """

    return EventPool()


def test_add_delete(event_pool):
    """
        Adds an event to the queue, calls it
    """

    event = Event(1, 1, True)

    event_pool.push(event)

    assert len(event_pool.stack) == 1, "Assuming the event pool has data"

    event_2 = event_pool.next_and_delete(1)

    assert event_2.get_dest() == 1
    assert event_2.msg_type == 1
    assert event_2.payload is True

    assert len(event_pool.stack) == 0, "Assuming it has been deleted"


def test_priority(event_pool):
    """
        Test is priority is treated correctly
    """

    event = Event(1, 1, True)
    event_priority = Event(1, 2, False)

    event_pool.push(event)
    event_pool.push_priority(event_priority)

    assert len(event_pool.stack) == 2, "Assuming push are correct"

    event_priority_2 = event_pool.next_priority_and_delete(1)

    assert len(event_pool.stack) == 1, "Assuming delete worked"

    assert event_priority_2.get_dest() == 1
    assert event_priority_2.msg_type == 2
    assert event_priority_2.payload is False

    event_pool.push_priority(event_priority_2)

    assert len(event_pool.stack) == 2, "assumes push is correct"

    assert event_pool.next_and_delete(1).msg_type == 1, "Next is non prio event"
    assert event_pool.next_and_delete(1).msg_type == 2, "Next is prio event"

    assert len(event_pool.stack) == 0, "Assumes is clear"


def test_listeners(event_pool):
    """
        Test listeners
    """

    listener_flag = []  # Must be an object

    event_pool.register_listener(lambda _event, l=listener_flag: (l.append(1)))

    event = Event(1, 1, True)
    event_pool.push(event)

    assert len(listener_flag) == 1
