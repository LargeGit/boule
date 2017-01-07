"""module team_account"""
from boule import Boule


class TeamAccount(Boule):
    """
    Class TeamAccount
    Properties: team_id, account_id
    Methods:
    __init__(self, t_id, acc_id)
    __str__(self)
    @classmethod: get_aids_for_given_tid(cls, team_id)
    @classmethod: get_tids_for_given_aid(cls, acc_id)
    @classmethod: exists(cls, t_id, acc_id)
    @classmethod: def delete_account_from_team(cls, team_id, account_id)
    """
    # pylint: disable=W0231

    NAME = 'team_account'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = []
    meta = {"unique_id": 0, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new account/team combination
    def __init__(self, t_id, acc_id):
        self.team_id = t_id
        self.account_id = acc_id
        TeamAccount.table.append(self)

    # define __str___ output
    def __str__(self):
        return ("<team_account>\n"
                + "  <team_id>" + self.team_id + "</team_id\n"
                + "  <account_id>" + self.account_id + "</account_id>\n"
                + "</team_account>\n")

    @classmethod
    def get_aids_for_given_tid(cls, team_id):
        """Get all accounts in a team
        return the array of account_id's if any exist, otherwise return False
        """
        result = []
        for row in cls.table:
            if row.team_id == team_id:
                # success = True
                result.append(row.account_id)
        return result

    @classmethod
    def get_tids_for_given_aid(cls, acc_id):
        """Get all teams for a account
        return the array of team_id's if any exist, otherwise return falsedocstring
        """
        result = []
        for row in cls.table:
            if row.account_id == acc_id:
                # success = True
                result.append(row.team_id)
        return result

    @classmethod
    def exists(cls, t_id, acc_id):
        """check if id combination exists in the Team/Account lookup tables
        """
        for row in cls.table:
            if row.team_id == t_id and row.account_id == acc_id:
                return True
        return False

    @classmethod
    def delete_account_from_team(cls, team_id, account_id):
        """Delete a account from a team (for admin use only)
        Also, modifying the accounts in a team is an admin only action
        achieved by deleting a row, and adding a new one
        returns True = successful delete or False = combination not found
        """
        for row in cls.table:
            if row.team == team_id and row.account == account_id:
                TeamAccount.table.remove(row)
                return True
        return False
