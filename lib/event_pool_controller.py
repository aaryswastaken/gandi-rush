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

    def next(self, dest):
        """
            Returns next event to treat

            Parameters:
                dest (int): The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

    def next_and_delete(self, dest):
        """
            Returns next event and deletes it from the stack

            Parameters:
                dest (int): The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

    def next_priority(self, dest):
        """
            Returns the next event flagged as important

            Parameters:
                dest (int); The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

    def next_priority_and_delete(self, dest):
        """
            Returns the next event flagged as important and deletes
                it from the stack

            Parameters:
                dest (int): The destination of the message

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
    TYPE_UI_REFRESH = 1     # Just reloads the whole board
    TYPE_UI_UPDATE = 2      # Undates according to modifications on the payload
    TYPE_UI_ACTION = 3      # When the user makes a move
    TYPE_SCORE_UPDATE = 4   # Updates the score

    def __init__(self, dest, msg_type, payload):
        self.dest = dest
        self.msg_type = msg_type
        self.payload = payload

    def get_dest(self):
        """
            Returns the destination
        """

        return self.dest

    def update_payload(self, new_payload):
        """
            Updates the payload
        """

        self.payload = new_payload

    def clone(self):
        """
            Clones itself
        """

        clone = Event(self.dest, self.msg_type, self.payload)
        return clone

    def derive_pooled_event(self):
        """
            Derives the pooled event from the event
        """

        return PooledEvent.from_event(self)

class PooledEvent(Event):
    """
        This class defines a Pooled Event (just an event + a pool id)
    """

    def __init__(self, dest, mt, pl, eid):
        super().__init__(dest, mt, pl)
        self.pe_id = eid
        self.flag = 0

    @staticmethod
    def from_event(event):
        """
            Derives a PooledEvent from an Event (poor implementation)
        """

        return super().__init__(event.dest, event.msg_type, event.payload)

    def set_flag(self, f_level=0):
        """
            Set flag
        """

        self.flag = f_level

    def set_id(self, eid):
        """
            Set event id
        """

        self.pe_id = eid
