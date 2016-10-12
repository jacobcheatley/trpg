from .base_function import Function


# INVENTORY MANIPULATION
class GiveItemFunction(Function):
    def __init__(self, args):
        self.item_id = args[0]
        self.count = args[1]

    def _do_function(self, campaign):
        campaign.player.inventory.add(self.item_id, self.count)


class TakeItemFunction(Function):
    def __init__(self, args):
        self.item_id = args[0]
        self.count = args[1]

    def _do_function(self, campaign):
        campaign.player.inventory.remove(self.item_id, self.count)


class GiveCurrencyFunction(Function):
    def __init__(self, args):
        self.count = args[0]

    def _do_function(self, campaign):
        campaign.player.inventory.currency += self.count


class TakeCurrencyFunction(Function):
    def __init__(self, args):
        self.count = args[0]

    def _do_function(self, campaign):
        campaign.player.inventory.currency -= self.count
        # TODO: Refine logic


# GETTERS
class GetItemCountFunction(Function):
    def __init__(self, args):
        self.item_id = args[0]

    def _do_function(self, campaign):
        inventory_items = campaign.player.inventory.items
        if self.item_id in inventory_items:
            return inventory_items[self.item_id]
        return 0


class GetCurrencyFunction(Function):
    def __init__(self, args):
        pass

    def _do_function(self, campaign):
        return campaign.player.inventory.currency
