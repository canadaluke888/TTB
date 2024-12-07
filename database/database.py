import sqlite3
import os
from rich.console import Console
from message_panel.message_panel import MessagePanel
from autocomplete.autocomplete import Autocomplete


class Database:
    def __init__(self, console: Console):
        """
        Initialize the Database manager.
        :param console: Console instance for rich text output.
        """
        self.console = console
        self.message_panel = MessagePanel(self.console)
        self.autocomplete = Autocomplete(self.console)
        self.current_database = None
        self.connection = None
        self.cursor = None
        self.database_directory = os.path.join(os.getcwd(), "databases")
        self.ensure_database_directory()

    def ensure_database_directory(self):
        """
        Ensure the 'databases' directory exists in the current working directory.
        """
        if not os.path.exists(self.database_directory):
            os.makedirs(self.database_directory)
            self.message_panel.create_information_message(f"Created 'databases' directory at {self.database_directory}")
            
    def connect(self, db_name: str):
        """
        Connect to the specified SQLite database in the 'databases' directory.
        """
        db_path = os.path.join(self.database_directory, db_name)
        if not os.path.exists(db_path):
            self.message_panel.create_error_message(f"Database '{db_name}' does not exist in the 'databases' directory.")
            return
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.current_database = db_name
            self.message_panel.create_information_message(f"Connected to database: {db_name}")
        except sqlite3.Error as e:
            self.message_panel.create_error_message(f"Failed to connect to database: {e}")

    def close(self):
        """
        Close the current database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            self.current_database = None
            self.message_panel.create_information_message("Database connection closed.")

    def get_current_database(self):
        """
        Get the name of the currently connected database.
        """
        return self.current_database

    def is_connected(self):
        """
        Check if a database is currently connected.
        """
        return self.connection is not None

    def create_database(self, db_name: str):
        """
        Create a new SQLite database in the 'databases' directory.
        """
        db_path = os.path.join(self.database_directory, db_name)
        if os.path.exists(db_path):
            self.message_panel.create_error_message("Database already exists. Connect instead.")
            return
        try:
            open(db_path, 'w').close()  # Create an empty file
            self.message_panel.create_information_message(f"Database created: {db_name}")
            self.connect(db_name)
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to create database: {e}")

    def delete_database(self, db_name: str):
        """
        Delete the specified SQLite database from the 'databases' directory.
        """
        db_path = os.path.join(self.database_directory, db_name)
        if not os.path.exists(db_path):
            self.message_panel.create_error_message("Database does not exist.")
            return
        try:
            os.remove(db_path)
            self.message_panel.create_information_message(f"Database deleted: {db_name}")
            if self.current_database == db_name:
                self.close()
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to delete database: {e}")

    def list_databases(self):
        """
        List all SQLite databases in the 'databases' directory.
        """
        databases = [f for f in os.listdir(self.database_directory) if f.endswith('.db')]
        if not databases:
            self.message_panel.create_error_message("No databases found.")
            return []

        self.console.print("[bold green]Available Databases:[/]")
        for idx, db in enumerate(databases, start=1):
            self.console.print(f"{idx}. {db}")
        return databases

    def select_database(self):
        """
        Allow the user to select a database from the 'databases' directory.
        """
        databases = self.list_databases()
        if not databases:
            return

        try:
            db_number = int(self.console.input("[bold yellow]Select a database number[/]: ")) - 1
            if 0 <= db_number < len(databases):
                self.connect(databases[db_number])
            else:
                self.message_panel.create_error_message("Invlalid database number.")
        except ValueError:
            self.message_panel.create_error_message("Invalid input. Please enter a valid number.")

    def launch_database(self):
        """
        Interactive interface for managing databases.
        """
        self.message_panel.print_database_instructions()
        while True:
            command = self.console.input(
                "[bold red]Database Manager[/] - [bold yellow]Enter a command[/]: "
            ).strip().lower()

            if command == "create database":
                db_name = self.console.input(
                    "[bold yellow]Enter the name for the new database (without .db)[/]: "
                ) + ".db"
                self.create_database(db_name)

            elif command == "delete database":
                db_name = self.console.input(
                    "[bold yellow]Enter the name of the database to delete (without .db)[/]: "
                ) + ".db"
                self.delete_database(db_name)

            elif command == "list databases":
                self.list_databases()

            elif command == "select database":
                self.select_database()

            elif command == "current database":
                self.message_panel.create_information_message(f"Current database: {self.current_database}")

            elif command == "close database":
                self.close()

            elif command == "help":
                self.message_panel.print_database_instructions()

            elif command == "exit":
                break

            else:
                self.message_panel.create_error_message("Invalid input.")
                self.autocomplete.suggest_command(command, self.autocomplete.database_commands)
