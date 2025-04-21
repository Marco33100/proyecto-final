# Puedes encontrar el archivo original aquí si quieres descargarlo directamente:
# https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
from micropython import const
import framebuf
import time
# Dirección del OLED: 0x3C por defecto
class SSD1306_I2C(framebuf.FrameBuffer):
    def init(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.height * self.width // 8)
        super().init(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()
    def init_display(self):
        for cmd in (
            0xAE, 0xA4, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40, 0x8D,
            0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12, 0x81, 0xCF, 0xD9,
            0xF1, 0xDB, 0x40, 0xA6, 0xAF):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()
    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))
    def show(self):
        self.i2c.writeto(self.addr, bytearray([0x40]) + self.buffer)

