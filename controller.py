# -*- coding: UTF-8 -*-


"""Открываем Serial port на пинах RxD и TxD, предварительно прописываем в terminal RaspberryPi 3B+:
            $ sudo systemctl stop serial-getty@ttyS0.service
            $ sudo systemctl disable serial-getty@ttyS0.service	
            $ sudo nano /boot/cmdline.txt
   Убираем строчку console=serial0,11520 в config строке загрузки:
            dwc_otg.lpm_enable=0 '>console=serial0,11520<' console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 
            elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
   чтобы очистить порт от Bluetooth
   
   backup:
            console=serial0,115200 console=tty1 root=PARTUUID=97709164-02 rootfstype=ext4 elevator=deadline 
            fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles

    # fm0 = [0xAA, 0x0A, 0x0B, 0x7f]
    # fm1 = [0xAA, 0x0A, 0x0D, 0x7f]
    # fm0_0 = [0xAA, 0x0A, 0x0B, 0x00]
    # fm1_0 = [0xAA, 0x0A, 0x0D, 0x00]
    # rm0 = [0xAA, 0x0A, 0x09, 0x7f]
    # rm1 = [0xAA, 0x0A, 0x0F, 0x7f]
    # rm0_0 = [0xAA, 0x0A, 0x09, 0x00]
    # rm1_0 = [0xAA, 0x0A, 0x0F, 0x00]
    # brake0 = [0xAA, 0xAA, 0x06, 0x7f]
    # brake1 = [0xAA, 0xAA, 0x07, 0x7f]
"""
import serial


class Controller:
    def __init__(self, pin: str, x_coord: int, y_coord: int):

        self.right_motor_hex_string = list()
        self.left_motor_hex_string = list()
        self.motor_speed = 0
        self.twist_speed = 0

        self.pin = pin
        self.x = x_coord
        self.y = y_coord

        self.zero_x = 127
        self.zero_y = 127

        self.extra_speed = 0

        self.timeout = 0.5
        self.write_timeout = 0
        self.s = serial.Serial(port='/dev/ttyS0',
                               baudrate=9600,
                               bytesize=serial.EIGHTBITS,
                               write_timeout=0)
        self.run()

    def forward_move(self):
        if self.y > self.zero_y or (self.y == self.zero_y and (self.x < self.zero_x < self.x)):
            print("Forward move")

            self.motor_speed = self.y - 127
            if self.y >= 217:
                self.motor_speed = 127
            elif 217 >= self.y > self.zero_y and (self.x <= 37 or self.x >= 217):
                self.motor_speed = 127

            if self.x < self.zero_x:
                self.twist_speed = self.zero_x - self.x  # left
                if self.y == self.zero_y:
                    self.motor_speed = self.twist_speed

                self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                self.left_motor_hex_string.append(self.motor_speed - self.twist_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                self.right_motor_hex_string.append(self.motor_speed)

            elif self.x > self.zero_x:
                self.twist_speed = self.x - self.zero_x  # right
                if self.y == self.zero_y:
                    self.motor_speed = self.twist_speed

                self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                self.right_motor_hex_string.append(self.motor_speed - self.twist_speed)

            else:
                self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                self.right_motor_hex_string.append(self.motor_speed)

        else:
            self.motor_speed = 0
            print("Stop")
            self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
            self.left_motor_hex_string.append(self.motor_speed)

            self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
            self.right_motor_hex_string.append(self.motor_speed)

        print("Speed: ", self.motor_speed)

    def reverse_move(self):
        if self.y < self.zero_y:  # or (self.y == self.zero_y and (self.x < self.zero_x < self.x)):
            print("Reverse move")

            self.motor_speed = 127 - self.y
            if self.y <= 37:
                self.motor_speed = 127
            elif 37 <= self.y < self.zero_y and (self.x <= 37 or self.x >= 217):
                self.motor_speed = 127

            if self.x < self.zero_x:
                self.twist_speed = self.zero_x - self.x  # left
                if self.y == self.zero_y:
                    self.motor_speed = self.twist_speed

                self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                self.right_motor_hex_string.append(self.motor_speed - self.twist_speed)

            elif self.x > self.zero_x:
                self.twist_speed = self.x - self.zero_x  # right
                if self.y == self.zero_y:
                    self.motor_speed = self.twist_speed

                self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                self.left_motor_hex_string.append(self.motor_speed - self.twist_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                self.right_motor_hex_string.append(self.motor_speed)

            else:
                self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                self.right_motor_hex_string.append(self.motor_speed)

        else:
            self.motor_speed = 0
            print("Stop")
            self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
            self.left_motor_hex_string.append(self.motor_speed)

            self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
            self.right_motor_hex_string.append(self.motor_speed)

        print("Speed: ", self.motor_speed)

    def run(self):
        try:
            if self.y >= self.zero_y:
                self.forward_move()
            else:
                self.reverse_move()

        except Exception as e:
            print("WARNING1: ", e)
        finally:
            self.twister_bister(self.left_motor_hex_string, self.right_motor_hex_string)

    def twister_bister(self, left, right):
        try:
            if not self.s.isOpen():
                self.s.open()
                self.s.write(bytes(left))
                print("Serial: ", self.s.read())
                self.s.write(bytes(right))
                print("Serial: ", self.s.read())
                self.s.close()
            else:
                self.s.write(bytes(left))
                self.s.write(bytes(right))
                self.s.close()
        except Exception as e:
            print("WARNING2: ", e)


