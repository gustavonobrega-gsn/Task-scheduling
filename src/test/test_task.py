import unittest
from entities.task import Task


class TestTask(unittest.TestCase):
    def test_name(self):

        task_name = "task_name"

        task = Task(task_name)

        self.assertEqual(task_name, task.get_name())

    def test_duration(self):

        task_name = "task_name"
        task_duration = 6

        task = Task(task_name)
        task.set_duration(task_duration)

        self.assertEqual(task_duration, task.get_duration())

    def test_dependencies(self):

        task_name = "task_name"
        dependencies = [
            "task_name2",
            "task_name3",
            "task_name4",
            "task_name5",
            "task_name6",
        ]

        task = Task(task_name)

        for dependency in dependencies:
            task.add_dependency(dependency)

        task_dependencies = task.get_dependencies_tasks_name()
        task_dependencies_list = [*task_dependencies]

        index_task_dependencies_list = 0
        while index_task_dependencies_list < len(task_dependencies_list):

            self.assertEqual(
                task_dependencies_list[index_task_dependencies_list],
                dependencies[index_task_dependencies_list],
            )

            index_task_dependencies_list += 1

    def test_required_for(self):

        task_name = "task_name"
        required_for_tasks = [
            "task_name2",
            "task_name3",
            "task_name4",
            "task_name5",
            "task_name6",
        ]

        task = Task(task_name)

        for required_for_task in required_for_tasks:
            task.add_required_for_task_name(required_for_task)

        task_required_for = task.get_required_for_tasks_name()
        task_required_for_list = [*task_required_for]

        index_task_required_for_list = 0
        while index_task_required_for_list < len(task_required_for_list):

            self.assertEqual(
                task_required_for_list[index_task_required_for_list],
                required_for_tasks[index_task_required_for_list],
            )

            index_task_required_for_list += 1
