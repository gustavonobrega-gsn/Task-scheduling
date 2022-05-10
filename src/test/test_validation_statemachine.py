import unittest
from unittest.mock import call
import mock
from statemachines.task_validation_statemachine.context import Context
from managers.task_manager import TaskManager


class TestValidationStateMachine(unittest.TestCase):
    def make_assertions(
        self,
        input,
        exp_tasks_names,
        exp_tasks_durations,
        exp_tasks_dependencies,
    ):

        mock_task_manager = mock.create_autospec(TaskManager)

        mock_task_manager.validate_dependencies.return_value = None

        context = Context()
        self.assertTrue(context.validate(input, mock_task_manager))

        index_mock_calls = 0
        index_task = 0
        index_task_dep = 0

        state = "name"
        # last call reserved for validation
        while index_mock_calls < len(mock_task_manager.method_calls) - 1:

            if state == "name":
                self.assertEqual(
                    mock_task_manager.method_calls[index_mock_calls],
                    call.create_task(exp_tasks_names[index_task]),
                )
                state = "duration"

            elif state == "duration":
                self.assertEqual(
                    mock_task_manager.method_calls[index_mock_calls],
                    call.set_task_duration(
                        exp_tasks_names[index_task],
                        exp_tasks_durations[index_task],
                    ),
                )

                if not exp_tasks_dependencies[index_task]:
                    state = "name"
                    index_task += 1
                else:
                    state = "dependencies"
                    index_task_dep = 0

            elif state == "dependencies":
                self.assertEqual(
                    mock_task_manager.method_calls[index_mock_calls],
                    call.add_task_dependency(
                        exp_tasks_names[index_task],
                        exp_tasks_dependencies[index_task][index_task_dep],
                    ),
                )
                index_task_dep += 1

                if index_task_dep >= len(
                    exp_tasks_dependencies[index_task]
                ):
                    state = "name"
                    index_task += 1

            index_mock_calls += 1

        self.assertEqual(
            mock_task_manager.method_calls[index_mock_calls],
            call.validate_dependencies(),
        )

    def make_assertion_fail(self, input, exp_error_line, exp_error_column):

        mock_task_manager = mock.create_autospec(TaskManager)

        context = Context()
        self.assertFalse(
            context.validate(input, mock_task_manager)
        )

        self.assertEqual(
            exp_error_line, context.get_error_line()
        )
        self.assertEqual(
            exp_error_column, context.get_error_column()
        )

    def test_example(self):

        input = """A(1)
B(1) after [A]
C(1)
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_tasks_names = ["A", "B", "C", "D", "F", "G", "H", "I"]
        exp_tasks_durations = [1, 1, 1, 1, 1, 1, 1, 1]
        exp_tasks_dependencies = [
            [],
            ["A"],
            ["A"],
            ["B"],
            ["B", "C"],
            ["C"],
            ["D", "F"],
            ["F", "G"],
        ]

        self.make_assertions(
            input,
            exp_tasks_names,
            exp_tasks_durations,
            exp_tasks_dependencies,
        )

    def test_fail_example_1(self):

        input = """A(-1)"""

        exp_error_line = 1
        exp_error_column = 3

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_example_2(self):

        input = """A(1)
B(1) afer [A]"""

        mock_task_manager = mock.create_autospec(TaskManager)

        exp_error_line = 2
        exp_error_column = 6

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_example_multiple_spaces_and_breaklines(self):

        input = """A               (
            1
            )  
B
(1) after 

[A
]
C( 1)  
  after          [A]  
D(1)



                           after   [B]
F(1)   after 
  [B, 
   C]
G(1               ) after [C]
H(1)   
after [D


                                ,

 F]
I
(1)  after 
  
  [         F,                         G
  ]  
  
    """

        exp_tasks_names = ["A", "B", "C", "D", "F", "G", "H", "I"]
        exp_tasks_durations = [1, 1, 1, 1, 1, 1, 1, 1]
        exp_tasks_dependencies = [
            [],
            ["A"],
            ["A"],
            ["B"],
            ["B", "C"],
            ["C"],
            ["D", "F"],
            ["F", "G"],
        ]

        self.make_assertions(
            input,
            exp_tasks_names,
            exp_tasks_durations,
            exp_tasks_dependencies,
        )

    def test_fail_empty_input(self):

        input = """"""

        exp_error_line = 1
        exp_error_column = 1

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_task_name(self):

        input = """(1)
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 1
        exp_error_column = 1

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_open_parent_task_name_containig_number(self):

        input = """A1)
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 1
        # as task name accepts number, here task name will be 'A1'
        exp_error_column = 3

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_opening_parentheses_space_in_position(self):

        input = """A 1)
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        mock_task_manager = mock.create_autospec(TaskManager)

        exp_error_line = 1
        exp_error_column = 3

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_duration(self):

        input = """A ()
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 1
        exp_error_column = 4

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_closing_parentheses(self):

        input = """A (1
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 2
        exp_error_column = 1

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_after_keyword(self):

        input = """A (1)
B(1) [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 2
        exp_error_column = 6

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_opening_square_bracket(self):

        input = """A (1)
B(1) after A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 2
        exp_error_column = 12

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_dependency(self):

        input = """A (1)
B(1) after []
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 2
        exp_error_column = 13

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_dependency_just_comma(self):

        input = """A (1)
B(1) after [,]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 2
        exp_error_column = 13

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_second_dependency(self):

        input = """A (1)
B(1) after [A,]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 2
        exp_error_column = 15

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_closing_square_bracket(self):

        input = """A (1)
B(1) after [A,C
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G]"""

        exp_error_line = 3
        exp_error_column = 1

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_opening_parentheses_on_opening_square_bracket(self):

        input = """A(1) after (B]"""

        # in this case, after can be considered as task name, followed by
        # opening parentheses and failing where should be located the duration
        exp_error_line = 1
        exp_error_column = 13

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_incomplete_statement_first_opening_parentheses(self):

        input = """A("""

        exp_error_line = 1
        exp_error_column = 3

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_incomplete_statement_after_after_keyword(self):

        input = """A(56) after"""

        exp_error_line = 1
        exp_error_column = 12

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_word_on_opening_square_bracket_1(self):

        input = """A(1) after B("""

        exp_error_line = 1
        exp_error_column = 12

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_word_on_opening_square_bracket_2(self):

        input = """A(1) after B(1]"""

        exp_error_line = 1
        exp_error_column = 12

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_word_on_duration(self):

        input = """A(dfg)"""

        exp_error_line = 1
        exp_error_column = 3

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_comma_on_dependencies(self):

        input = """A(1)
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D F]
I(1) after 
  [F, G]"""

        exp_error_line = 10
        exp_error_column = 15

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_last_opening_square_bracket(self):

        input = """A(1)
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  F, G]"""

        exp_error_line = 12
        exp_error_column = 3

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_first_closing_parentheses_no_last_comma(self):

        input = """A(1
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F G]"""

        exp_error_line = 2
        exp_error_column = 1

        self.make_assertion_fail(input, exp_error_line, exp_error_column)

    def test_fail_no_final_closing_square_bracket(self):

        input = """A(1)
B(1) after [A]
C(1) 
  after [A]
D(1) after [B]
F(1) after 
  [B, 
   C]
G(1) after [C]
H(1) after [D, F]
I(1) after 
  [F, G"""

        exp_error_line = 12
        exp_error_column = 8

        self.make_assertion_fail(input, exp_error_line, exp_error_column)
