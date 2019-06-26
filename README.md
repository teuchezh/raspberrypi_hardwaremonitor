# Raspberry Pi Hardware monitor
![PROJECT PHOTO](https://github.com/Cherkes001/raspberrypi_hardwaremonitor/blob/master/pics/0.png)

* [RUS](#chapter-0)
* [Системные требования](#chapter-1)
* [Установка](#chapter-2)
* [Настройки скрипта](#chapter-3)


<a id="chapter-0"></a>

### *Монитор железа для Raspberry Pi.*

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
 
 ### *Системные требования.*
 * Необходимо наличие установленного *Python.*
 * Необходимо включить *i2c.*
 * Необходимо включить *1-Wire.*

<a id="chapter-2"></a>

### *Установка.*
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

<a id="chapter-3"></a>

### *Настройки скрипта*

1. Адрес дисплея.
В строке `I2C_ADDR  = 0x27`.
`0x27` - заменить на ваш адрес.
Как? - См. ниже.

2. ID - датчика DS18B20.
В строке `tfile=open("/sys/bus/w1/devices/28-0317249ce7ff/w1_slave")`.
`28-0317249ce7ff` - заменить на ваш ID.

3. Вывод состояния памяти внешнего хранилища.
В строке `hdd = run_cmd ("df -BMB | grep /mnt/*** | awk '{print $2\"/\"$3, $5}'")`
Там где - `/mnt/***` прописать вашу точку монтирования.

> Часть кода скрипта найден на просторах интернета.