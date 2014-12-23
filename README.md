After registering a new RHEL box with RHN, its a long process disabling and enabling 
repositories manually by running subscription manager one by one.

This script automates the process so you can indicate multiple repositories

We use the subscription-manager command to mass-enable or mass-disable yum repositories/sofware channels.
Useful for RHEL 6, 7 based systems registered with Red Hat RHN using the certificate system.
Requires Python 3 and above.

*Remember to change to your python 3 version number on top of the script file



