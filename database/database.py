import sqlite3
from message_panel.message_panel import MessagePanel
import json
from rich.panel import Panel
import os
from autocomplete.autocomplete import Autocomplete

class Database:
    
    def __init__(self, console):
        self.console = console
        self.autocomplete = Autocomplete(self.console)
        self.message_panel = MessagePanel(self.console)
        self.databases_file = "database/databases.json"
        self.databases = self.load_databases()
        self.current_database = None
        
    def load_databases(self) -> dict:
        with open(self.databases_file, 'r') as f:
            return json.load(f)
        
    def save_databases(self):
        with open(self.databases_file, 'w') as f:
            json.dump(self.databases, f, indent=4)
            
    def create_new_database(self):
        database_name = self.console.input("[bold yellow]Enter a name for the database[/]: ")
        self.databases[database_name] = {"tables": {}}
        self.save_databases()
        self.message_panel.create_information_message(f"{database_name} database created.")
        
    def show_availalable_databases(self):
        database_list = "\n".join([f"[bold cyan]{i + 1}[/]: {db_name}" for i, db_name in enumerate(self.databases.keys())])
        self.console.print(
            Panel(
                database_list,
                title="Available Databases",
                border_style="green",
                expand=False
            )
        )
            
    def set_database(self):
        if len(self.databases.items()) < 1:
            self.message_panel.create_error_message("Please create a database first.")
            return
        else:
            self.show_availalable_databases()

        try:
            selection = int(self.console.input("[bold yellow]Enter the number corresponding to the database you want to set:[/] ")) - 1
            if 0 <= selection < len(self.databases):
                selected_db_name = list(self.databases.keys())[selection]
                self.current_database = selected_db_name
                self.message_panel.create_information_message(f"Database '{selected_db_name}' is now set as the current database.")
            else:
                self.message_panel.create_error_message("Invalid selection. Please choose a valid number.")
        except ValueError:
            self.message_panel.create_error_message("Invalid input. Please enter a number.")
            
    import os

    def delete_database(self):
        if len(self.databases.items()) < 1:
            self.message_panel.create_error_message("Please create a database first.")
            return

        self.show_availalable_databases()

        try:
            selection = int(self.console.input("[bold yellow]Enter the number corresponding to the database you want to delete:[/] ")) - 1
            if 0 <= selection < len(self.databases):
                selected_db_name = list(self.databases.keys())[selection]

                # Confirm deletion
                confirm = self.console.input(f"[bold red]Are you sure you want to delete database '{selected_db_name}'? (yes/no):[/] ").lower().strip()
                if confirm == "yes":
                    # Remove from the JSON data
                    del self.databases[selected_db_name]
                    self.save_databases()

                    # Delete the database file
                    db_file_path = f"database/db/{selected_db_name}.db"
                    if os.path.exists(db_file_path):
                        os.remove(db_file_path)

                    self.message_panel.create_information_message(f"Database '{selected_db_name}' has been deleted.")
                else:
                    self.message_panel.create_information_message("Database deletion canceled.")
            else:
                self.message_panel.create_error_message("Invalid selection. Please choose a valid number.")
        except ValueError:
            self.message_panel.create_error_message("Invalid input. Please enter a number.")

                
        def show_available_tables(self):
            if self.current_database is None:
                self.message_panel.create_error_message("Please set a database first.")
                return

            try:
                # Corrected the path to match the folder structure
                connection = sqlite3.connect(f"database/db/{self.current_database}.db")
                cursor = connection.cursor()

                # Fetch table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                if not tables:
                    self.message_panel.create_information_message("No tables found in the current database.")
                else:
                    # Display tables in a panel
                    table_list = "\n".join([f"[bold cyan]{i + 1}[/]: {table[0]}" for i, table in enumerate(tables)])
                    self.console.print(
                        Panel(
                            table_list,
                            title=f"Tables in '{self.current_database}'",
                            border_style="green",
                            expand=False
                        )
                    )

            except sqlite3.Error as e:
                self.message_panel.create_error_message(f"Error accessing database: {e}")
            finally:
                connection.close()
            
    def view_table(self):
        if self.current_database is None:
            self.message_panel.create_error_message("Please set a database first.")
            return

        try:
            connection = sqlite3.connect(f"database/db/{self.current_database}.db")
            cursor = connection.cursor()

            # Fetch table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            if not tables:
                self.message_panel.create_information_message("No tables found in the current database.")
                return

            # Display available tables
            table_list = "\n".join([f"[bold cyan]{i + 1}[/]: {table[0]}" for i, table in enumerate(tables)])
            self.console.print(
                Panel(
                    table_list,
                    title=f"Tables in '{self.current_database}'",
                    border_style="green",
                    expand=False
                )
            )

            # Prompt user to select a table
            try:
                selection = int(self.console.input("[bold yellow]Enter the number corresponding to the table you want to view:[/] ")) - 1
                if 0 <= selection < len(tables):
                    selected_table = tables[selection][0]
                    
                    # Escape table name
                    escaped_table_name = f"[{selected_table}]"

                    # Fetch table contents
                    cursor.execute(f"SELECT * FROM {escaped_table_name};")
                    rows = cursor.fetchall()

                    # Fetch column names
                    cursor.execute(f"PRAGMA table_info({escaped_table_name});")
                    columns = [col[1] for col in cursor.fetchall()]

                    if not rows:
                        self.message_panel.create_information_message(f"Table '{selected_table}' is empty.")
                        return

                    # Display table data using Rich's Table
                    from rich.table import Table as RichTable

                    rich_table = RichTable(title=f"Contents of '{selected_table}'", show_lines=True)
                    for column in columns:
                        rich_table.add_column(column, style="cyan")

                    for row in rows:
                        rich_table.add_row(*[str(cell) for cell in row])

                    self.console.print(rich_table)
                else:
                    self.message_panel.create_error_message("Invalid selection. Please choose a valid number.")
            except ValueError:
                self.message_panel.create_error_message("Invalid input. Please enter a number.")

        except sqlite3.Error as e:
            self.message_panel.create_error_message(f"Error accessing database: {e}")
        finally:
            connection.close()


            
    def delete_table(self):
        if self.current_database is None:
            self.message_panel.create_error_message("Please set a database first.")
            return

        try:
            # Connect to the SQLite database
            connection = sqlite3.connect(f"database/db/{self.current_database}.db")
            cursor = connection.cursor()

            # Fetch table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            if not tables:
                self.message_panel.create_information_message("No tables found in the current database.")
                return

            # Display tables in a panel
            table_list = "\n".join([f"[bold cyan]{i + 1}[/]: {table[0]}" for i, table in enumerate(tables)])
            self.console.print(
                Panel(
                    table_list,
                    title=f"Tables in '{self.current_database}'",
                    border_style="green",
                    expand=False
                )
            )

            # Prompt user to select a table to delete
            try:
                selection = int(self.console.input("[bold yellow]Enter the number corresponding to the table you want to delete:[/] ")) - 1
                if 0 <= selection < len(tables):
                    selected_table = tables[selection][0]

                    # Escape table name
                    escaped_table_name = f"[{selected_table}]"

                    # Confirm deletion
                    confirm = self.console.input(f"[bold red]Are you sure you want to delete table '{selected_table}'? (yes/no):[/] ").lower().strip()
                    if confirm == "yes":
                        # Delete the selected table
                        cursor.execute(f"DROP TABLE IF EXISTS {escaped_table_name};")
                        connection.commit()
                        self.message_panel.create_information_message(f"Table '{selected_table}' has been deleted.")
                    else:
                        self.message_panel.create_information_message("Table deletion canceled.")
                else:
                    self.message_panel.create_error_message("Invalid selection. Please choose a valid number.")
            except ValueError:
                self.message_panel.create_error_message("Invalid input. Please enter a number.")

        except sqlite3.Error as e:
            self.message_panel.create_error_message(f"Error accessing database: {e}")
        finally:
            connection.close()
            
    def show_set_database(self):
        return self.message_panel.create_information_message(f"Set database: {self.current_database}")
            
    def launch_database_editor(self):
        self.message_panel.print_database_instructions()
        
        while True:
            database_command = self.console.input("[bold red]Database[/] - [bold yellow]Enter a command[/]: ").lower()
            if database_command == "create database":
                self.create_new_database()
            elif database_command == "delete database":
                self.delete_database()
            elif database_command == "set database":
                self.set_database()
            elif database_command == "show available tables":
                self.show_available_tables()
            elif database_command == "view table":
                self.view_table()
            elif database_command == "delete table":
                self.delete_table()
            elif database_command == "show set database":
                self.show_set_database()
            elif database_command == "help":
                self.message_panel.print_database_instructions()
            elif database_command == "show available databases":
                self.show_availalable_databases()
            elif database_command == "exit":
                break
            else:
                self.message_panel.create_error_message("Inavalid input.")
                self.autocomplete.suggest_command(database_command, self.autocomplete.database_commands)
