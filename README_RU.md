# Raspberry Pi Hardware Monitor
![PROJECT PHOTO](https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/0.png)

* [INFO](#chapter-0)
* [Системные требования](#chapter-1)
* [Подключение](#chapter-2)
* [Установка](#chapter-3)
* [Настройки скрипта](#chapter-4)
* [Настройка](#chapter-5)
* [Возможные ошибки](#chapter-6)
* [Cahngelog](#chapter-7)

<a id="chapter-0"></a>

### *Монитор железа для Raspberry Pi*

![PIC0](https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/1.png)
![PIC1](https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/2.png)

Выводит информацию на дисплей LCD2004.
Что выводится?
На данный момент сделано:
 - *Вывод IP адреса.*
 - *Вывод загрузки RAM.*
 - *Вывод состояния памяти SD-карты.*
 - *Вывод состояния памяти внешнего носителя (прим. HDD/SSD).*
 - *Вывод Uptime.*
 - *Вывод температуры CPU.*
 - *Вывод температуры с внешнего датчика DS18B20.*
 - *Вывод текущей даты.*

В планах сделать:
 - *Добавить управление вентилятором.*
 - *Разбить скрипт на куски.*

 <a id="chapter-1"></a>

 ### *Системные требования*
 * Необходимо наличие установленного *Python.*
 * Необходимо включить *i2c.*
 * Необходимо включить *1-Wire.*

<a id="chapter-2"></a>

### *Подключение*
Raspberry PI  | LCD 2004
------------- | -------------
         5V   |   5V
         SDA  |   SDA
         SCL  |   SCL
         GND  |   GND

Raspberry PI  | DS18B20
------------- | -------------
         5V   |   5V
       GPIO7  |   DATA
         GND  |   GND

<a id="chapter-3"></a>

### *Установка*
Все команды выполняются в терминале последовательно от root.
1) Переходим в домашнюю папку:
`cd /home/pi`
2) Клонируем репозиторий:
`sudo git clone https://github.com/Cherkes001/raspberrypi_hardwaremonitor.git`
3) Переходим в папку со скриптом:
`cd raspberrypi_hardwaremonitor`
4) Даем права на выполнение скрипту:
`sudo chmod +x hardware_monitor.py`
5) Запуск:
`./hardware_monitor.py`

### *Автозапуск*
Дополнение от @alexinario
Если делали по инструкции, то скрипт окажется в данной директории, далее прописываете данные команды:  

`sudo cp -i /home/pi/raspberrypi_hardwaremonitor/hardware_monitor.py /bin`  
`sudo crontab -e`  
Добавить в crontab:  
`@reboot python /bin/hardware_monitor.py &`  

<a id="chapter-4"></a>

### *Настройки скрипта*
0. Для отключения вывода какой-либо необходимо просто закомментировать строку в скрипте через знак `#`.

1. Адрес дисплея.
В строке `I2C_ADDR  = 0x27`.
`0x27` - заменить на ваш адрес.
Как? - См. ниже.

2. ID - датчика DS18B20.
В строке `tfile=open("/sys/bus/w1/devices/28-0317249ce7ff/w1_slave")`.<br>
`28-0317249ce7ff` - заменить на ваш ID.

3. Вывод состояния памяти внешнего хранилища.
В строке `hdd = run_cmd ("df -BMB | grep /mnt/*** | awk '{print $2\"/\"$3, $5}'")`<br>
Там где - `/mnt/***` прописать вашу точку монтирования.

<a id="chapter-5></a>

### *Настройка*
1. Адрес дисплея:<br>
`sudo i2cdetect -y 1`<br>
Будет выведена таблица, где обычно 27 или 3F - это и есть адрес дисплея. <br>
2. ID датчика DS18B20:<br>
После подключения датчика выполняем следующие команды:<br>
1. `sudo modprobe w1-gpio && sudo modprobe w1_therm`<br>
2. `ls -l /sys/bus/w1/devices/`<br>

Будет выведена похожая информация:<br>
`total 0<br>
total 0<br>
lrwxrwxrwx 1 root root 0 Nov 29 10:49 28-0317249ce7ff -> ../../../devices/w1_bus_master1/28-0317249ce7ff<br>
lrwxrwxrwx 1 root root 0 Nov 29 10:49 w1_bus_master1 -> ../../../devices/w1_bus_master1`<br>

Каждый датчик имеет уникальный номер. Находим ID датчика. В моем случае 28-0317249ce7ff.<br>

<a id="chapter-6"></a>

### *Возможные ошибки*
1. Не правильный i2c адрес дисплея или дисплей не найден.<br>
Укажите свой адрес дисплея (*прим.* обычно *0x27* или *0x3F*) и проверьте соединения.<br>
`Traceback (most recent call last):<br>
  File "./dispy.py", line 146, in <module><br>
    lcd_byte(0x01, LCD_CMD)<br>
  File "./dispy.py", line 99, in lcd_byte<br>
    bus.write_byte(I2C_ADDR, bits_high)<br>
IOError: [Errno 121] Remote I/O error`<br>

2. Не правильный ID датчика DS18B20 или датчик не найден.<br>
Укажите свой ID датчка и проверьте соединения. Если данный датчик не используется, то просто отключите его вывод просто закомментировав строку.<br>
`Traceback (most recent call last):<br>
  File "./dispy.py", line 142, in <module><br>
    main()<br>
  File "./dispy.py", line 136, in main<br>
    lcd_string("DS18B20 Temp:{}".format(get_dallas()),LCD_LINE_2)<br>
  File "./dispy.py", line 77, in get_dallas<br>
    tfile=open("/sys/bus/w1/devices/28-0317249ce7ff/w1_slave")<br>
IOError: [Errno 2] No such file or directory: '/sys/bus/w1/devices/28-0317249ce7ff/w1_slave'`<br>

<a id="chapter-7"></a>

### *Changelog*
---15/09/2019 ---<br>
Добавлен перевод на Английский язык для файла README.

---08.07.2019---<br>
Добавлен вывод загрузки CPU;<br>
Другой способ вывода UPtime;<br>
Наполнение readme;<br>

---20.06.2020---<br>
Коммит @wildrun0;<br>

---19.11.2020---<br>
Обновление Readme;<br>

> Часть кода скрипта найден на просторах интернета.
