from .task_name_state import TaskNameState
from utils.utils import apply_regex


class Context:

    def __init__(self):

        self._state = TaskNameState(self)

        self._is_statement_valid = False

        self._line = 1
        self._column = 1

        # used to store dependencies colunms and lines
        # after file is read, if a dependency was not presented as task,
        # will display dependency column and line
        # if unknow dependency exits in more than one place, stores only
        # the first place top to bottom, left to right
        self._dependencies_position = {}

    def init_temp_task(self, task_name):
        self._temp_task_name = task_name

        return self._task_manager.create_task(self._temp_task_name)

    def set_temp_task_duration(self, duration):
        self._task_manager.set_task_duration(self._temp_task_name, duration)

    def add_temp_task_dependency(self, dep_name):
        self._task_manager.add_task_dependency(self._temp_task_name, dep_name)

        # track dependencies position
        # used if dependency was not declared as Task
        if dep_name not in self._dependencies_position:
            self._dependencies_position[dep_name] = (self._line, self._column)

    def change_state(self, state):
        self._state = state

    def set_statement_valid(self, is_statement_valid):
        self._is_statement_valid = is_statement_valid

    def get_error_column(self):
        return self._column

    def get_error_line(self):
        return self._line

    def validate(self, input, task_manager):

        self._task_manager = task_manager

        regex_space_or_tab = r"[ \t]+"
        regex_linebreak = r"(\r\n?|\n)"

        while input:
            # remove blank spaces and tabs before next state
            filtered_string = apply_regex(regex_space_or_tab, input)
            if not filtered_string:
                # remove break lines before next state
                filtered_string = apply_regex(regex_linebreak, input)
                if filtered_string:
                    # if breakline, return column index to begin
                    self._column = 0
                    self._line += filtered_string.span()[1]
                else:
                    # validate and process state
                    filtered_string = self._state.validate(input)

                    # go to next state
                    self._state.set_next_state()

            # advance the input as many indexes as filtered string size got
            # from the regex
            if filtered_string:
                self._column += filtered_string.span()[1]
                input = input[filtered_string.span()[1]:]

            # unexpected input syntax
            else:
                return False

        if self._is_statement_valid:
            # check if all dependencies were described and sets the way around
            # dependency, also know as required_for_task
            unknow_dependency_name = self._task_manager.validate_dependencies()

            if unknow_dependency_name:
                # if dependency not stated as task, set line and column as
                # found first in the input
                self._line, self._column = self._dependencies_position[
                    unknow_dependency_name
                ]
                self._is_statement_valid = False

        return self._is_statement_valid
