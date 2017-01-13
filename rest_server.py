"""provide a web server and services for dev puposes
TODO: is this thread safe?
"""
import json
from bottle import route, run, request
import io
# from library import *
import data
import helper as help

# import setup_db
import boule
import ladder
import match
import team
import account
import lookup

# pylint: disable=R0904

accounts = []
teams = []
ladders = []
matches = []

account_team = []  # put each accounts in multiple teams. id1 = account (unique), id2 = team (0 to many)
team_ladder = []   # put each team in multiple ladders. id1 = team (unique), id2 = ladder (0 to many)
ladder_match = []  # for each ladder store mulitple matches
match_team_score = []   # for each match add two teams + scores (tuples) per game

tables = {"account":accounts, "team":teams, "match":matches, "ladder":ladders}

BASIC_PARAM_SET = {'name': '', 'second_name': '', 'nickname': '', 'email': '',
                   'mobile': '', 'ranking': data.DEFAULT_RANKING,
                   'proliferate': False}

def return_helper(result):
    result_string = "["
    if not result:
        return "[]"
    if type(result) is list: 
        for item in result:
            result_string = result_string + json.dumps(item.__dict__, indent=2) + ", "
        return result_string[:-2] + "]"
    return json.dumps(result.__dict__, indent=2)

"""
All the GET commands
Syntax:
get /account/            returns ids of all accounts along with their names and all other details
get /team/               returns names of all teams along with their ids
get /match/              returns names all matches along with their ids
get /ladder/             returns names of all ladders along with their 

get /account/<status>/      return accounts of given status {active|hold|pending|suspended|deleted|complete}
get /team/<status>/         return teams of given status {active|hold|pending|suspended|deleted|complete}
get /match/<status>/        return matchs of given status {active|hold|pending|suspended|deleted|complete}
get /ladder/<status>/       return ladders of given status {active|hold|pending|suspended|deleted|complete}

get /account/id         returns account details for the given name|id - name, my_id, nickname, date created,
                        date modified, email, mobile
get /team/id            returns team details for the given name|id - name, my_id, date created, date modified,
                        accounts, ranking
get /match/id            returns details for the match id given - name, my_id, date created, teams, score
get /ladder/id/          returns details for name|id given - name, my_id, date created

get /account/total          return total number of accounts
get /team/total             return total number of teams
get /match/total            return total number of matches
get /ladder/total           return total number of ladders

get /account/<status>/total return accounts of given status {active|hold|pending|suspended|deleted|complete}
get /team/<status>/total    return teams of given status {active|hold|pending|suspended|deleted|complete}
get /match/<status>/total   return matchs of given status {active|hold|pending|suspended|deleted|complete}
get /ladder/<status>/total  return number of teams in ladders of given status
                            {active|hold|pending|suspended|deleted|complete}

get /account/id/teams    returns a list of the teams for which the given account is a member
get /team/id/matches     returns the matches played by the given team id
get /team/id/accounts    returns the accounts making up the given team
get /team/id/ladders     returns the ladders containing the given team
get /match/id/teams      returns teams and scores for the given match id
get /match/id/ladders    returns ladder deatails for the given match id
get /ladder/id/teams/    returns all teams names in the specified ladder along with their ids
                         in ranking order(highest first)
get /ladder/id/matches/  returns all ladder match names, ids, teams, and scores in date order(newest first)

get /database            load the databases from disk - WARNING overwrites anything currently in memory

get /event
get /event/id
get /event/total

TODO
get /event/last&number=number_of_events
get /event/today
get /event/since&datetime=datestring

get /account|team|match|ladder/created&since=datestring
get /account|team|match|ladder/modifed&since=datestring
"""


@route('/<table:re:account|team|match|ladder>/', method='GET')
@route('/<table:re:account|team|match|ladder>', method='GET')
def get_all(table):
    """docstring"""
    result_items = tables[table]
    return return_helper(result_items)


@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/', method='GET')
@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>', method='GET')
def get_all_by_status(table, status):
    """docstring"""
    result_items = help.get_items_by_value(tables[table], "status", status)
    return return_helper(result_items)

