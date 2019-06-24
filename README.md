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

Выводит мнформацию на дисплей LCD2004.
Что выводится?
На данный момент сделано:
 - *Вывод IP адреса.*
 - *Вывод загрузки RAM.*
 - *Вывод состояния памяти SD-карты.*
 - *Вывод состояния памяти внешнего носителя (прим. HDD/SSD).*
 - *Вывод Uptime.*
 - *Вывод температуры CPU.*
 - *Вывод тепературы с внешнего датчика DS18B20.*
 - *Вывод текущей даты.*

В планах сделать:
 - *Добавить управление вентилятором.*
 - *Разбить скрипт на куски.*

 <a id="chapter-1"></a>
 
 ### *Системные требования.*
 * Необходимо наличе установленного *Python.*
 * Необходимо включить *i2c.*
 * Необходимо включить *1-Wire.*

<a id="chapter-2"></a>

### *Установка.*
Все команды выполняются в терминале последовательно от root.
1) Переходим в домашнюю папку:
`cd home/pi`
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


> Часть кода скрипта найден на просторах интернета.