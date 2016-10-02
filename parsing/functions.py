class Function:
    """Base class for DSL functions."""
    def __init__(self, verb):
        self.verb = verb

    def _do_function(self, campaign):
        pass

    def __call__(self, campaign):
        self._do_function(campaign)


class GotoFunction(Function):
    """Function class to go to a new scenario."""
    def __init__(self, args):
        super().__init__('goto')
        self.scenario = args[0]

    def _do_function(self, campaign):
        campaign.goto(self.scenario)
