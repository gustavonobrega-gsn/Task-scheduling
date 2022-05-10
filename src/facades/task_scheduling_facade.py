from statemachines.task_validation_statemachine.context import Context
from managers.task_manager import TaskManager
from algorithms.task_scheduling_algorithm import TaskSchedulingAlgorithm


class TaskSchedulingFacade:

    def schedule_task(self, input_text):

        # create a task manager that will hold the task pool
        task_manager = TaskManager()

        # create validation statemachine context
        context = Context()

        # check if input is valid while building the task pool in task_manager
        is_valid = context.validate(input_text, task_manager)

        # if error on the input, return erro message
        if not is_valid:
            output_text = (
                f"Error: "
                f"line "
                f"{str(context.get_error_line())}, "
                f"column "
                f"{str(context.get_error_column())}"
            )
        # if input ok
        else:
            # create a task scheduling algorithm layer
            task_scheduling = TaskSchedulingAlgorithm()
            # calculate scheduling metrics using the task pool
            # from task_manager and some optimization variables
            task_scheduling.calculate_schedule_metrics(task_manager)

            # prepare output string
            output_text = f"""Critical: {
                '->'.join(
                task_name for task_name in task_scheduling.get_longest_chain()
                )
            }
Minimum: {str(task_scheduling.get_minimum_duration())}
Parallelism: {str(task_scheduling.get_maximum_parallelism())}"""

        # return output with the metrics
        return output_text
