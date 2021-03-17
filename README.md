# WALL-E
Raspberry Pi + Blynk app + 2 Motors + 2 Leds + Pololu controller + Battery + 3 сhips and some wires = wall_e

## Pic

![pic 1](https://github.com/AvEgA-ChuDoTvoreC/wall_e/blob/main/pic/pos1.jpg)
![pic 2](https://github.com/AvEgA-ChuDoTvoreC/wall_e/blob/main/pic/pos2.jpg)

## Installation

Raspberry Pi set up:

```bash
$ sudo apt-get install python-virtualenv
$ virtualenv walle --python=python3.7

$ git clone https://github.com/AvEgA-ChuDoTvoreC/wall_e.git
$ cd wall_e
$ pip install -r requirements.txt
$ python robot_move.py
```

## Schemas, Diagrams and Connections

Schema below will help to understand the way to set up joystick via code:

![joystick_diagram](https://github.com/AvEgA-ChuDoTvoreC/wall_e/blob/main/pic/joystick_diagram.jpg)