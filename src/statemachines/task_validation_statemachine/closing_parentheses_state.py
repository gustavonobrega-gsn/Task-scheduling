from .abstract_state import AbstractState
from utils.utils import apply_regex
from utils.utils import get_next_substring_index


class ClosingParenthesesState(AbstractState):

    def validate(self, input):

        from .task_name_state import TaskNameState
        from .generic_state import GenericState
        from .dependency_state import DependencyState

        regex = r"[\)]"

        self._next_state = TaskNameState(self._context)

        opening_parentheses = apply_regex(regex, input)
        if opening_parentheses:

            # this state can represent the end of the current statement or
            # the continuation of it the definition will be set looking
            # what is nearest
            # having '(' near means that next will come a new statement
            # having '[' near means that next will come the dependencies
            next_open_parenthes_index = get_next_substring_index(input, "(")
            next_open_squar_brac_index = get_next_substring_index(input, "[")

            if next_open_squar_brac_index < next_open_parenthes_index:
                after_keyword_regex = r"\bafter\b"
                opening_square_bracket_regex = r"[\[]"

                open_square_brac_state = GenericState(
                    self._context,
                    opening_square_bracket_regex,
                    DependencyState(self._context),
                )
                self._next_state = GenericState(
                    self._context, after_keyword_regex, open_square_brac_state
                )

            else:
                self._context.set_statement_valid(True)

        return opening_parentheses

    def set_next_state(self):
        self._context.change_state(self._next_state)
