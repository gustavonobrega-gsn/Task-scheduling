# Instructions

## Prerequisites

You will need Python3 and pip installed. Go to [Python download page](https://www.python.org/downloads/), download and install it accordingly to your OS.

## How to Run

- Using Python command line:
  - Open a terminal command line, go to this project root directory and execute:
</br></br>`python3 src/schedule-tasks.py "input_file"`
</br></br>where "input_file" must represent a file in the file system, eg: test/example.tasks.in

- Executing binary File:
  - Using pip, install pyinstaller executing:
</br></br>`pip install pyinstaller --upgrade`
</br></br>
  - From this project root directory, generate binary executing:
</br></br>`pyinstaller src/schedule-tasks.py --onefile`
</br></br>
  - Move binary file dist/schedule-tasks to this project root directory, Linux example:
</br></br>`mv dist/schedule-tasks .`
</br></br>
  - Execute binary passing a file as argument, Linux example:
</br></br>`./schedule-tasks test/example.tasks.in`

## How to Test

Open a terminal command line, go to this project src directory and execute:
</br></br>`python3 -m unittest "input_file"`
</br></br>where "input_file" must represent a file in the file system, eg: test/test_algorithm.py
</br></br>To run all tests at once, in src directory, execute:
</br></br>`python3 -m unittest`
</br></br>Note: Among the tests, there is test_general.py, that uses each one of the files with extension tasks.in from test directory as input for the program and compares the program output with the content of the file with same name, same directory, but with extension sched.out.
