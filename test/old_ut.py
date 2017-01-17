"""creat a basic data structure"""
# setup a basic db
import setup_db

from random import randint
from rest_server import *

from bottle import request, run, post, tob
import io
import json


BASE = {"name": "--", "second_name": "--", "nickname": "--", "email": "--", 
        "mobile": "--", "ranking":1600, "proliferate":True}

def set_up_post(body):
    request.bind({})
    s_body_json = json.dumps(body, indent=2)
    request.environ['CONTENT_LENGTH'] = str(len(tob(s_body_json)))
    request.environ['wsgi.input'] = io.BytesIO()
    request.environ['wsgi.input'].write(tob(s_body_json))
    request.environ['wsgi.input'].seek(0)

# now run a load more tests
print("create a ladder with int name")
request.bind({})
body = {**BASE, **{"name": 23}}  # name is type int, should be str
set_up_post(body)
s_response = post_table('ladder')
result = json.loads(s_response)
assert not result["response"]

print("create a ladder with bool name")
request.bind({})
body = {**BASE, **{"name": False}}  # name is type bool, should be str
set_up_post(body)
s_response = post_table('ladder')
result = json.loads(s_response)
print ("RESULT : ", result)
assert not result["response"]

print("create a ladder with list name")
request.bind({})
body = {**BASE, **{"name": ["foo", "bar", 1]}}  # name is type list, should be str
set_up_post(body)
s_response = post_table('ladder')
result = json.loads(s_response)
assert not result["response"]

print("create a ladder with a dict name")
request.bind({})
body = {**BASE, **{"name": {}}}  # name is type dict, should be str
set_up_post(body)
s_response = post_table('ladder')
result = json.loads(s_response)
assert not result["response"]

""" TODO this one does not work
print("create a ladder with wierd name")
request.bind({})
body = {**BASE, **{"name": "\n\t\n%20hello   \nworld"}}  # name is type list, should be str
set_up_post(body)
s_response = post_table('ladder')
result = json.loads(s_response)
assert result["response"] == "40000005"
"""

# /<table:re:account|team|match|ladder>
s_response = list_all_tables('account')
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 30, "not enough accounts"
s_response = list_all_tables('team')
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 40, "not enough teams"
s_response = list_all_tables('match')
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 60, "not enough matches"
s_response = list_all_tables('ladder')
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 4, "not enough ladders"

# /<table:re:account|team|match|ladder>/active
# should be the same
s_response = list_all_tables_status('account', "active")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 30, "not enough accounts"
s_response = list_all_tables_status('team', "active")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 40, "not enough teams"
s_response = list_all_tables_status('match', "active")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 60, "not enough matches"
s_response = list_all_tables_status('ladder', "active")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 4, "not enough ladders"

# /table:re:account|team|match|ladder>/deleted
# should be none
s_response = list_all_tables_status('account', "deleted")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 0, "not enough accounts"
s_response = list_all_tables_status('team', "deleted")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 0, "not enough teams"
s_response = list_all_tables_status('match', "deleted")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 0, "not enough matches"
s_response = list_all_tables_status('ladder', "deleted")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 0, "not enough ladders"

# move ladder 4 to deleted
s_response = put_table_status('ladder', 40000004, "deleted")
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))


# /<table:re:account|team|match|ladder>/<my_id:int>
# should be one
s_response = list_table_by_id('account', 10000004)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 1, "not enough accounts"
s_response = list_table_by_id('team', 20000014)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 1, "not enough teams"
s_response = list_table_by_id('match', 30000034)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 1, "not enough matches"
s_response = list_table_by_id('ladder', 40000002)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 1, "not enough ladders"

# /<table:re:account|team|match|ladder>/total
s_response = get_size_of_table('account')
result = json.loads(s_response)
assert result["size"] == 30, "not enough accounts"
s_response = get_size_of_table('team')
result = json.loads(s_response)
assert result["size"] == 40, "not enough teams"
s_response = get_size_of_table('match')
result = json.loads(s_response)
assert result["size"] == 60, "not enough matches"
s_response = get_size_of_table('ladder')
result = json.loads(s_response)
assert result["size"] == 4, "not enough ladders"

# /<table:re:account|team|match|ladder>/<status:re:active|deleted|suspended|hold|pending|complete>/total
s_response = get_size_of_table_status('account', "active")
result = json.loads(s_response)
assert result["size"] == 30, "not enough accounts"
s_response = get_size_of_table_status('team', "deleted")
result = json.loads(s_response)
assert result["size"] == 0, "not enough teams"
s_response = get_size_of_table_status('match', "hello")
result = json.loads(s_response)
assert result["size"] == 0, "not enough matches"
s_response = get_size_of_table_status('ladder', "deleted")
result = json.loads(s_response)
assert result["size"] == 1, "not enough ladders"

# /account/<my_id:int>/teams
s_response = list_teams_for_account(10000008)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 0, "not enough"

# /team/<my_id:int>/matches
s_response = list_matches_for_team(20000015)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 1, "not enough"

# /team/<my_id:int>/accounts
s_response = list_accounts_for_team(20000023)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 0, "not enough"

# /team/<my_id:int>/ladders
s_response = list_ladders_for_team(20000004)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 0, "not enough"

# /match/<my_id:int>/teams
s_response = list_teams_for_match(30000043)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 1, "not enough"

# /match/<my_id:int>/ladders
s_response = list_ladders_for_match(30000002)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 0, "not enough"

# /ladder/<my_id:int>/teams
s_response = list_teams_for_ladder(40000002)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 1, "not enough"

# /ladder/<my_id:int>/matches
s_response = list_matches_for_ladder(40000003)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) > 1, "not enough"

# /match/<my_id:int>/ladders with bad number
s_response = list_ladders_for_match(3)
result = json.loads(s_response.replace("<p>", "").replace("</p>", "").replace("}{", ","))
assert len(result) == 0, "not enough"

"""

# /<table:re:team|match|ladder>/<my_id:int>/<status:re:active|deleted|suspended|hold|pending|complete>/total
table_id_status_total(table, my_id, status)
s_response = table_id_status_total('account', my_id, status)
result = json.loads(s_response)
assert len(result["response"]) > 1, "not enough"

# /<table:re:team|match|ladder>/<my_id:int>/total
total_ladder_id(table, my_id):

# /database
get_database():

# /event
get_event():

# /event/<event_id:int>
get_event_id(event_id):

# /event/total
total_event_id()

print ("import of a db complete, now do other tests")
print("Add two more accounts")
params = {'name':'Bob', 'second_name':'Smith', 'nickname':'Smithy',
          'email':'bob@smith', 'mobile':'123456789', 'ranking':1600,
          'proliferate':True}
# profilerate causes a team to be created which is added to the default ladder
bob_account_id = create_table('account', params)
print("Account Bob: " + bob_account_id +" added")
params = {'name':'Augustus', 'second_name':'Gloop', 'nickname':'Oggy',
          'email':'august@gloop', 'mobile':'888888888', 'ranking':1600,
          'proliferate':False}
aug_account_id = create_table('account', params)
print("Account Augustus : " + aug_account_id +" added")

# check there are two accounts, one team called "Bob Smith", and that team is in the ladder
if not account_id_by_name("Bob Smith"):
    print("***** ERROR: newly created account is not there  *******")
    raise SystemExit

bob_team_id = team_id_by_name("Bob Smith's Team")
if not bob_team_id:
    print("***** ERROR: newly created team for Bob Smith is not there  *******")
    raise SystemExit
print("Bob's team ID : " + bob_team_id)

# check if Bob Smith is in the Default Ladder
if not entry_exists(Boules.DEFAULT_LADDER_ID, int(bob_team_id)):
    print("***** ERROR: Team Bob not in the ladder  *******")
    read_ladder("40000001")
    raise SystemExit

# check if Bob is in his own team
if not entry_exists(int(bob_team_id), int(bob_account_id)):
    print("***** ERROR: Team Bob not in a team  *******")
    raise SystemExit

if not account_id_by_name("Augustus Gloop"):
    print("***** ERROR: newly cerated account is not there  *******")
    raise SystemExit

if team_id_by_name("Augustus Gloop's Team"):
    print("***** ERROR: newly created account should not have a team  *******")
    raise SystemExit

# check if Augutus is in the Default Ladder
if entry_exists(Boules.DEFAULT_LADDER_ID, int(aug_account_id)):
    print("***** ERROR: Augustus' Team is in the ladder  *******")
    raise SystemExit

# check if Bob Augustus in his own team
if get_teams_per_account(my_id=aug_account_id):
    print("***** ERROR: Augusutus is in a Team  *******")
    raise SystemExit

print("checking that accounts exist")
if not id_exists(10000001):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(10000005):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(30000001):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(30000005):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(20000001):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(20000005):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(40000001):
    print("***** ERROR  *******")
    raise SystemExit
if not id_exists(40000003):
    print("***** ERROR  *******")
    raise SystemExit
print("...they do exist\n")

print("append random account entry with _messed with")
i_account_id_list = get_all_account_ids()
print(i_account_id_list)
id_inst = get_instance_by_id(i_account_id_list[randint(1, len(i_account_id_list))])
print (id_inst)
id_inst.set_name(id_inst.get_name() + "_messed with")
id_inst.set_second_name(id_inst.get_second_name() + "_messed with")
id_inst.set_nickname(id_inst.get_nickname() + "_messed with")
id_inst.set_email(id_inst.get_email() + "_messed with")
id_inst.set_mobile(id_inst.get_mobile() + "_messed with")
print("check that it worked")
if id_inst.get_name()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
if id_inst.get_second_name()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
if id_inst.get_nickname()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
if id_inst.get_email()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
if id_inst.get_mobile()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
print("Success")

print("append random team entry with _messed with")
i_team_id_list = get_all_team_ids()
id_inst = get_instance_by_id(i_team_id_list[randint(1, len(i_team_id_list))])
id_inst.set_name(id_inst.get_name() + "_messed with")
print("check that it worked")
if id_inst.get_name()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
print("Success")

print("append random match entry with _messed with")
i_match_id_list = get_all_match_ids()
id_inst = get_instance_by_id(i_match_id_list[randint(1, len(i_match_id_list))])
id_inst.set_name(id_inst.get_name() + "_messed with")
print("check that it worked")
if id_inst.get_name()[-11:] != "messed with":
    print("***** ERROR  *******")
    raise SystemExit
print("Success")

 not the ladder
print("append all  Ladder entries with _messed with")
for item in Ladder.get_full_table():
    params["name"] = item.get_name() + "_messed with"
    if not Ladder.update(item.get_id(), params):
        print("***** ERROR  *******")
        raise SystemExit

print("check that it worked")
for item in Ladder.get_full_table():
    if item.get_name()[-7:] != "updated":
        print("***** ERROR  *******")
        raise SystemExit
print("Success")

params["fn"] = input("First Name: ")
params["sn"] = input("Surname: ")
params["nn"] = input("Nickname: ")
params["em"] = input("Email: ")
params["mb"] = input("Mobile: ")
if not Account.update(args_list[1], params):
    print("***** ERROR  *******")
    raise SystemExit

print("save Account/Team/Match/Ladder databases")
Account.save_data()
Team.save_data()
Match.save_data()
Ladder.save_data()
LadderTeam.save_data()
TeamAccount.save_data()
LadderMatch.save_data()
MatchTeamScore.save_data()
print("success")

print("delete all Account entries")
for item in get_all_account_ids():
    if not delete(item):
        print("***** ERROR  *******")
        raise SystemExit
print("check that it worked")
for item in get_all_account_ids():
    item_inst = get_instance_by_id(item)
    if item_inst.get_status() != Boules.STATUS['deleted']:
        print("***** ERROR  *******")
        raise SystemExit
print("Success")

print("delete all Team entries")
for item in get_all_team_ids():
    if not delete(item):
        print("***** ERROR  *******")
        raise SystemExit
print("check that it worked")
for item in get_all_team_ids():
    item_inst = get_instance_by_id(item)
    if item_inst.get_status() != Boules.STATUS['deleted']:
        print("***** ERROR  *******")
        raise SystemExit
print("Success")

print("delete all Match entries")
for item in get_all_match_ids():
    if not delete(item):
        print("***** ERROR  *******")
        raise SystemExit
print("check that it worked")
for item in get_all_match_ids():
    item_inst = get_instance_by_id(item)
    if item_inst.get_status() != Boules.STATUS['deleted']:
        print("***** ERROR  *******")
        raise SystemExit
print("Success")

print("delete all Ladder entries")
for item in get_all_ladder_ids():
    if not delete(item):
        print("***** ERROR  *******")
        raise SystemExit
print("check that it worked")
for item in get_all_ladder_ids():
    item_inst = get_instance_by_id(item)
    if item_inst.get_status() != Boules.STATUS['deleted']:
        print("***** ERROR  *******")
        raise SystemExit
print("Success")

# Test meta get/set
print("Checking Account meta operations")
params_id = Account.get_meta_id()
params_author = Account.get_meta_author()
params_version = Account.get_meta_version()
params_last_saved = Account.get_meta_last_saved()

Account.set_meta_id(999)
Account.set_meta_author("bob")
Account.set_meta_version("999")
Account.set_meta_last_saved("tomorrow")

if Account.get_meta_id() != 999:
    print("***** ERROR  *******")
    raise SystemExit
if Account.get_meta_author() != "bob":
    print("***** ERROR  *******")
    raise SystemExit
if Account.get_meta_version() != "999":
    print("***** ERROR  *******")
    raise SystemExit
if Account.get_meta_last_saved() != "tomorrow":
    print("***** ERROR  *******")
    raise SystemExit

Account.set_meta_id(params_id)
Account.set_meta_author(params_author)
Account.set_meta_version(params_version)
Account.set_meta_last_saved(params_last_saved)
print("Success")

print("Checking Team meta operations")
params_id = Team.get_meta_id()
params_author = Team.get_meta_author()
params_version = Team.get_meta_version()
params_last_saved = Team.get_meta_last_saved()

Team.set_meta_id(999)
Team.set_meta_author("bob")
Team.set_meta_version("999")
Team.set_meta_last_saved("tomorrow")

if Team.get_meta_id() != 999:
    print("***** ERROR  *******")
    raise SystemExit
if Team.get_meta_author() != "bob":
    print("***** ERROR  *******")
    raise SystemExit
if Team.get_meta_version() != "999":
    print("***** ERROR  *******")
    raise SystemExit
if Team.get_meta_last_saved() != "tomorrow":
    print("***** ERROR  *******")
    raise SystemExit

Team.set_meta_id(params_id)
Team.set_meta_author(params_author)
Team.set_meta_version(params_version)
Team.set_meta_last_saved(params_last_saved)
print("Success")

print("Checking Match meta operations")
params_id = Match.get_meta_id()
params_author = Match.get_meta_author()
params_version = Match.get_meta_version()
params_last_saved = Match.get_meta_last_saved()

Match.set_meta_id(999)
Match.set_meta_author("bob")
Match.set_meta_version("999")
Match.set_meta_last_saved("tomorrow")

if Match.get_meta_id() != 999:
    print("***** ERROR  *******")
    raise SystemExit
if Match.get_meta_author() != "bob":
    print("***** ERROR  *******")
    raise SystemExit
if Match.get_meta_version() != "999":
    print("***** ERROR  *******")
    raise SystemExit
if Match.get_meta_last_saved() != "tomorrow":
    print("***** ERROR  *******")
    raise SystemExit

Match.set_meta_id(params_id)
Match.set_meta_author(params_author)
Match.set_meta_version(params_version)
Match.set_meta_last_saved(params_last_saved)
print("Success")

print("Checking Ladder meta operations")
params_id = Ladder.get_meta_id()
params_author = Ladder.get_meta_author()
params_version = Ladder.get_meta_version()
params_last_saved = Ladder.get_meta_last_saved()

Ladder.set_meta_id(999)
Ladder.set_meta_author("bob")
Ladder.set_meta_version("999")
Ladder.set_meta_last_saved("tomorrow")

if Ladder.get_meta_id() != 999:
    print("***** ERROR  *******")
    raise SystemExit
if Ladder.get_meta_author() != "bob":
    print("***** ERROR  *******")
    raise SystemExit
if Ladder.get_meta_version() != "999":
    print("***** ERROR  *******")
    raise SystemExit
if Ladder.get_meta_last_saved() != "tomorrow":
    print("***** ERROR  *******")
    raise SystemExit

Ladder.set_meta_id(params_id)
Ladder.set_meta_author(params_author)
Ladder.set_meta_version(params_version)
Ladder.set_meta_last_saved(params_last_saved)
print("Success")
"""

print("*** Overall Status SUCCESS ***")

