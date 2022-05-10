from .abstract_state import AbstractState
from utils.utils import apply_regex


class GenericState(AbstractState):

    def __init__(self, context, regex, next_state):
        self._context = context
        self._regex = regex
        self._next_state = next_state

    def validate(self, input):
        filtered_string = apply_regex(self._regex, input)
        return filtered_string

    def set_next_state(self):
        self._context.change_state(self._next_state)
