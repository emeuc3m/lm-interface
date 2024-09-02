import hashlib
from src.db_utils import DBConnection


def validate_login(user_name: str, password: str):
    """
    Validates login credentials

    Args:
        user_name (str): User name in the database
        password (str): Plain text password inputted by the user

    Returns:
        bool: True if credentials are correct, False otherwise
    """
    expected_password, salt = DBConnection().get_user_login_info(user_name)
    if not (expected_password):
        # User was not found in the DB
        return False
    password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()
    if password != expected_password:
        return False
    return True