@route('/<table:re:account|team|match|ladder>/<i_id:int>/', method='GET')
@route('/<table:re:account|team|match|ladder>/<i_id:int>', method='GET')
def get_table_by_id(table, i_id):
    """docstring"""
    result_items = help.get_item_by_id(tables[table], str(i_id))
    return return_helper(result_items)


@route('/<table:re:account|team|match|ladder>/total/', method='GET')
@route('/<table:re:account|team|match|ladder>/total', method='GET')
def get_size_of_table(table):
    """docstring"""
    return str(len(tables[table]))


@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/total/', method='GET')
@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/total', method='GET')
def get_size_of_table_status(table, status):
    """docstring"""
    result_list = help.get_items_by_value(tables[table], "status", status)
    return str(len(result_list))


@route('/account/<i_id:int>/teams/', method='GET')
@route('/account/<i_id:int>/teams', method='GET')
def get_teams_for_account(i_id):
    """docstring"""
    # get all team lookups for given account id
    lookup_list = help.get_items_by_value(account_team, "id1", str(i_id))
    print(lookup_list)
    # for each team lookup, pull the team id, and get the associated team data
    # put the result in a json formatted string
    result_items = []
    for item in lookup_list:
        team = help.get_item_by_id(teams, item.id2)
        result_items.append(team)
    print("***HERE***", result_items)
    return return_helper(result_items)


@route('/team/<i_id:int>/accounts/', method='GET')
@route('/team/<i_id:int>/accounts', method='GET')
def get_accounts_for_team(i_id):
    """docstring"""
    # get all account lookups for given team id
    lookup_list = help.get_items_by_value(account_team, "id2", str(i_id))
    # for each account lookup, pull the account instance, and get the associated data
    # put the result in a json formatted string
    result_items = []
    for item in lookup_list:
        account = help.get_item_by_id(accounts, item.id1)
        result_items.append(account)
    return return_helper(result_items)


@route('/team/<i_id:int>/ladders/', method='GET')
@route('/team/<i_id:int>/ladders', method='GET')
def get_ladders_for_team(i_id):
    """docstring"""
    # get all ladder lookups for given team id
    lookup_list = help.get_items_by_value(team_ladder, "id1", str(i_id))
    # for each lookup, pull the team instance, and get the associated data
    # put the result in a json formatted string
    # print("*** length of lookup list ***", len(lookup_list))
    result_items = []
    for item in lookup_list:
        ladder = help.get_item_by_id(ladders, item.id2)
        result_items.append(ladder)
    return return_helper(result_items)

# TODO does this need scores
@route('/team/<i_id:int>/matches/', method='GET')
@route('/team/<i_id:int>/matches', method='GET')
def get_matches_for_team(i_id):
    """docstring"""
    # get all account lookups for given team id
    lookup_list = help.get_items_by_value(match_team_score, "id2", str(i_id))
    # for each account lookup, pull the account id, and get the associated account data
    # put the result in a json formatted string
    result_items = []
    for item in lookup_list:
        match = help.get_item_by_id(matches, item.id1)
        result_items.append(match)
    return return_helper(result_items)

# TODO does this needs scores
@route('/match/<i_id:int>/teams/', method='GET')
@route('/match/<i_id:int>/teams', method='GET')
def get_teams_for_match(i_id):
    """docstring"""
    # get all match lookups for given team id
    lookup_list = help.get_items_by_value(match_team_score, "id1", str(i_id))
    # for each account lookup, pull the account id, and get the associated account data
    # put the result in a json formatted string
    result_items = []
    for item in lookup_list:
        team = help.get_item_by_id(teams, item.id2)
        result_items.append(team)
    return return_helper(result_items)


