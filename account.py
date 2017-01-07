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
    def __init__(self, first_name="---", second_name="---",
        role=Account.USER, nickname="---", email="---", mobile="---", ranking=0):
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

    @property
    def id(self):
        return self._id 

   @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        # TODO add any name validation here
        self._first_name = value

   @property
    def second_name(self):
        return self._second_name

    @second_name.setter
    def second_name(self, value):
        # TODO add any name validation here
        self._second_name = value

   @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        # TODO add any name validation here
        self._role = value

   @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        # TODO add any name validation here
        self._nickname = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # TODO add any name validation here
        self._email = value

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        # TODO add any name validation here
        self._mobile = value

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        # TODO add any name validation here
        self._ranking = value

        
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
                return str(row.id)
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
