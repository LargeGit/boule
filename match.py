"""docstring"""
from boule import Boule
import time


class Match(Boule):
    """
    Class Match
    Properties: match_id, match_name, match_date_created,
                match_last_modified, match_status, match_accounts

    Methods: get all + get full name
             set all
             get meta["unique_id"]
    """

    NAME = 'match'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor

    meta = {"unique_id": 30000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new match
    def __init__(self, match_name="---"):
        super().__init__()
        Match.meta["unique_id"] += 1
        self._id = str(Match.meta["unique_id"])
        self._name = match_name

    @property
    def id(self):
        return self._id 

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._name = value
