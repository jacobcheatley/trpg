class Function:
    """Base class for DSL functions."""
    def _do_function(self, campaign):
        pass

    def __call__(self, campaign):
        self._do_function(campaign)
