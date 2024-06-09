import os
import sys
import time
from db.create_tabels import CreateTables
from services.menu_system import MenuSystem
from services.account_service import AccountService

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    create_tables = CreateTables()
    create_tables.create_tables()
    menu_system = MenuSystem()
    account_service = AccountService()

    # Check for auto-login
    if account_service.is_auto_login_enabled():
        username = account_service.get_auto_login_username()
        if username and account_service.login(username):
            clear()
            menu_system.main_menu(username)
            return

    while True:
        menu_system.user_menu()
        user_input = input("Enter Option: ")
        if user_input not in ['1', '2', '3']:
            clear()
            print("\n==== Invalid Option, Please Try Again ====\n")
        elif user_input == '3':
            clear()
            print("Goodbye!")
            sys.exit()
        else:
            break

    while True:
        if user_input == '1':
            username = menu_system.login_flow()
            if username:
                clear()
                menu_system.main_menu(username)
        elif user_input == '2':
            username = menu_system.register_flow()
            if username:
                clear()
                menu_system.main_menu(username)
        elif user_input == '3':
            print("Goodbye!")
            sys.exit()

if __name__ == '__main__':
    clear()
    main()
