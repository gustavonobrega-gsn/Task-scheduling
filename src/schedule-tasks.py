from utils.utils import *
from facades.task_scheduling_facade import TaskSchedulingFacade


def main():
    # get file name from comand line
    input_file = get_first_command_line_argument()

    # get input file content
    input_text = read_file(input_file)

    # create framework facade
    task_scheduling_facade = TaskSchedulingFacade()

    # make use and get result from framework
    output_text = task_scheduling_facade.schedule_task(input_text)

    # write result output
    print_stdout(output_text)


if __name__ == "__main__":

    main()
