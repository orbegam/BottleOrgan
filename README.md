# BottleOrgan
The code for the bottle organ project in GeekCon 2019

https://youtu.be/hZUGD56VnGA

## Setup
The PC running this code should be connected to:
1. A MIDI Device
2. An Arduino loaded with the StandardFirmata sketch

The **servo_config.json** file contains the pin number, mute angle and play angle for each MIDI note.

The following python packages are required:
 ```
 pip install pyfirmata
 pip install pygame
 ```
 
## Usage

```
python geekcon.py
```
