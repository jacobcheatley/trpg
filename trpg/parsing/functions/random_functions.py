from .base_function import Function
import random


class RandIntFunction(Function):
    def __init__(self, args):
        self.min = args[0]
        self.max = args[1]

    def _do_function(self, campaign):
        return random.randint(self.min, self.max)


class RandChoiceFunction(Function):
    def __init__(self, args):
        self.choices = args

    def _do_function(self, campaign):
        return random.choice(self.choices)


class RandChanceFunction(Function):
    def __init__(self, args):
        self.chance = args[0]

    def _do_function(self, campaign):
        return self.chance > random.random()
