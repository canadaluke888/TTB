from rich.table import Table
from message_panel.message_panel import MessagePanel


class TableBuilder:
    def __init__(self, console, settings):
        self.console = console
        self.settings = settings
        self.message_panel = MessagePanel(self.console)
        self.name = self.name_table()
        self.table_data = {"columns": [], "rows": []}

    def name_table(self) -> str:
        return self.console.input("[bold yellow]Enter a name for the new table[/]: ")

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
            builder_command = self.console.input("[bold red]Table Builder[/] - [bold yellow]Enter a command[/]: ")

            if builder_command == "print_help":
                self.message_panel.print_table_builder_instructions()

            elif builder_command == "add_column":
                self.add_column()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "add_row":
                self.add_row()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "edit_cell":
                self.edit_cell()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "remove_column":
                self.remove_column()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "remove_row":
                self.remove_row()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()

            elif builder_command == "print_table":
                self.print_table()

            elif builder_command == "print_table_data":
                self.print_table_data()

            elif builder_command == "clear_table":
                self.clear_table()

            elif builder_command == "rename":
                self.name = self.name_table()
                if self.settings.get_autoprint_table() == "on":
                    self.print_table()
                
            elif builder_command == "help":
                self.message_panel.print_table_builder_instructions()
                
            elif builder_command == "exit":
                break

            else:
                self.message_panel.create_error_message("Invalid Command.")
