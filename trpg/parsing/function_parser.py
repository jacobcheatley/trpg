from pyparsing import *
from .functions import *

tokens_map = {
    # Misc
    'goto': GotoFunction,
    'show_message': ShowMessageFunction,
    'print': ShowMessageFunction,
    # Functional
    'custom': CustomFunction,
    'repeat': RepeatFunction,
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
    'abs': AbsFunction,
    'max': MaxFunction,
    'min': MinFunction,
    # Random
    'rand_int': RandIntFunction,
    'rand_choice': RandChoiceFunction,
    'rand_chance': RandChanceFunction,
    # Global
    'set_global': SetGlobalFunction,
    'get_global': GetGlobalFunction
}


class FunctionParser:
    def __init__(self, campaign):
        self.bnf = self.make_bnf()
        self.campaign = campaign

    def early_eval(self, arg):
        try:
            return arg(self.campaign)
        except:
            return arg

    def make_function_parse_action(self):
        def func_parse_action(string, location, tokens):
            name = tokens[0].name
            args_temp = tokens[0].args
            args = []
            for arg_temp in args_temp:
                args.append(self.early_eval(arg_temp))
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
        return float(tokens[0])

    def not_parse_action(self, string, location, tokens):
        return not self.early_eval(tokens[0][1])

    def compare_parse_action(self, string, location, tokens):
        tokens = tokens[0]
        if tokens[1] == '<':
            return self.early_eval(tokens[0]) < self.early_eval(tokens[2])
        elif tokens[1] == '>':
            return self.early_eval(tokens[0]) > self.early_eval(tokens[2])
        elif tokens[1] == '<=':
            return self.early_eval(tokens[0]) <= self.early_eval(tokens[2])
        elif tokens[1] == '>=':
            return self.early_eval(tokens[0]) >= self.early_eval(tokens[2])
        return False  # This shouldn't happen

    @staticmethod
    def eq_parse_action(self, string, location, tokens):
        tokens = tokens[0]
        if tokens[1] == '==':
            return self.early_eval(tokens[0]) == self.early_eval(tokens[2])
        elif tokens[1] == '!=':
            return self.early_eval(tokens[0]) != self.early_eval(tokens[2])
        return False  # This shouldn't happen

    def and_parse_action(self, string, location, tokens):
        tokens = tokens[0]
        return self.early_eval(tokens[0]) and self.early_eval(tokens[2])

    def or_parse_action(self, string, location, tokens):
        tokens = tokens[0]
        return self.early_eval(tokens[0]) or self.early_eval(tokens[2])

    def add_parse_action(self, string, location, tokens):
        result = self.early_eval(tokens[0][0])
        for operator, operand in zip(tokens[0][1::2], tokens[0][2::2]):
            if operator == '+':
                result += self.early_eval(operand)
            elif operator == '-':
                result -= self.early_eval(operand)
        return result

    def mult_parse_action(self, string, location, tokens):
        result = self.early_eval(tokens[0][0])
        for operator, operand in zip(tokens[0][1::2], tokens[0][2::2]):
            if operator == '*':
                result *= self.early_eval(operand)
            elif operator == '/':
                result /= self.early_eval(operand)
            elif operand == '%':
                result %= self.early_eval(operand)
        return result

    @staticmethod
    def code_parse_action(string, location, tokens):
        def combined_function(campaign):
            for func in tokens:
                func(campaign)

        return combined_function

    def if_parse_action(self, string, location, tokens):
        def do_if(campaign):
            if_result = self.early_eval(tokens[1])
            if if_result:
                tokens[2](campaign)
                return
            else:
                for elif_condition, elif_code in zip(tokens[4::3], tokens[5::3]):
                    elif_result = self.early_eval(elif_condition)
                    if elif_result:
                        elif_code(campaign)
                        return
                if tokens[-2] == 'else':
                    tokens[-1](campaign)
                    return

        return do_if

    @staticmethod
    def logical_parse_action(string, location, tokens):
        if tokens[0] == 'if':
            return FunctionParser.if_parse_action(string, location, tokens)
        else:
            return FunctionParser.code_parse_action(string, location, tokens)

    @staticmethod
    def program_parse_action(string, location, tokens):
        def program_result(campaign):
            for statement in tokens:
                statement(campaign)

        return program_result

    def make_bnf(self):
        expr = Forward()

        # Building blocks
        PLUS, MINUS, MULT, DIV = map(Literal, '+-*/')
        LPAR, RPAR, SEMI, LBRAC, RBRAC = map(Suppress, '();{}')
        NOT = Literal('!')
        LT, GT, LTE, GTE = map(Literal, '< > <= >='.split())
        EQ, NEQ = map(Literal, '== !='.split())
        AND, OR = map(Literal, '&& ||'.split())
        IF, ELIF, ELSE = map(Keyword, 'if elif else'.split())

        # func_name = Word(alphas, alphas + "_")
        func_name = Regex(r'(?!if)[a-z][a-z_]*')
        integer = Regex(r'-?\d+')
        real = Regex(r'-?\d+\.\d*')
        true = Literal('true')
        false = Literal('false')
        bool = true | false
        string = sglQuotedString

        # More complex
        args = Group(Optional(delimitedList(expr))).setResultsName('args')
        function_call = Group(func_name.setResultsName('name') + LPAR + args + RPAR)

        operand = string | real | integer | bool | function_call

        # Logic
        if_block = Forward()
        code_block = delimitedList(function_call | if_block, SEMI)
        logical_block = code_block
        if_block << IF + LPAR + expr + RPAR + \
                    LBRAC + \
                    logical_block + \
                    RBRAC + \
                    ZeroOrMore(ELIF + LPAR + expr + RPAR +
                               LBRAC +
                               logical_block +
                               RBRAC) + \
                    Optional(ELSE + LBRAC +
                             logical_block +
                             RBRAC)

        # Mathematics Operators
        addop = PLUS | MINUS
        multop = MULT | DIV

        # Boolean Operators
        notop = NOT
        compareop = LTE | GTE | LT | GT
        eqop = EQ | NEQ
        andop = AND
        orop = OR

        expr << infixNotation(operand,
                              [
                                  (notop, 1, opAssoc.RIGHT, self.not_parse_action),
                                  (multop, 2, opAssoc.LEFT, self.mult_parse_action),
                                  (addop, 2, opAssoc.LEFT, self.add_parse_action),
                                  (compareop, 2, opAssoc.LEFT, self.compare_parse_action),
                                  (eqop, 2, opAssoc.LEFT, self.eq_parse_action),
                                  (andop, 2, opAssoc.LEFT, self.and_parse_action),
                                  (orop, 2, opAssoc.LEFT, self.or_parse_action)
                              ])

        # Final Thing
        program = delimitedList(logical_block, SEMI)

        # Parse Actions
        integer.setParseAction(self.int_parse_action)
        real.setParseAction(self.real_parse_action)
        bool.setParseAction(self.bool_parse_action)
        string.setParseAction(self.string_parse_action)

        function_call.setParseAction(self.make_function_parse_action())
        code_block.setParseAction(self.code_parse_action)
        if_block.setParseAction(self.if_parse_action)
        program.setParseAction(self.program_parse_action)

        return program.setResultsName('run')

    def parse_function(self, func_string):
        try:
            return self.bnf.parseString(func_string)
        except ParseException:
            print('**Error parsing function {}.**'.format(func_string))
