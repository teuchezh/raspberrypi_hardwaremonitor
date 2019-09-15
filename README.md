# Raspberry Pi Hardware Monitor
![PROJECT PHOTO] (https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/0.png)

* [Перейти на Русский](https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/REAME_RU.md)
* [INFO](#chapter-0)
* [System requirements](#chapter-1)
* [Connection](#chapter-2)
* [Installation](#chapter-3)
* [Script settings](#chapter-4)
* [Setup](# chapter-5)
* [Possible errors](#chapter-6)
* [Cahngelog](# chapter-7)

<a id="chapter-0"></a>

### *Hardware Monitor for Raspberry Pi*

![PIC0](https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/1.png)
![PIC1] (https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/2.png)

Displays information on the LCD2004 display.
What is displayed?
Currently done:
 - *Output IP address.*
 - *RAM loading output.*
 - *Displays the status of the SD card's memory.*
 - *Displays the memory status of external media (approx. HDD / SSD).*
 - *Uptime output.*
 - *CPU temperature output.*
 - *Temperature output from external sensor DS18B20.*
 - *Displays the current date.*

The plans to do:
 - *Add fan control.*
 - *Break the script into pieces.*

 <a id="chapter-1"></a>

 ### *System requirements*
 * Requires installed *Python.*
 * You must enable *i2c.*
 * You must enable *1-Wire.*

<a id="chapter-2"></a>

### * Connection *
Raspberry PI | LCD 2004
-------------| -------------
         5V  | 5V
         SDA | SDA
         SCL | SCL
         GND | GND

Raspberry PI  | DS18B20
------------- | -------------
           5V | 5V
        GPIO7 | DATA
          GND | GND

<a id="chapter-3"></a>

### *Installation*
All commands are executed in the terminal sequentially from root.
1) Go to the home folder:
`cd / home / pi`
2) Clone the repository:
`sudo git clone https: // github.com / Cherkes001 / raspberrypi_hardwaremonitor.git`
3) Go to the folder with the script:
`cd raspberrypi_hardwaremonitor`
4) We give the right to execute the script:
`sudo chmod + x hardware_monitor.py`
5) Launch:
`. / hardware_monitor.py`

### *Autostart*
1)
2)
3)

<a id="chapter-4"></a>

### *Script settings*
0. To disable any output, you just need to comment out the line in the script through the `#` sign.

1. Display address.
In the line `I2C_ADDR = 0x27`.
`0x27` - replace with your address.
How? - See below.

2. ID - sensor DS18B20.
In the line `tfile = open (" / sys / bus / w1 / devices / 28-0317249ce7ff / w1_slave ")`.<br>
`28-0317249ce7ff` - replace with your ID.

3. Displaying the memory status of external storage.
In the line `hdd = run_cmd (" df -BMB | grep / mnt / *** | awk '{print $ 2 \ "/ \" $ 3, $ 5}' ")`<br>
Where - `/ mnt / ***` register your mount point.

<a id="chapter-5></a>

### *Setup*
1. Display Address:<br>
`sudo i2cdetect -y 1`<br>
A table will be displayed, where usually 27 or 3F - this is the display address.<br>
2. DS18B20 Sensor ID: <br>
After connecting the sensor, execute the following commands:<br>
1. `sudo modprobe w1-gpio && sudo modprobe w1_therm`<br>
2. `ls -l / sys / bus / w1 / devices /`<br>

Similar information will be displayed:<br>
`total 0<br>
total 0<br>
lrwxrwxrwx 1 root root 0 Nov 29 10:49 28-0317249ce7ff -> ../../../devices/w1_bus_master1/28-0317249ce7ff<br>
lrwxrwxrwx 1 root root 0 Nov 29 10:49 w1_bus_master1 -> ../../../ devices / w1_bus_master1`<br>

Each sensor has a unique number. Find the sensor ID. In my case, 28-0317249ce7ff.<br>

<a id="chapter-6"></a>

### *Possible mistakes*
1. Invalid i2c display address or display not found. <br>
Indicate your display address (* approx. * Usually * 0x27 * or * 0x3F *) and check the connections.<br>
`Traceback (most recent call last):<br>
  File "./dispy.py", line 146, in <module><br>
    lcd_byte (0x01, LCD_CMD) <br>
  File "./dispy.py", line 99, in lcd_byte<br>
    bus.write_byte (I2C_ADDR, bits_high)<br>
IOError: [Errno 121] Remote I / O error`<br>

2. Invalid DS18B20 sensor ID or sensor not found.<br>
Enter your sensor ID and check the connections. If this sensor is not used, then simply disable its output by simply commenting out the line. <br>
`Traceback (most recent call last):<br>
  File "./dispy.py", line 142, in <module><br>
    main ()<br>
  File "./dispy.py", line 136, in main<br>
    lcd_string ("DS18B20 Temp: {}". format (get_dallas ()), LCD_LINE_2)<br>
  File "./dispy.py", line 77, in get_dallas<br>
    tfile = open ("/ sys / bus / w1 / devices / 28-0317249ce7ff / w1_slave")<br>
IOError: [Errno 2] No such file or directory: '/ sys / bus / w1 / devices / 28-0317249ce7ff / w1_slave'`<br>

<a id="chapter-7"> </a>

### *Changelog*
--- 15/09/2019 ---<br>
Added EN translation for README File.

--- 08/07/2019 ---<br>
Added CPU load output;<br>
Another way to output UPtime;<br>
Filling readme;<br>

> Part of the script code is found on the Internet.