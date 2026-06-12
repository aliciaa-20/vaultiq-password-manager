from database import create_database
from auth import register_user, login_user
from vault import add_credential, view_credentials


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

        user_id = login_user(username, password)

        if user_id:

            while True:

                print("\n=== Vault Menu ===")
                print("1. Add Credential")
                print("2. View Credentials")
                print("3. Logout")

                vault_choice = input("Choose an option: ")

                if vault_choice == "1":

                    website = input("Website: ")
                    email = input("Email: ")
                    password = input("Password: ")
                    notes = input("Notes: ")

                    add_credential(
                        user_id,
                        website,
                        email,
                        password,
                        notes
                    )

                elif vault_choice == "2":

                    view_credentials(user_id)

                elif vault_choice == "3":

                    print("Logged out!")
                    break

                else:
                    print("Invalid option!")

    elif choice == "3":

        print("Goodbye!")
        break

    else:
        print("Invalid option!")