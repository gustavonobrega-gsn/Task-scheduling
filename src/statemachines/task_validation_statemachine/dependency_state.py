from .abstract_state import AbstractState
from utils.utils import apply_regex
from utils.utils import get_next_substring_index


class DependencyState(AbstractState):

    def validate(self, input):

        from .closing_square_bracket_state import ClosingSquareBracketState
        from .generic_state import GenericState

        regex = r"[a-zA-Z0-9]+"

        self._next_state = ClosingSquareBracketState(self._context)

        dependency = apply_regex(regex, input)
        if dependency:
            self._context.add_temp_task_dependency(dependency.group())

            # this state can represent the end of the collection of
            # dependencies or the continuation of it
            # the definition will be set looking what is nearest
            # having ',' near means that next will come more dependencies
            # having ']' near means that this element is the last dependency

            next_comma_index = get_next_substring_index(input, ",")
            next_close_squar_brack_index = get_next_substring_index(input, "]")

            if next_comma_index < next_close_squar_brack_index:
                regex_get_comma = r"[\,]"

                dependency_state = DependencyState(self._context)
                self._next_state = GenericState(
                    self._context, regex_get_comma, dependency_state
                )

        return dependency

    def set_next_state(self):
        self._context.change_state(self._next_state)
