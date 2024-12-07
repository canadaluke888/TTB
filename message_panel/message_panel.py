from rich.panel import Panel
from functools import cache

class MessagePanel:
    
    def __init__(self, console):
        self.console = console
        
        
    def create_information_message(self, message: str):
        self.console.print(Panel(f"[bold yellow]{message}[/]", title="[bold green]Information[/]", title_align="center", border_style="white"))
        
    def create_error_message(self, message: str):
        self.console.print(Panel(f"[bold red]{message}[/]", title="[bold red]Error[/]", title_align="center", border_style="white"))
        
    @cache
    def print_welcome_message(self):
        self.console.print(Panel("""
                                 [bold yellow]
                                 A terminal app where you can build and edit tables.
                                 
                                 SQLite database supported!
                                 [/]
                                 
                                 [bold red]Type 'help' for instructions.[/]
                                 """,
                                 title="[bold red]Terminal Table Builder[/]", 
                                 subtitle="[bold white]Welcome![/]", 
                                 subtitle_align="center", 
                                 border_style="cyan"
                                 )
                           )
        
    @cache
    def print_main_menu_instructions(self):
        self.console.print(Panel("""
                                 [green]
                                 table builder - Enter the table builder.
                                 database - Enter the database editor.
                                 settings - Enter the settings.
                                 exit - Exit the application.
                                 [/]
                                 """,
                                 title="[bold red]Main Menu[/] - [bold white]Instructions[/]",
                                 title_align="center",
                                 border_style="cyan"
                                 )
        )
    
    @cache
    def print_table_builder_instructions(self):
        self.console.print(Panel(""""
                                 [bold blue]Welcome to the Table Builder![/]
                                 
                                 [green]
                                 add column - Add a column to the table.
                                 add row - Add a row to the table.
                                 remove column - Removes a column from the table.
                                 remove row - Removes a row from the table.
                                 edit cell - Allows you to edit the content of a cell in the table.
                                 print table - Prints the table to the screen.
                                 rename - Renames the table.
                                 print table data - Prints the JSON data for the table.
                                 save table - Saves the table to the curretly set database.
                                 clear table - Clears the table from memory.
                                 load table - Loads a table from the database.
                                 load csv - Loads a CSV file into a formatted table.
                                 exit - Go back to the main menu.
                                 help - Prints this screen.
                                 [/]
                                 """, 
                                 title="[bold red]Table Builder[/] - [bold white]Instructions[/]", 
                                 title_align="center", 
                                 border_style="cyan"
                                 ))
        
    @cache
    def print_settings_instructions(self):
        self.console.print(Panel("""
                                 [bold pink]Welcome to the Settings![/]
                                 
                                 [bold yellow]Instructions[/]:
                                 [green]
                                 Enter the setting and then the value.
                                 [/green]
                                 
                                 [bold red]Enter 'print settings' to show the current settings.[/]
                                 """,
                                 title="[bold red]Settings[/] - [bold white]Instructions[/]", 
                                 title_align="center",
                                 border_style="cyan"
                                 ))
        
    @cache
    def print_database_instructions(self):
        self.console.print(Panel("""
                                 [bold yellow]Welcome to Databases![/]
                                 
                                 
                                 [blue]
                                 Here you can setup a database to save your tables you build in, making it easy to transfer.
                                 [/]
                                 
                                 
                                 [green]
                                 create database - Creates a new database.
                                 delete database - Deletes an existing database.
                                 set database - Set an available database as the current working database.
                                 show available databases - Prints the list of currently saved databases.
                                 help - Shows this screen.
                                 show available tables - Prints a list of saved tables under the currently set database.
                                 view table - Prints the saved table to the screen from the currently saved database.
                                 delete table - Deletes the table from the currently set database.
                                 show set database - Shows the curretly set database.
                                 [/]
                                 
                                 
                                 [bold red]'Exit' to go back to main menu.[/]
                                                                 
                                 """,
                                 title="[bold red]Database[/] - [bold white]Instructions[/]",
                                 title_align="center",
                                 subtitle="Instructions",
                                 subtitle_align="center",
                                 border_style="cyan"))