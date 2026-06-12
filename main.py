from database import create_database
from auth import register_user

create_database()

username = input("Enter username: ")
password = input("Enter password: ")

register_user(username, password)