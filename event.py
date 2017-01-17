"""docstring"""
import time

from boules import Boules


class Event(Boules):
    """
    Event Class
    attributes:
    event_id, event_type, event_level, event_category
    event_timestamp, event_description, event_acknowledge
    Methods: get all + get full name
             set all
             get unique_id
    """
    NAME = 'account'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = {}
    meta = {"unique_id": 50000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new account
    def __init__(self, **kwargs):
        Event.meta["unique_id"] += 1
        self.event_id = str(Event.meta["unique_id"])
        self.event_type = kwargs["type"]
        self.event_level = kwargs["level"]
        self.event_category = kwargs["cat"]
        self.event_timestamp = time.strftime("%d/%m/%Y %I:%M:%S")
        self.event_description = kwargs['desc']
        self.event_acknowledge = False
        Event.table[str(Event.meta["unique_id"])] = self.__dict__
        print(str(self))

    def __str__(self):
        return (self.event_id + ": "
                # + (self.event_type + " " * 8)[:8]
                # + (self.event_level + " " * 8)[:8]
                + (self.event_category + " " * 8)[:8]
                # + (self.event_timestamp + " " * 20)[:20]
                # + (str(self.event_acknowledge) + " " * 6)[:6]
                + (self.event_description + " " * 160)[:160])

    def flip_acknowledge(self):
        """docstring"""
        if self.event_acknowledge:
            self.event_acknowledge = False
        else:
            self.event_acknowledge = True
