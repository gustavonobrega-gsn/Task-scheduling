class TaskSchedulingAlgorithmResources:

    def get_no_dependencies_tasks_name(self):
        return self._no_dependencies_tasks_name

    def set_no_dependencies_tasks_name(self, no_dependencies_tasks_name):
        self._no_dependencies_tasks_name = no_dependencies_tasks_name

    def append_no_dependencies_tasks_name(self, no_dependencies_task_name):
        self._no_dependencies_tasks_name.append(no_dependencies_task_name)

    def remove_no_dependencies_tasks_name(self, no_dependencies_tasks_index):
        del self._no_dependencies_tasks_name[no_dependencies_tasks_index]

    def get_remaining_dependencies(self, task_name):
        return self._remaining_dependencies[task_name]

    def has_remaining_dependencies(self, task_name):
        return task_name in self._remaining_dependencies

    def set_remaining_dependencies(self, task_name, dependencies):
        self._remaining_dependencies[task_name] = dependencies

    def remove_task_remaining_dependency(self, task_name, dependency):
        self._remaining_dependencies[task_name].remove(dependency)

    def clear_remaining_dependencies(self):
        self._remaining_dependencies = {}
        self._last_dependency = {}

    def get_last_dependency(self, task_name):
        if task_name in self._last_dependency:
            return self._last_dependency[task_name]
        else:
            return None

    def set_last_dependency(self, task_name, dependency):
        self._last_dependency[task_name] = dependency

    def clear_tasks_done(self):
        self._tasks_done = set()

    def add_tasks_done(self, task_name):
        self._tasks_done.add(task_name)

    def has_task_done(self, task_name):
        return task_name in self._tasks_done

    def get_tasks_remaning_duration(self, task_name):
        return self._tasks_remaning_duration[task_name]

    def has_task_remaning_duration(self, task_name):
        return task_name in self._tasks_remaning_duration

    def clear_tasks_remaning_duration(
        self,
    ):
        self._tasks_remaning_duration = {}

    def set_tasks_remaning_duration(self, task_name, task_duration):
        self._tasks_remaning_duration[task_name] = task_duration

    def get_last_longest_chain_task(self):
        return self._last_longest_chain_task

    def set_last_longest_chain_task(self, last_longest_chain_task):
        self._last_longest_chain_task = last_longest_chain_task
