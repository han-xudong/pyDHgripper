# -*- coding=utf-8 -*-

# ------------------------------------------------------------------
# File Name:        Gripper.py
# Author:           Han Xudong
# Version:          1.0.0
# Created:          2024/08/17
# Description:      This is a class to control RGD grippers.
# Function List:    in_range: Check if the value is in the range.
#                   Gripper: Gripper class to control RGD grippers.
# History:
#       <author>        <version>       <time>      <desc>
#       Han Xudong      1.0.0           2024/08/17  Created file
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
            set_addr = 0x06
        else:
            set_addr = 0x03
        
        # Set the value
        val = val if val >= 0 else val - 1
        bytes_ = val.to_bytes(2, 
                              byteorder='big', 
                              signed=True)
        val_l = int.from_bytes(bytes_[0:1], 
                               byteorder='big', 
                               signed=True)
        val_h = int.from_bytes(bytes_[1:2], 
                               byteorder='big', 
                               signed=True)
        crc_l, crc_h = self.cal_crc([0x01, 
                                     set_addr, 
                                     modbus_high_addr, 
                                     modbus_low_addr, 
                                     val_l, 
                                     val_h])
        # Set the command
        cdata = [0x01, 
                 set_addr, 
                 modbus_high_addr, 
                 modbus_low_addr, 
                 val_l, 
                 val_h,
                 crc_l,
                 crc_h]
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
            time.sleep(0.005)
            return

    def init_state(self):
        '''Initialize the gripper.

        Args:
            None
        
        Returns:
            None
        '''

        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x00, 
                        val=165)

    def set_force(self, 
                  val):
        '''Set the force of the gripper.
        
        Args:
            val: The value to be set.
            
        Returns:
            None
        '''

        in_range(val, 
                 val_min=20, 
                 val_max=100)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x01, 
                        val=val)

    def set_pos(self, 
                val, 
                blocking=True):
        '''Set the position of the gripper.
        
        Args:
            val: The value to be set.
            blocking: Blocking mode.
            
        Returns:
            None
        '''

        in_range(val, 
                 val_min=0, 
                 val_max=1000)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x03, 
                        val=val)

        if blocking:
            while True:
                current_position = self.write_uart(modbus_high_addr=0x02, 
                                                   modbus_low_addr=0x02,
                                                   is_set=False)
                if current_position == val:
                    break
                time.sleep(0.01)

    def set_vel(self, 
                val):
        '''Set the velocity of the gripper.

        Args:
            val: The value to be set.

        Returns:
            None
        '''

        in_range(val, 
                 val_min=1, 
                 val_max=100)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x04, 
                        val=val)

    def set_abs_rot(self, 
                    val):
        '''Set the absolute rotation angle of the gripper.

        Args:
            val: The value to be set.

        Returns:
            None
        '''

        in_range(val, 
                 val_min=-32768, 
                 val_max=32767)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x05, 
                        val=val,
                        is_read=False)

    def set_rot_vel(self, 
                    val):
        '''Set the rotation force of the gripper.
        
        Args:
            val: The value to be set.
            
        Returns:
            None
        '''

        in_range(val, 
                 val_min=1, 
                 val_max=100)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x07, 
                        val=val,
                        is_read=False)

    # 设置旋转力值
    def set_rot_force(self, 
                      val):
        in_range(val, 
                 val_min=20, 
                 val_max=100)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x08, 
                        val=val)

    def set_rel_rot(self, val):
        '''Set the relative rotation angle of the gripper.

        Args:
            val: The value to be set.

        Returns:
            None
        '''

        in_range(val, 
                 val_min=-32768, 
                 val_max=32767)
        self.write_uart(modbus_high_addr=0x01, 
                        modbus_low_addr=0x09, 
                        val=val)
        
    def init_feedback(self):
        '''Initialize the feedback.

        Args:
            None

        Returns:
            None
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x00, 
                                is_set=False)
        while rdata == 0:
            self.init_state()
            rdata = self.write_uart(modbus_high_addr=0x02, 
                                    modbus_low_addr=0x00, 
                                    is_set=False)
        while rdata == 2:
            time.sleep(0.1)
            rdata = self.write_uart(modbus_high_addr=0x02, 
                                    modbus_low_addr=0x00, 
                                    is_set=False)


    def read_state(self):
        '''Read the state of the gripper.

        Args:
            None

        Returns:
            rdata: The data read from the serial port.
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x01, 
                                is_set=False)
        return rdata

    def read_pos(self):
        '''Read the position of the gripper.

        Args:
            None

        Returns:
            rdata: The data read from the serial port.
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x02, 
                                is_set=False)
        return rdata
    
    def read_cur(self):
        '''Read the current of the gripper.

        Args:
            None

        Returns:
            rdata: The data read from the serial port.
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x04, 
                                is_set=False)
        return rdata
    
    def read_err(self):
        '''Read the error of the gripper.

        Args:
            None

        Returns:
            rdata: The data read from the serial port.
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x05, 
                                is_set=False)
        return rdata
    
    def read_rot(self):
        '''Read the rotation angle of the gripper.

        Args:
            None

        Returns:
            rdata: The data read from the serial port.
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x08, 
                                is_set=False)
        return rdata
    
    def init_rot_feedback(self):
        '''Initialize the rotation feedback.

        Args:
            None

        Returns:
            None
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x0A, 
                                is_set=False)
        while rdata == 0:
            self.init_state()
            rdata = self.write_uart(modbus_high_addr=0x02, 
                                    modbus_low_addr=0x0A, 
                                    is_set=False)
        while rdata == 2:
            time.sleep(0.1)
            rdata = self.write_uart(modbus_high_addr=0x02, 
                                    modbus_low_addr=0x0A, 
                                    is_set=False)
            
    def read_rot_state(self):
        '''Read the rotation state of the gripper.

        Args:
            None

        Returns:
            rdata: The data read from the serial port.
        '''

        rdata = self.write_uart(modbus_high_addr=0x02, 
                                modbus_low_addr=0x0B, 
                                is_set=False)
        return rdata
    
    def init_dir(self,
                 val):
        '''Initialize the direction.

        Args:
            val: The value to be set.
            0 is open, 1 is close.

        Returns:
            None
        '''

        self.write_uart(modbus_high_addr=0x03, 
                        modbus_low_addr=0x01, 
                        val=val)

if __name__ == "__main__":
    gripper = Gripper(port="/dev/ttyUSB0")
    time.sleep(0.2)
    gripper.set_pos(800)

