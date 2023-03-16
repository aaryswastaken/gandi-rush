"""
    This modules focuses on the event pool and its management
"""

class EventPool():
    """
        The event pool is a FIFO stack
    """

    def __init__(self):
        """
            Creating the pool
        """

        self.stack = []
        self.priority_id = []
        self.listener = []

    def next(self):
        """
            Returns next event to treat

            Parameters:
                None

            Returns:
                event (PooledEvent): The next event
        """

    def next_and_delete(self):
        """
            Returns next event and deletes it from the stack

            Parameters:
                None

            Returns:
                event (PooledEvent): The next event
        """

    def push(self, event):
        """
            Pushes an event to the stack

            Parameters:
                event (Event): The event to push

            Returns
                id (int): PooledEvent id
        """

    def push_priority(self, event):
        """
            Pushed an important event

            Parameters:
                event (event): The event to push

            Returns:
                id (int): PooledEvent id
        """

    def register_listener(self, listener, scope=None):
        """
            Add a listener to the listener list. Listeners are
                called when an event in their scope is pushed
                with the event as argument. The event is not
                deleted from the stack

            Parameters:
                listener (function): The listener of the form:
                    my_listener(event)

                scope (list<int> | None, optional): The scope of the listening
                    - 0: Low priority only
                    - 1: High priority only
                    - None: All queued events

            Returns:
                id (int): The listener id
        """

    def unregister_listener(self, listener_id):
        """
            Removes the listener from the listener list (shouldn't be usable)

            Parameters:
                listener_id (int): The listener id

            Returns:
                None
        """

    def remove_event(self, event):
        """
            Removes an event using its reference

            Parameters:
                event (PooledEvent): The pooled event to delete

            Returns:
                success (boolean)
        """

    def remove_event_from_stack_id(self, event_id):
        """
            Removes the event with the corresponding pool id

            Parameters:
                event_id (int): The pooled id of the event

            Returns:
                success (bolean)
        """


class Event():
    """
        This class defines an event and its methods and its methods
    """

class PooledEvent(Event):
    """
        This class defines a Pooled Event (just an event + a pool id)
    """

