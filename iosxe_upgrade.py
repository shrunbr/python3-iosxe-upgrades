# Author: shrunbr
# Creation Date: 2020.04.10

from datetime import datetime
from netmiko import Netmiko, file_transfer
import getpass
import sys

device = input("Device IP: ")
user = input("Username: ")
user_pass = getpass.getpass("Password: ")

net_connect = Netmiko(
    host=device,
    username=user,
    password=user_pass,
    device_type="cisco_ios",
    global_delay_factor=2,
)

# Make sure connection is established
print(net_connect.find_prompt())

# Get current IOS/IOS-XE image
current_image = net_connect.send_command("show version | i image")
print(f"\n\n---------- Current System Image ----------")
print(current_image)
print(f"---------- End ----------")
print("\n")
# Copy file to device via TFTP
tftp_server = input("TFTP Server IP: ")
tftp_image = input("TFTP Image File: ")
tftp_transfer = f"copy tftp://{tftp_server}/{tftp_image} flash:"

starttime = datetime.now()
print("Starting TFTP Transfer, please wait...")
transfer_output = net_connect.send_command(
    tftp_transfer,
    expect_string=r'Destination filename'
)
transfer_output += net_connect.send_command('\n', expect_string=r'#')
end_time = datetime.now()

print("\n")
print("-" * 10)
print(transfer_output)
print("-" * 10)
print("\n")
print("Total time: {}".format(end_time - starttime))
print("\n")

# Verify transfered file MD5 hash
verify_md5 = input("Verify File MD5 Hash? (yes or no): ")

if "yes" in verify_md5:
    md5_hash = input("Expected MD5 Hash: ")
    verify_md5_cmd = f"verify /md5 flash:{tftp_image} {md5_hash}"
    print("Verifying MD5 Hash, please wait...")
    verify_output = net_connect.send_command(verify_md5_cmd)
    if "Verified" in verify_output:
        print("MD5 Hash Successful")
    else:
        print("MD5 Hash Failed")
        exit()
if "no" in verify_md5:
    pass
print("\n")
# Set boot system to packages.conf
bootsystem_cmd = "boot system flash:packages.conf"
bootsystem_check = "show boot system"

net_connect.send_config_set(bootsystem_cmd)
verify_bootsystem = net_connect.send_command(bootsystem_check)
if "flash:packages.conf" in verify_bootsystem:
    print("Boot system set to packages.conf")
else:
    print("Setting boot system failed!")
    exit()
print("\n")
# Install image to flash
print("Installing file to flash, please wait...")
request_platform = f"request platform software package install switch all file flash:{tftp_image}"
request_plaform_output = net_connect.send_command(request_platform)
if "SUCCESS" in request_plaform_output:
    print("Installed image to flash successfully.")
else:
    print("Failed to install image to flash!")
    exit()
print("\n")

# Reboot to apply image
confirm_continue = input("Do you wish to apply the config changes and reboot? (y or n): ")
if "y" in confirm_continue:
    reload_cmd = "reload"
    write_cmd = "wr"
    net_connect.send_command(write_cmd, expect_string=r'#')
    print("Config Saved.")
    print("Device reloading... Check manually after reload with 'show version' command.")
    net_connect.send_command(reload_cmd, expect_string='confirm')
    net_connect.send_command('\n')
if "n" in confirm_continue:
    print("Script exiting...")
    net_connect.disconnect()
    exit()

net_connect.disconnect()