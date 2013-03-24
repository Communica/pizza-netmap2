## switch simulator.

The simplest form of simulating the nms provided switch status list, is to have a static
file with switch status. It is made by make-switches.py and with logic cut from planning.cpp and transformed to python. 

To make a static file, run:

shellprompt >  ./make-switches.py > switchlist.txt

This will give a txtfile of the format:
...
e69-2 on
e69-3 on
e69-4 on
e71-1 on
e71-2 on
e71-3 on
e71-4 on
e73-1 off
e73-2 off
e73-3 off
e73-4 off
e75-1 on
e75-2 on
e77-1 on
e77-2 on
... 


This is the same as will be given from the nms perl script. 