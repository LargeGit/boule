
import sys
sys.path.append("C:\\Users\\jonba\\Desktop\\git_boules\\trunk\\")

import pytest

from random import randint

from rest_server import *

from bottle import request, run, post, tob
import io
import json


import helper as helper

BASE = {"first_name": "--", "second_name": "--", "nickname": "--", "email": "email@email.email",
        "mobile": "-0987654321", "ranking": 1600, "role": 1}

FIRST_NAMES = ['John', 'Sue', 'Bob', 'Steve', 'Andy', 'Dave', 'Dan', 'Simon',
               'Imogen', 'Keith', 'Eddy', 'Amanda', 'Trevor', 'Patrick', 'Sarah',
               'Liz', 'Tom', 'Nigel', 'Charlie', 'Fred', 'Geoff', 'Harry', 'Leo',
               'Malcolm', 'Oscar', 'Penny', 'Ron', 'Victoria', 'Brian', 'Chris']

SECOND_NAMES = ['Andrews', 'Bristow', 'Chambers', 'Davies', 'Edmonds', 'Flintstone',
                'Gibbons', 'Holmes', 'Innes', 'Jacobs', 'Kelly', 'Lambert', 'McBride',
                'Pearson', 'Quincey', 'Rowlands', 'Sanders', 'Smith', 'Williams',
                'Strachan', 'Charlton', 'Sarandon', 'DiCaprio', 'Dench', 'Atkinson',
                'Henry', 'Roberts', 'Singh', 'Chan', 'Rossi']

TEAM_NAMES = ['The Boulestiful Game', 'Billy Boules', 'Boulster Your Chances',
              'Ten Pin Bouling', 'Street Boulers', 'More Boules You',
              'Its all in the Wrist', 'Boules Bombers', 'Le Tosseurs',
              'Super Charged Chuckers', 'Golden Boules', 'Go Boules List Tick',
              'Boules Dah Dash', 'The Bouldies', 'Volley Boules', 'Foot Boules',
              'You Shall Go To The Boules', 'After the Boules is Over',
              'Boules Up', 'Boules Yer Eyes Out']
              
NICKNAMES = ['Skanks', 'Tricky', 'Hagar', 'BouleyBouley', 'Boulesboy', 'Yak', 'Tibbles',
             'Invincible Pants', 'Mouse', 'The Dolphin', 'Player X', 'Da Bomb',
             'My Luck', 'Lilypad', 'Ace', 'Old Blue Eyes', 'The Tall Man', 'Binky',
             'The Mighty Thwarb', 'Screech', 'Mr Pink', 'Oggy', 'Sniff', 'Egg',
             'Bouley McBoule', 'Abel Boulester', 'The Dark Destroyer', 'Sticky',
             'Smithy', 'Bobby']
LADDER_NAMES = ['Luckington Ladder', 'Under 21s', 'Veterans', 'Luckington Ladies']

ACC_LIST = [({"first_name": FIRST_NAMES[value], "second_name": SECOND_NAMES[value], "nickname": NICKNAMES[value]}, str(10000001 + value)) for value in range(4)]

TEAM_LIST = [(TEAM_NAMES[value], str(20000001 + value)) for value in range(4)]

LADDER_LIST = [(LADDER_NAMES[i], str(40000001 + i)) for i in range(4)]

def set_up_post(body1):
    request.bind({})
    s_body_json = json.dumps(body1, indent=2)
    request.environ['CONTENT_LENGTH'] = str(len(tob(s_body_json)))
    request.environ['wsgi.input'] = io.BytesIO()
    request.environ['wsgi.input'].write(tob(s_body_json))
    request.environ['wsgi.input'].seek(0)

@pytest.mark.parametrize("ladder_name, expected", [i for i in LADDER_LIST])
def test_create_ladder(ladder_name, expected):
    body = {"name": ladder_name}
    set_up_post(body)
    s_response = post_new_ladder()
    
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    result = result[0]
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["_id"]) is str, "return value in dict is not of correct type"
    assert result["_id"] == expected, "return value is not correct value, expected 40000001"
   
ladder1 = help.get_item_by_id(ladders, "40000001")
ladder2 = help.get_item_by_id(ladders, "40000002")
ladder3 = help.get_item_by_id(ladders, "40000003")
ladder4 = help.get_item_by_id(ladders, "40000004")


@pytest.mark.parametrize("account_details, expected", [i for i in ACC_LIST])
def test_create_account(account_details, expected):
    body = {**BASE, **account_details}
    set_up_post(body)
    s_response = post_new_account()
        
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    result = result[0]
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["_id"]) is str, "return value in dict is not of correct type"
    assert result["_id"] == expected, "return value is not correct"
  
