"""Class Lookup
"""
from boule import Boule


class Lookup(Boule):
    """
    Class Lookup
    Properties: ladder_id, match_id

    Methods:    __init__(self, ladder_id, match_id)
                __str__(self)
                get_mids_for_given_lid (ladder_id)
                get_lids_for_given_mid (match_id
                LadderMatch_exists (ladder_id, match_id)
                get_full_MatchLadderMatch_list ()
                delete_match_from_ladder (ladder_id, match_id)
    """
    # pylint: disable=W0231

    NAME = 'lookup'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    meta = {"unique_id": 0, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new match/ladder combination
    def __init__(self, id1, id2):
        self._id1 = id1
        self._id2 = id2

    @property
    def id1(self):
        return self._id1

    @property
    def id2(self):
        return self._id2

    @property
    def id_pair(self):
        return [self._id1, self._id2]
