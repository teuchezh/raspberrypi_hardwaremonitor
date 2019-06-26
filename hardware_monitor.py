#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://raspberrytips.nl/lcd-scherm-20x4-i2c-raspberry-pi/
# https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load?answertab=votes#tab-top
# https://github.com/adafruit/Adafruit_Python_SSD1306

import sys
import smbus
import time
import datetime
import subprocess
from subprocess import check_output         # Импортируем библиотеку по работе с внешними процессами
from re import findall                      # Импортируем библиотеку по работе с регулярными выражениями
import os

I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line


LCD_BACKLIGHT  = 0x08  # On 0X08 / Off 0x00

ENABLE = 0b00000100 # Enable bit

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

#Запрос IP-адреса
def get_my_ipwlan():
    val = run_cmd(["hostname -I | cut -d\' \' -f1 | head --bytes -1"])
    if val == "":
      val = "No connection!"
    return val

#Запрос загрузки RAM
def get_memusage():
    ram = run_cmd ("free -m | awk 'NR==2{print $3\"MB/\"$2\"MB\"}'")
    return(ram)

#Запрос памяти SD-карты
def get_checkmem():
    mem = run_cmd("df -B100000000 | grep /dev/root | awk '{print $3/10\"/\"$2/10\"GB\", $5}'")
    return (mem)

#Запрос памяти HDD
def get_checkhdd():
    hdd = run_cmd ("df -BMB | grep /mnt/*** | awk '{print $2\"/\"$3, $5}'")
    return (hdd)

#Заппрос Uptime
def get_uptime():
    uptime = run_cmd ("uptime | awk 'NR==1{print $3}'")
    return (uptime)

#Запрос температуры CPU
def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode()    # Выполняем запрос температуры
    temp = float(findall('\d+\.\d+', temp)[0])                   # Извлекаем при помощи регулярного выражения значение температуры из строки "temp=47.8'C"
    return(temp)                                                 # Возвращаем результат

#Запрос темперауры с датчика DS18B20
def get_dallas():
    tfile=open("/sys/bus/w1/devices/28-0317249ce7ff/w1_slave")
    ttext=tfile.read()
    tfile.close()
    temp=ttext.split("\n")[1].split(" ")[9]
    temperature=float(temp[2:])/1000
    return temperature


def lcd_init():
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


def main():
  lcd_init()
  while True:
    now = datetime.datetime.now()
    temp = get_temp()

    lcd_string("IP:{}".format(get_my_ipwlan()),LCD_LINE_1)
    lcd_string("RAM:{}".format(get_memusage()),LCD_LINE_2)
    lcd_string("CPU Temp:{}".format(get_temp()),LCD_LINE_3)
    lcd_string("SD mem:{}".format(get_checkmem()),LCD_LINE_4)
    time.sleep(5)

    lcd_byte(0x01, LCD_CMD)
    lcd_string("Uptime:{}".format(get_uptime()),LCD_LINE_1)
    lcd_string("DS18B20 Temp:{}".format(get_dallas()),LCD_LINE_2)
    lcd_string( str(now.day)+'/'+str(now.month)+'/'+str(now.year)+' '+str(now.hour)+':'+str(now.minute),LCD_LINE_3)
    time.sleep(5)
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)