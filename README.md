# Memory Management Testing Platform

[Slovak](README.sk.md) version

In this project, a new testing platform designed for evaluation of dynamic memory allocation algorithms focused on real-time systems is created. The platform producing statistics about the allocation algorithms. A graphic user interface is included in this platform, which is launched on an external computer connected to the testing platform. The platform is performing the testing according to various test scenarios. For hardware, Arduino Uno microcomputer is used. The test results are sent via USB-UART to the external computer, where the results are displayed with GUI-based application. The main goal of the new testing platform is to be able to evaluate various new memory allocation algorithms and their implementations and to compare their attributes and performance to other existing algorithms. In addition to that, it will be possible to see online changes in memory during the execution of the testing scenarios. Because of repetitive allocation and freeing of the memory blocks of various sizes and locations, one can observe how fragmentation appears in the memory. After all of this, one can also compare different memory allocation methods and algorithms according to their response times and determinism.

On the base of this project an article was published at conference IIT.SRC 2017.

## Architecture of testing platform

![Alt text](img/architecture.png?raw=true "Architecture of testing platform")

The test platform is created by two parts, the first part being on the Arduino MEGA 2560 mini computer and the second on an external computer. The first part is running FreeRTOS operating system and extends it with the case management algorithms. These are implemented in the same language as the FreeRTOS operating system and therefore the C language. The second part, which contains graphical elements and runs on an external computer, is implemented in Python 2.7.

Based on a graphical interface design, Qt Designer was used to generate an xml file and converted ten to Python.

## User interface

![Alt text](img/gui.png?raw=true "Gui")

## Implementation of algorithms
Within the project we created and compared implementation of two memory management algorithms: Best fit and Worst fit.

For correct and fast functioning of both algorithms, it is necessary to store free blocks of memory in a data structure that keeps them organized in the correct order - linked list of blocks. In the case of the Best fit algorithm, the arrangement of free blocks is from the smallest to the largest. Worst fit algorithm from largest to smallest.

One block of memory is a data structure that represents the header of the memory block. It contains three data. The type of this data depends on the memory in which the implementation will work. In any case, their meaning remains the same. These are:
- a pointer (address) to the next free block
- a pointer (address) to the previous physical block
- block size


## Results of testing
Testing was performed in 4 scenarios, each scenario being specific to its memory requirements in terms of the size of allocated blocks.
Each scenario consists of multiple tasks of allocating, reallocating and releasing memory blocks.

Statistics are captured after the 4th test scenario, which works with different block sizes and combines all 3 types of requests. This simulates the real use of memory in practice. The scenario thus reveals the memory state after a sufficiently long period of memory usage to be able to see the strengths and weaknesses of each algorithm.

#### Porovnanie časov
![Alt text](img/en_times.png?raw=true "Time")
From the time point of view, the Worst fit algorithm works faster with different block sizes, which also had a better test time.

#### Porovnanie fragmentácie
![Alt text](img/en_free_blocks.png?raw=true "free blocks")

![Alt text](img/en_num_blocks.png?raw=true "num blocks")

## License
This project was created as bachelor thesis in FIIT STU. May 2017.

