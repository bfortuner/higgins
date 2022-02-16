from higgins.actions import Action


class CountRows(Action):
    """Action counts the number of rows in the data object from the previous Action."""

    def run(self):
        raise NotImplementedError
