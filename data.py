
# pylint: disable=R0904

MAX_TEAM_SIZE = 3
MAX_TEAMS_IN_MATCH = 2
DEFAULT_LADDER_ID = "40000001"

accounts = []
teams = []
ladders = []
matches = []


account_teams_list = []  # put each accounts in multiple teams. id1 = account (unique), id2 = team (0 to many)
team_ladders_list = []   # put each team in multiple ladders. id1 = team (unique), id2 = ladder (0 to many)
ladder_matches_list = []  # for each ladder store mulitple matches

match_teams_scores_list = []   # for each match add two teams + scores (tuples) per game
