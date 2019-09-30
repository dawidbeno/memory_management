# Memory Management testing platform
In this project, a new testing platform designed for evaluation of dynamic memory allocation algorithms focused on real-time systems is created. The platform producing statistics about the allocation algorithms. A graphic user interface is included in this platform, which is launched on an external computer connected to the testing platform. The platform is performing the testing according to various test scenarios. For hardware, Arduino Uno microcomputer is used. The test results are sent via USB-UART to the external computer, where the results are displayed with GUI-based application. The main goal of the new testing platform is to be able to evaluate various new memory allocation algorithms and their implementations and to compare their attributes and performance to other existing algorithms. In addition to that, it will be possible to see online changes in memory during the execution of the testing scenarios. Because of repetitive allocation and freeing of the memory blocks of various sizes and locations, one can observe how fragmentation appears in the memory. After all of this, one can also compare different memory allocation methods and algorithms according to their response times and determinism.

## Architecture of testing platform

![Alt text](img/architecture.png?raw=true "Architecture of testing platform")

## User interface

![Alt text](img/gui.png?raw=true "Gui")

