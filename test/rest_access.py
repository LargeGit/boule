"""Integration tests
"""
import json
from random import randint
import requests

BASE_URL = 'http://localhost:8080'
BASE = {"name": "---", "second_name": "---", "nickname": "---", "email": "---",
        "mobile": "---", "ranking": 1600, "role": 1}
PROXIES = {"http": None}
"""
Create a mini league with one ladder, 8 accounts, 10 teams, and 20 random matches etc
"""
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

# create 4 ladders
RESOURCE = '/ladder'
for index in range(4):
    body = {**BASE, **{"name": LADDER_NAMES.pop(randint(0, 3-index))}}
    s_body_json = json.dumps(body, indent=2)
    r = requests.post(BASE_URL + RESOURCE, proxies=PROXIES, data=s_body_json)
print("4 ladders created")

# create 20 accounts with teams in default ladder
for index in range(20):
    body = {**BASE, **{"first_name": FIRST_NAMES.pop(randint(0, 19-index)),
                       "second_name": SECOND_NAMES.pop(randint(0, 19-index)),
                       "nickname": NICKNAMES.pop(randint(0, 19-index)),
                       "email": "email@address", "mobile": str(randint(0, 999999999))}}
    RESOURCE = '/account'
    s_body_json = json.dumps(body, indent=2)
    r = requests.post(BASE_URL + RESOURCE, proxies=PROXIES, data=s_body_json)
    a_dict = r.json()[0]
    new_acc_id = a_dict["_id"]
    new_team_name = a_dict["_first_name"] + " " + a_dict["_second_name"] + " team"
    # create new team
    body = {"name": new_team_name}
    RESOURCE = '/team'
    s_body_json = json.dumps(body, indent=2)
    r = requests.post(BASE_URL + RESOURCE, proxies=PROXIES, data=s_body_json)
    t_dict = r.json()[0]
    new_team_id = t_dict["_id"]
    # put account in team
    RESOURCE = '/team/' + new_team_id + '/account/' + new_acc_id + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)
    # put team in ladder
    RESOURCE = '/ladder/40000001/team/' + new_team_id + "/"
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)
print("20 accounts/teams created and put in default ladder")    

RESOURCE = '/account'
# create 10 without teams
for index in range(10):
    body = {**BASE, **{"first_name": FIRST_NAMES.pop(randint(0, 9-index)),
                       "second_name": SECOND_NAMES.pop(randint(0, 9-index)),
                       "nickname": NICKNAMES.pop(randint(0, 9-index)),
                       "email": "email@address", "mobile": str(randint(0, 999999999))}}
    s_body_json = json.dumps(body, indent=2)
    r = requests.post(BASE_URL + RESOURCE, proxies=PROXIES, data=s_body_json)

# create 20 more teams
RESOURCE = '/team'
for index in range(20):
    body = {**BASE, **{"name": TEAM_NAMES.pop(randint(0, 19-index))}}
    s_body_json = json.dumps(body, indent=2)
    r = requests.post(BASE_URL + RESOURCE, proxies=PROXIES, data=s_body_json)

# we now have 40 teams, 30 accounts (10 without teams), and 4 ladders

# put the last 20 teams in a random ladder and random accounts in the teams
for index in range(21, 40):
    tid = str(20000000 + index)
    RESOURCE = '/ladder/' + str(40000000 + randint(1, 4)) + '/team/' + tid + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)
    RESOURCE = '/team/' + tid + '/account/' + str(10000000 + randint(1, 30)) + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)
    RESOURCE = '/team/' + tid + '/account/' + str(10000000 + randint(1, 30)) + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)
    RESOURCE = '/team/' + tid + '/account/' + str(10000000 + randint(1, 30)) + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)

# create 60 matches
for index in range(60):
    body = {**BASE, **{"name": "match" + str(index+1).zfill(2)}}
    s_body_json = json.dumps(body, indent=2)
    RESOURCE = '/match/'
    r = requests.post(BASE_URL + RESOURCE, proxies=PROXIES, data=s_body_json)

# put 2 teams with random number of scores in every match
for index in range(60):
    mid = str(30000000 + index + 1)
    no_of_scores = randint(1, 5)
    team_list = [x + 1 for x in range(0, 40)]
    tid = str(20000000 + team_list.pop(randint(0, 39)))
    score = '/'.join([str(randint(0, 13)) for item in range(no_of_scores)])
    RESOURCE = '/match/' + mid + '/team/' + tid + '/' + score + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)
    tid = str(20000000 + team_list.pop(randint(0, 38)))
    score = '/'.join([str(randint(0, 13)) for item in range(no_of_scores)])
    RESOURCE = '/match/' + mid + '/team/' + tid + '/' + score
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)

# scatter 60 matches over 4 ladders
for index in range(60):
    mid = str(30000000 + index + 1)
    RESOURCE = '/ladder/' + str(40000000 + randint(1, 4)) + '/match/' + mid + '/'
    r = requests.put(BASE_URL + RESOURCE, proxies=PROXIES)

# get totals and lists
L_RESOURCE = ['/account/total', '/ladder/total', '/match/total', '/team/total',
              '/account', '/team', '/match', '/ladder',
              '/account/10000009', '/team/20000004', '/match/30000007', '/ladder/40000003',
              '/account/10000004/teams', '/team/20000001/matches', '/team/20000007/accounts',
              '/team/20000002/ladders', '/match/30000002/teams', '/match/30000007/ladders',
              '/ladder/40000001/teams/', '/ladder/40000003/matches/']
LIST_OF_STATUS = ['/active', '/hold', '/pending', 
                  '/suspended', '/deleted', '/complete']
LIST_OF_TABLE = ['/account', '/team', '/match', '/ladder']
for uri in L_RESOURCE:
    res = BASE_URL + uri
    r = requests.get(res, proxies=PROXIES)
    print(res)
    print(r.text)
for uri in LIST_OF_TABLE:
    for sts in LIST_OF_STATUS:
        res = BASE_URL + uri + sts
        r = requests.get(res, proxies=PROXIES)
        print(res)
        print(r.text)
        res = BASE_URL + uri + sts + '/total'
        r = requests.get(res, proxies=PROXIES)
        print(res)
        print(r.text)