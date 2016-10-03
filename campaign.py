import json
from json_helper import hook
from parsing.command_parser import CommandParser
from parsing.function_parser import FunctionParser


# Random Functions
def default_debug(message):
    print('!!!' + message + '!!!')


class Campaign:
    def __init__(self, json_fp, read=input, write=print, debug=default_debug):
        """Represents all the data in an entire running campaign"""

        # Get a temporary dictionary of the deserialized campaign data
        dictionary_rep = json.load(open(json_fp, 'r'), object_hook=hook)
        self.funcs = dictionary_rep['funcs']
        self.stats = dictionary_rep['stats']
        self.items = dictionary_rep['items']
        self.scenarios = dictionary_rep['scenarios']

        # These objects are the only ones a campaign should modify and save
        self.player = dictionary_rep['player']
        self.globals = dictionary_rep['globals']
        # TODO: shops, globals, encounters

        # Endpoint specific
        self.read = read
        self.write = write
        self.debug = debug

        # Parsers for commands and functions
        self.command_parser = CommandParser()
        self.function_parser = FunctionParser(self)

    def __getitem__(self, item):
        return self.__dict__[item]

    def run(self):
        """Starts the campaign running. Begins an input -> process -> reply loop."""

        self.debug('STARTING CAMPAIGN')
        self.view_current_scenario()
        while True:
            command_string = self.read('>> ')
            cmd = self.command_parser.parse_command(command_string)
            if cmd is not None:
                cmd.command(self)

    # HELPER FUNCTIONS
    def view_current_scenario(self):
        """Prints all information about the current scenario."""
        options_text = ['{0}: {1}'.format(number + 1, option) for number, option in enumerate(self.available_options())]
        result = '**{0.name}**\n*{0.desc}*\n-\n{1}'.format(self.current_scenario(), '\n'.join(options_text))
        self.write(result)

    # HELPER GETTERS
    def item_name(self, item_id):
        return self.items[item_id].name

    def current_scenario(self):
        return self.scenarios[self.player.scenario]

    def available_options(self):
        return [option for option in self.current_scenario().options]

    def health_setting(self):
        return self.stats.health

    def resource_setting(self, name):
        return self.stats.resource[name]

    def other_setting(self, name):
        return self.stats.other[name]

    # COMMAND INPUT FUNCTIONS
    def dummy_function(self):
        """A useless function."""
        self.debug('NOT IMPLEMENTED')
        pass

    def choose_option(self, option_number):
        try:
            self.run_function(self.available_options()[option_number-1].func)
        except IndexError as e:
            self.debug(str(e))
            self.write('Not a valid option number.')

    def view_inventory(self, owner):
        """Displays the player or shop inventory."""
        inventory = owner.inventory
        sorted_ids = sorted(inventory.items, key=lambda item: self.item_name(item))
        data = [(inventory.items[item_id], self.item_name(item_id), item_id) for item_id in sorted_ids]
        items_text = ['- {0[0]} {0[1]} [\'{0[2]}\']'.format(item_info) for item_info in data]
        self.write('**Currency:** {0.currency}\n**Items:**\n{1}'.format(inventory, '\n'.join(items_text)))

    def view_stats(self):
        """Displays the player's stats."""
        stats = self.player.stats
        health_string = '**{}:**: {}/{}'.format(self.health_setting().name, stats.health.current, stats.health.max)

        resources_data = ((self.resource_setting(stat_id).name, stat.current, stat.max) for stat_id, stat in sorted(stats.resource.items()))
        resources_string = '\n'.join(('**{}:**: {}/{}'.format(name, current, max) for name, current, max in resources_data))

        other_data = ((self.other_setting(stat_id).name, stat.current) for stat_id, stat in sorted(stats.other.items()))
        other_string = '\n'.join(('**{}:**: {}'.format(name, current) for name, current in other_data))

        self.write('{}\n-\n{}\n-\n{}'.format(health_string, resources_string, other_string))

    # LANGUAGE FUNCTIONS
    def run_function(self, func_string):
        func = self.function_parser.parse_function(func_string)
        if func is not None:
            func.run(self)
        else:
            self.debug('????')
