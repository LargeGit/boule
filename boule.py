"""The parent class from which all data objects inherit"""
import logging
import time
import pickle
import os

class Boule:
    """Docstring"""
    STATUS = {"active": "active", "deleted": "deleted", "suspended": "suspended",
    "hold": "hold", "pending": "pending", "complete": "complete"}
    
    PATH = 'C:\\Users\\jonba\\Desktop\\BouleData\\'
    EXTENSION = '.pickle'

    def __init__(self):
        """Cover the common action for any new Account/Team/Match/Ladder object instantiation
        """
        self._modified = self._created = time.strftime("%d/%m/%Y %I:%M:%S")
        self._status = Boule.STATUS["active"]

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
        self._modified = value





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
            with open(Boule.PATH + cls.NAME + Boule.EXTENSION, 'rb') as f_handle:
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
            with open(Boule.PATH + cls.NAME + Boule.EXTENSION, 'wb') as f_handle:
                pickle.dump([cls.meta, cls.table], f_handle)
                logging.info("Module %s: Data written to database file", cls)
                return()
        except:
            # TODO a better mechanism is required here - to ensure we don't just lose data
            logging.critical("Module Account: failed to save meta and/or account data")
            logging.critical("Path was %s ", Boule.PATH + cls.NAME + Boule.EXTENSION)
            # TODO this is the wrong exit command
            exit("execution halted: Failed to save data")

    @classmethod
    def database_file_exists(cls):
        """@classmethod to check if database file exists for give class
        returns True or False
        """
        return os.path.isfile(Boule.PATH + cls.NAME + Boule.EXTENSION)

    @classmethod
    def database_file_remove(cls):
        """@classmethod to delete a database pickle file from disk"""
        try:
            os.remove(Boule.PATH + cls.NAME + Boule.EXTENSION)
            return True
        except:
            logging.critical("Path was %s ", Boule.PATH + cls.NAME + Boule.EXTENSION)
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
            cls.table[id]["status"] = Boule.STATUS["deleted"]
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
        if kwargs["status"] not in Boule.STATUS.values():
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