from .base_function import Function


# NOT IMPLEMENTED
class NotImplementedFunction(Function):
    def __init__(self, args):
        pass

    def _do_function(self, campaign):
        campaign.debug('FUNCTION NOT IMPLEMENTED')


# SCENARIO FUNCTIONS
class GotoFunction(Function):
    def __init__(self, args):
        self.scenario_name = args[0]

    def _do_function(self, campaign):
        campaign.player.scenario = self.scenario_name
        campaign.view_current_scenario()


# DISPLAY FUNCTIONS
class ShowMessageFunction(Function):
    def __init__(self, args):
        self.message = args[0]

    def _do_function(self, campaign):
        campaign.write(self.message)


# GLOBALS
class SetGlobalFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.globals[self.name] = self.value


class GetGlobalFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        return campaign.globals[self.name]
