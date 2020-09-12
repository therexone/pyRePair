""" 
Python script to remove and re-pair a bluetooth device 
after reboot on Linux
"""

from PyBluetoothctl import PyBluetoothctl
import time

# Set your MAC address here
mac_address = 'FC:58:FA:68:94:7F'

# Timeout period for scanning in seconds
timeout = 10


if __name__ == '__main__':
    pair_success = False
    max_tries = 3
    while not pair_success:
        print(f'Initialising pyRePair\n Device address set as {mac_address}')
        bt = PyBluetoothctl()

        # start the scan
        bt.start_scan()

        # get paired devices
        devices = bt.get_paired_devices()

        device_already_paired = False

        # check for target devices in paired devices
        for device in devices:
            if device['mac_address'] == mac_address:
                print(f'Device {device} is already paired, removing...\n')
                device_already_paired = True
                break
        # remove the device if it is paired
        if(device_already_paired):
            removed = bt.remove(mac_address)
            time.sleep(1)
            print(f'Device: {mac_address} removed') if removed else print(
                'Failed to remove device')
        else:
            print('Device is not paired')

        # search for the device
        print('Looking for devices....\n')

        device_found_after_scan = False

        t_end = time.time() + timeout
        while(device_found_after_scan is False):
            
            discoverable_devices = bt.get_discoverable_devices()
            print(f'{len(discoverable_devices)} devices found')
            
            for device in discoverable_devices:
                if device['mac_address'] == mac_address:
                    print(f'Device {mac_address} found!, Trying to connect...')
                    device_found_after_scan = True
            if time.time() > t_end:
                break

        # pair and connect with the device
        if(device_found_after_scan):
            print('Trying to pair...')
            pair_success = bt.pair(mac_address)
            if pair_success:
                print('Pair Success! Connecting...')
                connect_success = bt.connect(mac_address)
                print('Connected Succesfully!') if connect_success else print(
                    'Failed to connect!')
        else:
            print('Device not found after scanning')
            
        max_tries -= 1
