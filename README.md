# uppaal2ros
A translator to accelerate development when going from the formal verification software UPPAAL to the robotics simulation trinity of ROS, Gazebo and ArduPilot.

## What is Uppaal?
Uppaal is an integrated tool environment for modeling, validation and verification of real-time systems modeled as networks of timed automata, extended with data types (bounded integers, arrays, etc.).
The tool is developed in collaboration between the Department of Information Technology at Uppsala University, Sweden and the Department of Computer Science at Aalborg University in Denmark.
The use of Uppaal is appropriate for systems that can be modeled as a collection of non-deterministic processes with finite control structure and real-valued clocks, communicating through channels or shared variables. The software consists of three main parts: a description language, a simulator and a model-checker.


## What is ROS (Robot Operating System)?
The Robot Operating System (ROS) is a flexible framework for writing robot software. It is a collection of tools,libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across awide variety of robotic platforms.
ROS provides libraries, tools, hardware abstraction, device drivers, visualizers, message-passing, packagemanagement, and more to help software developers create robot applications. In the future we expect ROS willbe replaced by ROS2.

## What is Gazebo?
Gazebo is a well-designed open-source robotics simulator that makes it possible to rapidly test algorithms, design robots, perform regression testing, and train AI system using realistic scenarios. It offers the ability to accurately and efficiently simulate populations of robots in complex indoor and outdoor environments.

## What is Ardupilot?

