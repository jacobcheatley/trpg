from pyparsing import *
from .functions import *


tokens_map = {
    'goto': GotoFunction
}


class FunctionParser:
    def __init__(self):
        self.bnf = self.make_bnf()

    @staticmethod
    def make_function_parse_action():
        def func_parse_action(string, location, tokens):
            cls = tokens_map[tokens[0].name]
            args = tokens[0].args
            # print(string)
            # print(args)
            return cls(args)

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
