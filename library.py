"""this file provides a higher level set of methods that access the data classes
to make any action atomic at the REST level(or any other interface)
TODO: pull out any non-class methods from the data classes, and put them here
"""

import data

from ladder_team import LadderTeam
from team_account import TeamAccount
from match_team_score import MatchTeamScore
from ladder_match import LadderMatch

from account import Account
from team import Team
from match import Match
from ladder import Ladder

from event import Event

from boule import Boule


def load_all_tables():
    """docstring"""
    Account.load_data()
    Team.load_data()
    Match.load_data()
    Ladder.load_data()
    LadderTeam.load_data()
    TeamAccount.load_data()
    LadderMatch.load_data()
    MatchTeamScore.load_data()
    Event.load_data()
    Event(type="system", level="info", cat="database", desc="all databases loaded into memory")
    return True


def save_all_tables():
    """docstring"""
    Account.save_data()
    Team.save_data()
    Match.save_data()
    Ladder.save_data()
    LadderTeam.save_data()
    TeamAccount.save_data()
    LadderMatch.save_data()
    MatchTeamScore.save_data()
    Event.save_data()
    Event(type="system", level="info", cat="database", desc="all databases saved to disk")
    return True


def delete_all_tables():
    """docstring"""
    if Account.database_file_exists():
        Account.database_file_remove()
    if Team.database_file_exists():
        Team.database_file_remove()
    if Match.database_file_exists():
        Match.database_file_remove()
    if Ladder.database_file_exists():
        Ladder.database_file_remove()
    if LadderTeam.database_file_exists():
        LadderTeam.database_file_remove()
    if TeamAccount.database_file_exists():
        TeamAccount.database_file_remove()
    if LadderMatch.database_file_exists():
        LadderMatch.database_file_remove()
    if MatchTeamScore.database_file_exists():
        MatchTeamScore.database_file_remove()
    if Event.database_file_exists():
        Event.database_file_remove()
    Event(type="system", level="warning", cat="database", desc="all databases files deleted")
    return True


def load_account_table():
    """docstring"""
    Account.load_data()
    Event(type="system", level="info", cat="database", desc="account database loaded")
    return True


def load_team_table():
    """docstring"""
    Team.load_data()
    Event(type="system", level="info", cat="database", desc="team database loaded")
    return True


def load_match_table():
    """docstring"""
    Match.load_data()
    Event(type="system", level="info", cat="database", desc="match database loaded")
    return True


def load_ladder_table():
    """docstring"""
    Ladder.load_data()
    Event(type="system", level="info", cat="database", desc="ladder database loaded")
    return True

BASIC_PARAM_SET = {'name': '', 'second_name': '', 'nickname': '', 'email': '',
                   'mobile': '', 'ranking': data.DEFAULT_RANKING, 'proliferate': False}


