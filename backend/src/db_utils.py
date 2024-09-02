import json


class DBConnection:
    """
    Class used to connect to a database
    For this small example, the database is a simple json file
    """

    def __init__(self):
        self.db_name = "users.json"
        self.db_path = "src/db/" + self.db_name

    def get_user_login_info(self, user_name: str):
        """
        Retrieves user's hashed password and salt

        Args:
            user_name (str): Name of the user in the database

        Returns:
            (str, str): User's password and salt
        """
        with open(self.db_path) as file:
            db = json.load(file)
            user_info = db.get(user_name, {})
            password = user_info.get("password", "")
            salt = user_info.get("salt", "")
        return password, salt