@route('/match/<i_id:int>/ladders/', method='GET')
@route('/match/<i_id:int>/ladders', method='GET')
def get_ladders_for_match(i_id):
    """docstring"""
    # get all account lookups for given team id
    lookup_list = help.get_items_by_value(ladder_match, "id2", str(i_id))
    # for each account lookup, pull the account id, and get the associated account data
    # put the result in a json formatted string
    result_items = []
    for item in lookup_list:
        ladder = help.get_item_by_id(ladders, item.id1)
        result_items.append(ladder)
    return return_helper(result_items)


@route('/ladder/<i_id:int>/teams/', method='GET')
@route('/ladder/<i_id:int>/teams', method='GET')
def get_teams_for_ladder(i_id):
    """docstring"""
    # get all account lookups for given team id
    lookup_list = help.get_items_by_value(team_ladder, "id2", str(i_id))
    # for each account lookup, pull the account id, and get the associated account data
    # put the result in a json formatted string
    result_items = []
    for item in lookup_list:
        team = help.get_item_by_id(teams, item.id1)
        result_items.append(team)
    return return_helper(result_items)


@route('/ladder/<i_id:int>/matches/', method='GET')
@route('/ladder/<i_id:int>/matches', method='GET')
def get_matches_for_ladder(i_id):
    """docstring"""
    # get all account lookups for given team id
    result_list = help.get_items_by_value(ladder_match, "id1", str(i_id))
    result = ""
    # for each account lookup, pull the account id, and get the associated account data
    # put the result in a json formatted string
    result_items = []
    for item in result_list:
        match = help.get_item_by_id(matches, item.id2)
        result_items.append(match)
    return return_helper(result_items)

# TODO fix this one
@route('/database/', method='GET')
@route('/database', method='GET')
def get_database():
    """docstring"""
    load_all_tables()
    return json.dumps({"response": 'database loaded'}, indent=2)

# TODO fix this one
@route('/event/', method='GET')
@route('/event', method='GET')
def get_event():
    """docstring"""
    result = read_event()
    s_result = ""
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result

# TODO fix this one
@route('/event/<event_id:int>/', method='GET')
@route('/event/<event_id:int>', method='GET')
def get_event_id(event_id):
    """docstring"""
    event_id = str(event_id)
    result = read_event(my_id=event_id)
    if result:
        return "<p>" + json.dumps(result, indent=2) + "</p>"
    else:
        return "<p>ID not found</p>"

# TODO fix this one
@route('/event/total/', method='GET')
@route('/event/total', method='GET')
def total_event_id():
    """docstring"""
    return json.dumps({"response": size_of_event}, indent=2)

"""
All the POST commands
Syntax:
Data provided in the body of the POST request. Settings data provided in the body of the POST request
Everything is done in JSON format
New account can be added to a new team and that team added to the default ladder by setting {'proliferate':True}
The id of each is auto-generated: accounts = 1xxxxxxx, teams = 2xxxxxxx, matches = 3xxxxxxx, ladders = 4xxxxxxx
post /ladder   create a new ladder      
post /match/   create a new match       
post /account/ create a new account     
post /team/    create a new team        
NOTE: currently only id supported not name
"""

@route('/account', method='POST')
@route('/account/', method='POST')
def post_new_account():
    """docstring"""
    bytesio_body_json = request.body                    # gives us a type<byteIO> object
    b_body_json = bytesio_body_json.getvalue()          # convert to type<byte> object
    s_body_json = b_body_json.decode(encoding="UTF-8")  # convert to string
    data_dict = json.loads(s_body_json)                 # convert to dictionary
    # FIXME insufficient checking    
    temp_item = account.Account()
    accounts.append(temp_item)
    for key, value in data_dict.items():
        setattr(temp_item, key, value)
    return json.dumps({"id": temp_item.id}, indent=2)

@route('/team', method='POST')
@route('/team/', method='POST')
def post_new_team():
    """docstring"""
    bytesio_body_json = request.body                    # gives us a type<byteIO> object
    b_body_json = bytesio_body_json.getvalue()          # convert to type<byte> object
    s_body_json = b_body_json.decode(encoding="UTF-8")  # convert to string
    data_dict = json.loads(s_body_json)                 # convert to dictionary
    # FIXME insufficient checking    
    temp_item = team.Team(data_dict["name"])
    teams.append(temp_item)
    return json.dumps({"id": temp_item.id}, indent=2)

