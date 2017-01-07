"""provide a web server and services for dev puposes
TODO: is this thread safe?
"""
import json
from bottle import route, run, request
import io
from library import *

import setup_db

BASIC_PARAM_SET = {'name': '', 'second_name': '', 'nickname': '', 'email': '',
                   'mobile': '', 'ranking': Boule.DEFAULT_RANKING,
                   'proliferate': False}

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
def list_all_tables(table):
    """docstring"""
    result = read_tables(table=table)
    s_result = ""
    if not result:
        return "<p>" + '{}' + "</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/', method='GET')
@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>', method='GET')
def list_all_tables_status(table, status):
    """docstring"""
    result = read_tables(table=table, status=status)
    s_result = ""
    if not result:
        return "<p>" + '{}' + "</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/<table:re:account|team|match|ladder>/<i_id:int>/', method='GET')
@route('/<table:re:account|team|match|ladder>/<i_id:int>', method='GET')
def list_table_by_id(table, i_id):
    """docstring"""
    my_id = str(i_id)
    result = read_tables(table=table, my_id=my_id)
    if result:
        return "<p>" + json.dumps(result, indent=2) + "</p>"
    else:
        return "<p>ID not found</p>"


@route('/<table:re:account|team|match|ladder>/total/', method='GET')
@route('/<table:re:account|team|match|ladder>/total', method='GET')
def get_size_of_table(table):
    """docstring"""
    result = size_of_table(table=table)
    if result:
        return json.dumps({'size': result}, indent=2)
    else:
        return json.dumps({'size': 0}, indent=2)


@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/total/', method='GET')
@route('/<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/total', method='GET')
def get_size_of_table_status(table, status):
    """docstring"""
    result = size_of_table(table=table, status=status)
    if result:
        return json.dumps({'size': result}, indent=2)
    else:
        return json.dumps({'size': 0}, indent=2)


