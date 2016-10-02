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
    """Command class for showing inventory."""
    def __init__(self, quals):
        super().__init__('INV')

    def _do_command(self, campaign):
        campaign.view_inventory(campaign.player)

    @staticmethod
    def help_description():
        return 'INV: Check your inventory.'


class ChoiceCommand(Command):
    """Command class for choosing an option in a scenario."""
    def __init__(self, quals):
        super().__init__('DO')
        try:
            self.option_number = int(quals['choice'])
        except ValueError:
            self.option_number = -1

    def _do_command(self, campaign):
        campaign.choose_option(self.option_number)

    @staticmethod
    def help_description():
        return 'nothing/DO <N>: Do option number N.'


class LookCommand(Command):
    """Command class for showing scenario information again."""
    def __init__(self, quals):
        super().__init__('LOOK')

    def _do_command(self, campaign):
        campaign.view_current_scenario()

    @staticmethod
    def help_description():
        return 'LOOK: View current scenario info again.'


class HelpCommand(Command):
    """Command class for getting help on the other commands."""
    def __init__(self, quals):
        super().__init__('HELP')

    def _do_command(self, campaign):
        command_helps = [command.help_description() for command in [
            ChoiceCommand,
            InventoryCommand,
            LookCommand
        ]]
        campaign.write('\n'.join(command_helps))
