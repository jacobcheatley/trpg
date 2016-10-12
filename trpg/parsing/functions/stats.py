from .base_function import Function


# OTHER/NORMAL STATS
# CURRENT VALUE SETTERS
class IncStatFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.other[self.name].current += self.value


class DecStatFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.other[self.name].current -= self.value


class SetStatFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.other[self.name].current = self.value


# GETTERS
class GetStatFunction(Function):
    def __init__(self, args):
        self.name = args[0]

    def _do_function(self, campaign):
        return campaign.player.stats.other[self.name].current


# RESOURCE STATS
# CURRENT VALUE SETTERS
class IncResFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].current += self.value


class DecResFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].current -= self.value


class SetResFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].current = self.value


# MIN VALUE SETTERS
class IncResMinFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].min += self.value


class DecResMinFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].min -= self.value


class SetResMinFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].min = self.value


# MAX VALUE SETTERS
class IncResMaxFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].max += self.value


class DecResMaxFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].max -= self.value


class SetResMaxFunction(Function):
    def __init__(self, args):
        self.name = args[0]
        self.value = args[1]

    def _do_function(self, campaign):
        campaign.player.stats.resource[self.name].max = self.value


# GETTERS
class GetResFunction(Function):
    def __init__(self, args):
        self.name = args[0]

    def _do_function(self, campaign):
        return campaign.player.stats.resource[self.name].current


class GetResMinFunction(Function):
    def __init__(self, args):
        self.name = args[0]

    def _do_function(self, campaign):
        return campaign.player.stats.resource[self.name].min


class GetResMaxFunction(Function):
    def __init__(self, args):
        self.name = args[0]

    def _do_function(self, campaign):
        return campaign.player.stats.resource[self.name].max


# HEALTH STATS
# CURRENT VALUE SETTERS
class IncHealthFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.current += self.value


class DecHealthFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.current -= self.value


class SetHealthFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.current = self.value


# MIN VALUE SETTERS
class IncHealthMinFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.min += self.value


class DecHealthMinFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.min -= self.value


class SetHealthMinFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.min = self.value


# MAX VALUE SETTERS
class IncHealthMaxFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.max += self.value


class DecHealthMaxFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.max -= self.value


class SetHealthMaxFunction(Function):
    def __init__(self, args):
        self.value = args[0]

    def _do_function(self, campaign):
        campaign.player.stats.health.max = self.value


# GETTERS
class GetHealthFunction(Function):
    def __init__(self, args):
        pass

    def _do_function(self, campaign):
        return campaign.player.stats.health.current


class GetHealthMinFunction(Function):
    def __init__(self, args):
        pass

    def _do_function(self, campaign):
        return campaign.player.stats.health.min


class GetHealthMaxFunction(Function):
    def __init__(self, args):
        pass

    def _do_function(self, campaign):
        return campaign.player.stats.health.max
