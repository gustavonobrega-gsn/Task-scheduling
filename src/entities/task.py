from collections import OrderedDict


class Task:

    def __init__(self, name):
        self._name = name
        self._dependencies_tasks_name = OrderedDict({})
        self._required_for_tasks_name = OrderedDict({})

    def get_name(self):
        return self._name

    def get_duration(self):
        return self._duration

    def set_duration(self, duration):
        self._duration = duration

    def get_dependencies_tasks_name(self):
        return self._dependencies_tasks_name

    def add_dependency(self, dependency_name):
        self._dependencies_tasks_name[dependency_name] = None

    def get_required_for_tasks_name(self):
        return self._required_for_tasks_name

    def add_required_for_task_name(self, required_for_task_name):
        self._required_for_tasks_name[required_for_task_name] = None