def create_table(table, passed_params):
    """create_account - usually called as a POST request
    """
    my_params = {**BASIC_PARAM_SET, **passed_params}
    if type(my_params['name']) != type(' ') \
            or type(my_params['second_name']) != type(' ') \
            or type(my_params['nickname']) != type(' ') \
            or type(my_params['email']) != type(' ') \
            or type(my_params['mobile']) != type(' '):
            event_text = "create failed - invalid paramters supplied. All should be type(str)"
            Event(type="system", level="info", cat="account", desc=event_text)
            return False
    if table == 'account':
        my_params['ranking'] = data.DEFAULT_RANKING
        if Account.details_exist(my_params):
            event_text = "account \"" + my_params["name"] + " " + my_params["second_name"] + \
                         "\"not created, duplicate details"
            Event(type="system", level="info", cat="account", desc=event_text)
            return False
        new_account_instance = Account(my_params)
        s_new_acc_id = new_account_instance.get_id()
        event_text = "Account: " + s_new_acc_id + ", created for user \"" + my_params["name"] + " " + \
                     my_params["second_name"] + "\""
        Event(type="system", level="info", cat="account", desc=event_text)
        my_params['name'] = new_account_instance.get_full_name(s_new_acc_id) + "'s Team"
        if my_params['proliferate']:
            new_team_instance = Team(my_params)
            new_team_id = new_team_instance.get_id()
            event_text = "Team: " + new_team_id + ", created with name \"" + my_params["name"] + "\""
            Event(type="system", level="info", cat="team", desc=event_text)
            add_account_to_team(new_team_id, s_new_acc_id)
            add_team_to_ladder(Boule.DEFAULT_LADDER_ID, new_team_id)
        return str(s_new_acc_id)
    if table == 'team':
        if Team.get_id_by_name(my_params["name"]):
            event_text = "Team not created due to duplicate name"
            Event(type="system", level="info", cat="team", desc=event_text)
            return False
        my_params['ranking'] = data.DEFAULT_RANKING
        new_team_instance = Team(my_params)
        new_team_id = new_team_instance.get_id()
        event_text = "Team: " + new_team_id + " created for team \"" + my_params["name"] + "\""
        Event(type="system", level="info", cat="team", desc=event_text)
        return str(new_team_instance.get_id())
    if table == 'match':
        if Match.get_id_by_name(my_params["name"]):
            event_text = "Match not created due to duplicate name"
            Event(type="system", level="info", cat="match", desc=event_text)
            return False
        new_match_instance = Match(my_params)
        new_match_id = new_match_instance.get_id()
        event_text = "Meam: " + new_match_id + " created with name \"" + my_params["name"] + "\""
        Event(type="system", level="info", cat="match", desc=event_text)
        return str(new_match_instance.get_id())
    if table == 'ladder':
        if Ladder.get_id_by_name(my_params["name"]):
            event_text = "Ladder not created due to duplicate name"
            Event(type="system", level="info", cat="ladder", desc=event_text)
            return False
        new_ladder_instance = Ladder(my_params)
        new_ladder_id = new_ladder_instance.get_id()
        event_text = "Ladder: " + new_ladder_id + " created with name \"" + my_params["name"] + "\""
        Event(type="system", level="info", cat="ladder", desc=event_text)
        return str(new_ladder_instance.get_id())


def read_tables(**kwargs):
    """docstring"""
    result = False
    if ("table" in kwargs) and kwargs["table"] == 'account':
        result = Account.get_all(**kwargs)
    if ("table" in kwargs) and kwargs["table"] == 'team':
        result = Team.get_all(**kwargs)
    if ("table" in kwargs) and kwargs["table"] == 'match':
        result = Match.get_all(**kwargs)
    if ("table" in kwargs) and kwargs["table"] == 'ladder':
        result = Ladder.get_all(**kwargs)
    return result


def nuclear_delete_account():
    """Very drastic - use with caution
    get list of teams containing this account
    get of matches containing all those teams
    get a list of all ladders containing those teams
    remove all the match entries from ladder_match, regardless of Ladder
    remove all the match entries from match_team_score, regardless of team (i.e. remove the opponents also)
    remove all the team_ladder entries, regardless of ladder
    remove all the team_account entries, regardless of account (i.e. remove teamates also)
    delete the account
    delate all teams
    """
    pass


def nuclear_delete_team():
    """docstring"""
    pass


def nuclear_delete_ladder():
    """docstring"""
    pass


def nuclear_delete_match(id_number):
    """docstring"""
    # TODO: this needs writing
    return id_number


def delete(id_number):
    """docstring"""
    # success = False
    if (Account.delete(id_number) or Match.delete(id_number)
            or Team.delete(id_number) or Ladder.delete(id_number)):
        event_text = "ID number: " + id_number + " deleted"
        Event(type="system", level="info", cat="table", desc=event_text)
        return True
    else:
        event_text = "ID number: " + id_number + " delete failed"
        Event(type="system", level="info", cat="table", desc=event_text)
        return False


