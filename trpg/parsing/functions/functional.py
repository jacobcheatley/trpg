from .base_function import Function
import re


def transform_args(args):
    return ["'{}'".format(arg) if isinstance(arg, str) else str(arg) for arg in args]


# CUSTOM
class CustomFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.args = transform_args(args[1:])

    def repl(self, m):
        return self.args[int(m.group(1))]

    def _do_function(self, campaign):
        if self.name in campaign.funcs:
            custom_func_string = campaign.funcs[self.name]
            new_func_string = re.sub(r'\[(\d+)\]', self.repl, custom_func_string)
            campaign.run_function(new_func_string)
        else:
            campaign.debug('FUNCTION NOT IMPLEMENTED')


class RepeatFunction(Function):
    def __init__(self, args):
        self.times = args[0]
        function_name = args[1]
        function_args = transform_args(args[2:])
        self.func_string = '{}({})'.format(function_name, ','.join(function_args))

    def _do_function(self, campaign):
        campaign.run_function(';'.join(self.func_string for _ in range(self.times)))
