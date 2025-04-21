from machine import I2C
import time

class MLX90614:
    def __init__(self, i2c, address=0x5A):
        self.i2c = i2c
        self.address = address

    def read16(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 3)
        temp = data[1] << 8 | data[0]
        return temp

    def read_temp_raw(self, register):
        raw = self.read16(register)
        return raw * 0.02 - 273.15

    def read_object_temp(self):
        return self.read_temp_raw(0x07)

    def read_ambient_temp(self):
        return self.read_temp_raw(0x06)

