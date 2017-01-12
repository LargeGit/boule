"""creat a basic data structure"""
from random import randint
from rest_server import *

from bottle import request, run, post, tob
import io
import json

BASE = {"name": "--", "second_name": "--", "nickname": "--", "email": "--",
        "mobile": "--", "ranking": 1600, "proliferate": True}

FIRST_NAMES = ['John', 'Sue', 'Bob', 'Steve', 'Andy', 'Dave', 'Dan', 'Simon',
               'Imogen', 'Keith', 'Eddy', 'Amanda', 'Trevor', 'Patrick', 'Sarah',
               'Liz', 'Tom', 'Nigel', 'Charlie', 'Fred', 'Geoff', 'Harry', 'Leo',
               'Malcolm', 'Oscar', 'Penny', 'Ron', 'Victoria', 'Brian', 'Chris']
SECOND_NAMES = ['Andrews', 'Bristow', 'Chambers', 'Davies', 'Edmonds', 'Flintstone',
                'Gibbons', 'Holmes', 'Innes', 'Jacobs', 'Kelly', 'Lambert', 'McBride',
                'Pearson', 'Quincey', 'Rowlands', 'Sanders', 'Smith', 'Williams',
                'Starchan', 'Charlton', 'Sarandon', 'DiCaprio', 'Dench', 'Atkinson',
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


def set_up_post(body1):
    request.bind({})
    s_body_json = json.dumps(body1, indent=2)
    request.environ['CONTENT_LENGTH'] = str(len(tob(s_body_json)))
    request.environ['wsgi.input'] = io.BytesIO()
    request.environ['wsgi.input'].write(tob(s_body_json))
    request.environ['wsgi.input'].seek(0)

# create 4 ladders
print("create 4 ladders")
for index in range(4):
    body = {**BASE, **{"name": LADDER_NAMES.pop(randint(0, 3 - index))}}
    set_up_post(body)
    s_response = post_new_ladder()
    result = json.loads(s_response)
    assert type(result["response"]) == type(' ')
    # assert result["response"] == str(40000001 + index), "return value is not correct"

# create 20 accounts with teams in default ladder
print("create 20 accounts with teams in default ladder")
for index in range(20):
    body = {**BASE, **{"name": FIRST_NAMES.pop(randint(0, 19 - index)),
                       "second_name": SECOND_NAMES.pop(randint(0, 19-index)),
                       "nickname": NICKNAMES.pop(randint(0, 19-index)),
                       "email": str(randint(0, 99999))+"@"+str(randint(0, 99999)),
                       "mobile": str(randint(0, 999999999))}}
    set_up_post(body)
    s_response = post_new_account()
    result = json.loads(s_response)
    # assert result["response"] == str(10000001 + index), "return value is not correct"
    # TODO also check team exists, and that team is in ladder

# create 10 without teams
print("create 10 more accounts without teams")
BASE['proliferate'] = False
for index in range(10):
    body = {**BASE, **{"name": FIRST_NAMES.pop(randint(0, 9-index)),
                       "second_name": SECOND_NAMES.pop(randint(0, 9-index)),
                       "nickname": NICKNAMES.pop(randint(0, 9-index)),
                       "email": str(randint(0, 99999))+"@"+str(randint(0, 99999)),
                       "mobile": str(randint(0, 999999999))}}
    set_up_post(body)
    s_response = post_new_account()
    result = json.loads(s_response)
    # assert result["response"] == str(10000021 + index), "return value is not correct"
    # TODO also check team exists, and that team is in ladder

# create 20 more teams
print("create 20 more teams")
for index in range(20):
    body = {**BASE, **{"name": TEAM_NAMES.pop(randint(0, 19-index))}}
    set_up_post(body)
    s_response = post_new_team()
    result = json.loads(s_response)
    # assert result["response"] == str(20000021 + index), "return value is not correct"

# we now have 40 teams, 30 accounts(10 without teams), and 4 ladders
print("we now have 40 teams, 30 accounts(10 without teams), and 4 ladders")

# put the last 20 teams in a random ladder and random accounts in the teams
print("put the last 20 teams in a random ladder and random accounts in the teams")
for index in range(21, 40):
    tid = str(20000000 + index)
    lid = str(40000000 + randint(1, 4))
    put_team_in_ladder(lid, tid)
    for loop in range(randint(1, 3)):
        aid = str(10000000+randint(1, 30))
        put_account_in_team(tid, aid)

# create 60 matches and put 2 random teams in each
print("Creating 60 and put 2 random teams in each")
for index in range(60):
    body = {**BASE, **{"name": "match" + str(index+1).zfill(2)}}
    set_up_post(body)
    s_response = post_new_match()
    mid = json.loads(s_response)
    # assert mid["response"] == str(30000001 + index), "return value is not correct"
    team_list = [x for x in range(1, 41)]
    tid = str(20000000 + team_list.pop(randint(0, 39)))
    my_path = str(randint(0, 13)) + "/" + str(randint(0, 13)) + "/" + str(randint(0, 13))
    put_team_in_match(mid["response"], tid, my_path)
    tid = str(20000000 + team_list.pop(randint(0, 38)))
    my_path = str(randint(0, 13)) + "/" + str(randint(0, 13)) + "/" + str(randint(0, 13))
    put_team_in_match(mid["response"], tid, my_path)

# scatter 60 matches over 4 ladders
print("Scattering 60 matches over 4 ladders")
for index in range(60):
    mid = str(30000001 + index)
    lid = str(40000000 + randint(1, 4))
    put_match_in_ladder(lid, mid)
