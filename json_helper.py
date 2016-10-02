from data_classes import *


def hook(obj):
    # TODO: Hook all types
    if '__type__' in obj:
        obj_type = obj.pop('__type__')
        if obj_type == 'scenario':
            return Scenario(**obj)
        elif obj_type == 'player':
            return Player(**obj)
        elif obj_type == 'item':
            return Item(**obj)
        elif obj_type == 'inventory':
            return Inventory(**obj)
        elif obj_type == 'option':
            return Option(**obj)
        elif obj_type == 'player_stats':
            return PlayerStats(**obj)
        elif obj_type == 'resource_stat':
            return ResourceStat(**obj)
        elif obj_type == 'other_stat':
            return OtherStat(**obj)
    return obj
