from database import create_database
from auth import register_user, login_user

create_database()

while True:

    print("\n=== VaultIQ ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":

        username = input("Username: ")
        password = input("Password: ")

        register_user(username, password)

    elif choice == "2":

        username = input("Username: ")
        password = input("Password: ")

        login_user(username, password)

    elif choice == "3":

        print("Goodbye!")
        break

    else:
        print("Invalid option!")