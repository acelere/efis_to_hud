# Optional instructions for development on Windows

Follow this install guide to get Windows configured properly to enable HUD project development on Windows without requiring an actual Raspberry pi for development.

1- First install Python 2.7.16 or later (do not install the 3.x version).  Install the 32 bit version: 
  
  https://www.python.org/ftp/python/2.7.16/python-2.7.16.msi

2- Second install Pygame:
  
  https://www.pygame.org/wiki/GettingStarted

3- Third install Pyserial by opening a command prompt and typing: 
  
  pip install pyserial

4- Fourth install windows-curses by opening a command prompt and typing:

  pip install windows-curses

5- Clone the HUD project into your local Windows PC:

  git clone https://github.com/dinglewanker/efis_to_hud.git
  
Now it should be possible to follow the normal HUD project directions to run the HUD project within Windows.  You will not need to run the setup.sh script or perform any of the steps required to configure the Raspberry pi since you are using Windows instead.  Be aware of some of the differences in development/running Python in Windows vs Linux.  Example: You don't need to put "sudo" in front of commands in Windows.

NOTE:
In order to run the HUD project on Windows, you will need to use the option hud.cfg file to configure the serial port to use with Windows.  You must select a serial port that is available and not in use.  Find the ports by opening the Windows Device Manager and expanding the 
Ports (COM & LPT) menu item.  Enter the proper COM port selection in the hud.cfg file ie: COM1, COM2, COM6, COM? etc.
