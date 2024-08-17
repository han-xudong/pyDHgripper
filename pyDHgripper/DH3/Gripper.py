# -*- coding=utf-8 -*-

# ------------------------------------------------------------------
# File Name:        Gripper.py
# Author:           Jie Yu, Han Xudong
# Version:          1.0.1
# Created:          2022/08/09
# Description:      This is a class to control DH3 grippers.
# Function List:    in_range: Check if the value is in the range.
#                   Gripper: Gripper class to control DH3 grippers.
# History:
#       <author>        <version>       <time>      <desc>
#       Jie Yu          1.0.0           2022/08/09  Created file
#       Han Xudong      1.0.1           2024/08/17  Modified the file
# ------------------------------------------------------------------

import serial
import time
import crcmod

def in_range(val, 
             val_min, 
             val_max):
    '''Check if the value is in the range.
    
    Args:
        val: The value to be checked.
        val_min: The minimum value.
        val_max: The maximum value.
        
    Raises:
        RuntimeError: If the value is out of range.
    '''

    if not val_min <= val <= val_max:
        raise RuntimeError('!!! VALUE IS OUT OF RANGE !!!')

class Gripper(object):
    def __init__(self, 
                 port="/dev/ttyUSB0") -> None:
        '''Initialize the gripper.
        
        Args:
            port: The port of the gripper.

        Returns:
            None
        '''

        # Initialize the serial port
        self.ser = serial.Serial(port=port, 
                                 baudrate=115200)
        # Initialize the CRC
        self.crc16 = crcmod.mkCrcFun(0x18005, 
                                     rev=True, 
                                     initCrc=0xFFFF, 
                                     xorOut=0x0000)
        # Initialize the gripper
        self.init_state()

    def cal_crc(self, 
                array):
        '''Calculate the CRC.
        
        Args:
            array: The array to be calculated.
            
        Returns:
            crc_l: The low value of the CRC.
            crc_h: The high value of the CRC.
        '''

        bytes_ = b''
        for i in range(len(array)):
            bytes_ = bytes_ + array[i].to_bytes(1, 
                                                byteorder='big', 
                                                signed=True)
        crc = self.crc16(bytes_).to_bytes(2, 
                                          byteorder='big', 
                                          signed=False)
        crc_h = int.from_bytes(crc[0:1], 
                              byteorder='big', 
                              signed=False)
        crc_l = int.from_bytes(crc[1:2], 
                              byteorder='big', 
                              signed=False)
        return crc_l, crc_h

    def read_uart(self):
        '''Read the data from the serial port.

        Args:
            None
        
        Returns:
            udata: The data read from the serial port.
        '''

        time.sleep(0.08)
        udata = self.ser.read_all()
        return udata
    
    def write_uart(self, 
                   modbus_high_addr, 
                   modbus_low_addr, 
                   val=0x01, 
                   is_set=True, 
                   is_read=True):
        '''Send the command to the gripper.

        Args:
            modbus_high_addr: The high address of the modbus.
            modbus_low_addr: The low address of the modbus.
            val: The value to be set.
            is_set: If the value is to be set.
            is_read: If the value is to be read.

        Returns:
            data: The data read from the serial port.
        '''

        # Set the address
        if is_set:
            set_addr = 0x01
        else:
            set_addr = 0x00

        # Set the command
        cdata = [0xFF, 
                 0xFE, 
                 0xFD, 
                 0xFC, 
                 0x01, 
                 modbus_high_addr, 
                 modbus_low_addr, 
                 set_addr, 
                 0x00, 
                 (val >> 24) & 0xFF,   
                 (val >> 16) & 0xFF, 
                 (val >> 8) & 0xFF, 
                 val & 0xFF, 
                 0xFB]
        for i in range(len(cdata)):
            cdata[i] = cdata[i] if cdata[i] >= 0 else cdata[i] + 256
        # Write the data
        self.ser.write(cdata)

        # Read the data
        if is_read:
            udata = self.read_uart()
            data = int.from_bytes(udata[3:5], 
                                  byteorder='big', 
                                  signed=True)
            if data < 0:
                data = data + 1
            self.ser.flush()
            return data
        else:
            time.sleep(0.01)
            return
        
    def init_feedback(self):
        '''Initialize the feedback.
        
        Args:
            None
            
        Returns:
            None
        '''

        self.write_uart(modbus_high_addr=0x08, 
                        modbus_low_addr=0x01, 
                        val=-1)
        
    def init_state(self):
        '''Initialize the gripper.
        
        Args:
            None
            
        Returns:
            None
        '''

        self.write_uart(modbus_high_addr=0x08, 
                        modbus_low_addr=0x02, 
                        val=0)

    def read_open_force(self):
        '''Read the force.
        
        Args:
            None
            
        Returns:
            force: The force value.
        '''

        force = self.write_uart(modbus_high_addr=0x05, 
                                modbus_low_addr=0x02, 
                                is_set=False)
        return force

    def set_open_force(self, 
                       val):
        '''Set the force.
        
        Args:
            val: The force value.
            
        Returns:
            None
        '''

        in_range(val, 
                 val_min=10, 
                 val_max=90)
        self.write_uart(modbus_high_addr=0x05, 
                        modbus_low_addr=0x02, 
                        val=val)
        
    def read_close_force(self):
        '''Read the force.
        
        Args:
            None
            
        Returns:
            force: The force value.
        '''

        force = self.write_uart(modbus_high_addr=0x05, 
                                modbus_low_addr=0x03, 
                                is_set=False)
        return force
    
    def set_close_force(self,
                        val):
        '''Set the force.
        
        Args:
            val: The force value.
            
        Returns:
            None
        '''

        in_range(val, 
                 val_min=10, 
                 val_max=90)
        self.write_uart(modbus_high_addr=0x05, 
                        modbus_low_addr=0x03, 
                        val=val)
        
    def read_pos(self):
        '''Read the position.
        
        Args:
            None
            
        Returns:
            pos: The position value.
        '''

        pos = self.write_uart(modbus_high_addr=0x06, 
                              modbus_low_addr=0x02, 
                              is_set=False)
        return pos

    def set_pos(self, 
                val,
                blocking=True):
        '''Set the position.

        Args:
            val: The position value.
            blocking: Blocking mode.

        Returns:
            None
        '''

        in_range(val, 
                 val_min=0, 
                 val_max=95)
        self.write_uart(modbus_high_addr=0x06, 
                        modbus_low_addr=0x02, 
                        val=val)
        if blocking:
            while True:
                curr_pos = self.read_pos()
                if curr_pos == val:
                    break
        
    def read_ang(self):
        '''Read the angle.
        
        Args:
            None
            
        Returns:
            ang: The angle value.
        '''

        ang = self.write_uart(modbus_high_addr=0x07, 
                              modbus_low_addr=0x02, 
                              is_set=False)
        return ang

    def set_ang(self, 
                val,
                blocking=True):
        '''Set the angle.

        Args:
            val: The angle value.
            blocking: Blocking mode.

        Returns:
            None
        '''
        in_range(val, 
                 val_min=0, 
                 val_max=100)
        self.write_uart(modbus_high_addr=0x07, 
                        modbus_low_addr=0x02, 
                        val=val)
        
        if blocking:
            while True:
                curr_ang = self.read_ang()
                if curr_ang == val:
                    break
        
    def read_state(self):
        '''Read the state.
        
        Args:
            None
            
        Returns:
            state: The state value.
        '''

        state = self.write_uart(modbus_high_addr=0x0F, 
                                modbus_low_addr=0x01, 
                                is_set=False)
        return state


if __name__ == "__main__":
    gripper = Gripper(port="/dev/ttyUSB0")
    time.sleep(0.2)
    gripper.set_pos(50)
