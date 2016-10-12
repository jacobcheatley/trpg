from pyparsing import *
from .commands import *


class CommandParser:
    def __init__(self):
        self.bnf = self.make_bnf()

    @staticmethod
    def make_command_parse_action(cls):
        def cmd_parse_action(s, l, tokens):
            return cls(tokens)

        return cmd_parse_action

    def make_bnf(self):
        inv_verb = oneOf("INV INVENTORY I", caseless=True)
        stat_verb = oneOf("STAT STATS STATISTICS S", caseless=True)
        choice_verb = oneOf('DO', caseless=True) | empty
        look_verb = oneOf('LOOK', caseless=True)
        help_verb = oneOf("HELP H ?", caseless=True)

        inv_command = inv_verb
        stat_command = stat_verb
        choice_command = choice_verb + Word(nums).setResultsName('choice')
        look_command = look_verb
        help_command = help_verb

        inv_command.setParseAction(self.make_command_parse_action(InventoryCommand))
        stat_command.setParseAction(self.make_command_parse_action(StatCommand))
        choice_command.setParseAction(self.make_command_parse_action(ChoiceCommand))
        look_command.setParseAction(self.make_command_parse_action(LookCommand))
        help_command.setParseAction(self.make_command_parse_action(HelpCommand))

        return (
            inv_command |
            stat_command |
            choice_command |
            look_command |
            help_command
        ).setResultsName("command") + LineEnd()

    def parse_command(self, command_string):
        try:
            return self.bnf.parseString(command_string)
        except ParseException:
            print('**Error parsing command input.**')
