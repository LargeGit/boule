
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
    
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["id"]) is str, "return value in dict is not of correct type"
    assert result["id"] == expected, "return value is not correct value, expected 40000001"
   
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
        
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["id"]) is str, "return value in dict is not of correct type"
    assert result["id"] == expected, "return value is not correct"
  
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
    
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["id"]) is str, "return value in dict is not of correct type"
    assert result["id"] == expected, "return value is not correct value, expected 40000001"
    
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
    
    assert type(result) is dict, "return does not convert to a dictionary"
    assert type(result["id"]) is str, "return value in dict is not of correct type"
    assert result["id"] == expected, "return value is not correct value, expected 40000001"
    
match1 = help.get_item_by_id(matches, "30000001")
match2 = help.get_item_by_id(matches, "30000002")
match3 = help.get_item_by_id(matches, "30000003")
match4 = help.get_item_by_id(matches, "30000004")


@pytest.mark.parametrize("account_id", [str(10000000 + i) for i in range(4)])
@pytest.mark.parametrize("team_id", [str(20000000 + i) for i in range(4)])
def test_add_account_to_team(account_id, team_id):
    response = put_account_in_team(account_id, team_id)
    assert response == "{}"

@pytest.mark.parametrize("team_id", [str(20000000 + i) for i in range(4)])
@pytest.mark.parametrize("ladder_id", [str(40000000 + i) for i in range(4)])    
def test_add_team_to_ladder(team_id, ladder_id):
    response = put_team_in_ladder(ladder_id, team_id)
    assert response == "{}"

@pytest.mark.parametrize("team_id", [str(20000000 + i) for i in range(4)])
@pytest.mark.parametrize("match_id", [str(30000000 + i) for i in range(4)])
def test_add_team_to_match(team_id, match_id):
    response = put_team_in_match(match_id, team_id, False)
    assert response == "{}"

@pytest.mark.parametrize("match_id", [str(30000000 + i) for i in range(4)])
@pytest.mark.parametrize("ladder_id", [str(40000000 + i) for i in range(4)])    
def test_add_match_to_ladder(match_id, ladder_id):
    response = put_match_in_ladder(ladder_id, match_id)
    assert response == "{}"

'''
account_team = []
team_ladder = []   # put each team in multiple ladders. id1 = team (unique), id2 = ladder (0 to many)
ladder_match = []  # for each ladder store mulitple matches
match_team_score
'''