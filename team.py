"""docstring"""
from boule import Boule


class Team(Boule):
    """
    Class Team
    Properties: team_id, team_name, team_date_created,
                team_last_modified, team_status, team_accounts

    Methods: get all + get full name
             set all
             get meta["unique_id"]
    """
    NAME = 'team'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = {}
    meta = {"unique_id": 20000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new team
    def __init__(self, my_dict):
        super().__init__(my_dict)
        Team.meta["unique_id"] += 1
        self.ranking = my_dict['ranking']
        Team.table[str(Team.meta["unique_id"])] = self.__dict__
        self.s_id = str(Team.meta["unique_id"])
