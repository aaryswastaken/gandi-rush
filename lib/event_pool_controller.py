"""
    This modules focuses on the event pool and its management

    Author: @aaryswastaken
    Created Date: 03/16/2023
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
        self.listener = []

    def next(self, dest):
        """
            Returns next event to treat

            Parameters:
                dest (int): The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

        # Simple break-free implementation of a find algorithm
        i = 0
        out = None

        while i < len(self.stack) and out is None:
            if self.stack[i].dest == dest:
                out = self.stack[i]
            i += 1

        return out

    def next_and_delete(self, dest):
        """
            Returns next event and deletes it from the stack

            Parameters:
                dest (int): The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

        # Same as self.next but with a pop instead
        i = 0
        out = None

        while i < len(self.stack) and out is None:
            if self.stack[i].dest == dest:
                out = self.stack.pop(i)
            i += 1

        return out

    def next_priority(self, dest):
        """
            Returns the next event flagged as important

            Parameters:
                dest (int); The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

        # Same but filtered with only priority events
        i = 0
        out = None

        while i < len(self.stack) and out is None:
            if self.stack[i].flag == 1 and self.stack[i].dest == dest:
                out = self.stack[i]
            i += 1

        return out

    def next_priority_and_delete(self, dest):
        """
            Returns the next event flagged as important and deletes
                it from the stack

            Parameters:
                dest (int): The destination of the message

            Returns:
                event (PooledEvent): The next event
        """

        # ...
        i = 0
        out = None

        while i < len(self.stack) and out is None:
            if self.stack[i].flag == 1 and self.stack[i].dest == dest:
                out = self.stack.pop(i)
            i += 1

        return out

    def push(self, event):
        """
            Pushes an event to the stack

            Parameters:
                event (Event): The event to push

            Returns
                id (int): PooledEvent id
        """

        # Compute the id of the pooled event (pool id = pid)
        pid = len(self.stack) + 1
        pooled_event = event.derive_pooled_event(pid)  # Deive a pooled event

        # Push it to the stack
        self.stack.append(pooled_event)

        # Call for listeners
        for listener in self.listener:
            # Only the one that are only focused on low-priority event and listener
            # that are listening everything
            if (listener["scope"] == 0 or listener["scope"] is None) \
                    and listener["active"] is True:

                listener["l"](event)

        return pid # Returning the pid "JICO"

    def push_priority(self, event):
        """
            Pushed an important event

            Parameters:
                event (event): The event to push

            Returns:
                id (int): PooledEvent id
        """

        # Same as self.push except the event has a priority flag and we call
        # the suitable listeners
        pid = len(self.stack) + 1
        pooled_event = event.derive_pooled_event(pid)
        pooled_event.flag = 1

        self.stack.append(pooled_event)

        for listener in self.listener:
            if (listener["scope"] == 1 or listener["scope"] is None) \
                    and listener["active"] is True:

                listener["l"](event)

        return pid

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

        # Append the listener with a bit of context to identify it
        self.listener.append({"l": listener, "scope": scope, "active": True})

        return len(self.listener) # Poorly written listener_id returner

    def unregister_listener(self, listener_id):
        """
            Removes the listener from the listener list (shouldn't be usable)

            Parameters:
                listener_id (int): The listener id

            Returns:
                None
        """

        # Obvious
        self.listener[listener_id].active = False

    def remove_event(self, event):
        """
            Removes an event using its reference

            Parameters:
                event (PooledEvent): The pooled event to delete

            Returns:
                success (boolean)
        """

        # Classical break-free element-property-based array element deleter
        # Note: same as `self.remove_event_from_stack_id(event.pid)`
        i = 0
        res = False

        while i < len(self.stack) and not res:
            if self.stack[i].pid == event.pid:
                self.stack.pop(i)
                res = True
            i += 1

        return res

    def remove_event_from_stack_id(self, event_id):
        """
            Removes the event with the corresponding pool id

            Parameters:
                event_id (int): The pooled id of the event

            Returns:
                success (bolean)
        """

        # Same as self.remove_event but with pid rather than the event
        i = 0
        res = False

        while i < len(self.stack) and not res:
            if self.stack[i].pid == event_id:
                self.stack.pop(i)
                res = True
            i += 1

        return res


class Event():
    """
        This class defines an event and its methods and its methods
    """

    TYPE_GRID_PERMUTATION = 0   #
    TYPE_UI_REFRESH = 1         # Just reloads the whole board
    TYPE_UI_UPDATE = 2          # Undates according to modifications on the payload
    TYPE_UI_ACTION = 3          # When the user makes a move
    TYPE_SCORE_UPDATE = 4       # Updates the score
    TYPE_GEN_TRIGGER = 5

    TYPE_GRID_PERMUTATION_ERROR = 10
    TYPE_GRID_TICK_ERROR = 11

    TYPE_EXIT_ALL = 99

    def __init__(self, dest, msg_type, payload):
        # 0: ui -> grid manager
        # 1: grid manager -> ui
        # 2: grid manager -> grid creator (probably not used)
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

    def derive_pooled_event(self, pid):
        """
            Derives the pooled event from the event
        """

        return PooledEvent.from_event(self, pid)

class PooledEvent(Event):
    """
        This class defines a Pooled Event (just an event + a pool id)
    """

    def __init__(self, dest, mt, pl, pid):
        super().__init__(dest, mt, pl)
        self.pe_id = pid
        self.flag = 0

    @staticmethod
    def from_event(event, pid):
        """
            Derives a PooledEvent from an Event (poor implementation)
        """

        return PooledEvent(event.dest, event.msg_type, event.payload, pid)

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