account1 = help.get_item_by_id(accounts, "10000001")
account2 = help.get_item_by_id(accounts, "10000002")
account3 = help.get_item_by_id(accounts, "10000003")
account4 = help.get_item_by_id(accounts, "10000004")


@pytest.mark.parametrize("team_name, expected", [i for i in TEAM_LIST])
def test_create_team(team_name, expected):
    body = {"name": team_name}
    set_up_post(body)
    s_response = post_new_team()

    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    result = result[0]    
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["_id"]) is str, "return value in dict is not of correct type"
    assert result["_id"] == expected, "return value is not correct value, expected 40000001"
    
team1 = help.get_item_by_id(teams, "20000001")
team2 = help.get_item_by_id(teams, "20000002")
team3 = help.get_item_by_id(teams, "20000003")
team4 = help.get_item_by_id(teams, "20000004")


@pytest.mark.parametrize("match_name, expected", [("match" + str(i), str(30000001 + i)) for i in range(4)])
def test_create_match(match_name, expected):
    body = {"name": match_name}
    set_up_post(body)
    s_response = post_new_match()
    
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    result = result[0]
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["_id"]) is str, "return value in dict is not of correct type"
    assert result["_id"] == expected, "return value is not correct value, expected 40000001"
    
match1 = help.get_item_by_id(matches, "30000001")
match2 = help.get_item_by_id(matches, "30000002")
match3 = help.get_item_by_id(matches, "30000003")
match4 = help.get_item_by_id(matches, "30000004")


@pytest.mark.parametrize("account_id", [str(10000000 + i + 1) for i in range(4)])
@pytest.mark.parametrize("team_id", [str(20000000 + i + 1) for i in range(4)])
def test_add_account_to_team(account_id, team_id):
    response = put_account_in_team(account_id, team_id)
    assert response == "[]"

@pytest.mark.parametrize("team_id", [str(20000000 + i + 1) for i in range(4)])
@pytest.mark.parametrize("ladder_id", [str(40000000 + i + 1) for i in range(4)])    
def test_add_team_to_ladder(team_id, ladder_id):
    response = put_team_in_ladder(ladder_id, team_id)
    assert response == "[]"

@pytest.mark.parametrize("team_id", [str(20000000 + i + 1) for i in range(4)])
@pytest.mark.parametrize("match_id", [str(30000000 + i + 1) for i in range(4)])
def test_add_team_to_match(team_id, match_id):
    response = put_team_in_match(match_id, team_id, False)
    assert response == "[]"

@pytest.mark.parametrize("match_id", [str(30000000 + i + 1) for i in range(4)])
@pytest.mark.parametrize("ladder_id", [str(40000000 + i + 1) for i in range(4)])    
def test_add_match_to_ladder(match_id, ladder_id):
    response = put_match_in_ladder(ladder_id, match_id)
    assert response == "[]"

# now test all the gets
@pytest.mark.parametrize("table, expected", [("account", "1000000"), ("team", "2000000"), ("match", "3000000"), ("ladder", "4000000")])
def test_get_tables(table, expected):
    s_response = get_all(table)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert type(result) is list, "return does not convert to a list"
    assert type(result[0]) is dict, "return value in dict is not of correct type"
    for i in range(4):
        assert result[i]["_id"] == expected + str(i + 1), "return value is not correct value"

@pytest.mark.parametrize("table, id_to_change, status", [("account", "10000001", "deleted"), ("team", "20000001", "suspended"), ("match", "30000001", "hold"), ("ladder", "40000001", "pending")])
def test_put_table_status(table, id_to_change, status):
    s_response = put_table_status(table, id_to_change, status)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert result[0]["_status"] == status, "status not changed"

@pytest.mark.parametrize("table, changed_status", [("account", "deleted"), ("team", "suspended"), ("match", "hold"), ("ladder", "pending")])    
@pytest.mark.parametrize("status", ["active", "deleted", "suspended", "hold", "pending", "complete"])
def test_get_all_by_status(table, changed_status, status):
    s_response = get_all_by_status(table, status)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert type(result) is list, "return does not convert to a list"
    if status == "active":
        assert len(result) == 3, "return list is not right"
    elif status == changed_status:
        assert len(result) == 1, "return list is not right"
    else:
        assert len(result) == 0

