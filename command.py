class Command:
    """Base class for player input commands."""
    def __init__(self, verb):
        self.verb = verb

    def _do_command(self, campaign):
        pass

    @staticmethod
    def help_description():
        return ""

    def __call__(self, campaign):
        self._do_command(campaign)


class InventoryCommand(Command):
    def __init__(self, quals):
        super().__init__('INV')

    def _do_command(self, campaign):
        campaign.view_inventory(campaign.player)

    @staticmethod
    def help_description():
        return 'INV: Check your inventory.'


class ChoiceCommand(Command):
    def __init__(self, quals):
        super().__init__('DO')

    def _do_command(self, campaign):
        campaign.dummy_function()

    @staticmethod
    def help_description():
        return 'nothing/DO <N>: Do option number N.'


class LookCommand(Command):
    def __init__(self, quals):
        super().__init__('LOOK')

    def _do_command(self, campaign):
        campaign.view_current_scenario()

    @staticmethod
    def help_description():
        return 'LOOK: View current scenario info again.'


class HelpCommand(Command):
    def __init__(self, quals):
        super().__init__('HELP')

    def _do_command(self, campaign):
        command_helps = [command.help_description() for command in [
            ChoiceCommand,
            InventoryCommand,
            LookCommand
        ]]
        campaign.write('\n'.join(command_helps))
