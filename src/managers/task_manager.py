from entities.task import Task


class TaskManager:

    def __init__(self):
        self._task_pool = {}

        self._no_dependencies_lowest_duration = None
        self._no_dependencies_tasks_name = []

    # return lowest duration amount tasks that dont have dependencies
    def get_no_dependencies_lowest_duration(self):
        return self._no_dependencies_lowest_duration

    # return copy of list of tasks with no dependencies
    def get_no_dependencies_tasks_name(self):
        return [*self._no_dependencies_tasks_name]

    def get_task(self, task_name):
        return self._task_pool[task_name]

    def create_task(self, task_name):

        # return false if task already exist in the pool
        if task_name in self._task_pool:
            return False

        # create a task
        task = Task(task_name)
        # store in the pool
        self._task_pool[task_name] = task

        return True

    def set_task_duration(self, task_name, task_duration):

        # get task from the pool
        task = self._task_pool[task_name]
        # set duration
        task.set_duration(task_duration)

    def add_task_dependency(self, task_name, task_dependency_name):

        # get task from the pool
        task = self._task_pool[task_name]
        # set dependencies_task
        task.add_dependency(task_dependency_name)

    # check if all dependecies were defined as tasks
    # and build algorithm optimization settings:
    # 1. tasks with no depedencies
    # 2. lowest duration amoung tasks with no depedencies
    # 3. inverse dependence aslso know as required for
    # if validation is not ok,
    # return first dependency name with no task definition
    # got from top to bottom, left to right
    # return None if validation is ok
    def validate_dependencies(self):

        self._no_dependencies_lowest_duration = None
        self._no_dependencies_tasks_name = []

        # for each task in the pool
        for task_name in self._task_pool:

            task = self._task_pool[task_name]

            # if the task has no dependency
            if not task.get_dependencies_tasks_name():

                # store tasks with no dependencies
                self._no_dependencies_tasks_name.append(task_name)

                # track lowest initial duration from tasks that do not
                # have dependencies
                if (self._no_dependencies_lowest_duration is None) or (
                    task.get_duration() < self._no_dependencies_lowest_duration
                ):
                    self._no_dependencies_lowest_duration = task.get_duration()

            # if the task has dependency
            else:

                # for each dependecy task
                for task_dependency_name in task.get_dependencies_tasks_name():

                    # if dependecy task does not exist in the pool, it is an
                    # unknow dependency and return its name
                    if task_dependency_name not in self._task_pool:
                        return task_dependency_name

                    # get dependecy task from the pool
                    task_dependency = self._task_pool[task_dependency_name]

                    # add current task on their required_for collection
                    task_dependency.add_required_for_task_name(task_name)

        return None
