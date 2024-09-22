pyDHgripper: Control DH Gripper with Python
===========================================

Description
-----------

PyDHgripper is a Python library that allows you to control the DH
gripper with Python. The DH grippers are a series of robot grippers
which is widely used in grasping tasks. This library is based on the
Modbus protocol, and the support types of DH gripper includes AG-95,
DH-3, RGD, and PGE series.

Hardware Requirements
---------------------

-  DH gripper
-  USB-to-RS485 converter
-  24V DC power supply

Here is a connection example for AG-95 gripper

Installation
------------

The ``pyDHgripper`` library supports Python 2.x and Python 3.x. You can
install the library using the following command:

.. code:: bash

   pip install pydhgripper

Or you can install the library from the source code:

.. code:: bash

   git clone https://github.com/han-xudong/pyDHgripper.git
   cd pyDHgripper
   pip install pip -U
   pip install -r requirements.txt

Quick Start
-----------

For Linux, it's needed to set the serial port permission first:

.. code:: bash

   sudo chmod 777 /dev/ttyUSB0
   # For CTS-B1.0,
   # sudo chmod 777 /dev/ttyACM0
   sudo usermod -aG dialout {userName}
   reboot

Several types of DH grippers can be controlled with ``pyDHgripper``. For
example, to control the AG-95 gripper:

.. code:: python

   from pydhgripper import AG95

   gripper = AG95(port='/dev/ttyUSB0')

And here are some functions that can be used to control the gripper:

-  ``read_state``: Read the state of the gripper.

.. code:: python

   gripper.read_state()

-  ``read_pos``: Read the position of the gripper.

.. code:: python

   gripper.read_pos()

-  ``set_force``: Set the force of the gripper.

.. code:: python

   gripper.set_force(val='{FORCE}')

-  ``set_pos``: Set the position of the gripper.

.. code:: python

   gripper.set_pos(val='{POSITION}')

-  ``set_vel``: Set the velocity of the gripper.

.. code:: python

   gripper.set_vel(val='{VELOCITY}')

For more functions, please refer to the source code.

License and Acknowledgement
---------------------------

PyDHgripper is licensed under the MIT License.

Some core codes are developed based on
`DaHuan-FingerControl <https://github.com/FrankJIE09/DaHuan-FingerControl>`__
by Frank.

The DH grippers are developed by DH Robotics. For more information,
please refer to the `DH Robotics
website <http://en.dh-robotics.com/>`__.
