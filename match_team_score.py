"""docstring"""
from boules import Boules


class MatchTeamScore(Boules):
    """
    Class Team
    Properties: match_id {int}, account_id {int}, score {list of int}

    Methods:    add
                delete
    """
    # pylint: disable=W0231

    NAME = 'match_team_score'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = []
    meta = {"unique_id": 0, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new match team combination
    def __init__(self, m_id, t_id, list_scores):
        self.match_id = m_id
        self.team_id = t_id
        self.scores = list_scores
        MatchTeamScore.table.append(self)

    # define __str___ output
    def __str__(self):
        return ("<match_team_score>\n"
                + "  <match_id>" + self.match_id + "</match_id>\n"
                + "  <team_id>" + self.team_id + "</team_id>\n"
                + "  <score>" + self.scores + "</score_id>\n"
                + "</match_team_score>\n")

    def get_match_team_score(self):
        """docstring"""
        return self.scores

    def set_match_team_score(self, l_score):
        """docstring"""
        self.scores = l_score

    @classmethod
    def get_tids_for_given_mid(cls, m_id):
        """Get all accounts or teams and their scores for a given match
        return a list of account_id/team_id's and the score if any exist, otherwise return False
        """
        result = []
        # print ("get_tids_for_given_mid : ", m_id)
        for row in cls.table:
            if row.match_id == m_id:
                result.append([row.team_id, row.scores])
        return result

    @classmethod
    def get_mids_for_given_tid(cls, t_id):
        """Get all matches for a given account or team
        return the array of match_id's if any exist, otherwise return false
        """
        result = []
        for row in cls.table:
            if row.team_id == t_id:
                result.append(row.match_id)
        return result

    @classmethod
    def exists(cls, m_id, t_id):
        """check if macth account/team combination already exists
        """
        for row in cls.table:
            if row.match_id == m_id and row.team_id == t_id:
                return True
        return False

    @classmethod
    def delete_match_team_entry(cls, m_id, t_id):
        """Delete a account from a team (for admin use only)
        Also, modifying the accounts in a team is an admin only action
        achieved by deleting a row, and adding a new one
        returns True = successful delete or False = combination not found
        """
        for row in cls.table:
            if row.match_id == m_id and row.team_id == t_id:
                cls.table.remove(row)
                return True
        return False
