
# python3-iosxe-upgrades
My first python3 script using netmiko to perform IOS-XE software upgrades in a semi-automated fashion.

## Requirements
* Python3
* Netmiko 3.1.0

## Getting Started
First you'll need python3 and netmiko 3.1.0 installed. I use WSL so the commands below are Ubuntu/Debian based.

`sudo apt-get install python3 python3-pip`
`pip3 install netmiko`

Once you have those two done you're ready to go!

## Launching the script
Launch the script  using `python3 iosxe-upgrades.py`. Throughout the script it'll ask you for a few variables:
* Target device IP address
* Username
* Password
* TFTP Server IP
* Image name on TFTP server
* MD5 (expected) hash
* If you want to apply and reboot

## Example output
Username: cisco

Password:

testswitch#


---------- Current System Image ----------

System image file is "flash:packages.conf"

---------- End ----------


TFTP Server IP: 10.10.10.10

TFTP Image File: cat9k_iosxe.16.12.03.SPA.bin

Starting TFTP Transfer, please wait...


----------
Destination filename [cat9k_iosxe.16.12.03.SPA.bin]? Accessing tftp://10.10.10.10/cat9k_iosxe.16.12.03.SPA.bin...

Loading cat9k_iosxe.16.12.03.SPA.bin from 10.10.10.10 (via GigabitEthernet0/0): 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!O!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!O!!!!!O!!!!O!!!!O!!!!!!!!!!!!!!!!!!!O!!!!!!!!!!!!!!!!!!!!!!!!!!!

[OK - 805013186 bytes]

805013186 bytes copied in 98.392 secs (8181693 bytes/sec)



Total time: 0:01:41.961399


Verify File MD5 Hash? (yes or no): yes

Expected MD5 Hash: e578d84cc4bd2f4d1f0cdedbf9bd2604

Verifying MD5 Hash, please wait...

MD5 Hash Successful


Boot system set to packages.conf


Installing file to flash, please wait...
Installed image to flash successfully.



Do you wish to apply the config changes and reboot? (y or n): y

Config Saved.

...

OSError: Socket is closed

The **OSError: Socket is closed** is normal, the switch abruptly kills the connection which causes this, I am working on a way to have that show more cleanly.
