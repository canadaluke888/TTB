from difflib import get_close_matches
import json
from message_panel.message_panel import MessagePanel
from functools import cache

class Autocomplete:
    
    def __init__(self, console):
        
        self.console = console
        
        self.cutoff = 0.6
        
        self.message_panel = MessagePanel(self.console)
        
        self.command_list_file = "settings/command_list.json"
        
        self.all_commands = self.load_command_list()
        
        self.main_menu_commands = self.get_main_menu_commands()
        
        self.settings_commands = self.get_settings_commands()
        
        self.table_builder_commands = self.get_table_builder_commands()
        
    @cache
    def load_command_list(self):
        with open(self.command_list_file, 'r') as f:
            return json.load(f)
        
    @cache
    def get_main_menu_commands(self):
        return self.all_commands.get("main_menu")
    
    @cache
    def get_settings_commands(self):
        return self.all_commands.get("settings")
    
    @cache
    def get_table_builder_commands(self):
        return self.all_commands.get("table_builder")
    
    def suggest_command(self, user_input, commands):
        """
        Suggest the closest commands to the user's input.

        :param user_input: The command input by the user.
        """
        matches = get_close_matches(user_input, commands, n=1, cutoff=self.cutoff)
        if matches:
            formatted_matches = ", ".join([f"'{match}'" for match in matches])
            self.message_panel.create_information_message(
                f"Did you mean: {formatted_matches}?"
            )
        else:
            return