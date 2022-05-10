import unittest
from managers.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def test_create_task(self):

        task_name = "Task_1"

        task_mgr = TaskManager()
        result = task_mgr.create_task(task_name)

        self.assertTrue(result)
        self.assertEqual(task_name, task_mgr.get_task(task_name).get_name())

    def test_create_task_duplicated(self):

        task_name = "Task_1"

        task_manager = TaskManager()
        result = task_manager.create_task(task_name)

        self.assertTrue(result)

        result = task_manager.create_task(task_name)

        self.assertFalse(result)

    def test_unknow_dependency(self):

        tasks_names = ["A", "B", "C", "D", "F", "G", "H", "I"]
        tasks_durations = [1, 1, 1, 1, 1, 1, 1, 1]
        tasks_dependencies = [
            ["Z"],
            ["A"],
            ["A"],
            ["B"],
            ["B", "C"],
            ["C"],
            ["D", "F"],
            ["F", "G"],
        ]

        task_manager = TaskManager()

        for i in range(len(tasks_names)):

            task_manager.create_task(tasks_names[i])
            task_manager.set_task_duration(tasks_names[i], tasks_durations[i])

            for dep_name in tasks_dependencies[i]:
                task_manager.add_task_dependency(tasks_names[i], dep_name)

        unknow_dependency = task_manager.validate_dependencies()
        self.assertEqual(unknow_dependency, "Z")

    def make_assertions(
        self,
        tasks_names,
        tasks_durations,
        tasks_dependencies,
        tasks_required_for,
        tasks_no_dependencies_tasks_name,
        lowest_duration,
    ):

        task_mng = TaskManager()

        for i in range(len(tasks_names)):

            task_mng.create_task(tasks_names[i])
            task_mng.set_task_duration(tasks_names[i], tasks_durations[i])

            for dependency_name in tasks_dependencies[i]:
                task_mng.add_task_dependency(tasks_names[i], dependency_name)

        unknow_dependency = task_mng.validate_dependencies()
        self.assertEqual(unknow_dependency, None)

        for i in range(len(tasks_names)):

            self.assertEqual(
                task_mng.get_task(tasks_names[i]).get_name(), tasks_names[i]
            )
            self.assertEqual(
                task_mng.get_task(tasks_names[i]).get_duration(),
                tasks_durations[i],
            )

            dependencies = list(
                task_mng.get_task(tasks_names[i]).get_dependencies_tasks_name()
            )

            for index_dependencies in range(len(dependencies)):
                self.assertEqual(
                    dependencies[index_dependencies],
                    tasks_dependencies[i][index_dependencies],
                )

            required_for = list(
                task_mng.get_task(tasks_names[i]).get_required_for_tasks_name()
            )

            for index_required_for in range(len(required_for)):
                self.assertEqual(
                    required_for[index_required_for],
                    tasks_required_for[i][index_required_for],
                )

        no_dep_tasks_name = task_mng.get_no_dependencies_tasks_name()

        for index_no_dep_tasks in range(len(no_dep_tasks_name)):
            self.assertEqual(
                no_dep_tasks_name[index_no_dep_tasks],
                tasks_no_dependencies_tasks_name[index_no_dep_tasks],
            )

        self.assertEqual(
            task_mng.get_no_dependencies_lowest_duration(), lowest_duration
        )

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

        exp_tasks_required_for = [
            ["B", "C"],
            ["D", "F"],
            ["F", "G"],
            ["H"],
            ["H", "I"],
            ["I"],
            [],
            [],
        ]
        exp_tasks_no_dependencies_tasks_name = ["A"]
        exp_lowest_duration = 1

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            exp_tasks_required_for,
            exp_tasks_no_dependencies_tasks_name,
            exp_lowest_duration,
        )

    def test_different_durations(self):
        tasks_names = ["A", "B", "C", "D", "F"]
        tasks_durations = [10, 5, 4, 3, 2, 1]
        tasks_dependencies = [[], ["A"], ["A"], ["A"], ["A"], ["A"]]

        exp_tasks_required_for = [["B", "C", "D", "F"], [], [], [], [], []]
        exp_tasks_no_dependencies_tasks_name = ["A"]
        exp_lowest_duration = 10

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            exp_tasks_required_for,
            exp_tasks_no_dependencies_tasks_name,
            exp_lowest_duration,
        )

    def test_multiple_no_dependencies_tasks(self):
        tasks_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        tasks_durations = [10, 5, 4, 3, 2, 1, 5, 6]
        tasks_dependencies = [[], ["A"], ["A"], ["A"], ["A"], ["A"], [], []]

        exp_tasks_required_for = [
            ["B", "C", "D", "E", "F"],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
        exp_tasks_no_dependencies_tasks_name = ["A", "G", "H"]
        exp_lowest_duration = 5

        self.make_assertions(
            tasks_names,
            tasks_durations,
            tasks_dependencies,
            exp_tasks_required_for,
            exp_tasks_no_dependencies_tasks_name,
            exp_lowest_duration,
        )
