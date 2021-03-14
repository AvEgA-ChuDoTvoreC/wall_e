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
        self.pin = pin
        self.twist_speed = 0
        self.right_motor_hex_string = list()
        self.left_motor_hex_string = list()

        self.timeout = 0.5
        self.write_timeout = 0
        self.s = serial.Serial(port='/dev/ttyS0',
                               baudrate=9600,
                               bytesize=serial.EIGHTBITS,
                               write_timeout=0)

        try:
            if y_coord > 127:
                print("Forward move")
                self.motor_speed = y_coord - 127

                if x_coord < 127:
                    self.twist_speed = 127 - x_coord    # left
                    self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                    self.left_motor_hex_string.append(self.motor_speed - self.twist_speed)

                    self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                    self.right_motor_hex_string.append(self.motor_speed)

                elif x_coord > 127:
                    self.twist_speed = x_coord - 127  # right
                    self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                    self.left_motor_hex_string.append(self.motor_speed)

                    self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                    self.right_motor_hex_string.append(self.motor_speed - self.twist_speed)

                else:
                    self.left_motor_hex_string = [0xAA, 0x0A, 0x0D]
                    self.left_motor_hex_string.append(self.motor_speed)

                    self.right_motor_hex_string = [0xAA, 0x0A, 0x0B]
                    self.right_motor_hex_string.append(self.motor_speed)

            elif y_coord < 127:
                print("Reverse move")
                self.motor_speed = 127 - y_coord

                if x_coord < 127:
                    self.twist_speed = 127 - x_coord    # left
                    self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                    self.left_motor_hex_string.append(self.motor_speed)

                    self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                    self.right_motor_hex_string.append(self.motor_speed - self.twist_speed)

                elif x_coord > 127:
                    self.twist_speed = x_coord - 127   # right
                    self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                    self.left_motor_hex_string.append(self.motor_speed - self.twist_speed)

                    self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                    self.right_motor_hex_string.append(self.motor_speed)

                else:
                    self.left_motor_hex_string = [0xAA, 0x0A, 0x09]
                    self.left_motor_hex_string.append(self.motor_speed)

                    self.right_motor_hex_string = [0xAA, 0x0A, 0x0F]
                    self.right_motor_hex_string.append(self.motor_speed)
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


