import unittest
from os import listdir
from os.path import isfile, join
from utils.utils import *
from facades.task_scheduling_facade import TaskSchedulingFacade


class TestGeneral(unittest.TestCase):
    def test_inputs(self):

        input_ext = "tasks.in"
        output_ext = "sched.out"

        test_directory = "../test/"
        input_files = [
            test_directory + f
            for f in listdir(test_directory)
            if isfile(join(test_directory, f))
        ]

        for input_file in input_files:

            if input_ext in input_file:

                output_file = input_file.replace(input_ext, output_ext)

                expected_output_text = read_file(output_file)

                input_text = read_file(input_file)

                task_scheduling_facade = TaskSchedulingFacade()
                output_text = task_scheduling_facade.schedule_task(input_text)

                self.assertEqual(expected_output_text, output_text)

                del task_scheduling_facade
