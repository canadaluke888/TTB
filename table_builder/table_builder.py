from rich.table import Table
from message_panel.message_panel import MessagePanel
import csv
import os
from autocomplete.autocomplete import Autocomplete

class TableBuilder:
    def __init__(self, console, settings, database):
        self.console = console
        self.database = database
        self.autocomplete = Autocomplete(self.console)
        self.settings = settings
        self.message_panel = MessagePanel(self.console)
        self.name = self.name_table()
        self.table_data = {"columns": [], "rows": []}
        self.table_saved = False
        
    def ensure_connected_database(self):
        """
        Ensure there is a connected database before proceeding with table operations.
        """
        if not self.database.is_connected():
            self.message_panel.create_error_message("No database connected.")
            return False
        return True
        
    def save_to_database(self):
        """
        Save the current table data to the connected database.
        """
        if not self.ensure_connected_database():
            return

        try:
            # Safely quote the table name
            quoted_table_name = f'"{self.name}"'
            columns_definition = ", ".join(f'"{col}" TEXT' for col in self.table_data["columns"])
            
            # Create the table if it does not exist
            self.database.cursor.execute(f"CREATE TABLE IF NOT EXISTS {quoted_table_name} ({columns_definition})")
            
            # Clear existing data
            self.database.cursor.execute(f"DELETE FROM {quoted_table_name}")

            # Insert new rows
            for row in self.table_data["rows"]:
                column_names = ", ".join(f'"{col}"' for col in self.table_data["columns"])
                placeholders = ", ".join("?" for _ in self.table_data["columns"])
                values = [row.get(col, "") for col in self.table_data["columns"]]
                self.database.cursor.execute(
                    f"INSERT INTO {quoted_table_name} ({column_names}) VALUES ({placeholders})", values
                )

            self.database.connection.commit()
            self.table_saved = True
            self.message_panel.create_information_message(f"[bold green]Table '{self.name}' saved to database '{self.database.get_current_database()}'.[/]")
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to saved to database: {e}")

            
    def load_from_database(self):
        """
        Load a table from the connected database.
        """
        if not self.ensure_connected_database():
            return

        try:
            self.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.database.cursor.fetchall()]

            if not tables:
                self.message_panel.create_error_message("No tables found in database.")
                return

            self.console.print("[bold green]Available Tables:[/]")
            for idx, table in enumerate(tables, start=1):
                self.console.print(f"{idx}. {table}")

            table_number = int(self.console.input("[bold yellow]Enter the number of the table to load[/]: ")) - 1
            if 0 <= table_number < len(tables):
                table_name = tables[table_number]
                quoted_table_name = f'"{table_name}"'  # Safely quote the table name
                self.database.cursor.execute(f"SELECT * FROM {quoted_table_name}")
                rows = self.database.cursor.fetchall()
                columns = [desc[0] for desc in self.database.cursor.description]

                self.table_data["columns"] = columns
                self.table_data["rows"] = [
                    {col: row[i] for i, col in enumerate(columns)}
                    for row in rows
                ]

                self.name = table_name
                self.table_saved = True
                self.message_panel.create_information_message(f"[bold green]Table '{table_name}' loaded successfully from database '{self.database.get_current_database()}'.[/]")
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()
            else:
                self.message_panel.create_error_message("Invalid table number.")
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to load table: {e}")


    def list_tables(self):
        """
        List all tables in the connected database.
        """
        if not self.ensure_connected_database():
            return

        try:
            self.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.database.cursor.fetchall()]

            if tables:
                self.console.print("[bold green]Available Tables:[/]")
                for idx, table in enumerate(tables, start=1):
                    self.console.print(f"{idx}. {table}")
            else:
                self.message_panel.create_error_message("No tables found in the database.")
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to list tables: {e}")
        
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

            self.table_saved = True
            self.message_panel.create_information_message(
                f"Table data successfully saved to '{file_name}'."
            )
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to save file: {e}")

    def name_table(self) -> str:
        self.table_saved = False
        return self.console.input("[bold yellow]Enter a name for the new table[/]: ")

            
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

                self.table_saved = False
                self.message_panel.create_information_message("CSV file loaded successfully.")
                
                # Automatically print the table if the setting is enabled
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()
        except Exception as e:
            self.message_panel.create_error_message(f"Failed to load CSV file: {e}")

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
            self.table_saved = False
            self.message_panel.create_information_message("Column added.")
        else:
            self.message_panel.create_error_message("Column already exists.")

    def add_row(self):
        row_data = {}
        for column in self.table_data["columns"]:
            cell_data = self.console.input(f"[bold yellow]Enter data for column {column}[/]: ")
            row_data[column] = cell_data
        self.table_data["rows"].append(row_data)
        self.table_saved = False
        self.message_panel.create_information_message("Row added.")

    def edit_cell(self):
        row_number = int(self.console.input("[bold yellow]Enter row number to edit (1-based index)[/]: ")) - 1
        column_name = self.console.input("[bold yellow]Enter column name[/]: ")
        if 0 <= row_number < len(self.table_data["rows"]) and column_name in self.table_data["columns"]:
            new_data = self.console.input(f"[bold yellow]Enter new data for cell in row {row_number + 1}, column {column_name}[/]: ")
            self.table_data["rows"][row_number][column_name] = new_data
            self.table_saved = False
            self.message_panel.create_information_message("Cell updated.")
        else:
            self.message_panel.create_error_message("Invalid row number or column name.")

    def remove_column(self):
        column_name = self.console.input("[bold yellow]Enter column name to remove[/]: ")
        if column_name in self.table_data["columns"]:
            self.table_data["columns"].remove(column_name)
            for row in self.table_data["rows"]:
                row.pop(column_name, None)
            self.table_saved = False
            self.message_panel.create_information_message("Column removed.")
        else:
            self.message_panel.create_error_message("Column not found.")

    def remove_row(self):
        row_number = int(self.console.input("[bold yellow]Enter row number to remove (1-based index)[/]: ")) - 1
        if 0 <= row_number < len(self.table_data["rows"]):
            self.table_data["rows"].pop(row_number)
            self.table_saved = False
            self.message_panel.create_information_message("Row removed.")
        else:
            self.message_panel.create_error_message("Invalid row number.")
            
    def delete_table(self):
        """
        Delete a table from the connected database by selecting it from a list of available tables.
        """
        if not self.ensure_connected_database():
            return

        try:
            # Get the list of available tables
            self.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.database.cursor.fetchall()]

            if not tables:
                self.console.print("[bold yellow]No tables found in the database.[/]")
                return

            # Display the available tables
            self.console.print("[bold green]Available Tables:[/]")
            for idx, table in enumerate(tables, start=1):
                self.console.print(f"{idx}. {table}")

            # Get user selection
            table_number = int(self.console.input("[bold yellow]Enter the number of the table to delete[/]: ")) - 1

            # Validate selection
            if 0 <= table_number < len(tables):
                table_name = tables[table_number]
                quoted_table_name = f'"{table_name}"'  # Safely quote the table name

                # Confirm deletion
                confirm = self.console.input(f"[bold red]Are you sure you want to delete table '{table_name}'? (y/n)[/]: ").lower().strip()
                if confirm == 'y':
                    # Execute deletion
                    self.database.cursor.execute(f"DROP TABLE {quoted_table_name}")
                    self.database.connection.commit()
                    self.console.print(f"[bold green]Table '{table_name}' has been deleted successfully.[/]")
                else:
                    self.console.print("[bold yellow]Table deletion cancelled.[/]")
            else:
                self.console.print("[bold red]Invalid table number.[/]")
        except Exception as e:
            self.console.print(f"[bold red]Failed to delete table: {e}[/]")


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
                self.load_from_database()
                
            elif builder_command == "save table":
                self.save_to_database()
                
            elif builder_command == "delete table":
                self.delete_table()
                
            elif builder_command == "load csv":
                self.load_csv()
            
            elif builder_command == "list tables":
                self.list_tables()

            elif builder_command == "save csv":
                self.save_to_csv()

            elif builder_command == "help":
                self.message_panel.print_table_builder_instructions()

            elif builder_command == "exit":
                if not self.table_saved:
                    exit_response = self.console.input("[bold red]Are you sure you want to exit without saving? (y/n)[/]: ").lower().strip()
                    
                    if exit_response == "y":
                        break
                    elif exit_response == "n":
                        continue
                    else:
                        self.message_panel.create_error_message("Invalid input.")
                        
                else:
                    break

            else:
                self.message_panel.create_error_message("Invalid Command.")
                self.autocomplete.suggest_command(builder_command, self.autocomplete.table_builder_commands)
