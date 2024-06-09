import configparser
import msvcrt
import logging
import os
import regex as re
from db.model import UserModel
from cryptography.fernet import Fernet
from utils.encript import encript, check_password

LOG_FILE = 'logs/account_service.log'

class AccountService:
    def __init__(self):
        self.user_model = UserModel()
        self.config_file = 'logs/auto_login.ini'
        self.setup_logging()


    def setup_logging(self):
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

    def log_action(self, message):
        logging.info(message)
    


    def login(self, username, password=None):
        user = self.user_model.get_user(username)
        if not user:
            # print("\nLogin Failed: User not found")
            self.log_action(f"Login Failed: User {username} not found")
            return False
        if password is None:
            print("Auto Login Successful")
            self.log_action(f"Auto Login Successful: User {username}")
            return user[0]  # Assuming user_id is at index 0
        if check_password(password, user[3]):
            print("Login Successful")
            self.log_action(f"Login Successful: User {username}")
            return user[0]  # Assuming user_id is at index 0
        else:
            self.log_action(f"Login Failed: Invalid Password for User {username}")
            return False

    def register(self, username, email, password):
        encrypted_password = encript(password)
        user_id = self.user_model.create_user(username, email, encrypted_password)
        if user_id:
            print("Registration Successful")
            self.log_action(f"Registration Successful: User {username}")
            return user_id
        else:
            self.log_action(f"Registration Failed: User {username}")
            return False

    def logout(self, username):
        self.log_action(f"User {username} logged out")
    
    def toggle_auto_login(self, username=None):
        config = configparser.ConfigParser()

        # Read the existing config file
        if os.path.exists(self.config_file):
            config.read(self.config_file)
        else:
            config['auto_login'] = {'enabled': 'False', 'username': ''}

        # Toggle the auto-login state
        if config['auto_login'].getboolean('enabled'):
            config['auto_login']['enabled'] = 'False'
            config['auto_login']['username'] = ''
            print("Auto-login has been disabled.")
        else:
            if username:
                config['auto_login']['enabled'] = 'True'
                config['auto_login']['username'] = username
                print("Auto-login has been enabled for user:", username)
            else:
                print("Cannot enable auto-login without a username.")

        # Write the changes back to the config file
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def is_auto_login_enabled(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            return config['auto_login'].getboolean('enabled')
        return False

    def get_auto_login_username(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            return config['auto_login']['username']
        return None


    @staticmethod
    def get_password(prompt="Enter Password: "):
        print(prompt, end='', flush=True)
        password = []
        while True:
            ch = msvcrt.getch()
            if ch in {b'\n', b'\r'}:
                print()
                break
            elif ch == b'\x08':  # Backspace
                if password:
                    password.pop()
                    print('\b \b', end='', flush=True)
            else:
                password.append(ch.decode('utf-8'))
                print('*', end='', flush=True)
        return ''.join(password)

    @staticmethod
    def validate_username(username):
        pattern = re.compile(r"^[a-zA-Z0-9_]{5,}$")
        return pattern.match(username)

    @staticmethod
    def validate_email(email):
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(email)

    @staticmethod
    def validate_password(password):
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$")
        return pattern.match(password)

    def get_valid_username(self):
        while True:
            username = input("Enter Username: ").title()
            if self.validate_username(username):
                return username
            else:
                print("Invalid Username. Must be at least 5 characters long and can include letters, numbers, and underscores.")

    def get_valid_email(self):
        while True:
            email = input("Enter Email: ")
            if self.validate_email(email):
                return email
            else:
                print("Invalid Email format.")

    def get_valid_password(self):
        while True:
            password = self.get_password("Enter Password: ")
            if self.validate_password(password):
                confirm_password = self.get_password("Confirm Password: ")
                if password == confirm_password:
                    return password
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Password must contain at least 8 characters, one uppercase, one lowercase, one digit, and one special character.")

    def get_valid_confirm_password(self, password):
        while True:
            confirm_password = self.get_password("Confirm Password: ")
            if password == confirm_password:
                return confirm_password
            else:
                print("Passwords do not match. Please try again.")

