from pyparsing import *
from .functions import *


tokens_map = {
    # Misc
    'goto': GotoFunction,
    'show_message': ShowMessageFunction,
    # Stats Setters
    'inc_stat': IncStatFunction,
    'dec_stat': DecStatFunction,
    'set_stat': SetStatFunction,
    'inc_res': IncResFunction,
    'dec_res': DecResFunction,
    'set_res': SetResFunction,
    'inc_res_min': IncResMinFunction,
    'dec_res_min': DecResMinFunction,
    'set_res_min': SetResMinFunction,
    'inc_res_max': IncResMaxFunction,
    'dec_res_max': DecResMaxFunction,
    'set_res_max': SetResMaxFunction,
    'inc_health': IncHealthFunction,
    'dec_health': DecHealthFunction,
    'set_health': SetHealthFunction,
    'inc_health_min': IncHealthMinFunction,
    'dec_health_min': DecHealthMinFunction,
    'set_health_min': SetHealthMinFunction,
    'inc_health_max': IncHealthMaxFunction,
    'dec_health_max': DecHealthMaxFunction,
    'set_health_max': SetHealthMaxFunction,
    # Stats Getters
    'get_stat': GetStatFunction,
    'get_res': GetResFunction,
    'get_res_min': GetResMinFunction,
    'get_res_max': GetResMaxFunction,
    'get_health': GetHealthFunction,
    'get_health_min': GetHealthMinFunction,
    'get_health_max': GetHealthMaxFunction,
    # Inventory Manipulation
    'give_item': GiveItemFunction,
    'take_item': TakeItemFunction,
    'give_currency': GiveCurrencyFunction,
    'take_currency': TakeCurrencyFunction,
    # Inventory Getters
    'get_item_count': GetItemCountFunction,
    'get_currency': GetCurrencyFunction,
}


class FunctionParser:
    def __init__(self):
        self.bnf = self.make_bnf()

    @staticmethod
    def make_function_parse_action():
        def func_parse_action(string, location, tokens):
            name = tokens[0].name
            args = tokens[0].args
            if name in tokens_map:
                cls = tokens_map[name]
                return cls(args)
            else:
                return NotImplementedFunction(args)

        return func_parse_action

    @staticmethod
    def int_parse_action(string, location, tokens):
        return int(tokens[0])

    @staticmethod
    def string_parse_action(string, location, tokens):
        return tokens[0].strip('\'')

    @staticmethod
    def bool_parse_action(string, location, tokens):
        if tokens[0] == 'true':
            return True
        else:
            return False

    @staticmethod
    def real_parse_action(string, location, tokens):
        return float(string)

    def make_bnf(self):
        expr = Forward()

        # Building blocks
        LPAR, RPAR, SEMI = map(Suppress, '();')
        identifier = Word(alphas, alphas + "_")
        integer = Regex(r"-?\d+")
        real = Regex(r"-?\d+\.\d*")
        true = Literal('true')
        false = Literal('false')
        bool = true | false
        string = sglQuotedString

        # More complex
        args = Group(Optional(delimitedList(expr))).setResultsName('args')
        function_call = Group(identifier.setResultsName('name') + LPAR + args + RPAR)
        operand = string | integer | real | bool | function_call
        expr << operand  # Will soon have mathematical stuff

        # Parse Actions
        integer.setParseAction(self.int_parse_action)
        real.setParseAction(self.real_parse_action)
        bool.setParseAction(self.bool_parse_action)
        string.setParseAction(self.string_parse_action)

        function_call.setParseAction(self.make_function_parse_action())

        return (
            function_call
        ).setResultsName('function')

    def parse_function(self, func_string):
        try:
            return self.bnf.parseString(func_string)
        except ParseException:
            print('**Error parsing function {}.**'.format(func_string))
