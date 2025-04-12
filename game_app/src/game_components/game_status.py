class GameStatus:

    def __init__(self):
        self._current_state = "main"
        self._current_location = None

    def get_current_state(self):
        return self._current_state

    def get_current_location(self):
        return self._current_location

    def set_current_state(self, state):
        self._current_state = state

    def set_current_location(self, location):
        self._current_location = location
