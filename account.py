"""docstring"""
import time
from boule import Boule


class Account(Boule):
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

    GUEST = 0
    USER = 1
    ADMIN = 99

    # table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    table = {}
    meta = {"unique_id": 10000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new account
    def __init__(self, my_dict):
        super().__init__(my_dict)
        Account.meta["unique_id"] += 1
        self.second_name = my_dict["second_name"]
        self.role = Account.USER
        self.nickname = my_dict["nickname"]
        self.email = my_dict["email"]
        self.mobile = my_dict["mobile"]
        self.ranking = my_dict['ranking']
        Account.table[str(Account.meta["unique_id"])] = self.__dict__
        self.s_id = str(Account.meta["unique_id"])  # important to add this after the dict has been updated

    # ******************************************
    # ********   data get operations    ********
    # ******************************************

    @classmethod
    def get_second_name(cls, s_id):
        """docstring"""
        if s_id in cls.table:
            return cls.table[s_id]["second_name"]
        else:
            return False

    @classmethod
    def get_full_name(cls, s_id):
        """docstring"""
        if s_id in cls.table:
            return cls.table[s_id]["name"] + " " + cls.table[s_id]["second_name"]
        else:
            return False

    @classmethod
    def get_nickname(cls, s_id):
        """docstring"""
        if s_id in cls.table:
            return cls.table[s_id]["nickname"]
        else:
            return False

    @classmethod
    def get_email(cls, s_id):
        """docstring"""
        if s_id in cls.table:
            return cls.table[s_id]["email"]
        else:
            return False

    @classmethod
    def get_mobile(cls, s_id):
        """docstring"""
        if s_id in cls.table:
            return cls.table[s_id]["mobile"]
        else:
            return False

    @classmethod
    def get_role(cls, s_id):
        """docstring"""
        if s_id in cls.table:
            return cls.table[s_id]["role"]
        else:
            return False

    # ******************************************
    # ********   data set operations    ********
    # ******************************************

    def set_second_name(self, new_second_name):
        """docstring"""
        self.second_name = new_second_name
        self.modified = time.strftime("%d/%m/%Y %I:%M:%S")

    def set_nickname(self, new_nickname):
        """docstring"""
        self.nickname = new_nickname
        self.modified = time.strftime("%d/%m/%Y %I:%M:%S")

    def set_email(self, new_email):
        """docstring"""
        self.email = new_email
        self.modified = time.strftime("%d/%m/%Y %I:%M:%S")

    def set_ranking(self, new_ranking):
        """docstring"""
        self.ranking = new_ranking
        self.modified = time.strftime("%d/%m/%Y %I:%M:%S")

    def set_mobile(self, new_mobile):
        """docstring"""
        self.mobile = new_mobile
        self.modified = time.strftime("%d/%m/%Y %I:%M:%S")

    # ******************************************
    # ********      other operations    ********
    # ******************************************
    @classmethod
    def get_id_by_name(cls, name_to_find):
        """overrides the parent version in Boule
        """
        for row in cls.table:
            if name_to_find == row.name + " " + row.second_name:
                return str(row.s_id)
        return False

    @classmethod
    def get_name_by_id(cls, id_to_find):
        """@classmethod to get the name attribute based on id match"""
        if id_to_find in cls.table:
            return cls.table[id_to_find]["name"] + " " + cls.table[id_to_find]["second_name"]
        else:
            return False

    @classmethod
    def details_exist(cls, d_details):
        for row in cls.table.values():
            # print(row["nickname"], d_details["nickname"])
            # print (row["email"], d_details["email"])
            # print (row["mobile"], d_details["mobile"])
            if ((row["nickname"] == d_details["nickname"]) and (row["nickname"] != "")) \
                    or ((row["email"] == d_details["email"]) and (row["email"] != "")) \
                    or ((row["mobile"] == d_details["mobile"]) and (row["mobile"] != "")):
                return True
        return False
