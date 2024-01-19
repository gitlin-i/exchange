


class EmptyListError(Exception):
    def __init__(self, message="list is empty!!"):
        self.message = message
        super().__init__(self.message)