@pytest.mark.parametrize("table, id", [("account", "10000001"), ("team", "20000002"), ("match", "30000003"), ("ladder", "40000004")])
def test_get_tables_by_id(table, id):
    s_response = get_table_by_id(table, id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert type(result) is list, "return does not convert to a list"
    assert len(result) == 1
    assert result[0]["_id"] == id, "ids donot match expected"

@pytest.mark.parametrize("table, expected", [("account", "4"), ("team", "4"), ("match", "4"), ("ladder", "4")])
def test_get_table_size(table, expected):
    s_response = get_size_of_table(table)
    assert type(s_response) is str, "return is not a string"
    assert s_response == expected, "table size is not as expected"

@pytest.mark.parametrize("table, changed_status", [("account", "deleted"), ("team", "suspended"), ("match", "hold"), ("ladder", "pending")])    
@pytest.mark.parametrize("status", ["active", "deleted", "suspended", "hold", "pending", "complete"])
def test_get_table_size_with_status(table, changed_status, status):
    s_response = get_size_of_table_status(table, status)
    if status == "active":
        assert s_response == "3", "table size is not as expected"
    elif status == changed_status:
        assert s_response == "1", "table size is not as expected"
    else:
        assert s_response == "0", "table size is not as expected"


temp_list = ["20000001", "20000002", "20000003", "20000004"]
@pytest.mark.parametrize("acc_id, expected_list", [("10000001", temp_list), ("10000002", temp_list), ("10000003", temp_list), ("10000004", temp_list)])
def test_get_teams_for_account(acc_id, expected_list):
    s_response = get_teams_for_account(acc_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["10000001", "10000002", "10000003", "10000004"]
@pytest.mark.parametrize("team_id, expected_list", [("20000001", temp_list), ("20000002", temp_list), ("20000003", temp_list), ("20000004", temp_list)])
def test_get_accounts_for_team(team_id, expected_list):
    s_response = get_accounts_for_team(team_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["40000001", "40000002", "40000003", "40000004"]
@pytest.mark.parametrize("team_id, expected_list", [("20000001", temp_list), ("20000002", temp_list), ("20000003", temp_list), ("20000004", temp_list)])
def test_get_ladders_for_team(team_id, expected_list):
    s_response = get_ladders_for_team(team_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["30000001", "30000002", "30000003", "30000004"]
@pytest.mark.parametrize("team_id, expected_list", [("20000001", temp_list), ("20000002", temp_list), ("20000003", temp_list), ("20000004", temp_list)])
def test_get_matches_for_team(team_id, expected_list):
    s_response = get_matches_for_team(team_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["20000001", "20000002", "20000003", "20000004"]
@pytest.mark.parametrize("match_id, expected_list", [("30000001", temp_list), ("30000002", temp_list), ("30000003", temp_list), ("30000004", temp_list)])
def test_get_teams_for_match(match_id, expected_list):
    s_response = get_teams_for_match(match_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["40000001", "40000002", "40000003", "40000004"]
@pytest.mark.parametrize("match_id, expected_list", [("30000001", temp_list), ("30000002", temp_list), ("30000003", temp_list), ("30000004", temp_list)])
def test_get_teams_for_match(match_id, expected_list):
    s_response = get_ladders_for_match(match_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["20000001", "20000002", "20000003", "20000004"]
@pytest.mark.parametrize("ladder_id, expected_list", [("40000001", temp_list), ("40000002", temp_list), ("40000003", temp_list), ("40000004", temp_list)])
def test_get_teams_for_ladder(ladder_id, expected_list):
    s_response = get_teams_for_ladder(ladder_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

temp_list = ["30000001", "30000002", "30000003", "30000004"]
@pytest.mark.parametrize("ladder_id, expected_list", [("40000001", temp_list), ("40000002", temp_list), ("40000003", temp_list), ("40000004", temp_list)])
def test_get_matches_for_ladder(ladder_id, expected_list):
    s_response = get_matches_for_ladder(ladder_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    assert sorted([value['_id'] for value in result]) == sorted(expected_list), "table size is not as expected"

TEAM_LIST = [("1", "new name"), ("2","another new name"), ("3", "this name has changed"), ("4", "not the same as it was before")]
@pytest.mark.parametrize("table, prefix", [("team", "2000000"), ("match", "3000000"), ("ladder", "4000000")])
@pytest.mark.parametrize("my_id, new_name", TEAM_LIST)
def test_put_table_name(table, prefix, my_id, new_name):
    s_response = put_table_name(table, prefix + my_id, new_name)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    result = result[0]
    assert result["_name"] == new_name, "rename has not worked"
'''
def test_put_account_details(table, prefix, my_id, new_name):
    s_response = put_account_details(i_id)
    assert type(s_response) is str, "return is not a string"
    result = json.loads(s_response)
    result = result[0]
    assert result["_name"] == new_name, "rename has not worked"
'''