#!/usr/bin/python3
#Путь к интерпретатору Python v3.
# -*- coding: utf-8 -*-
#Выбор кодировки (без него не работает Русский язык).

"""
This file is part of HURsT.
HURsT is a research program for computing the Hurst exponent 
(in development).
Use this program on your own pril and risk.
HURsT Copyright © 2020 Konstantin Pankov 
(e-mail: konstantin.p.96@gmail.com), Mikhail Riapolov.

    HURsT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Any distribution and / or change must be agreed with the authors and
    is prohibited without their permission.
    At this stage of the program development, authors are forbidden to 
    embed any of HURsT modules (code components) into other programs.

    HURsT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with HURsT.  If not, see <https://www.gnu.org/licenses/>.


Этот файл — часть HURsT.
HURsT — это исследовательская программа для расчёта показателя Хёрста 
(в разработке). 
Используйте эту программу на свой страх и риск.
HURsT Copyright © 2020 Константин Панков 
(e-mail: konstantin.p.96@gmail.com), Михаил Ряполов.

   HURsT - свободная программа: вы можете перераспространять ее и/или
   изменять ее на условиях Стандартной общественной лицензии GNU
   в том виде, в каком она была опубликована 
   Фондом свободного программного обеспечения; либо версии 3 лицензии, 
   либо (по вашему выбору) любой более поздней версии.

   Любое распространиение и/или изменение должно быть согласовано с
   авторами и запрещается без их разрешения.
   На данном этапе развития программы авторами запрещается встраивать 
   любой из модулей (компонентов кода) HURsT в другие программы.

   HURsT распространяется в надежде, что она будет полезной,
   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
   общественной лицензии GNU.

   Вы должны были получить копию Стандартной общественной лицензии GNU
   вместе с этой программой. Если это не так, см.
   <https://www.gnu.org/licenses/>.
"""

"""
Программа HURsT для расчёта показателя Хёрста.
Основной исполняемый файл.
v.1.1.9a от 28.05.2021.
"""

#Подключаем парсер конфига.
import configparser
#Подключаем модуль парсинга аргументов (ключей) командной строки.
import argparse
#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль системных команд.
import sys
#Подключаем модуль взаимодействия с системой.
import os
#Подключаем свой модуль считывания входного файла.
import csv_file
#Подключаем свой модуль расчёта показателя Хёрста методом CoLoRaDe.
import colorade

#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %H:%M:%S |')

class Config:
    """
    Класс для работы с конфигрурационными файлами и 
    настройками программы.
    """
    
    def __init__(self, argv=[], configfile="config.ini"):
        """
        Функция, использующая по умолчанию файл конфигурации
        с именем 'config.ini', в которой можно 
        переопределять настройки из командной строки и
        имя файла конфигурации.
        """
        self.read_config(configfile)
        
    def read_config(self, configfile):
        """
        Функция загрузки настроек из файла конфигурации.
        Механизм чтения конфига, поиска нужных значений 
        и присваивания значений пременным. 
        """
        config = configparser.ConfigParser()
        
        #Считываем настройки из файла конфигурации.
        config.read(configfile)
        
        #Читаем значения из конфига.
        self.method = str(config.get("Settings", "Method"))
        self.e = float(config.get("CoLoRaDe", "e"))
        self.window_size = int(config.get("CoLoRaDe", "Window_size"))
        self.debug = int(config.get("Settings", "Debug"))
        self.out_format = str(config.get("Settings", "OutFormat"))
    
    def parse_params(self):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Функция для переопределения настроек
        параметрами командной строки.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        #Вызов парсера.
        argprs = argparse.ArgumentParser(prog='HURsT',\
        description="HURsT - программа для расчёта показателя Хёрста." \
        + '\n' + "HURsT Copyright © 2020 Konstantin Pankov " +
        "(e-mail: konstantin.p.96@gmail.com), Mikhail Riapolov.",\
        prefix_chars='-')
        
        """
        Варианты ключей и параметров программы:
        -m --method - метод расчёта показателя Хёрста;
        -f --file - входной csv файл с анализируемыми данными метрики.
        """
        
        #Группа для определения настроек ключами командной строки.
        cmd_args = argprs.add_argument_group('Command line arguments',\
        'Определение настроек ключами (аргументами) командной строки.')
        
        #Для выбора метода вычисления.
        #Новые методы добавлять в варианты выбора!
        cmd_args.add_argument('-m', '--method', default='colorade',\
        type=str, choices=['colorade'], dest='method',\
        help='Выбор метода расчёта показателя Хёрста. \
        colorade - использовать метод CoLoRaDe.')
        #choices=['colorade', 'другой метод']
        
        #Для входного файла.
        cmd_args.add_argument('-f', '--file', type=str,\
        dest='input_file', help='Имя входного csv файла.')
        
        #Для минимальной погрешности вычисления H.
        cmd_args.add_argument('-e', '--epsilon', type=float,\
        dest='e', help='Минимальная погрешность вычисления H.')
        
        #Для размера скользящего окна.
        cmd_args.add_argument('-w', '--window', type=int,\
        dest='window_size', help='Размер скользящего окна: число или\
        0 - автоматически подстраивается под размер всей выборки\
        с соотношением 1:5.')
        
        #Для дебага (по уровням).
        cmd_args.add_argument('-d', '--debug', type=int,\
        dest='debug', help='Выбор уровня дебага. 0 - выкл. \
        1 и далее - вкл.')
        
        #Для формата выходного файла.
        cmd_args.add_argument('--format', type=str,\
        dest='out_format',\
        help='Выбор варианта форматирования выходного файла:\
		full - полное, с колонками доп. данных и названиями колонок;\
		default - вывод только одной колонки данных (H).')
        
        #Если при запуске программы не заданы ключи командной строки,
        #то показывается справка.
        if len(sys.argv)==1:
            argprs.print_help(sys.stderr)
            sys.exit(1)
        
        #Запуск парсера аргументов с заданием ему имени
        #для дальнейшего обращения к результату.
        self.arguments = argprs.parse_args()
        
        #Возвращаем значения аргументов из функции.
        return self.arguments
        
    
        

