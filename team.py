"""docstring"""
from boule import Boule
import time
import data

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

    meta = {"unique_id": 20000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor   

    # initialise a new team
    def __init__(self, team_name="---", team_ranking=data.DEFAULT_RANKING):
        super().__init__()
        Team.meta["unique_id"] += 1
        self._id = str(Team.meta["unique_id"])
        self._name = team_name
        self._ranking = team_ranking

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

    @property
    def ranking(self):
        return self._team_ranking

    @ranking.setter
    def ranking(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._ranking = value
