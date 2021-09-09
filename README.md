
# uppaal2ros
Formal verification ensures assurance to the modeling and design of robotic applications in executing autonomous operations. However, transitioning from formally validated models created in formal environments/software such as UPPAAL to simulation software such as Robot Operating System (ROS), Gazebo and ArduPilot takes effort and is prone to human errors. Therefore, we present a translator to accelerate development when going from the formal verification software UPPAAL to the robotics simulation trinity of ROS, Gazebo and ArduPilot. This work has been submitted for publication in IEEE Systems Journal and is under review.

# Table of Contents
1. [What is Uppaal?](#what-is-uppaal)

2. [What is ROS?](#what-is-ros-robot-operating-system)

3. [What is Gazebo?](#what-is-gazebo)

4. [What is Ardupilot?](#what-is-ardupilot)

5. [What is Mavros?](#what-is-mavros)

6. [What is Mavlink?](#what-is-mavlink)

7. [What is Software In the Loop Simulation (SITL)?](#what-is-software-in-the-loop-simulation-sitl)

8. [Simulation Environment Installation Guide](#simulation-environment-installation-guide)

    a. [ROS Installation](#ros-installation)    
        
    b. [MAVROS Installation](#mavros-installation)
    
    c. [Ardupilot Tools Installation](#ardupilot-tools-installation)
    
    d. [Gazebo Installation](#gazebo-installation)
    
    e. [For the SITL Simulator](#for-the-sitl-simulator)
    
    f. [Connecting Ardupilot with ROS](#connecting-ardupilot-with-ros)
    
    g. [Troubleshooting](#troubleshooting)
    
    h. [Initialization of the Catkin Workspace](#initialization-of-the-catkin-workspace)

9. [Running the Simulation](#running-the-simulation)

## What is Uppaal?
Uppaal is an integrated tool environment for modeling, validation and verification of real-time systems modeled as networks of timed automata, extended with data types (bounded integers, arrays, etc.).
The tool is developed in collaboration between the Department of Information Technology at Uppsala University, Sweden and the Department of Computer Science at Aalborg University in Denmark.
The use of Uppaal is appropriate for systems that can be modeled as a collection of non-deterministic processes with finite control structure and real-valued clocks, communicating through channels or shared variables. The software consists of three main parts: a description language, a simulator and a model-checker.


## What is ROS (Robot Operating System)?
The Robot Operating System (ROS) is a flexible framework for writing robot software. It is a collection of tools,libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across awide variety of robotic platforms.
ROS provides libraries, tools, hardware abstraction, device drivers, visualizers, message-passing, packagemanagement, and more to help software developers create robot applications. In the future we expect ROS will be replaced by ROS2.

## What is Gazebo?
Gazebo is a well-designed open-source robotics simulator that makes it possible to rapidly test algorithms, design robots, perform regression testing, and train AI system using realistic scenarios. It offers the ability to accurately and efficiently simulate populations of robots in complex indoor and outdoor environments.

## What is Ardupilot?
ArduPilot is a trusted, versatile, and open source autopilot system that supports vehicle types inculuding multi-copters, traditional helicopters, fixed wing aircraft, boats, submarines, rovers and more. The specific project within Ardupilot used in this research effort is Arducopter, which is the autopilot system for multicopters, helicopters, and other rotor vehicles. As part of the wider ArduPilot software platform, Arducopter works seamlessly with a variety of Ground Control Station programs that are used to setup the vehicle, monitor the vehicle’s flight in real-time and perform powerful mission planning activities.

## What is MAVROS?
MAVROS is a ROS “node” that can convert between ROS topics and MAVLink messages allowing ArduPilotvehicles to communicate with ROS. The MAVROS code can be found here.
A node is a process that performs computation. Nodes are combined together into a graph and communicatewith one another using streaming topics, RPC services, and the Parameter Server. These nodes are meant tooperate at a fine-grained scale; a robot control system will usually comprise many nodes. For example, one nodecontrols a laser range-finder, one Node controls the robot's wheel motors, one node performs localization, onenode performs path planning, one node provides a graphical view of the system, and so on.

## What is MAVLink?
MAVLink is a very lightweight messaging protocol for communicating with drones (and between onboard dronecomponents). It follows a modern hybrid publish-subscribe and point-to-point design pattern: data streams are sent /published as topics while configuration sub-protocols such as the mission protocol or parameter protocol arepoint-to-point with retransmission. Messages are defined within XML files.

## What is Software In The Loop Simulation (SITL)?
SITL allows you to run ArduPilot on your PC directly, without any special hardware. It takes advantage of the fact that ArduPilot is a portable autopilot that can run on a very wide variety of platforms. Your PC is just another platform that ArduPilot can be built and run on.
When running in SITL sensor data comes from a flight dynamics model in a flight simulator. ArduPilot has awide range of vehicle simulators built in, and can interface to several external simulators like Gazebo. This allows ArduPilot to be tested on a very wide variety of vehicle types. 
A big advantage of ArduPilot on SITL is it gives you access to the full range of development tools available todesktop C++ development, such as interactive debuggers, static analyzers and dynamic analysis tools. Thismakes developing and testing new features in ArduPilot much simpler.

# Simulation Environment Installation Guide
### ROS Installation
#### 1. Setup the sources.list
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```
#### 2. Setup the keys
```
sudo apt install curl # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```
#### 3. Installation
```
sudo apt insall ros-neotic-desktop-full
```
#### 4. Other
You can always install a specific package found @ https://index.ros.org/packages/page/1/time/#noetic directly using:
```
sudo apt install ros-noetic-PACKAGE
```
### MAVROS Installation
ROS repository has binary packages for Ubuntu x86, amd64 (x86_64) and armhf (ARMv7).

Just use apt-get for installation:
```
sudo apt-get install ros-noetic-mavros ros-noetic-mavros-extras
```
Then install GeographicLib datasets by running the *install_geographiclib_datasets.sh* script:
```
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
sudo chmod +x ./install_geographiclib_datasets.sh
```
### Ardupilot Tools Installation
As recommended by Ardupilot (https://ardupilot.org/dev/docs/ros-install.html#installing-mavros)

For ease of use on a desktop computer, please also install RQT:
```
sudo apt-get install ros-noetic-rqt ros-noetic-rqt-common-plugins ros-noetic-rqt-robot-plugins
```
We recommend using caktin_tools instead of the default catkin_make as it is more powerful:
```
sudo apt-get install python3-catkin-tools
```
### Gazebo Installation
We will be using a standard version of ArduPilot but a custom plugin for Gazebo, until the gazebo plugin gets merged into Gazebo-master.

This plugin can be used with or without ROS integration.
```
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'

wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

sudo apt update

sudo apt install gazebo9 libgazebo9-dev
```
The first time gazebo is executed requires the download of some models and it could take some time, so please be patient. Let’s give a try.
```
gazebo --verbose
```
It should open an empty world.
### For the SITL Simulator
First, fork the ardupilot repo, then clone. https://ardupilot.org/dev/docs/building-setup-linux.html

Then install the required packages using:
```
Tools/environment_install/install-prereqs-ubuntu.sh -y
```
Reload the path (log-out and log-in to make permanent):
```
. ~/.profile
```
In a terminal window start Gazebo:
```
gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_demo.world
```
In another terminal window, enter the ArduCopter directory and start the SITL simulation:
```
cd ~/ardupilot/ArduCopter sim_vehicle.py -f gazebo-iris -D --console --map
```

### Connecting Ardupilot with ROS
Launch an SITL instance:
```
cd ~/ardupilot/ArduCopter sim_vehicle.py -f gazebo-iris -D --console --map
```
The next step is to create a new directory for a launch file. In a new terminal, we run these:
```
cd ardupilot
mkdir launch
cd launch
```
We then copy mavros default launch file for ardupilot and then open to edit it:
```
roscp mavros apm.launch apm.launch
gedit apm.launch
```
To connect to SITL we modify the first line to
```
<arg name="fcu_url" default="udp://127.0.0.1:14551@14555" />
```

We save the file and launch it with:
```
roslaunch apm.launch
```

The connection is now complete.

### Troubleshooting
Since GeographicLib requires certain datasets (mainly the geoid dataset) so to fulfill certain calculations, these may be needed to be installed manually by the user. If you run into GeographicLib error, run these:
```
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
chmod +x install_geographiclib_datasets.sh

sudo ./install_geographiclib_datasets.sh
```

Additionally, we can use RQT to see all the topics that mavros has to create from ardupilot information. In a new terminal, type:
```
rqt
```
We can now see all the topics that mavros has to create from ardupilot information.

### Initialization of the Catkin Workspace
We use catkin build instead of catkin_make. Please install the following:
```
sudo apt-get install python-wstool python-rosinstall-generator python-catkin-tools
```
Then, initialize the catkin workspace:
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin init
```
Add a line to end of ~/.bashrc by running the following command:
```
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```
update global variables
```
source ~/.bashrcRu
```
Clone the IQ Simulation ROS Package
```
cd ~/catkin_ws/src
git clone https://github.com/Intelligent-Quads/iq_sim.git
```
Run the following to tell gazebo where to look for the iq models
```
echo "GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:$HOME/catkin_ws/src/iq_sim/models" >> ~/.bashrc
```
Build instructions
Inside catkin_ws, run catkin build:
```
cd ~/catkin_ws
catkin build
```
update global variables
```
source ~/.bashrc
```
# Running the Simulation
Launch the world with the three drones spawned:
```
roslaunch iq_sim multi_drone.launch
```
Launch the three SITL instances, one for each drone

* New Terminal
```
cd ~/ardupilot/ArduCopter sim_vehicle.py -v ArduCopter -f gazebo-drone1 --console -I0
```
* New Terminal
```
cd ~/ardupilot/ArduCopter sim_vehicle.py -v ArduCopter -f gazebo-drone2 --console -I1
```
* New Terminal
```
cd ~/ardupilot/ArduCopter sim_vehicle.py -v ArduCopter -f gazebo-drone3 --console -I2
```
Run the same commands shown above but when running the SITL instances do:
```
sim_vehicle.py -v ArduCopter -f gazebo-drone1 -I0 --out=tcpin:0.0.0.0:8000
sim_vehicle.py -v ArduCopter -f gazebo-drone2 -I1 --out=tcpin:0.0.0.0:8100
sim_vehicle.py -v ArduCopter -f gazebo-drone3 -I2 --out=tcpin:0.0.0.0:8200
sim_vehicle.py -v ArduCopter -f gazebo-drone4 -I3 --out=tcpin:0.0.0.0:8300 
```
For ROS Connection
* New Terminal
```
cd ~/ardupilot_ws roslaunch iq_sim multi-apm.launch
```
Run the script:
* New Terminal
```
cd ~/ardupilot_ws roslaunch iq_gnc multi_square_sol.launch
```