if __name__ == "__main__":
    """
    Запуск функции main() только при запуске этого модуля, 
    но не при импорте.
    Если функция main не задана в явном виде (def main()),
    то весь код (после конструкции if __name__ == "__main__") 
    считается ею.
    """
    
    #Разделитель.
    print('\n')
    logging.info('\t')
    
    #Загрузка настроек из файла конфигурации с сохранением в переменную.
    #Если есть параметры командной строки, то они переопределяют
    #настройки из конфига.
    cfg = Config(sys.argv)
    
    #Вызов функции парсера командной строки.
    args = cfg.parse_params()
    
    
    #Следующие несколько настроек будут подгружаться из конфига,
    #если не заданы в качестве параметров командной строки.
    
    #Метод расчёта.
    if args.method != None:
        method = args.method
    else:
        method = cfg.method
    
    #Входной файл.
    if args.input_file != None:
        input_file = args.input_file
    else:
        print("Не задан входной файл!")
        logging.info("Не задан входной файл!")
        
    
    #Эпсилон - минимальная погрешность вычисления H.
    if args.e != None:
        e = args.e
    else:
        e = cfg.e
        
    #window_size - размер скользящего окна.
    if args.window_size != None:
        window_size = args.window_size
    else:
        window_size = cfg.window_size
        
    #Дебаг.
    if args.debug != None:
        debug = args.debug
    else:
        debug = cfg.debug
    
    #Формат выходного файла.
    if args.out_format != None:
        out_format = args.out_format
    else:
        out_format = cfg.out_format
		
    
    #---     
    #Запуск считывания входного файла.
    input_data = csv_file.csv_read(input_file)
    
    #Показ и логгирование имени входного файла.
    print("Входной файл: " + input_file)
    logging.info("Входной файл: " + input_file)
    
    #Запуск расчёта показателя Хёрста выбранным методом.
    if method == "colorade":
        #Запуск расчёта показателя Хёрста методом CoLoRaDe.
        H_colorade, e_H, window_size_real =\
        colorade.colorade(input_data, e, window_size, debug)
        
        #Запись полученных данных в csv файл.
        #Выходной файл помещается в директорию, где лежит входной файл,
        #к имени файла дописываются метод расчёта и обозначение "out".
        if out_format == 'default':
            csv_file.csv_write(input_file, method, window_size_real, e,\
            H_colorade, e_H)
            
        elif out_format == 'full':
            csv_file.csv_write_full(input_file, method,\
            window_size_real, e, H_colorade, e_H)
        
        logging.info("Размер окна: " + str(window_size_real))
        logging.info("Минимальная допустимая ошибка e: " + str(e))
    
    else:
        print("Выбран несуществующий метод!")
        logging.info("Выбран несуществующий метод!")
        

"""
Для обработки нескольких файлов одним или несколькими методами
надо написать bash скрипт с соответсвующими ключами и параметрами.
"""

"""
! Сделать скользяще окно с изменением шага. (?)
"""
