from message_panel.message_panel import MessagePanel
from rich.table import Table
import json

class Settings:
    
    def __init__(self, console):
        self.console = console
        self.settings_file = "settings/settings.json"
        self.message_panel = MessagePanel(self.console)
        self.settings = self.load_settings()
        
    def launch_settings(self):
        self.message_panel.print_settings_instructions()
        
        while True:
            setting = self.console.input("[bold red]Settings[/] - [bold yellow]Enter a setting[/]: ")
            
            if setting == "autoprint_table":
                value = self.console.input("[bold yellow]Turn Autoprint on or off[/]: ").lower()
                self.set_autoprint_table(value)
                self.save_settings()
                
            elif setting == "print_settings":
                self.print_settings()
                
            elif setting == "exit":
                break
                
            else:
                self.message_panel.create_error_message("Invalid Input.")
                
    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default settings if file is missing or corrupted
            return {"autoprint_table": False}
        
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
        
    def print_settings(self):
        table = Table(title="Settings", border_style="yellow", show_lines=True)
        table.add_column("Setting", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Value", style="magenta")
        
        # Dynamically add rows from settings dictionary
        for setting, value in self.settings.items():
            description = self.get_setting_description(setting)
            table.add_row(setting, description, "on" if value else "off")
        
        self.console.print(table)
        
    def get_setting_description(self, setting: str) -> str:
        descriptions = {
            "autoprint_table": "Automatically prints the table after a change has been made."
        }
        return descriptions.get(setting, "No description available.")
    
    def get_autoprint_table(self) -> str:
        value = self.settings.get("autoprint_table", False)
        return "on" if value else "off"
    
    def set_autoprint_table(self, value: str):
        value = value.lower().strip()
        if value == "on":
            self.settings["autoprint_table"] = True
            self.message_panel.create_information_message(f"autoprint_table [bold green]on[/]")
        elif value == "off":
            self.settings["autoprint_table"] = False
            self.message_panel.create_information_message(f"autoprint_table [bold red]off[/]")
        else:
            self.message_panel.create_error_message("Enter 'on' or 'off'.")
