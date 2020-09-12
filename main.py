from PyBluetoothctl import PyBluetoothctl
import time

# Set your MAC address here

mac_address = 'FC:58:FA:68:94:7F'
 
 
if __name__ == '__main__':
    print('Initialising pyRePair')
    bt = PyBluetoothctl()
    
    # start the scan
    bt.start_scan()
    
    # get paired devices
    devices = bt.get_paired_devices()
    
    device_already_paired = False
    
    # check for target devices in paired devices
    for device in devices:
        if device['mac_address'] == mac_address:
            print(f'Device {device} is already paired, removing...')
            device_already_paired = True
            break
    # remove the device if it is paired
    if(device_already_paired):
        removed = bt.remove(mac_address)
        time.sleep(1)
        print('Device removed') if removed else print('Failed to remove device')
    else:
        print('Device is not paired')
    
    # search for the device
    discoverable_devices = bt.get_discoverable_devices()
    print('Looking for devices....')
    print(discoverable_devices)
    
    device_found_after_scan = False
    for device in discoverable_devices:
        if device['mac_address'] == mac_address:
            print('Device found!')
            device_found_after_scan = True 
            
    # pair and connect with the device
    if(device_found_after_scan):
        pair_success = bt.pair(mac_address)
        if pair_success:
            connect_success = bt.connect(mac_address)
            print('Connected Succesfully!') if connect_success else print('failed to connect!')
    else: 
        print('Device not found after scanning')
            
            
    
        
    
        
        
 