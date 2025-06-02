# Client for Sensor2OSC 

Theres an interesting app that i have found on F-Droid called Sensor2OSC, it streams data over UDP.
Of various sensors in an android device.

Here an Client script i have made for it although with some certain issues it works
I definately come back to this when i get time, as this can be a backbone for various projects.


> Make sure that (remote device) sensor is sending data to current host with correct ip
> And Listen on correct and configured UDP Port on the HOST Device

```bash
# Getting Started

$ python3 main.py

```

Note to self (a slight blunder).

- Unread UDP Datagram bytes are discarded as they arent buffered by kernel as in TCP.
- recvfrom (for sender socket address).

Next Up.

- Handler for each sensor.
- a simple POC applications.


# References

- [Sensor2OSC](https://sensors2.org/osc/)
