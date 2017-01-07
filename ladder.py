"""docstring"""
from boule import Boule


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
    table = {}
    meta = {"unique_id": 40000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new ladder
    def __init__(self, my_dict):
        super().__init__(my_dict)
        Ladder.meta["unique_id"] += 1
        Ladder.table[str(Ladder.meta["unique_id"])] = self.__dict__
        self.s_id = str(Ladder.meta["unique_id"])
