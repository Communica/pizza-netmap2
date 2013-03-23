pizza-netmap2
=============

![A netmap in a pizzabox!](http://technocake.net/screenshots/pizzamap.jpg)

Pizza net map is a computer network monitoring device, inside a pizza box. 

We want to make a miniature model of The Gathering network. Participants access the network through switches and access points. We will monitor these and represent their status using LED lights on the model.

Our challenge is to make a modular system that is not limited to one application, but is flexible and can be applied to other networks, not necessarily computer networks.

We achieve this by using an Arduino and shift-registers to control an unlimited amount of LEDs and layouts. 

Our software communicates with an Arduino through a USB connection. A computer checks with the existing Network Management System to see which network access switches are online or not. Based on this data the computer turns a corresponding LED on or off.




