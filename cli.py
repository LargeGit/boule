"""cli for test purposes
"""
from library import *
from cmd import Cmd
import logging
import re

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG)


def _not_right_number_of_args_(args, number):
    args_list = args.split()
    if len(args) == 0:
        print("Invalid syntax: too few arguments")
        return True
    elif len(args_list) > number:
        print("Invalid syntax: too many arguments")
        return True
    else:
        return False


class BouleCLI(Cmd):
    """CLI class
    """
    def emptyline(self):
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_get(self, args):
        """simulate a http GET request
        Syntax:
        get /account/            returns names all accounts along with their ids
        get /account/id          returns account details for the given name|id - name, id, nickname, date created, date
        modified, email, mobile
        get /account/id/teams    returns a list of the teams for which the given account is a member

        get /team/               returns names of all teams along with their ids
        get /team/id             returns team details for the given name|id - name, id, date created, date modified,
        accounts, ranking
        get /team/id/matches     returns the matches played by the given team id
        get /team/id/accounts    returns the accounts making up the given team
        get /team/id/ladders     returns the ladders containing the given team

        get /match/              returns names all matches along with their ids
        get /match/id            returns details for the match id given - name, id, date created, teams, score
        get /match/id/teams      returns teams and scores for the given match id
        get /match/id/ladders    returns ladder deatails for the given match id

        get /ladder/             returns names of all ladders along with their ids
        get /ladder/id/          returns details for name|id given - name, id, date created
        get /ladder/id/teams/    returns all teams names in the specified ladder along with their ids - in ranking
        order(highest first)
        get /ladder/id/matches/  returns all ladder match names, ids, teams, and scores in date order(newest first)

        TODO
        get /account/total          return total number of accounts
        get /account/active/(total)  return accounts of given status {active|hold|pending|suspended|deleted|complete}


        NOTE: currently only id supported not name
        """
        if _not_right_number_of_args_(args, 1):
            return

        uri_list = [x.lower() for x in args.split("/") if x != '']
        # Accounts
        if uri_list[0] == 'account' and len(uri_list) == 1:   # get /account/
            result = read_account('all')
        elif uri_list[0] == 'account' and len(uri_list) == 2:   # get /account/id
            result = read_account(uri_list[1])
        elif uri_list[0] == 'account' and len(uri_list) == 3 and uri_list[2] == 'teams':  # get teams for given account
            result = get_teams_per_account(int(uri_list[1]))
        # Teams
        elif uri_list[0] == 'team' and len(uri_list) == 1:     # get /team/
            result = read_team('all')
        elif uri_list[0] == 'team' and len(uri_list) == 2:     # get /team/id
            result = read_team(int(uri_list[1]))
        elif uri_list[0] == 'team' and len(uri_list) == 3 and uri_list[2] == 'matches':  # get teams for given account
            result = get_matches_per_team(int(uri_list[1]))
        elif uri_list[0] == 'team' and len(uri_list) == 3 and uri_list[2] == 'accounts':  # get teams for given account
            result = get_accounts_per_team(int(uri_list[1]))
        elif uri_list[0] == 'team' and len(uri_list) == 3 and uri_list[2] == 'ladders':  # get teams for given account
            result = get_ladders_per_team(int(uri_list[1]))
        # Matches
        elif uri_list[0] == 'match' and len(uri_list) == 1:    # get /match/
            result = read_match('all')
        elif uri_list[0] == 'match' and len(uri_list) == 2:    # get /match/id
            result = read_match(int(uri_list[1]))
        elif uri_list[0] == 'match' and len(uri_list) == 3 and uri_list[2] == 'teams':   # get teams and scores for given match
            result = get_teams_per_match(int(uri_list[1]))
        elif uri_list[0] == 'match' and len(uri_list) == 3 and uri_list[2] == 'ladders':   # get teams and scores for given match
            result = get_ladders_per_match(int(uri_list[1]))
        # Ladders
        elif uri_list[0] == 'ladder' and len(uri_list) == 1:   # get /ladder/
            result = read_ladder('all')
        elif uri_list[0] == 'ladder' and len(uri_list) == 2:   # get /ladder/id
            result = read_ladder(int(uri_list[1]))
        elif uri_list[0] == 'ladder' and uri_list[2] == 'teams' and len(uri_list) == 3:     # get /ladder/id/teams/
            result = get_teams_per_ladder(int(uri_list[1]))
        elif uri_list[0] == 'ladder' and uri_list[2] == 'matches' and len(uri_list) == 3:     # get /ladder/id/matches/
            result = get_matches_per_ladder(int(uri_list[1]))
        else:
            result = "404"
        print(result)

    def do_post(self, args):
        """simulate a http POST request TODO
        Syntax:
        post /ladder/parameter_list?params     create a new ladder
        post /match/parameter_list?params      create a new match
        post /account/parameter_list?params    create a new account
        post /team/parameter_list?params       create a new team
        NOTE: currently only id supported not name
        """
        if _not_right_number_of_args_(args, 1):
            return
        result = "404"

        BASIC_PARAM_SET = {'name': '--', 'second_name': '--', 'nickname': '--',
                           'email': '--', 'mobile': '--', 'ranking': 1600,
                           'proliferate': True}
        args_split_in_two = args.split('?')
        cmds = [x.lower() for x in args_split_in_two[0].split("/") if x != '']
        if len(args_split_in_two) == 2:
            args_split_in_two[1] = args_split_in_two[1].replace('%20', ' ')
            second_half = args_split_in_two[1].replace('=', '&').split('&')
        else:
            second_half = []
        # turn parameters into a dictionary
        given_params = {second_half[i]: second_half[i + 1]
                        for i in range(0, len(second_half), 2)}
        # add the second set to the first dictionary(overwriting any duplicates)
        params = {**BASIC_PARAM_SET, **given_params}
        print(cmds, params)

        if len(cmds) == 2 and cmds[1] == 'parameter_list':
            if cmds[0] == 'account':
                create_account(params)
            if cmds[0] == 'team':
                create_team(params)
            if cmds[0] == 'laddter':
                create_ladder(params)
            if cmds[0] == 'match':
                create_match(params)
        print(result)

    def do_put(self, args):
        """simulate a http PUT request
        Syntax:
        put /ladder/id/parameter_list?params    update the Ladder with given id
        put /match/id/parameter_list?params     update the match with given id
        put /account/id/parameter_list?params   update the account with given id
        put /team/id/parameter_list?params      update the team with given id
        put /ladder/id/team/id                  adds a team to the ladder
        put /ladder/id/match/id                 adds a match to the ladder
        put /team/id/account/id                 adds an account to a team
        put /match/id/team/id                   adds an account to a team

        NOTE: currently only id supported not name
        """
        if _not_right_number_of_args_(args, 1):
            return

        uri_list = [x.lower() for x in args.split("/") if x != '']

        if uri_list[0] == 'account' and len(uri_list) == 1:   # get /account/
            result = Account.get_all()
        elif uri_list[0] == 'account' and len(uri_list) == 2:   # get /account/id
            result = Account.get_all(my_id=uri_list[1])
        elif uri_list[0] == 'team' and len(uri_list) == 1:     # get /team/
            result = Team.get_all()
        elif uri_list[0] == 'team' and len(uri_list) == 2:     # get /team/id
            result = Team.get_all(my_id=uri_list[1])
        elif uri_list[0] == 'match' and len(uri_list) == 1:    # get /match/
            result = Match.get_all()
        elif uri_list[0] == 'match' and len(uri_list) == 2:    # get /match/id
            result = Match.get_all(my_id=uri_list[1])
        elif uri_list[0] == 'ladder' and len(uri_list) == 1:   # get /ladder/
            result = Ladder.get_all()
        elif uri_list[0] == 'ladder' and len(uri_list) == 2:   # get /ladder/id
            result = Ladder.get_all(my_id=uri_list[1])
        elif uri_list[0] == 'ladder' and uri_list[2] == 'teams' and len(uri_list) == 3:     # get /ladder/id/teams/
            lad_id = int(uri_list[1])
            result = LadderTeam.get_all_teams(lad_id)
        elif uri_list[0] == 'ladder' and uri_list[2] == 'matches' and len(uri_list) == 3:     # get /ladder/id/matches/
            lad_id = int(uri_list[1])
            result = LadderMatch.get_all_matches(lad_id)
        else:
            result = "404"
        print(result)

    def do_delete(self, args):
        """simulate a http DELETE request
        Syntax:
        delete /ladder/id           deleting a ladder also deletes the associated matches, match associations, and
                                    team associations it does not delete the teams
        delete /ladder/id/team/id   disassociates the team from the ladder, also deletes matches featuring that team,
                                    and disassociates those matches from the ladder. It does not delete the team
        delete /ladder/id/match/id  delete a match from the ladder

        delete /match/id            delete a match, remeove the asscoiation of that match from ladders and team
        delete /account/id          delete an account. account cannot be deleted if it exists in a team with others,
                                    or if the team is part of a match. simply mark the account as "deleted" and any
                                    teams as "suspended"
        delete /account/id/force    delete an account, any teams, any matches with that team, remove that team from
                                    all ladders
                                    is part of a match
        delete /team/id             delete a new team
        delete /team/id/account/id  deletes an account from a team
        NOTE: currently only id supported not name
        """
        # TODO you can't delete a account who is part of a team
        # and you can't delete teams(or accounts) who are part of a match
        # in fact do not actually delete accounts as such - prune periodically based on any inactive accounts
        # TODO delete returns True or False depending on the success - capture this

        if _not_right_number_of_args_(args, 1):
            return
        args_list = args.split("/")
        if args_list[0] == "account" or args_list[0] == "team" or args_list[0] == "match" or args_list[0] == "ladder":
            delete(args_list[1])
        else:
            print("Invalid argument")
            result = "404"
            print(result)

    def do_load(self, args):
        """load all accounts, teams or matches from disk
        Syntax: load TYPE
        TYPE = account | team | match | ladder
        """
        if _not_right_number_of_args_(args, 1):
            return
        if args == "all":
            load_all_tables()
        elif args == "account":
            load_account_table()
        elif args == "team":
            load_team_table()
        elif args == "match":
            load_match_table()
        elif args == "ladder":
            load_ladder_table()
        else:
            print("Invalid argument")

        # logging.info("Module large_boule_cli: account_database:: %s\n\n", account_database)
        # logging.info("Module large_boule_cli: accounts:: %s\n\n", Boules.list_of_accounts)
        # TODO: loading will overwrite any changes - add a confirmation

    def do_save(self, args):
        """Saves the current accounts, teams, or matches to disk
        Syntax: list TYPE
        TYPE = account | team | match | all
        """
        if _not_right_number_of_args_(args, 1):
            return
        if args == "account":
            Account.save_data()
        elif args == "team":
            Team.save_data()
        elif args == "match":
            Match.save_data()
        elif args == "ladder":
            Ladder.save_data()
        else:
            print("Invalid argument")

    def do_add(self, args):
        """Add a new Account, Match or Team
        Syntax: add TYPE
        TYPE = account | team | match | ladder
        TYPE = account2team | teamstoladder | teamstomatch
        user is then prompted to add firstname, second name, nick name and email address
        """
        if _not_right_number_of_args_(args, 1):
            return
        params = {'name': '', 'second_name': '', 'nickname': '', 'email': '', 'mobile': ''}
        if args == "account":
            while not re.match(r'^[A-Z][a-z]+$', params['name']):
                params['name'] = input("First Name: ")
            while not re.match(r'^[A-Z][a-z]+$', params['second_name']):
                params['second_name'] = input("Surname: ")
            while not re.match(r'^[A-Z][a-z]+$', params['nickname']):
                params['nickname'] = input("nickname: ")
            while not re.match(r'^[a-z]+$', params['email']):
                params['email'] = input("email: ")
            params['mobile'] = input("mobile: ")
            new_account = Account(params)
            print(new_account)
            print("Account added to database, to a team and that team added to the default Ladder")
        elif args == "team":
            while not re.match(r'^[A-Z][a-z]+$', params['name']):
                params['name'] = input("Team Name: ")
            new_team_id = Team(params)
            print("Team added to database and to the default Ladder")
        elif args == "match":
            while not re.match(r'^[A-Z][a-z]+$', params['name']):
                params['name'] = input("Match Name: ")
            new_match_id = Match(params)
            print("Match added")
        elif args == "ladder":
            while not re.match(r'^[A-Z][a-z]+$', params['name']):
                params['name'] = input("Ladder Name: ")
            new_ladder_id = Ladder()
        elif args == "account2team":
            team_id = input("team ID: ")
            account_id = input("account ID: ")
            TeamAccount(team_id, account_id)
            print("Account " + str(account_id) + " added to team " + str(team_id))

    def do_modify(self, args):
        """Modify a account, team or match
        Syntax: delete PLAYER ID | MATCH ID | TEAM ID
        You will then be asked to enter fields to be modified in turn
        Anything left blank will not be changed
        """
        if _not_right_number_of_args_(args, 2):
            return
        args_list = args.split()
        params = {}
        if args_list[0] == "account":
            params["fn"] = input("First Name: ")
            params["sn"] = input("Surname: ")
            params["nn"] = input("Nickname: ")
            params["em"] = input("Email: ")
            params["mb"] = input("Mobile: ")
            if Account.update(args_list[1], params):
                print("Account modified")
                return
        elif args_list[0] == "team":
            params["tn"] = input("Team Name: ")
            if Team.update(args_list[1], params):
                print("Team modified")
                return
        elif args_list[0] == "match":
            params["mn"] = input("Match Name: ")
            if Match.update(args_list[1], params):
                print("Match modified")
                return
        elif args_list[0] == "ladder":
            params["ln"] = input("Ladder Name: ")
            if Ladder.update(args_list[1], params):
                print("Ladder modified")
                return
        else:
            print("Invalid argument")

    def do_quit(self, args):
        """Quits the program
        """
        print("Quitting")
        raise SystemExit

# create a ladder
params = {'name':'Default Ladder'}
new_ladder = Ladder(params)
# new_ladder_id = new_ladder.get_id()

if __name__ == '__main__':
    prompt = BouleCLI()
    prompt.prompt = 'Large Boules Ladder >>'
    prompt.cmdloop('Starting Large\' CLI prompt...')
