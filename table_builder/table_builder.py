from rich.table import Table
from message_panel.message_panel import MessagePanel
import sqlite3
from rich.panel import Panel
import csv
import os
from autocomplete.autocomplete import Autocomplete

class TableBuilder:
    def __init__(self, console, settings, database):
        self.console = console
        self.autocomplete = Autocomplete(self.console)
        self.settings = settings
        self.database = database
        self.message_panel = MessagePanel(self.console)
        self.name = self.name_table()
        self.table_data = {"columns": [], "rows": []}
        
    def save_to_csv(self):
        """
        Save the current table data to a CSV file.
        """
        use_table_name = self.console.input(
            "[bold yellow]Use table name as save file name? (y/n)[/]: ").lower().strip()

        if use_table_name == "y":
            file_name = f"{self.name}.csv"
        elif use_table_name == "n":
            file_name = self.console.input(
                "[bold yellow]Enter the name of the file (without extension)[/]: ") + ".csv"
        else:
            self.message_panel.create_error_message("Invalid input.")
            return

        # Write table data to the CSV file
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write header row (columns)
                if self.table_data["columns"]:
                    writer.writerow(self.table_data["columns"])

                # Write data rows
                for row in self.table_data["rows"]:
                    writer.writerow([row.get(column, "") for column in self.table_data["columns"]])

            self.message_panel.create_information_message(
                f"Table data successfully saved to '{file_name}'."
            )
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to save file: {e}")

    def name_table(self) -> str:
        return self.console.input("[bold yellow]Enter a name for the new table[/]: ")
    
    def save_table(self):
        if self.database.current_database is None:
            self.message_panel.create_error_message("Please set a database first.")
            return

        connection = None  # Initialize connection to avoid UnboundLocalError
        try:
            connection = sqlite3.connect(f"database/db/{self.database.current_database}.db")
            cursor = connection.cursor()

            # Escape table name to avoid reserved keyword issues
            escaped_table_name = f"[{self.name}]"

            # Create table if it doesn't exist
            columns_definition = ", ".join([f"{col} TEXT" for col in self.table_data["columns"]])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {escaped_table_name} ({columns_definition});")

            # Clear existing data in the table
            cursor.execute(f"DELETE FROM {escaped_table_name};")

            # Insert rows into the table
            for row in self.table_data["rows"]:
                placeholders = ", ".join(["?" for _ in self.table_data["columns"]])
                values = [row[col] for col in self.table_data["columns"]]
                cursor.execute(f"INSERT INTO {escaped_table_name} VALUES ({placeholders});", values)

            connection.commit()
            self.message_panel.create_information_message(f"Table '{self.name}' saved successfully.")

        except sqlite3.Error as e:
            self.message_panel.create_error_message(f"Error saving table: {e}")
        finally:
            if connection:  # Check if connection is initialized before closing
                connection.close()

            
    def load_csv(self):
        """
        Loads a CSV file and updates the table data for building a table.

        Prompts the user for the CSV file path and validates the input.
        """
        csv_path = self.console.input("[bold yellow]Enter path to CSV file[/]: ")

        # Check if the path is valid
        if not os.path.isfile(csv_path):
            self.message_panel.create_error_message("Invalid path or file does not exist.")
            return

        try:
            with open(csv_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)  # Convert reader to a list of rows
                
                if not rows:
                    self.message_panel.create_error_message("CSV file is empty.")
                    return

                # First row as columns
                self.table_data["columns"] = rows[0]
                # Remaining rows as data
                self.table_data["rows"] = [
                    {col: value for col, value in zip(self.table_data["columns"], row)}
                    for row in rows[1:]
                ]

                self.message_panel.create_information_message("CSV file loaded successfully.")
                
                # Automatically print the table if the setting is enabled
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to load CSV file: {e}")
            
    def load_table(self):
        if self.database.current_database is None:
            self.message_panel.create_error_message("Please set a database first.")
            return

        try:
            connection = sqlite3.connect(f"database/db/{self.database.current_database}.db")
            cursor = connection.cursor()

            # Show available tables
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
                    title=f"Tables in '{self.database.current_database}'",
                    border_style="green",
                    expand=False
                )
            )

            # Prompt user to select a table
            selection = int(self.console.input("[bold yellow]Enter the number corresponding to the table to load:[/] ")) - 1
            if 0 <= selection < len(tables):
                selected_table = tables[selection][0]

                # Load table structure and data
                cursor.execute(f"PRAGMA table_info({selected_table});")
                columns = [col[1] for col in cursor.fetchall()]
                cursor.execute(f"SELECT * FROM {selected_table};")
                rows = cursor.fetchall()

                self.name = selected_table
                self.table_data = {
                    "columns": columns,
                    "rows": [{col: str(cell) for col, cell in zip(columns, row)} for row in rows]
                }

                self.message_panel.create_information_message(f"Table '{selected_table}' loaded successfully.")
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()
            else:
                self.message_panel.create_error_message("Invalid selection. Please choose a valid number.")

        except ValueError:
            self.message_panel.create_error_message("Invalid input. Please enter a number.")
        except sqlite3.Error as e:
            self.message_panel.create_error_message(f"Error loading table: {e}")
        finally:
            connection.close()

    def get_num_columns(self):
        return len(self.table_data["columns"])

    def get_num_rows(self):
        return len(self.table_data["rows"])

    def add_column(self):
        column_name = self.console.input("[bold yellow]Enter column name[/]: ")
        if column_name not in self.table_data["columns"]:
            self.table_data["columns"].append(column_name)
            # Add empty values for the new column to existing rows
            for row in self.table_data["rows"]:
                row[column_name] = ""
            self.message_panel.create_information_message("Column added.")
        else:
            self.message_panel.create_error_message("Column already exists.")

    def add_row(self):
        row_data = {}
        for column in self.table_data["columns"]:
            cell_data = self.console.input(f"[bold yellow]Enter data for column {column}[/]: ")
            row_data[column] = cell_data
        self.table_data["rows"].append(row_data)
        self.message_panel.create_information_message("Row added.")

    def edit_cell(self):
        row_number = int(self.console.input("[bold yellow]Enter row number to edit (1-based index)[/]: ")) - 1
        column_name = self.console.input("[bold yellow]Enter column name[/]: ")
        if 0 <= row_number < len(self.table_data["rows"]) and column_name in self.table_data["columns"]:
            new_data = self.console.input(f"[bold yellow]Enter new data for cell in row {row_number + 1}, column {column_name}[/]: ")
            self.table_data["rows"][row_number][column_name] = new_data
            self.message_panel.create_information_message("Cell updated.")
        else:
            self.message_panel.create_error_message("Invalid row number or column name.")

    def remove_column(self):
        column_name = self.console.input("[bold yellow]Enter column name to remove[/]: ")
        if column_name in self.table_data["columns"]:
            self.table_data["columns"].remove(column_name)
            for row in self.table_data["rows"]:
                row.pop(column_name, None)
            self.message_panel.create_information_message("Column removed.")
        else:
            self.message_panel.create_error_message("Column not found.")

    def remove_row(self):
        row_number = int(self.console.input("[bold yellow]Enter row number to remove (1-based index)[/]: ")) - 1
        if 0 <= row_number < len(self.table_data["rows"]):
            self.table_data["rows"].pop(row_number)
            self.message_panel.create_information_message("Row removed.")
        else:
            self.message_panel.create_error_message("Invalid row number.")

    def build_table(self) -> Table:
        table = Table(title=self.name, border_style="yellow", show_lines=True)
        # Add columns
        for column in self.table_data["columns"]:
            table.add_column(column, style="cyan")
        # Add rows
        for row in self.table_data["rows"]:
            row_values = [row.get(column, "") for column in self.table_data["columns"]]
            table.add_row(*row_values, style="magenta")
        return table

    def print_table(self):
        table = self.build_table()
        self.console.print(table)

    def print_table_data(self):
        self.console.print(self.table_data)

    def clear_table(self):
        self.table_data = {"columns": [], "rows": []}
        self.message_panel.create_information_message("Table cleared.")

    def launch_builder(self):
        self.message_panel.print_table_builder_instructions()

        while True:
            builder_command = self.console.input("[bold red]Table Builder[/] - [bold yellow]Enter a command[/]: ").lower().strip()

            if builder_command == "print help":
                self.message_panel.print_table_builder_instructions()

            elif builder_command == "add column":
                self.add_column()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "add row":
                self.add_row()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "edit cell":
                self.edit_cell()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "remove column":
                self.remove_column()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "remove row":
                self.remove_row()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "print table":
                self.print_table()

            elif builder_command == "print table data":
                self.print_table_data()

            elif builder_command == "clear table":
                self.clear_table()

            elif builder_command == "rename":
                self.name = self.name_table()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "load table":
                self.load_table()
                
            elif builder_command == "load csv":
                self.load_csv()

            elif builder_command == "save csv":
                self.save_to_csv()

            elif builder_command == "save table":
                self.save_table()

            elif builder_command == "help":
                self.message_panel.print_table_builder_instructions()

            elif builder_command == "exit":
                break

            else:
                self.message_panel.create_error_message("Invalid Command.")
                self.autocomplete.suggest_command(builder_command, self.autocomplete.table_builder_commands)
