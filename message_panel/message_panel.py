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