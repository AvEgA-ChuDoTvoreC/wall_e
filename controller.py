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

        self.timeout = 0.5
        self.write_timeout = 0
        self.s = serial.Serial(port='/dev/ttyS0',
                               baudrate=9600,
                               bytesize=serial.EIGHTBITS,
                               write_timeout=0)

    def forward_move(self):
        if self.y > 127 or (self.y == 0 and (self.x < 127 < self.x)):
            print("Forward move")
            self.motor_speed = self.y - 127

            if self.x < 127:
                self.twist_speed = 127 - self.x  # left
                self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                self.left_motor_hex_string.append(self.motor_speed - self.twist_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                self.right_motor_hex_string.append(self.motor_speed)

            elif self.x > 127:
                self.twist_speed = self.x - 127  # right
                self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                self.right_motor_hex_string.append(self.motor_speed - self.twist_speed)

            else:
                self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                self.right_motor_hex_string.append(self.motor_speed)

    def reverse_move(self):
        if self.y < 127:
            print("Reverse move")
            self.motor_speed = 127 - self.y

            if self.x < 127:
                self.twist_speed = 127 - self.x  # left
                self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                self.right_motor_hex_string.append(self.motor_speed - self.twist_speed)

            elif self.x > 127:
                self.twist_speed = self.x - 127  # right
                self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                self.left_motor_hex_string.append(self.motor_speed - self.twist_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                self.right_motor_hex_string.append(self.motor_speed)

            else:
                self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                self.left_motor_hex_string.append(self.motor_speed)

                self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                self.right_motor_hex_string.append(self.motor_speed)

    def run(self):
        try:
            self.forward_move()
            self.reverse_move()

        except Exception as e:
            print("WARNING: ", e)
        finally:
            self.twister_bister(self.left_motor_hex_string, self.right_motor_hex_string)

    def twister_bister(self, left, right):
        if not self.s.isOpen():
            self.s.open()
            self.s.write(bytes(left))
            self.s.write(bytes(right))
            self.s.close()
        else:
            self.s.write(bytes(left))
            self.s.write(bytes(right))
            self.s.close()