def add_team_to_ladder(ladder_id, team_id):
    """docstring"""
    if not Ladder.id_exists(ladder_id) or not Team.id_exists(team_id):
        event_text = "Cannot add team: " + team_id + " to ladder: " + ladder_id + " - one or both do not exist"
        Event(type="system", level="info", cat="table", desc=event_text)
        return False
    if not LadderTeam.exists(ladder_id, team_id):
        LadderTeam(ladder_id, team_id)
        event_text = "Team: " + team_id + " added to ladder: " + ladder_id
        Event(type="system", level="info", cat="team", desc=event_text)
        return True
    else:
        Event(type="system", level="info", cat="team", desc="team already exists in ladder: no op")
        return True


def add_account_to_team(team_id, account_id):
    """docstring"""
    if not Team.id_exists(team_id) or not Account.id_exists(account_id):
        event_text = "Cannot add account: " + account_id + " to team: " + team_id + " - one or both do not exist"
        Event(type="system", level="info", cat="table", desc=event_text)
        return False
    if not TeamAccount.exists(team_id, account_id):
        TeamAccount(team_id, account_id)
        event_text = "Account : " + account_id + " added to team: " + team_id
        Event(type="system", level="info", cat="account", desc=event_text)
        return True
    else:
        event_text = "Account : " + account_id + " not added to team: " + team_id + " - combo already exists: no op"
        Event(type="system", level="info", cat="account", desc=event_text)
        return True        


def add_match_to_ladder(ladder_id, match_id):
    """docstring"""
    if not Ladder.id_exists(ladder_id) or not Match.id_exists(match_id):
        event_text = "Cannot add match: " + match_id + " to ladder: " + ladder_id + " - one or both do not exist"
        Event(type="system", level="info", cat="table", desc=event_text)
        return False
    if not LadderMatch.exists(ladder_id, match_id):
        LadderMatch(ladder_id, match_id)
        event_text = "Match: " + match_id + " added to ladder: " + ladder_id
        Event(type="system", level="info", cat="match", desc=event_text)
        return True
    else:
        event_text = "Match: " + match_id + " not added to ladder: " + ladder_id + " - combo already exists: no op"
        Event(type="system", level="info", cat="account", desc=event_text)
        return True 


def add_team_to_match(match_id, team_id, scores_list):
    """Add a Team (with a score) to a match, but only after running checks
    check mid exists and that tid exists
    check that the size of the match is currently <2
    you cabn't have more than 2 teams in a match, right
    """
    if len(scores_list) > 5:
        event_text = "Team: " + team_id + " not added to match:" + match_id + " - too many scores provided"
        Event(type="system", level="info", cat="match", desc=event_text)
        return False
    if not Match.id_exists(match_id) or not Team.id_exists(team_id):
        event_text = "Team: " + team_id + " not added to match:" + match_id + " - match or team (or both) do not exist"
        Event(type="system", level="info", cat="match", desc=event_text)
        return False
    if MatchTeamScore.exists(match_id, team_id):
        event_text = "Team: " + team_id + " not added to match:" + match_id + \
                     " - match/team combo already exists: no op"
        Event(type="system", level="info", cat="match", desc=event_text)
        return True
    if size_of(table='match', my_id=match_id) > 1:
        event_text = "Team: " + team_id + " not added to match:" + match_id + " - this match already has >1 teams"
        Event(type="system", level="info", cat="match", desc=event_text)
        return False
    MatchTeamScore(match_id, team_id, scores_list)
    event_text = "Team: " + team_id + " successfully added to match:" + match_id
    Event(type="system", level="info", cat="match", desc=event_text)
    return True


