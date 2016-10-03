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
    # Math
    'round': RoundFunction,
    'ceil': CeilFunction,
    'floor': FloorFunction,
    'pow': PowFunction,
    'factorial': FactorialFunction,
    'abs': AbsFunction
}


class OperParseActionHolder:
    def __init__(self):
        # initialize with a do-nothing parse action
        self.fn = lambda s, l, t: None

    def __call__(self, s, l, t):
        return self.fn(s, l, t)


class FunctionParser:
    def __init__(self, campaign):
        self.bnf = self.make_bnf()
        self.campaign = campaign

    def make_function_parse_action(self):
        def func_parse_action(string, location, tokens):
            name = tokens[0].name
            args_temp = tokens[0].args
            args = []
            if name != 'if':
                for arg_temp in args_temp:
                    try:
                        args.append(arg_temp(self.campaign))
                    except:
                        args.append(arg_temp)
            else:
                args = args_temp
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

    @staticmethod
    def add_parse_action(string, location, tokens):
        result = tokens[0][0]
        for operator, operand in zip(tokens[0][1::2], tokens[0][2::2]):
            if operator == '+':
                result += operand
            elif operator == '-':
                result -= operand
        return result

    @staticmethod
    def mult_parse_action(string, location, tokens):
        result = tokens[0][0]
        for operator, operand in zip(tokens[0][1::2], tokens[0][2::2]):
            if operator == '*':
                result *= operand
            elif operator == '/':
                result /= operand
            elif operand == '%':
                result %= operand
        return result

    @staticmethod
    def code_parse_action(string, location, tokens):
        def combined_function(campaign):
            for func in tokens:
                func(campaign)

        return combined_function

    def make_bnf(self):
        expr = Forward()

        # Building blocks
        LPAR, RPAR, SEMI = map(Suppress, '();')
        PLUS, MINUS, MULT, DIV = map(Literal, '+-*/')

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
        code_statement = delimitedList(function_call, SEMI)

        operand = string | integer | real | bool | function_call

        # Mathematics Basics
        addop = PLUS | MINUS
        multop = MULT | DIV

        expr << infixNotation(operand,
                              [
                                  (multop, 2, opAssoc.LEFT, self.mult_parse_action),
                                  (addop, 2, opAssoc.RIGHT, self.add_parse_action)
                              ])

        # Parse Actions
        integer.setParseAction(self.int_parse_action)
        real.setParseAction(self.real_parse_action)
        bool.setParseAction(self.bool_parse_action)
        string.setParseAction(self.string_parse_action)

        function_call.setParseAction(self.make_function_parse_action())
        function_call.setResultsName('function')
        code_statement.setParseAction(self.code_parse_action)

        return (
            code_statement
        ).setResultsName('run')

    def parse_function(self, func_string):
        try:
            return self.bnf.parseString(func_string)
        except ParseException:
            print('**Error parsing function {}.**'.format(func_string))
