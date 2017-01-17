"""Class Lookup
"""
from boules import Boules


class Lookup(Boules):
    """
    Class Lookup
    Properties: id1, id2, id_pair
    """
    # pylint: disable=W0231

    NAME = 'lookup'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    meta = {"unique_id": 0, "author": "large", "version": "1.0.0", "last_saved": ""}

    def __init__(self, id1, id2):
        self._id1 = str(id1)
        self._id2 = str(id2)

    @property
    def id1(self):
        return self._id1

    @property
    def id2(self):
        return self._id2

    @property
    def id_pair(self):
        return [self._id1, self._id2]
