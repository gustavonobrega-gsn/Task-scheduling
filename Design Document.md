# Design Document

The proposed solution will take place in the following steps:

- Validation
- Deserialization
- Data processing

## Validation

First step, input validation will be implemented using a state machine where each state will have a specific regular expression that will be applied as the input is scanned. The possible transitions between the states will be according to the input syntax presented in the problem description.

Expected valid Input syntax for each statement will be:

[**Task name**] [**opening parentheses**] [**duration**] [**closing parentheses**]

In addition, it's also possible having statements like:

[**Task name**] [**opening parentheses**] [**duration**] [**closing parentheses**] [**after**] [**opening square bracket**] [**Task collection**] [**closing square bracket**]

Where **Task collection** valid syntax will be:

For one Task: [**Task name**]
For many Tasks: [**Task name**] [**comma**] [**Task name**] [**comma**] ... [**Task name**] [**comma**] [**Task name**]

Elements description:

- **Task name**: any sized word (a-z, A-Z, 0-9)+, no special characters
- **opening parentheses**: character '('
- **duration**: non negative integer, zero is possible (0-9)+
- **closing parentheses**: character ')'
- **after**: lowercase keyword 'after'
- **opening square bracket**: character '['
- **comma**: character ','
- **closing square bracket**: : character ']'

Note that between each element there can be any number of whitespaces, tabs and line breaks (also including positions before and after border elements), but individually, the elements have to be concise and written without separating the characters that compose them.

In the state machine, for each element type, there will be a state containing a regular expression.

For each statement, the state machine starts at the state of the leftmost element of the input (**Task name**), following the states to the right, as the elements from the input are scanned.

Before the validation of each element, the existence of blank spaces and line breaks until the next element is checked in the current position of the input, keeping track of the number of lines and columns scanned so far. Once the next element has been found, if its validation is positive, the next state will obey the described syntax order, always proceeding from left to right.

Transitions will almost always have a single possible target state, with the exception of **closing parentheses** and **Task name** in the **Task collection**. For these states, there are two possible transitions that will be switched according to the element in front of the next one, which will need to be checked while still in the current state.

If there is any violation in the input syntax, an error indicating the line and column of the file will be printed and the program will terminate.

## Deserialization

This will be done in parallel with the validation step, where data can be validated and containerized following the states from the state machine as the input is scanned.

During the containerization process, data validation still happens. In case duplicated tasks names are detected, specifically during **Task name**, even if the dependencies are the same, the program will return an error text indicating the line and column of the file where the second declaration was found.

The tasks can come in any order, therefore there is no violation if a dependency declaration as Task comes after a Task that lists it as a dependency. That's why the program only analyses the dependencies at the end of this step, when it is aware of all tasks and dependencies. Also, there is no violation if the dependencies come duplicated in the dependency list for the same task. However, if a Task lists a dependency that was not declared anywhere in the file as a Task, similarly to duplicated tasks declaration, the program will return an error text with the line and column where the dependency was listed.

At the end of this, it is expected to have the whole data abstracted into Task classes, which will be composed by the Task name, the collection of the names of the Tasks which it is dependent on, and the collection of the names of the Tasks that depend on it.

For better performance, those collections will be implemented as ordered dictionaries having the key set as the name of the Task. After creation, each class will be stored on a task pool, which will be the only reference for the objects. Task pool will also be managed by a Task Manager that makes use of dictionary with key as Task name.

## Data processing

This processing step will also be divided into **two parts**:

The **first one** will calculate the the minimum duration, the highest parallelism and last element which ends the longest chain of tasks.

For this, a container will be used to store Tasks without dependencies. Initially the container will be filled with already known Tasks with no dependencies from the previous steps. The algorithm will run, adding and removing tasks, until this container is completely empty.

At the start of each iteration, the algorithm will keep track of the time spent so far (representing the minimum duration) and the maximum size of the container (representing the maximum parallelism).

At each iteration, the smallest amount of processing time among the elements that are in the collection will be subtracted from all of those elements. In the first iteration this lowest value will be filled with an already known value from the previous step. For optimization matter, during this subtraction operation, the algorithm will keep track of the lowest processing time to fill the lowest value on the next iteration. Beyond that, during this subtraction step, the task that is detected having a duration value equal to zero will be removed from the collection.

Just before removing that element, each element that is dependent on it (stored in this Task as collection of the names of Tasks that depend on it) will be evaluated if it still has any other unprocessed dependencies (checking if its object collection of Tasks which it is dependent on is not empty). If not, this element will be brought from the Tasks pool to the main container and its last dependency that was removed from the container will be stored to be used later as a direct link in the longest chain of tasks. In case two or more dependencies were removed as last dependencies, the algorithm will choose the one that was first present on the input of dependencies, from left to right.

At the end of this step, the minimum duration and the highest parallelism value will be obtained. Also, in the final iteration, the last element in the container will be the one which ends the longest chain of tasks. If there are two or more elements in the container, the one that was first present on the input as Task name, from top to bottom, will be considered as the last element.

The complexity for this step is expected as being on the best case O(N), i.e., on cases where on each iteration, elements from the previous iteration leaves the container after subtraction, bringing new elements, if it is the case of having elements that depend on it. In the worst case, the performance will be O(N²), as subtraction on the same remaining elements will happen on multiple iterations.

The **second one** will calculate the longest chain of tasks by a graph processing where each Task will represent a node.

Here, the longest chain of tasks will be considered the longest chain for the total duration of tasks, as this important metric indicates the worst-case scenario for using computational resources in resolving dependencies.

Starting from the last task stored on the previous step, following the link of last dependency for each task in the chain, after appending all tasks, the longest chain will be built.

Traversing this last dependencies link, the algorithm will be following a sub list of the input, so the time complexity for this step will be the O(logN).

## Tools expected to use

- Python3 installation
- Python modules: sys, collections, abc, re, unittest, mock
