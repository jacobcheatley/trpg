from .base_function import Function
import math


class RoundFunction(Function):
    def __init__(self, args):
        self.number = args[0]

    def _do_function(self, campaign):
        return int(round(self.number))


class CeilFunction(Function):
    def __init__(self, args):
        self.number = args[0]

    def _do_function(self, campaign):
        return int(math.ceil(self.number))


class FloorFunction(Function):
    def __init__(self, args):
        self.number = args[0]

    def _do_function(self, campaign):
        return int(math.floor(self.number))


class PowFunction(Function):
    def __init__(self, args):
        self.a = args[0]
        self.b = args[1]

    def _do_function(self, campaign):
        return self.a ** self.b


class FactorialFunction(Function):
    def __init__(self, args):
        self.number = args[0]

    def _do_function(self, campaign):
        return math.factorial(self.number)


class AbsFunction(Function):
    def __init__(self, args):
        self.number = args[0]

    def _do_function(self, campaign):
        return abs(self.number)