def get_accounts_per_team(**kwargs):
    """docstring"""
    success = False
    result = {}
    acc_ids = TeamAccount.get_aids_for_given_tid(kwargs["my_id"])
    if acc_ids:
        for acc_id in acc_ids:
            if ("status" in kwargs) and (Account.status_by_id(acc_id) != kwargs["status"]):
                continue
            result[str(acc_id)] = {'name': Account.get_name_by_id(acc_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_ladders_per_match(**kwargs):
    """docstring"""
    success = False
    result = {}
    ladder_ids = LadderMatch.get_lids_for_given_mid(kwargs["my_id"])
    if ladder_ids:
        for ladder_id in ladder_ids:
            if ("status" in kwargs) and (Ladder.status_by_id(ladder_id) != kwargs["status"]):
                continue
            result[str(ladder_id)] = {'name': Ladder.get_name_by_id(ladder_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_ladders_per_team(**kwargs):
    """docstring"""
    success = False
    result = {}
    ladder_ids = LadderTeam.get_lids_for_given_tid(kwargs["my_id"])
    if ladder_ids:
        for ladder_id in ladder_ids:
            if ("status" in kwargs) and (Ladder.status_by_id(ladder_id) != kwargs["status"]):
                continue
            result[str(ladder_id)] = {'name': Ladder.get_name_by_id(ladder_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_matches_per_team(**kwargs):
    """docstring"""
    success = False
    result = {}
    match_ids = MatchTeamScore.get_mids_for_given_tid(kwargs["my_id"])
    if match_ids:
        for match_id in match_ids:
            if ("status" in kwargs) and (Match.status_by_id(match_id) != kwargs["status"]):
                continue
            result[str(match_id)] = {'name': Match.get_name_by_id(match_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_matches_per_ladder(**kwargs):
    """docstring"""
    success = False
    result = {}
    match_ids = LadderMatch.get_mids_for_given_lid(kwargs["my_id"])
    if match_ids:
        for match_id in match_ids:
            if ("status" in kwargs) and (Match.status_by_id(match_id) != kwargs["status"]):
                continue
            result[str(match_id)] = {'name': Match.get_name_by_id(match_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_teams_per_account(**kwargs):
    """docstring"""
    success = False
    result = {}
    team_ids = TeamAccount.get_tids_for_given_aid(kwargs["my_id"])
    if team_ids:
        for team_id in team_ids:
            if ("status" in kwargs) and (Team.status_by_id(team_id) != kwargs["status"]):
                continue
            result[str(team_id)] = {'name': Team.get_name_by_id(team_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_teams_per_ladder(**kwargs):
    """docstring"""
    success = False
    result = {}
    team_ids = LadderTeam.get_tids_for_given_lid(kwargs["my_id"])
    if team_ids:
        for team_id in team_ids:
            if ("status" in kwargs) and (Team.status_by_id(team_id) != kwargs["status"]):
                continue
            result[str(team_id)] = {'name': Team.get_name_by_id(team_id)}
        success = True
    if success:
        return result
    else:
        return False


def get_teams_per_match(**kwargs):
    """docstring"""
    success = False
    result = {}
    team_ids = MatchTeamScore.get_tids_for_given_mid(kwargs["my_id"])
    if team_ids:
        for team_id in team_ids:   # team_ids is a list of [id, score] pairs
            if("status" in kwargs) and (Team.status_by_id(team_id[0]) != kwargs["status"]):
                continue
            result[str(team_id[0])] = {'name': Team.get_name_by_id(team_id[0]), 'score': team_id[1]}
        success = True
    if success:
        return result
    else:
        return False


def size_of(**kwargs):
    """Gives the number of accounts in a category=team
    or the number of teams in a category=ladder
    or the number of teams in a category=match
    for given status
    """
    if kwargs["table"] == 'ladder':
        result = get_teams_per_ladder(**kwargs)
        if result:
            return len(result)
        else:
            return 0
    if kwargs["table"] == 'team':
        result = get_accounts_per_team(**kwargs)
        if result:
            return len(result)
        else:
            return 0
    if kwargs["table"] == 'match':
        result = get_teams_per_match(**kwargs)
        if result:
            return len(result)
        else:
            return 0


def size_of_table(**kwargs):
    """Gives the number of accounts in a category=team
    or the number of teams in a category=ladder
    or the number of teams in a category=match
    for given status
    """
    if kwargs["table"] == 'ladder':
        return len(Ladder.get_all(**kwargs))
    if kwargs["table"] == 'team':
        return len(Team.get_all(**kwargs))
    if kwargs["table"] == 'match':
        return len(Match.get_all(**kwargs))
    if kwargs["table"] == 'account':
        return len(Account.get_all(**kwargs))


def update_status(**kwargs):
    """docstring"""
    result = False
    if "table" in kwargs and (kwargs["table"]) == 'account':
        result = Account.set_status(**kwargs)
    if "table" in kwargs and (kwargs["table"]) == 'team':
        result = Team.set_status(**kwargs)
    if "table" in kwargs and (kwargs["table"]) == 'match':
        result = Match.set_status(**kwargs)
    if "table" in kwargs and (kwargs["table"]) == 'ladder':
        result = Ladder.set_status(**kwargs)
    if result:
        return True
    else:
        return False


def update_name(**kwargs):
    """docstring"""
    result = False
    if "table" in kwargs and (kwargs["table"]) == 'team':
        result = Team.set_name(**kwargs)
    if "table" in kwargs and (kwargs["table"]) == 'match':
        result = Match.set_name(**kwargs)
    if "table" in kwargs and (kwargs["table"]) == 'ladder':
        result = Ladder.set_name(**kwargs)
    if result:
        return True
    else:
        return False


def update_account_details(d_details):
    success = False
    row = Account.get_instance_by_id(d_details["my_id"])
    if not row:
        return False        # Account ID not Found: no updates made
    if Account.details_exist(d_details):
        return False        # duplicate nickname, mobile or email: no updates made
    if "name" in d_details and d_details["name"] != "":
        row.set_name(d_details["name"])
        success = True
    if "second_name" in d_details and d_details["second_name"] != "":
        row.set_second_name(d_details["second_name"])
        success = True
    if "nickname" in d_details and d_details["nickname"] != "":
        row.set_nickname(d_details["nickname"])
        success = True
    if "email" in d_details and d_details["email"] != "":
        row.set_email(d_details["email"])
        success = True
    if "mobile" in d_details and d_details["mobile"] != "":
        row.set_mobile(d_details["mobile"])
        success = True
    if success:
        return True
    else:
        return False


def entry_exists(id1, id2):
    """docstring"""
    result = (TeamAccount.exists(id1, id2) or LadderMatch.exists(id1, id2)
              or LadderTeam.exists(id1, id2) or MatchTeamScore.exists(id1, id2))
    if result:
        return True
    else:
        return False


def id_number_exists(id_number):
    """docstring"""
    result = (Account.id_exists(id_number) or Team.id_exists(id_number)
              or Match.id_exists(id_number) or Ladder.id_exists(id_number))
    if result:
        return True
    else:
        return False


def account_id_by_name(name):
    """docstring"""
    result = Account.get_id_by_name(name)
    if result:
        return result
    else:
        return False


def team_id_by_name(name):
    """docstring"""
    result = Team.get_id_by_name(name)
    if result:
        return result
    else:
        return False


def get_all_account_ids(*status):
    """docstring"""
    result = Account.get_all_ids(*status)
    if result:
        return result
    else:
        return False


def get_all_team_ids(*status):
    """docstring"""
    result = Team.get_all_ids(*status)
    if result:
        return result
    else:
        return False


def get_all_match_ids(*status):
    """docstring"""
    result = Account.get_all_ids(*status)
    if result:
        return result
    else:
        return False


def get_all_ladder_ids(*status):
    """docstring"""
    result = Team.get_all_ids(*status)
    if result:
        return result
    else:
        return False


def get_instance_by_id(id_to_find):
    """docstring"""
    result = (Account.get_instance_by_id(id_to_find)
              or Team.get_instance_by_id(id_to_find)
              or Match.get_instance_by_id(id_to_find)
              or Ladder.get_instance_by_id(id_to_find))
    if result:
        return result
    else:
        return False


def read_event(**params):
    """docstring"""
    result = Event.get_all(**params)
    if result:
        return result
    else:
        return False


def size_of_event():
    """Gives the number of events in the database
    """
    result = Event.get_all()
    if result:
        return len(result)
    else:
        return False


def delete_from_any(my_id):
    result = Account.delete(my_id) or Team.delete(my_id) or Match.delete(my_id) or Ladder.delete(my_id)
    if result:
        return True
    else:
        return False       
