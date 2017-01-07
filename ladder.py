"""docstring"""
from boule import Boule
import time


class Ladder(Boule):
    """
    Class Ladder
    Properties: ladder_id, ladder_name, ladder_date_created,
                ladder_last_modified, ladder_status, ladder_accounts

    Methods: get all + get full name
             set all
             get meta["unique_id"]
    """

    NAME = 'ladder'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor

    meta = {"unique_id": 40000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new ladder
    def __init__(self, ladder_name="---"):
        super().__init__()
        Ladder.meta["unique_id"] += 1
        self._id = str(Ladder.meta["unique_id"])
        self._ladder_name = ladder_name

   @property
    def id(self):
        return self._id 

    @property
    def ladder_name(self):
        return self._ladder_name

    @ladder_name.setter
    def ladder_name(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._ladder_name = value