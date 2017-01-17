"""This module contains all the main data clasees"""
import logging
import time
import pickle
import os
import data

class Boules:
    """Docstring"""

    def __init__(self):
        """Cover the common action for any new Account/Team/Match/Ladder object instantiation
        """
        self._modified = self._created = time.strftime("%d/%m/%Y %I:%M:%S")
        self._status = data.STATUS["active"]

    @property
    def id(self):
        return self._id 

    @property
    def modified(self):
        return self._modified

    @property
    def created(self):
        return self._created

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        # TODO check vaue is a valid date object
        self._status = value
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")

class Account(Boules):
    """
    Account Class
    attributes:
    name, second_name, nickname, email, mobile,
    ranking, modified, created, status
    Methods: get all + get full name
             set all
             get unique_id
    """
    NAME = 'account'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = {}
    meta = {"unique_id": 10000000, "author": "large", "version": "1.0.0", "last_saved": ""}
    
    ROLES = {"admin": "admin", "user": "user", "viewer": "viewer"}

    # initialise a new account
    def __init__(self, first_name="---", second_name="---",
            role=data.USER, nickname="---", email="---", mobile="---", ranking=0):
        super().__init__()
        Account.meta["unique_id"] += 1
        self._id = str(Account.meta["unique_id"])
        self._first_name = first_name
        self._second_name = second_name
        self._role = role
        self._nickname = nickname
        self._email = email
        self._mobile = mobile
        self._player_ranking = ranking
    '''
    @property
    def id(self):
        return self._id 
    '''

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._first_name = value

    @property
    def second_name(self):
        return self._second_name

    @second_name.setter
    def second_name(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._second_name = value
    
    @property
    def full_name(self):
        return self._first_name + " " + self._second_name

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._role = value

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")        
        self._nickname = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._email = value

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._mobile = value

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._ranking = value

class Ladder(Boules):
    """
    Class Ladder
    Properties: ladder_id, ladder_name, ladder_date_created,
                ladder_last_modified, ladder_status, ladder_accounts

    Methods: get all + get full name
             set all
             get meta["unique_id"]
    """

    NAME = 'ladder'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor

    meta = {"unique_id": 40000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new ladder
    def __init__(self, new_name="---"):
        super().__init__()
        Ladder.meta["unique_id"] += 1
        self._id = str(Ladder.meta["unique_id"])
        self._name = new_name

    '''
    @property
    def id(self):
        return self._id 
    '''
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._name = new_name

class Team(Ladder):
    """
    Class Team
    Properties: team_id, team_name, team_date_created,
                team_last_modified, team_status, team_accounts

    Methods: get all + get full name
             set all
             get meta["unique_id"]
    """
    NAME = 'team'

    meta = {"unique_id": 20000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor   

    # initialise a new team
    def __init__(self, new_name="---", team_ranking=data.DEFAULT_RANKING):
        super().__init__(new_name)
        Team.meta["unique_id"] += 1
        self._id = str(Team.meta["unique_id"])
        self._ranking = team_ranking
    '''
    @property
    def id(self):
        return self._id 

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._name = value
    '''
    
    @property
    def ranking(self):
        return self._team_ranking

    @ranking.setter
    def ranking(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._ranking = value
      
class Match(Ladder):
    """
    Class Match
    Properties: match_id, match_name, match_date_created,
                match_last_modified, match_status, match_accounts

    Methods: get all + get full name
             set all
             get meta["unique_id"]
    """

    NAME = 'match'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor

    meta = {"unique_id": 30000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new match
    def __init__(self, new_name="---"):
        super().__init__(new_name)
        Match.meta["unique_id"] += 1
        self._id = str(Match.meta["unique_id"])

    '''    
    @property
    def id(self):
        return self._id 

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # TODO add any name validation here
        self._modified = time.strftime("%d/%m/%Y %I:%M:%S")
        self._name = value
    '''     

class Event(Boules):
    """
    Event Class
    attributes:
    event_id, event_type, event_level, event_category
    event_timestamp, event_description, event_acknowledge
    Methods: get all + get full name
             set all
             get unique_id
    """
    NAME = 'account'

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = {}
    meta = {"unique_id": 50000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new account
    def __init__(self, **kwargs):
        Event.meta["unique_id"] += 1
        self._id = str(Event.meta["unique_id"])
        self._type = kwargs["type"]
        self._level = kwargs["level"]
        self._category = kwargs["cat"]
        self._timestamp = time.strftime("%d/%m/%Y %I:%M:%S")
        self._description = kwargs['desc']
        self._acknowledge = False

    def __str__(self):
        return (self.event_id + ": "
                # + (self.event_type + " " * 8)[:8]
                # + (self.event_level + " " * 8)[:8]
                + (self.event_category + " " * 8)[:8]
                # + (self.event_timestamp + " " * 20)[:20]
                # + (str(self.event_acknowledge) + " " * 6)[:6]
                + (self.event_description + " " * 160)[:160])

    def flip_acknowledge(self):
        """docstring"""
        if self.acknowledge:
            self.event_acknowledge = False
        else:
            self.event_acknowledge = True

    @property
    def id(self):
        return self._id
        
    @property
    def type(self):
        return self._type
        
    @property
    def level(self):
        return self._level
        
    @property
    def category(self):
        return self._category
        
    @property
    def timestamp(self):
        return self._timestamp
        
    @property
    def description(self):
        return self._description
        
    @property
    def acknowledge(self):
        return self._acknowledge
        
    @acknowledge.setter
    def acknowledge(self, new_value):
        if new_value:
            self._acknowledge = True
        else:
            self._acknowledge = False

    '''
    # ******************************************
    # ********   data get operations    ********
    # ******************************************

    @classmethod
    def get_second_name(cls, id):
        """docstring"""
        if id in cls.table:
            return cls.table[id]["second_name"]
        else:
            return False

    @classmethod
    def get_full_name(cls, id):
        """docstring"""
        if id in cls.table:
            return cls.table[id]["name"] + " " + cls.table[id]["second_name"]
        else:
            return False

    @classmethod
    def get_nickname(cls, id):
        """docstring"""
        if id in cls.table:
            return cls.table[id]["nickname"]
        else:
            return False

    @classmethod
    def get_email(cls, id):
        """docstring"""
        if id in cls.table:
            return cls.table[id]["email"]
        else:
            return False

    @classmethod
    def get_mobile(cls, id):
        """docstring"""
        if id in cls.table:
            return cls.table[id]["mobile"]
        else:
            return False

    @classmethod
    def get_role(cls, id):
        """docstring"""
        if id in cls.table:
            return cls.table[id]["role"]
        else:
            return False


    
    @classmethod
    def get_by_id(cls, id, *status):
        if id not in cls.table:
            return False
        if status and cls.table[id]["status"] != status:
            return False
        return {id: cls.table[id]}
        
    @classmethod
    def get_all(cls, **kwargs):
        if "my_id" in kwargs:
            return {key: value for key, value in cls.table.items() if key == kwargs["my_id"]}
        if "status" in kwargs:
            return {key: value for key, value in cls.table.items() if value['status'] == kwargs["status"]}
        return cls.table
        
    @classmethod
    def get_items(cls, **kwargs):
        """@classmethod to return all entries for the given table type as dictionaries"""
        result = {}
        if "my_id" in kwargs and "status" in kwargs:
            result = cls.get_by_id(kwargs["my_id"], kwargs["status"])
        if "my_id" in kwargs and "status" not in kwargs:
            result = cls.get_by_id(kwargs["my_id"])
        if "my_id" not in kwargs and "status" in kwargs:
            result = cls.get_all(kwargs["status"])
        if "my_id" not in kwargs and "status" not in kwargs:
            result = cls.get_all()
        return result

    @classmethod
    def load_data(cls):
        """Class Method to load data from pickle file into table list"""
        try:
            with open(data.PATH + cls.NAME + data.EXTENSION, 'rb') as f_handle:
                both_objects_in_file = pickle.load(f_handle)
            logging.info("Module %s: data read successfully\n", cls)
            cls.meta = both_objects_in_file[0]
            cls.table = both_objects_in_file[1]
        except:
            logging.error("Module Account: execution halted: data could not be loaded")
            exit("execution halted: data could not be loaded") # TODO this is the wrong exit command

    @classmethod
    def save_data(cls):
        """Class Method to save data from table list into pickle file"""
        cls.meta["last_saved"] = time.strftime("%d/%m/%Y %I:%M:%S")
        try:
            with open(data.PATH + cls.NAME + data.EXTENSION, 'wb') as f_handle:
                pickle.dump([cls.meta, cls.table], f_handle)
                logging.info("Module %s: Data written to database file", cls)
                return()
        except:
            # TODO a better mechanism is required here - to ensure we don't just lose data
            logging.critical("Module Account: failed to save meta and/or account data")
            logging.critical("Path was %s ", data.PATH + cls.NAME + data.EXTENSION)
            # TODO this is the wrong exit command
            exit("execution halted: Failed to save data")

    @classmethod
    def database_file_exists(cls):
        """@classmethod to check if database file exists for give class
        returns True or False
        """
        return os.path.isfile(data.PATH + cls.NAME + data.EXTENSION)

    @classmethod
    def database_file_remove(cls):
        """@classmethod to delete a database pickle file from disk"""
        try:
            os.remove(data.PATH + cls.NAME + data.EXTENSION)
            return True
        except:
            logging.critical("Path was %s ", data.PATH + cls.NAME + data.EXTENSION)
            return False

    # Get instance with given ID
    @classmethod
    def status_by_id(cls, id_to_find):
        """@classmethod to return the status property for the given class and id"""
        if id_to_find in cls.table:
            return cls.table[id_to_find]["status"]
        else:
            return False

    @classmethod
    def id_exists(cls, id):
        """@classmethod to determine if a particular id exists in the table
        """
        if id in cls.table:
            return True
        else:
            return False

    @classmethod
    def delete(cls, id):
        """@classmethod to delete a row from the table (item from the list)"""
        if id not in cls.table:
            return False
        else:
            cls.table[id]["status"] = data.STATUS["deleted"]
            return True

    @classmethod
    def get_id_by_name(cls, name_to_find):
        """@classmethod return the id of the table row with supplied name"""
        result = [key for key, value in cls.table.items() if value['name'] == name_to_find]
        if result:
            return result[0]
        else:
            return False

    # ******************************************
    # ********   meta get operations    ********
    # ******************************************

    # get account meta unique_id for each class
    @classmethod
    def get_meta_id(cls):
        """@classmethod to get meta id"""
        return cls.meta["unique_id"]

    # get account meta author for each class
    @classmethod
    def get_meta_author(cls):
        """@classmethod to get meta author"""
        return cls.meta["author"]

    # get account meta version for each class
    @classmethod
    def get_meta_version(cls):
        """@classmethod to get meta version"""
        return cls.meta["version"]

    # get account meta last saved for each class
    @classmethod
    def get_meta_last_saved(cls):
        """@classmethod to get meta last saved"""
        return cls.meta["last_saved"]

    # ******************************************
    # ********   meta set operations    ********
    # ******************************************

    # set account meta "unique_id" for each class
    @classmethod
    def set_meta_id(cls, new_id):
        """@classmethod to set meta id"""
        cls.meta["unique_id"] = new_id
        return True

    # set account meta "author" for each class
    @classmethod
    def set_meta_author(cls, new_author):
        """@classmethod to set meta author"""
        cls.meta["author"] = new_author
        return True

    # set account meta "version" for each class
    @classmethod
    def set_meta_version(cls, new_version):
        """@classmethod to set meta version"""
        cls.meta["version"] = new_version
        return True

    # set meta "last saved" for each class
    @classmethod
    def set_meta_last_saved(cls, new_saved):
        """@classmethod to set meta last saved"""
        cls.meta["last_saved"] = new_saved
        return True

    # ******************************************
    # ********   data set operations    ********
    # ******************************************

    @classmethod
    def set_name(cls, **kwargs):
        """set name attribute"""
        if ("my_id" not in kwargs) or ("name" not in kwargs):
            return False
        new_name = kwargs["name"].replace("%20", " ")
        cls.table[kwargs["my_id"]]["name"] = new_name
        cls.table[kwargs["my_id"]]["modified"] = time.strftime("%d/%m/%Y %I:%M:%S")
        return True

    @classmethod
    def set_status(cls, **kwargs):
        """@classmethod to set the status based on id match"""
        if ("my_id" not in kwargs) or ("status" not in kwargs):
            return False
        if kwargs["status"] not in data.STATUS.values():
            return False
        if kwargs["my_id"] in cls.table:
            cls.table[kwargs["my_id"]]["status"] = kwargs["status"]
            cls.table[kwargs["my_id"]]["modified"] = time.strftime("%d/%m/%Y %I:%M:%S")
            return True
        else:
            return True

    @classmethod
    def get_name_by_id(cls, id_to_find):
        """@classmethod to get the name attribute based on id match"""
        if id_to_find in cls.table:
            return cls.table[id_to_find]["name"]
        else:
            return False

    @classmethod
    def get_ranking_by_id(cls, id_to_find):
        """@classmethod to get the ranking attribute based on id match
        Only Teams have a ranking attribute
        """
        if id_to_find in cls.table:
            return cls.table[id_to_find]["ranking"]
        else:
            return False

    @classmethod
    def get_all_ids(cls, *status):
        """return a list of all id numbers
        filtered by status, if provided
        """
        result = [key for key, value in cls.table.items() if value['status'] == status]
        return result

    def get_id(self):
        """return a list of all id numbers
        filtered by status, if provided
        """
        return self.id
    '''