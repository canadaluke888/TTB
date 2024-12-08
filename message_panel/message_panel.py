from rich.panel import Panel
from functools import cache

class MessagePanel:
    def __init__(self, console):
        """
        Initialize main console.

        Args:
            console (Console): rich console.
        """
        self.console = console

    def create_information_message(self, message: str) -> Panel:
        """
        Create a custom informational message from the system.

        Args:
            message (str): The message to display.

        Returns:
            Panel: The redered panel with the message.
        """
        self.console.print(
            Panel(
                f"[bold yellow]{message}[/]",
                title="[bold green]Information[/]",
                title_align="center",
                border_style="white",
            )
        )

    def create_error_message(self, message: str) -> Panel:
        """
        Create a custom error message from the system.

        Args:
            message (str): The message and, optionally, error you want to display.

        Returns:
            Panel: The rendered panel with the message.
        """
        self.console.print(
            Panel(
                f"[bold red]{message}[/]",
                title="[bold red]Error[/]",
                title_align="center",
                border_style="white",
            )
        )

    @cache
    def print_welcome_message(self) -> Panel:
        """
        Print the welcome message upon login.
        
        Return: The rendered panel with the welcome message.
        """
        
        self.console.print(
            Panel(
                """
[bold yellow]A terminal app where you can build and edit tables.[/]

[bold cyan]SQLite database supported![/]

[bold red]Type 'help' for instructions.[/]
                """,
                title="[bold red]Terminal Table Builder[/]",
                subtitle="[bold white]Welcome![/]",
                subtitle_align="center",
                border_style="cyan",
            )
        )

    @cache
    def print_main_menu_instructions(self) -> Panel:
        """
        Print the commands for the main menu.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(
                """
[green]
- table builder: Enter the table builder.
- settings: Enter the settings.
- exit: Exit the application.
[/]
                """,
                title="[bold red]Main Menu[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )

    @cache
    def print_table_builder_instructions(self) -> Panel:
        """
        Print the commands for the table builder portion of the app.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(
                """
[bold blue]Welcome to the Table Builder![/]

[green]
- add column: Add a column to the table.
- add row: Add a row to the table.
- remove column: Removes a column from the table.
- remove row: Removes a row from the table.
- edit cell: Allows you to edit the content of a cell in the table.
- print table: Prints the table to the screen.
- rename: Renames the table.
- print table data: Prints the JSON data for the table.
- clear table: Clears the table from memory.
- load table: Load a table from the database.
- delete table: Deletes the table from the database.
- save table: Save the table to the database.
- print table data: Print the JSON data for the current table.
- load csv: Loads a CSV file into a formatted table.
- load csv batch: Load a bunch of CSV files automatically from a directory into the database.
- list tables: List the avalable tables from the database.
- save csv: Save the data from the table to a CSV file.
- save pdf: Save the table to a PDF file.
- exit: Go back to the main menu.
- help: Prints this screen.
[/]
                """,
                title="[bold red]Table Builder[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )

    @cache
    def print_settings_instructions(self) -> Panel:
        """
        Print the commands for the settings.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(
                """
[bold pink]Welcome to the Settings![/]

[bold yellow]Instructions:[/]
[green]
- Enter the setting and then the value.
- Use 'print settings' to show the current settings.
[/green]
[bold red]Tip:[/] Double-check your input for accuracy!
                """,
                title="[bold red]Settings[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )

    @cache
    def print_database_instructions(self) -> Panel:
        """
        Print the commands for the database portion of the app.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(
                """
[bold yellow]Welcome to the Database Manager![/]

[green]
- [bold cyan]create database:[/] Create a new SQLite database and set it as the current database.
- [bold cyan]delete database:[/] Delete an existing SQLite database.
- [bold cyan]list databases:[/] List all databases in a specified directory.
- [bold cyan]select database:[/] Choose a database from a list of available databases.
- [bold cyan]current database:[/] Show the currently connected database.
- [bold cyan]search:[/] Search through the current  
- [bold cyan]help:[/] Print this instruction screen.
- [bold cyan]exit:[/] Return to the main menu.
[/green]

[bold red]Tip:[/] Use [bold cyan]select database[/] to view a set a database.[bold cyan]search[/] to locate table data.
                """,
                title="[bold red]Database Manager[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )
