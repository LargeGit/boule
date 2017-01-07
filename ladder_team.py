"""Class LadderTeam"""
from boule import Boule


class LadderTeam(Boule):
    """
    Class LadderTeam
    Properties: ladder_id, account_id

    Methods:    add
                delete
    """
    # pylint: disable=W0231

    NAME = 'ladder_team'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = []
    meta = {"unique_id": 0, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new ladder/team combination
    def __init__(self, l_id, t_id):
        self.ladder_id = l_id
        self.team_id = t_id
        LadderTeam.table.append(self)

    # define __str___ output
    def __str__(self):
        return ("<team_match>\n"
                + "  <ladder_id>" + self.ladder_id + "</ladder_id>\n"
                + "  <team_id>" + self.team_id + "</team_id>\n"
                + "</team_match>\n")

    @classmethod
    def get_tids_for_given_lid(cls, lad_id):
        """Get all accounts or teams and their ranks for a given match
        return a list of account_id/team_id's and the rank if any exist, otherwise return False
        """
        # success = False
        result = []
        for row in cls.table:
            if row.ladder_id == lad_id:
                # success = True
                result.append(row.team_id)
        return result

    @classmethod
    def get_lids_for_given_tid(cls, t_id):
        """Get all ladder id for a given team id"""
        # success = False
        result = []
        for row in cls.table:
            if row.team_id == t_id:
                # success = True
                result.append(row.ladder_id)
        return result

    @classmethod
    def exists(cls, l_id, t_id):
        """check if macth account/team combination already exists"""
        for row in LadderTeam.table:
            if row.ladder_id == l_id and row.team_id == t_id:
                return True
        return False

    @classmethod
    def delete_team_from_ladder(cls, l_id, t_id):
        """Delete a account from a team (for admin use only)
        Also, modifying the accounts in a team is an admin only action
        achieved by deleting a row, and adding a new one
        returns True = successful delete or False = combination not found
        """
        for row in cls.table:
            if row.ladder_id == l_id and row.team_id == t_id:
                LadderTeam.table.remove(row)
                return True
        return False