@route('/account/<i_id:int>/teams/', method='GET')
@route('/account/<i_id:int>/teams', method='GET')
def list_teams_for_account(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_teams_per_account(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/team/<i_id:int>/matches/', method='GET')
@route('/team/<i_id:int>/matches', method='GET')
def list_matches_for_team(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_matches_per_team(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/team/<i_id:int>/accounts/', method='GET')
@route('/team/<i_id:int>/accounts', method='GET')
def list_accounts_for_team(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_accounts_per_team(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/team/<i_id:int>/ladders/', method='GET')
@route('/team/<i_id:int>/ladders', method='GET')
def list_ladders_for_team(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_ladders_per_team(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/match/<i_id:int>/teams/', method='GET')
@route('/match/<i_id:int>/teams', method='GET')
def list_teams_for_match(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_teams_per_match(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/match/<i_id:int>/ladders/', method='GET')
@route('/match/<i_id:int>/ladders', method='GET')
def list_ladders_for_match(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_ladders_per_match(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/ladder/<i_id:int>/teams/', method='GET')
@route('/ladder/<i_id:int>/teams', method='GET')
def list_teams_for_ladder(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_teams_per_ladder(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/ladder/<i_id:int>/matches/', method='GET')
@route('/ladder/<i_id:int>/matches', method='GET')
def list_matches_for_ladder(i_id):
    """docstring"""
    my_id = str(i_id)
    result = get_matches_per_ladder(my_id=my_id)
    s_result = ""
    if not result:
        return "<p>{}</p>"
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


@route('/database/', method='GET')
@route('/database', method='GET')
def get_database():
    """docstring"""
    load_all_tables()
    return json.dumps({"response": 'database loaded'}, indent=2)


@route('/event/', method='GET')
@route('/event', method='GET')
def get_event():
    """docstring"""
    result = read_event()
    s_result = ""
    for key in sorted(result, reverse=True):
        s_result = s_result + "<p>" + json.dumps({key: result[key]}, indent=2) + "</p>"
    return s_result


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


@route('/<table:re:account|team|match|ladder>', method='POST')
@route('/<table:re:account|team|match|ladder>/', method='POST')
def post_table(table):
    """docstring"""
    bytesio_body_json = request.body                    # gives us a type<byteIO> object
    b_body_json = bytesio_body_json.getvalue()          # convert to type<byte> object
    s_body_json = b_body_json.decode(encoding="UTF-8")  # convert to string
    d_body_json = json.loads(s_body_json)               # convert to dictionary
    result = create_table(table, d_body_json)           # TODO: there must be a better way
    return json.dumps({"response": result}, indent=2)

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
    s_lid = str(lid)
    s_tid = str(tid)
    if add_team_to_ladder(s_lid, s_tid):
        return json.dumps({"response": 'added successfully'}, indent=2)
    else:
        return json.dumps({"response": 'failed to update. One of both ids are invalid, or ladder is full'}, indent=2)


@route('/ladder/<lid:int>/match/<mid:int>', method='PUT')
@route('/ladder/<lid:int>/match/<mid:int>/', method='PUT')
def put_match_in_ladder(lid, mid):
    """docstring"""
    s_lid = str(lid)
    s_mid = str(mid)
    if add_match_to_ladder(s_lid, s_mid):
        return json.dumps({"response": 'added successfully'}, indent=2)
    else:
        return json.dumps({"response": 'failed to update. One of both ids are invalid'}, indent=2)


@route('/team/<tid:int>/account/<aid:int>', method='PUT')
@route('/team/<tid:int>/account/<aid:int>/', method='PUT')
def put_account_in_team(tid, aid):
    """docstring"""
    s_tid = str(tid)
    s_aid = str(aid)
    if add_account_to_team(s_tid, s_aid):
        return json.dumps({"response": 'added successfully'}, indent=2)
    else:
        return json.dumps({"response": 'failed to update. One of both ids are invalid'}, indent=2)


@route('/match/<mid:int>/team/<tid:int>/<my_path:path>', method='PUT')
@route('/match/<mid:int>/team/<tid:int>/<my_path:path>/', method='PUT')
def put_team_in_match(mid, tid, my_path):
    """docstring"""
    s_mid = str(mid)
    s_tid = str(tid)
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


@route('/<table:re:account|team|match|ladder>/<i_id:int>/status/<status:re:active|deleted|suspended|hold|pending|complete>/', method='PUT')
@route('/<table:re:account|team|match|ladder>/<i_id:int>/status/<status:re:active|deleted|suspended|hold|pending|complete>', method='PUT')
def put_table_status(table, i_id, status):
    """docstring"""
    my_id = str(i_id)
    if update_status(table=table, my_id=my_id, status=status):
        return json.dumps({"response": 'status changed successfully'}, indent=2)
    else:
        return json.dumps({"response": 'failed to update status'}, indent=2)


@route('/<table:re:team|match|ladder>/<i_id:int>/name/<name>/', method='PUT')
@route('/<table:re:team|match|ladder>/<i_id:int>/name/<name>', method='PUT')
def put_table_name(table, i_id, name):
    """docstring"""
    my_id = str(i_id)
    if update_name(table=table, my_id=my_id, name=name):
        return json.dumps({"response": 'name changed successfully'}, indent=2)
    else:
        return json.dumps({"response": 'failed to update name'}, indent=2)


@route('/<account>/<i_id:int>/name/<name>/', method='PUT')
@route('/account>/<i_id:int>/name/<name>', method='PUT')
def put_account_details(i_id):
    """docstring"""
    my_id = str(i_id)
    bytesio_body_json = request.body                    # gives us a type<byteIO> object
    b_body_json = bytesio_body_json.getvalue()          # convert to type<byte> object
    s_body_json = b_body_json.decode(encoding="UTF-8")  # convert to string
    d_body_json = json.loads(s_body_json)               # convert to dictionary
    d_body_json["my_id"] = my_id
    result = update_account_details(d_body_json)
    return json.dumps({"response": result}, indent=2)


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

if __name__ == "__main__":
    # execute only if run as a script
    run(host='localhost', port=8080, debug=True)
