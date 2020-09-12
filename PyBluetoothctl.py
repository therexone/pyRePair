""" 
Python script to remove and re-pair a bluetooth device 
after reboot in debian based distros
"""
# https://gist.github.com/egorf/66d88056a9d703928f93

import time
import pexpect 
import subprocess

class PyBluetoothctl: 
    
    def __init__(self):
        # Make sure bluetooth card is unblocked and spawn bluetoothctl
        output = subprocess.run(['rfkill', 'unblock', 'bluetooth' ], capture_output=True)
        self.bctl_prompt = pexpect.spawn("bluetoothctl", echo=False, encoding="utf-8")
        
    def get_output(self, command, pause=1):
        """ Run a command in bluetoothctl prompt, return output as a list of lines."""
        
        self.bctl_prompt.sendline(command)
        time.sleep(pause)
        start_failed = self.bctl_prompt.expect(['bluetooth', pexpect.EOF])
        
        if start_failed:
            raise Exception('Bluetooth failed to start')
        
        
        return self.bctl_prompt.before.split('\r\n')
    
    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except Exception as e:
            print(e)
            return None
        
    def make_discoverable(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except Exception as e:
            print(e)
            return None
        
    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device
    
    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices", 5)
        except Exception as e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices
        
    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except Exception as e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices
        
    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output("info " + mac_address)
        except Exception as e:
            print(e)
            return None
        else:
            return out
    
    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            out = self.get_output("pair " + mac_address, 4)
        except Exception as e:
            print(e)
            return None
        else:
            res = self.bctl_prompt.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success
    
    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + mac_address, 3)
        except Exception as e:
            print(e)
            return None
        else:
            res = self.bctl_prompt.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success
        
    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except Exception as e:
            print(e)
            return None
        else:
            res = self.bctl_prompt.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success