from .abstract_state import AbstractState
from utils.utils import apply_regex


class DurationState(AbstractState):

    def validate(self, input):

        regex = r"[0-9]+"

        duration = apply_regex(regex, input)
        if duration:
            self._context.set_temp_task_duration(int(duration.group()))
        return duration

    def set_next_state(self):

        from .closing_parentheses_state import ClosingParenthesesState

        self._context.change_state(ClosingParenthesesState(self._context))
