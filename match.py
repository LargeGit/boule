"""docstring"""
from boule import Boule


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
    table = {}
    meta = {"unique_id": 30000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new match
    def __init__(self, my_dict):
        super().__init__(my_dict)
        Match.meta["unique_id"] += 1
        Match.table[str(Match.meta["unique_id"])] = self.__dict__
        self.s_id = str(Match.meta["unique_id"])
