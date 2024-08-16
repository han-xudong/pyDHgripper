# pyDHgripper: Control DH Gripper with Python

## Description

PyDHgripper is a python library that allows you to control the DH gripper with Python. The DH gripper is a kind of robot gripper. It is widely used in the field of robot control. This project is based on the serial communication protocol of the DH gripper. The types of DH gripper controlled with this library includes AG-95, DH-3, and PGE series.

## Hardware Requirements

- DH Gripper
- Serial Communication Device

## Installation

The `pyDHgripper` library supports Python 2.x and Python 3.x. You can install the library using the following command:

```bash
git clone https://github.com/han-xudong/pyDHgripper.git
cd pyDHgripper
pip install pip -U
pip install -r requirements.txt
```

## Quick Start

For Linux, it's needed to set the serial port permission first:

```bash
sudo chmod 777 /dev/ttyUSB0
# For communication box, sudo chmod 777 /dev/ttyACM0
sudo usermod -aG　dialout {userName}
reboot
```

Here are three types of DH grippers that can be controlled with `pyDHgripper`. For example, to control the AG-95 gripper:

```python
from pyDHgripper import AG95

gripper = AG95(port='/dev/ttyUSB0')
```

And here are some functions that can be used to control the gripper:

- `read_state`: Read the state of the gripper.

```python
gripper.read_state()
```

- `read_pos`: Read the position of the gripper.

```python
gripper.read_pos()
```

- `set_force`: Set the force of the gripper.

```python
gripper.set_force(val='{FORCE}')
```

- `set_pos`: Set the position of the gripper.

```python
gripper.set_pos(val='{POSITION}')
```

- `set_vel`: Set the velocity of the gripper.

```python
gripper.set_vel(val='{VELOCITY}')
```

For more functions, please refer to the source code.

## License and Acknowledgement

PyDHgripper is licensed under the MIT License.

The DH grippers are developed by DH Robotics. For more information, please refer to the [DH Robotics website](http://en.dh-robotics.com/).