@route('/ladder', method='POST')
@route('/ladder/', method='POST')
def post_new_ladder():
    """docstring"""
    bytesio_body_json = request.body                    # gives us a type<byteIO> object
    b_body_json = bytesio_body_json.getvalue()          # convert to type<byte> object
    s_body_json = b_body_json.decode(encoding="UTF-8")  # convert to string
    data_dict = json.loads(s_body_json)                 # convert to dictionary
    # FIXME insufficient checking
    temp_item = ladder.Ladder(data_dict["name"])
    ladders.append(temp_item)
    return json.dumps({"id": temp_item.id}, indent=2)

@route('/match', method='POST')
@route('/match/', method='POST')
def post_new_match():
    """docstring"""
    bytesio_body_json = request.body                    # gives us a type<byteIO> object
    b_body_json = bytesio_body_json.getvalue()          # convert to type<byte> object
    s_body_json = b_body_json.decode(encoding="UTF-8")  # convert to string
    data_dict = json.loads(s_body_json)                 # convert to dictionary
    # FIXME insufficient checking
    temp_item = match.Match(data_dict["name"])
    matches.append(temp_item)
    return json.dumps({"id": temp_item.id}, indent=2)

"""
All the PUT commands
Syntax:
put /ladder/id/team/id                  adds a team to the ladder
put /ladder/id/match/id                 adds a match to the ladder
put /team/id/account/id                 adds an account to a team
put /match/id/team/id/score             adds an team to a match with a score

put /database                           save the database to disk WARNING overwrites the existing stored copy
TODO: rotate databases(on each save, store the latest and remove any older than a week?)

put /account/id/status/<status>       update the status of the given account
put /team/id/status/<status>          update the status of the given account
put /match/id/status/<status>         update the status of the given account
put /ladder/id/status/<status>        update the status of the given account

put /ladder/id/name/<name>      update the Ladder with given id - can only change 'name'('size' is covered automatic)
put /match/id/name/<name>       update the match with given id - can only change 'name'
put /team/id/name/<name>        update the team with given id - can only change 'name'
                                ('ranking' and 'size' are automatic)
put /account/id/details         update the account with given id - can change 'name'
                                'second_name' 'mobile' 'email' 'nickname'

NOTE: currently only id supported not name
"""


@route('/ladder/<lid:int>/team/<tid:int>', method='PUT')
@route('/ladder/<lid:int>/team/<tid:int>/', method='PUT')
def put_team_in_ladder(lid, tid):
    """docstring"""
    lookup_item = lookup.Lookup(str(tid), str(lid))
    team_ladder.append(lookup_item)
    return "[]"
    # json.dumps({"response": 'failed to update. One of both ids are invalid, or ladder is full'}, indent=2)


@route('/ladder/<lid:int>/match/<mid:int>', method='PUT')
@route('/ladder/<lid:int>/match/<mid:int>/', method='PUT')
def put_match_in_ladder(lid, mid):
    """docstring"""
    lookup_item = lookup.Lookup(str(lid), str(mid))
    ladder_match.append(lookup_item)
    return "[]"
    # json.dumps({"response": 'failed to update. One of both ids are invalid, or ladder is full'}, indent=2)


@route('/team/<tid:int>/account/<aid:int>', method='PUT')
@route('/team/<tid:int>/account/<aid:int>/', method='PUT')
def put_account_in_team(aid, tid):
    """docstring"""
    lookup_item = lookup.Lookup(str(aid), str(tid))
    account_team.append(lookup_item)
    return "[]"
    # json.dumps({"response": 'failed to update. One of both ids are invalid, or ladder is full'}, indent=2)

