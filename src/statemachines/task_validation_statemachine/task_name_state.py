from .abstract_state import AbstractState
from utils.utils import apply_regex


class TaskNameState(AbstractState):

    def validate(self, input):

        from .generic_state import GenericState
        from .duration_state import DurationState

        regex = r"[a-zA-Z0-9]+"

        task_name = apply_regex(regex, input)
        if task_name:
            self._context.set_statement_valid(False)

            # create task, return false if task description is duplicated
            if not self._context.init_temp_task(task_name.group()):
                task_name = None

        opening_parentheses_regex = r"[\(]"
        duration_state = DurationState(self._context)
        self._next_state = GenericState(
            self._context, opening_parentheses_regex, duration_state
        )

        return task_name

    def set_next_state(self):
        self._context.change_state(self._next_state)
