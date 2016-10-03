from typing import Mapping, Sequence, Union, Any, Dict

Func = Union[str, bool]  # typing of func will change to Union[Callable, bool]


class Option:
    def __init__(self, desc: str = '', func: Func = ''):
        self.desc = desc
        self.func = func

    def __repr__(self):
        return self.desc


class Scenario:
    def __init__(self, name: str = '', desc: str = '', options: Sequence[Option] = None):
        self.name = name
        self.desc = desc
        self.options = options


class Item:
    def __init__(self, name: str = '', desc: str = '', value: int = 0, use: Func = False, equip: Func = False):
        self.name = name
        self.desc = desc
        self.value = value
        self.use = use
        self.equip = equip

    def __repr__(self):
        return self.name


class Inventory:
    def __init__(self, currency: int = 0, items: Dict[str, int] = None):
        self.currency = currency
        self.items = items

    def add(self, item_id, count):
        if item_id in self.items:
            self.items[item_id] += count
        else:
            self.items[item_id] = count

    def remove(self, item_id, count):
        if item_id in self.items:
            self.items[item_id] -= count
            if self.items[item_id] <= 0:
                self.items.pop(item_id, None)
        else:
            # TODO: Refine logic
            pass


class StatSetting:
    def __init__(self, name: str = '', desc: str = ''):
        self.name = name
        self.desc = desc


class StatSettings:
    def __init__(self, health_stat: StatSetting = None, resource_stats: Sequence[StatSetting] = None,
                 normal_stats: Sequence[StatSetting] = None):
        self.health_stat = health_stat
        self.resource_stats = resource_stats
        self.normal_stats = normal_stats


class ResourceStat:
    def __init__(self, min: int = 0, max: int = 0, current: int = 0):
        self.min = min
        self.max = max
        self.current = current


class OtherStat:
    def __init__(self, current: int = 0):
        self.current = current


class PlayerStats:
    def __init__(self, health: ResourceStat = None, resource: Dict[str, ResourceStat] = None,
                 other: Mapping[str, OtherStat] = None):
        self.health = health
        self.resource = resource
        self.other = other


class Player:
    def __init__(self, scenario: str = '', stats: PlayerStats = None, inventory: Inventory = None):
        self.scenario = scenario
        self.stats = stats
        self.inventory = inventory
