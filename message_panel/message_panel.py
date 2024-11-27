from rich.panel import Panel
from rich.markdown import Markdown

class MessagePanel:
    
    def __init__(self, console):
        self.console = console
        
        
    def create_information_message(self, message: str):
        self.console.print(Panel(f"[bold yellow]{message}[/]", title="Information", title_align="center", border_style="white"))
        
    def create_error_message(self, message: str):
        self.console.print(Panel(f"[bold red]{message}[/]", title="Error", title_align="center", border_style="white"))
        
    def print_welcome_message(self):
        self.console.print(Panel("""
                                 [bold yellow]A terminal app where you can build tables.[/]
                                 
                                 [bold red]Type 'help' for instructions.[/]
                                 """,
                                 title="Terminal Table Builder", 
                                 subtitle="Welcome!", 
                                 subtitle_align="center", 
                                 border_style="cyan"
                                 )
                           )
        
    def print_main_menu_instructions(self):
        self.console.print(Panel("""
                                 [green]
                                 table_builder - Enter the table builder.
                                 database - Enter the database editor.
                                 settings - Enter the settings.
                                 exit - Exit the application.
                                 [/]
                                 """,
                                 title="[bold red]Main Menu[/] - [bold yellow]Instructions[/]",
                                 title_align="center",
                                 border_style="cyan"
                                 )
        )
    def print_table_builder_instructions(self):
        self.console.print(Panel(""""
                                 [bold blue]Welcome to the Table Builder![/]
                                 
                                 [green]
                                 add_column - Add a column to the table.
                                 add_row - Add a row to the table.
                                 remove_column - Removes a column from the table.
                                 remove_row - Removes a row from the table.
                                 edit_cell - Allows you to edit the content of a cell in the table.
                                 print_table - Prints the table to the screen.
                                 rename - Renames the table.
                                 print_table_data - Prints the JSON data for the table.
                                 save_table - Saves the table to the curretly set database.
                                 load_table - Loads a table from the database.
                                 exit - Go back to the main menu.
                                 help - Prints this screen.
                                 [/]
                                 """, 
                                 title="Table Builder", 
                                 title_align="center", 
                                 subtitle="Instructions", 
                                 border_style="cyan"
                                 ))
        
    def print_settings_instructions(self):
        self.console.print(Panel("""
                                 [bold pink]Welcome to the Settings![/]
                                 
                                 [bold yellow]Instructions[/]:
                                 [green]
                                 Enter the setting and then the value.
                                 [/green]
                                 
                                 [bold red]Enter 'print_settings' to show the current settings.[/]
                                 """,
                                 title="Settings", 
                                 title_align="center", 
                                 subtitle="Instructions", 
                                 subtitle_align="center", 
                                 border_style="cyan"
                                 ))
        
    def print_database_instructions(self):
        self.console.print(Panel("""
                                 [bold yellow]Welcome to Databases![/]
                                 
                                 
                                 [blue]
                                 Here you can setup a database to save your tables you build in, making it easy to transfer.
                                 [/]
                                 
                                 
                                 [green]
                                 create_database - Creates a new database.
                                 delete_database - Deletes an existing database.
                                 set_database - Set an available database as the current working database.
                                 show_available_databases - Prints the list of currently saved databases.
                                 help - Shows this screen.
                                 show_available_tables - Prints a list of saved tables under the currently set database.
                                 view_table - Prints the saved table to the screen from the currently saved database.
                                 delete_table - Deletes the table from the currently set database.
                                 show_set_database - Shows the curretly set database.
                                 [/]
                                 
                                 
                                 [bold red]'Exit' to go back to main menu.[/]
                                                                 
                                 """,
                                 title="[bold red]Database[/] - [bold yellow]Instructions[/]",
                                 title_align="center",
                                 subtitle="Instructions",
                                 subtitle_align="center",
                                 border_style="cyan"))