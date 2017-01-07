"""Class LadderMatch
"""
from boule import Boule


class LadderMatch(Boule):
    """
    Class LadderMatch
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

    NAME = 'ladder_match'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = []
    meta = {"unique_id": 0, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new match/ladder combination
    def __init__(self, l_id, m_id):
        self.ladder_id = l_id
        self.match_id = m_id
        LadderMatch.table.append(self)

    # define __str___ output
    def __str__(self):
        return ("<ladder_match>\n"
                + "  <ladder_id>" + self.ladder_id + "</ladder_id>\n"
                + "  <match_id>" + self.match_id + "</match_id>\n"
                + "</ladder_match>\n")

    @classmethod
    def get_all_matches(cls, l_id):
        """get_all_matches
        return all teams names in the specified ladder
        along with their ids - in ranking order (highest first) maybe?
        """
        result = []
        for row in cls.table:
            if row.ladder_id == l_id:
                result = result + ("<laddermatch>\n"
                                   + "  <matchid>" + str(row.match_id) + "</teamid>\n"
                                   + "  <name>" + "</name>\n"
                                   + "</ladderteams>\n")
        if result == "":
            return False
        else:
            return result

    @classmethod
    def get_mids_for_given_lid(cls, l_id):
        """Get all matches in a ladder
        return the array of match_id's if any exist, otherwise return False
        If status is given, only find matching items
        """
        result = []
        for row in cls.table:
            if row.ladder_id == l_id:
                # success = True
                result.append(row.match_id)
        return result

    @classmethod
    def get_lids_for_given_mid(cls, m_id):
        """Get all ladders for a match
        return the array of ladder_id's if any exist, otherwise return false
        """
        result = []
        for row in cls.table:
            if row.match_id == m_id:
                # success = True
                result.append(row.ladder_id)
        return result

    @classmethod
    def exists(cls, l_id, m_id):
        """docstring"""
        # check if and id / id combination exists n one of our lookup tables
        for row in cls.table:
            if row.ladder_id == l_id and row.match_id == m_id:
                return True
        return False

    @classmethod
    def delete_match_from_ladder(cls, l_id, m_id):
        """Delete a match from a ladder (for admin use only)
        Also, modifying the matchs in a ladder is an admin only action
        achieved by deleting a row, and adding a new one
        returns True = successful delete or False = combination not found
        """
        for row in cls.table:
            if row.ladder_id == l_id and row.match_id == m_id:
                LadderMatch.table.remove(row)
                return True
        return False
