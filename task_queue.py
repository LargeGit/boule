# ***************************************************
# ****              Class TaskQueue             ****
# **** methods and attributes for TaskQueues   ****
# ***************************************************

from boules import Boules


class TaskQueue(Boules):
    """
    Class TaskQueue
    Properties: task_id, account_id
                
    Methods:    __init__(self, task_id, account_id)
                __str__(self)
                get_account_ids_for_given_task_id (task_id)
                get_task_ids_for_given_account_id (account_id)
                TaskQueue_exists (task_id, account_id)
                get_full_AccountTaskQueue_list ()
                delete_account_from_team (task_id, account_id)
    """

    TASK = {"active": "Active", "deleted": "Deleted", "suspended": "Suspended"}

    NAME = 'task_queue'

    # Table is the list that contains all the data for this class
    # Do not expose direcly out of this class, only via accessor
    Table = []
    meta = {"unique_id": 50000000, "author": "large", "version": "1.0.0", "last_saved": ""}

    # initialise a new task queue item
    def __init__(self, task_id, account_id):
        TaskQueue.meta["unique_id"] += 1
        self.id = TaskQueue.meta["unique_id"]
        self.team = task_id
        self.account = account_id
        TaskQueue.Table.append(self)

    # define __str___ output
    def __str__(self):
        return ("TaskQueue ID   : " + self.account +
                "\nSize      : " + self.team +
                "\n")

    # Get all accounts in a team
    # return the array of account_id's if any exist, otherwise return False
    def get_account_ids_for_given_task_id(task_id):
        success = False
        result = []
        for row in TaskQueue.Table:
            if row.team == task_id:
                success = True
                result.append(row.account)
        if success:
            return result
        else:
            return False

    # Get all teams for a account
    # return the array of task_id's if any exist, otherwise return false    
    def get_task_ids_for_given_account_id(account_id):
        success = False
        result = []
        for row in TaskQueue.Table:
            if row.account == account_id:
                success = True
                result.append(row.team)
        if success:
            return result
        else:
            return False

    # check if account team combination already exists
    def task_queue_exists(task_id, account_id):
        for row in TaskQueue.Table:
            if row.team == task_id and row.account == account_id:
                return True
        return False

    # Delete a account from a team (for admin use only)
    # Also, modifying the accounts in a team is an admin only action
    # achieved by deleting a row, and adding a new one
    # returns True = successful delete or False = combination not found
    def delete_account_from_team(task_id, account_id):
        for row in TaskQueue.Table:
            if row.team == task_id and row.account == account_id:
                TaskQueue.Table.remove(row)
                return True
        return False
