#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
Модуль считывания входных данных из файла.
v.1.1.1
"""

#Подключаем модуль взаимодействия с системой.
import os
#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль работы с файлами csv.
import csv

#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %H:%M:%S |')

#Считывание входного csv файла.
def csv_read(input_file):
    #Открываем входной файл.
    csv_file = open(input_file, "r", newline="")
    #Считываем содержимое.
    csv_reader = csv.reader(csv_file)
    
    #Создаём пустой список под данные из входного файла.
    input_data = []
    
    #Вытаскивание данных из файла.
    for row in csv_reader:
            #Считывание 0-го (первого) элемента в строке. 
            #Разделитель - запятая.
            input_data_row = row[0]
            
            #Дебаг
            #print(input_data_row)
            
            #Добавляем приведённые данные в список (к концу).
            input_data.append(float(input_data_row))

    #Закрываем входной файл.
    csv_file.close()
    
    #Возвращаем считанные данные в виде списка. Можно переделать в массив.
    return input_data
    
    
if __name__ == "__main__":
    input_file = "test.csv"
    csv_read(input_file)
