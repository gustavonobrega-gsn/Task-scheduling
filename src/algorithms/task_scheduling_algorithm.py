from entities.task_scheduling_algorithm_resources import (
    TaskSchedulingAlgorithmResources,
)


class TaskSchedulingAlgorithm:

    def __init__(self):

        self._minimum_duration = 0
        self._maximum_parallelism = 0
        self._longest_chain = []

    def get_minimum_duration(self):
        return self._minimum_duration

    def get_maximum_parallelism(self):
        return self._maximum_parallelism

    def get_longest_chain(self):
        return self._longest_chain

    # process min duration
    def _process_minimum_duration(self, current_shortest_duration):
        self._minimum_duration += current_shortest_duration

    # process max paralellism
    def _process_maximum_parallelism(self, current_parallelism):
        if self._maximum_parallelism < current_parallelism:
            self._maximum_parallelism = current_parallelism

    # store last dependency obeying the input order
    def _set_task_last_dependency(
        self, required_for_task, algorithm_resources
    ):
        # for each dependency, obeying the input order
        for dependency in required_for_task.get_dependencies_tasks_name():

            # if dependency was completed this iteration
            if algorithm_resources.has_task_done(dependency):

                # set is as direct responsable for the current task
                # this will be used to generate longest chain
                algorithm_resources.set_last_dependency(
                    required_for_task.get_name(),
                    dependency
                )
                # after last dependency, return
                return

    # process tasks that require task that was popped out from the container
    # if they don't have pending dependencies, set them to be brought inside
    # the container for the next iteration
    def _process_required_for(self, task, algorithm_resources, task_manager):

        shortest_duration = None

        # for each required_for_task
        for required_for_task_name in task.get_required_for_tasks_name():

            # get required_for_task from the task pool
            required_for_task = task_manager.get_task(required_for_task_name)

            # if remaining task dependencies and is not being tracked yet
            if not algorithm_resources.has_remaining_dependencies(
                required_for_task_name
            ):
                # add its dependencies to be tracked
                algorithm_resources.set_remaining_dependencies(
                    required_for_task_name,
                    set(required_for_task.get_dependencies_tasks_name()),
                )

            # remove current task dependency from it
            # and register last removed dependency
            algorithm_resources.remove_task_remaining_dependency(
                required_for_task_name, task.get_name()
            )

            # if there is no more pending dependencies
            if not algorithm_resources.get_remaining_dependencies(
                required_for_task_name
            ):

                # push task into the container
                algorithm_resources.append_no_dependencies_tasks_name(
                    required_for_task_name
                )

                # store last dependency obeying the input order
                self._set_task_last_dependency(
                    required_for_task, algorithm_resources
                )

                # keep track of the minimum duration
                if (shortest_duration is None) or (
                    required_for_task.get_duration() < shortest_duration
                ):
                    shortest_duration = required_for_task.get_duration()

        return shortest_duration

    # subtract current processing duration from current
    # task duration and add it to keep track
    # return the remainder of task duration
    def _process_task(self, task, shortest_duration, algorithm_resources):

        # if remaining task duration is not being tracked yet
        if not algorithm_resources.has_task_remaning_duration(task.get_name()):
            # add its duration to be tracked
            algorithm_resources.set_tasks_remaning_duration(
                task.get_name(), task.get_duration()
            )

        # subtract its duration with current shortest duration
        algorithm_resources.set_tasks_remaning_duration(
            task.get_name(),
            algorithm_resources.get_tasks_remaning_duration(task.get_name())
            - shortest_duration,
        )

        # return task duration
        return algorithm_resources.get_tasks_remaning_duration(task.get_name())

    # process current container state and return next iteration
    # shortest duration long
    # enough to remove at least one element from the container
    def _process_current_container_state(
        self, current_shortest_duration, algo_resources, task_manager
    ):

        next_shortest_duration = None

        # stores the tasks completed this iteration to be checked with their
        # required_for
        # once a required_for is dont have dependencies left, this buffer
        # will be used to check which dependency from it was the last one,
        # this will be its path to longest chain. If there are two or more
        # dependencies here, it will obey the order the dependencies appeared
        # in the input, from left to right
        algo_resources.clear_tasks_done()

        # for each name in the current container
        index = len(algo_resources.get_no_dependencies_tasks_name()) - 1
        while index >= 0:

            task_name = algo_resources.get_no_dependencies_tasks_name()[index]

            task = task_manager.get_task(task_name)

            # subtract task duration with current shortest
            # duration and add its duration to be tracked
            duration = self._process_task(
                task, current_shortest_duration, algo_resources
            )

            # if current task duration is zero or lower
            if duration <= 0:

                # add current task to task done this iteration
                algo_resources.add_tasks_done(task_name)

                # check the tasks that depend on current task already done,
                # put them in next container state if they dont have
                # pending dependencies.
                # also get lowest time from the new tasks brought inside.
                duration = self._process_required_for(
                    task, algo_resources, task_manager
                )

                # remove task from the container
                algo_resources.remove_no_dependencies_tasks_name(index)

            # store lowest duration for the next iteration
            if (next_shortest_duration is None) or (
                (duration) and (duration < next_shortest_duration)
            ):
                next_shortest_duration = duration

            # continue processing the tasks in the container
            index -= 1

        return next_shortest_duration

    # starting from the last task that occupied the first container
    # position, follows the chain of last depencies until find a task
    # with no dependencies, then, return the chain
    def _process_longest_chain(
        self, algorithm_resources
    ):
        # start longest chain
        longest_chain = []

        # start from the last task that occupied the first container position
        task = algorithm_resources.get_last_longest_chain_task()

        # while getting task dependencies
        while task:
            # since starts by the last task and follows until beginning,
            # insert task at first chain position
            longest_chain.insert(0, task)

            # continue following the chain od dependencies
            task = algorithm_resources.get_last_dependency(task)

        return longest_chain

    # calculate scheduling metrics using the task pool from task_manager and
    # some optimization variables
    def calculate_schedule_metrics(self, task_manager):

        # create algorithm resources class
        algorithm_resources = TaskSchedulingAlgorithmResources()

        # for the first iteration, minimum duration
        # is already known from previous steps
        shortest_duration = task_manager.get_no_dependencies_lowest_duration()

        # main container that stores the tasks that are being processed
        # for the first iteration, it is already filled with tasks already
        # known from previous steps
        algorithm_resources.set_no_dependencies_tasks_name(
            task_manager.get_no_dependencies_tasks_name()
        )

        # stores a map of dependencies for each task
        # once empty for a specific task, that task can be put into the
        # container
        algorithm_resources.clear_remaining_dependencies()

        # stores the remaining time for a task to be completed
        # duration zero means task is completed and can be removed
        # from the container
        algorithm_resources.clear_tasks_remaning_duration()

        # will iterate until this container is empty
        # meaning that all the tasks were processed
        while algorithm_resources.get_no_dependencies_tasks_name():

            # on each iteration, check the minimum time long enough
            # to remove at least one element from the container
            # and store the lowest value
            self._process_minimum_duration(shortest_duration)

            # parallelism is the number of tasks in the container on
            # one iteration.
            # keep track of the maximum value
            self._process_maximum_parallelism(
                len(algorithm_resources.get_no_dependencies_tasks_name())
            )

            # every iteration will store the first task from the container
            # once out of the loop, this will point to the last element
            # on the longest chain
            algorithm_resources.set_last_longest_chain_task(
                algorithm_resources.get_no_dependencies_tasks_name()[0]
            )

            # for each element in the container, subtract their duration with
            # current shortest duration.
            # in case after this the element contains zero duration, it will
            # be removed from the container and the elements that depends on
            # it will be checked if they can be brought to the container.
            # if they do not have any dependency to be processed, they can be
            # brought.
            # As the subtraction and bringing new elements to the container
            # happen, the algorithm will keep
            # track of the shortest duration enough to remove an element on
            # the next iteration. This value will be returned here
            shortest_duration = self._process_current_container_state(
                shortest_duration, algorithm_resources, task_manager
            )

        # starting from the last task that occupied the first container
        # position, follows the chain of last depencies until find a task
        # with no dependencies, then, return the chain
        self._longest_chain = self._process_longest_chain(
            algorithm_resources
        )