# TODO this needs sorting out
@route('/match/<mid:int>/team/<tid:int>/<my_path:path>', method='PUT')
@route('/match/<mid:int>/team/<tid:int>/<my_path:path>/', method='PUT')
def put_team_in_match(mid, tid, my_path):
    """docstring"""
    lookup_item = lookup.Lookup(str(mid), str(tid))
    match_team_score.append(lookup_item)
    return "[]"
    """
    l_score = my_path.split("/")
    result = True
    for item in l_score:
        if not item.isdigit():
            return json.dumps({s_mid + " " + s_tid: 'failed to update: invalid scores'}, indent=2)
    if add_team_to_match(s_mid, s_tid, l_score):
        return json.dumps({s_mid + " " + s_tid: 'added successfully'}, indent=2)
    else:
        return json.dumps({s_mid + " " + s_tid: 'failed to update. One of both ids are invalid, \
                          or match is already full, or too many scores'}, indent=2)
    """

@route('/<table:re:account|team|match|ladder>/<i_id:int>/status/<status:re:active|deleted|suspended|hold|pending|complete>/', method='PUT')
@route('/<table:re:account|team|match|ladder>/<i_id:int>/status/<status:re:active|deleted|suspended|hold|pending|complete>', method='PUT')
def put_table_status(table, i_id, status):
    """docstring"""
    temp_item = help.get_item_by_id(tables[table], str(i_id))
    temp_item.setattr(tables[table], "status", status)
    return json.dumps({"response": 'status changed successfully'}, indent=2)


@route('/<table:re:team|match|ladder>/<i_id:int>/name/<name>/', method='PUT')
@route('/<table:re:team|match|ladder>/<i_id:int>/name/<name>', method='PUT')
def put_table_name(table, i_id, name):
    """docstring"""
    temp_item = help.get_item_by_id(tables[table], str(i_id))
    temp_item.setattr(tables[table], "first_name", name)
    return json.dumps({"response": 'name changed successfully'}, indent=2)


@route('/<account>/<i_id:int>/name/<name>/', method='PUT')
@route('/account>/<i_id:int>/name/<name>', method='PUT')
def put_account_name(table, i_id, name):
    """docstring"""
    temp_item = help.get_item_by_id(accounts, str(i_id))
    temp_item.setattr(accounts, "first_name", name)
    return json.dumps({"response": 'name changed successfully'}, indent=2)


@route('/database', method='PUT')
@route('/database/', method='PUT')
def put_database():
    """docstring"""
    result = save_all_tables()
    if result:
        return json.dumps({"response": result}, indent=2)
    else:
        return json.dumps({"response": result}, indent=2)

"""
All the DELETE commands
Syntax:
delete /account/id          delete an account. account cannot be deleted if it exists in a team with others,
                            or if the team is part of a match, simply mark the account as "deleted"
                            and any teams as "suspended"
delete /team/id             delete a new team
delete /match/id            delete a match, remeove the asscoiation of that match from ladders and team
delete /ladder/id           deleting a ladder also deletes the associated matches, match associations,
                            and team associations it does not delete the teams

delete /database

TODO:
delete /ladder/id/team/id   disassociates the team from the ladder, also deletes matches featuring that team, and
                            disassociates those matches from the ladder. It does not delete the team
delete /ladder/id/match/id  delete a match from the ladder
delete /team/id/account/id  deletes an account from a team
delete /match/id/team/id    deletes an account from a team
delete /account/id/force    delete an account, any teams, any matches with that team, remove that team from
                            all ladders, all matches

NOTE: currently only id supported not name
"""


@route('/<table:re:account|team|match|ladder>/<i_id:int>/', method='DELETE')
@route('/<table:re:account|team|match|ladder>/<i_id:int>', method='DELETE')
def delete_any(table, i_id):
    """docstring"""
    my_id = str(i_id)
    result = delete_from_any(my_id)
    return json.dumps({"response": result}, indent=2)
    

@route('/database', method='DELETE')
@route('/database/', method='DELETE')
def delete_database():
    """docstring"""
    result = delete_all_tables()
    return json.dumps({"response": result}, indent=2)

# import setup_db

if __name__ == "__main__":
    # execute only if run as a script
    run(host='localhost', port=8080, debug=True)


