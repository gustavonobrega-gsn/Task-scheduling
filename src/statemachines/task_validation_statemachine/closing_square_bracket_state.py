from .abstract_state import AbstractState
from utils.utils import apply_regex


class ClosingSquareBracketState(AbstractState):

    def validate(self, input):

        regex = r"[\]]"

        closing_square_bracket = apply_regex(regex, input)
        if closing_square_bracket:
            self._context.set_statement_valid(True)

        return closing_square_bracket

    def set_next_state(self):

        from .task_name_state import TaskNameState

        self._context.change_state(TaskNameState(self._context))
