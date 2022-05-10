import unittest
from algorithms.task_scheduling_algorithm import TaskSchedulingAlgorithm
from managers.task_manager import TaskManager


class TestAlgorithm(unittest.TestCase):
    def create_task_manager(self, tasks_names, durations, dep):

        task_manager = TaskManager()

        for i in range(len(tasks_names)):

            task_manager.create_task(tasks_names[i])
            task_manager.set_task_duration(tasks_names[i], durations[i])

            for dep_name in dep[i]:
                task_manager.add_task_dependency(tasks_names[i], dep_name)

        task_manager.validate_dependencies()

        return task_manager

    def make_assertions(
        self,
        tasks_names,
        tasks_durations,
        tasks_dependencies,
        exp_minimum_duration,
        exp_maximum_parallelism,
        exp_long_chain,
    ):

        task_manager = self.create_task_manager(
            tasks_names, tasks_durations, tasks_dependencies
        )

        task_scheduling = TaskSchedulingAlgorithm()
        task_scheduling.calculate_schedule_metrics(task_manager)

        self.assertEqual(
            exp_minimum_duration, task_scheduling.get_minimum_duration()
        )
        self.assertEqual(
            exp_maximum_parallelism, task_scheduling.get_maximum_parallelism()
        )
        self.assertEqual(exp_long_chain, task_scheduling.get_longest_chain())

    def test_example(self):

        tasks_names = ["A", "B", "C", "D", "F", "G", "H", "I"]
        tasks_durations = [1, 1, 1, 1, 1, 1, 1, 1]
        tasks_dependencies = [
            [],
            ["A"],
            ["A"],
            ["B"],
            ["B", "C"],
            ["C"],
            ["D", "F"],
            ["F", "G"],
        ]

        expected_minimum_duration = 4
        expected_maximum_parallelism = 3
        expected_longest_chain = ["A", "B", "D", "H"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_longest_chain_order_same_values_different_task_position_1(self):

        tasks_names = ["A", "B", "C", "D", "E"]
        tasks_durations = [0, 1, 0, 0, 1]
        tasks_dependencies = [[], ["A"], ["B"], ["B"], ["C", "D"]]

        expected_minimum_duration = 2
        expected_maximum_parallelism = 2
        expected_longest_chain = ["A", "B", "C", "E"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_longest_chain_order_same_values_different_task_position_2(self):

        tasks_names = ["A", "B", "D", "C", "E"]
        tasks_durations = [0, 1, 0, 0, 1]
        tasks_dependencies = [[], ["A"], ["B"], ["B"], ["C", "D"]]

        expected_minimum_duration = 2
        expected_maximum_parallelism = 2
        expected_longest_chain = ["A", "B", "C", "E"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_longest_chain_order_same_values_diff_dep_position_1(self):

        tasks_names = ["A", "B", "C", "D", "E"]
        tasks_durations = [0, 1, 0, 0, 1]
        tasks_dependencies = [[], ["A"], ["B"], ["B"], ["D", "C"]]

        expected_minimum_duration = 2
        expected_maximum_parallelism = 2
        expected_longest_chain = ["A", "B", "D", "E"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_longest_chain_order_same_values_diff_dep_position_2(self):

        tasks_names = ["A", "B", "D", "C", "E"]
        tasks_durations = [0, 1, 0, 0, 1]
        tasks_dependencies = [[], ["A"], ["B"], ["B"], ["D", "C"]]

        expected_minimum_duration = 2
        expected_maximum_parallelism = 2
        expected_longest_chain = ["A", "B", "D", "E"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_wrost_case_complexity(self):

        tasks_names = ["A", "B", "C", "D", "E", "F"]
        tasks_durations = [1, 5, 4, 3, 2, 1]
        tasks_dependencies = [[], ["A"], ["A"], ["A"], ["A"], ["A"]]

        expected_minimum_duration = 6
        expected_maximum_parallelism = 5
        expected_longest_chain = ["A", "B"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_multiple_initial_no_dependencies(self):

        tasks_names = ["A", "B", "C", "D", "E"]
        tasks_durations = [9, 1, 1, 5, 9]
        tasks_dependencies = [[], ["A"], ["B"], [], ["D"]]

        expected_minimum_duration = 14
        expected_maximum_parallelism = 2
        expected_longest_chain = ["D", "E"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )

    def test_mult_init_no_dep_diferent_init_slowest_duration(self):

        tasks_names = ["A", "B", "C", "D", "E"]
        tasks_durations = [1, 1, 1, 5, 9]
        tasks_dependencies = [[], ["A"], ["B"], [], ["D"]]

        expected_minimum_duration = 14
        expected_maximum_parallelism = 2
        expected_longest_chain = ["D", "E"]

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            expected_minimum_duration,
            expected_maximum_parallelism,
            expected_longest_chain,
        )
