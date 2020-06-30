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
Модуль расчёта показателя Хёрста методом CoLoRaDe.
v.1.1.4a от 30.06.2020.
"""

#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль math для математики.
import math


#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %H:%M:%S |')


def comp_gamma(input_data, M, n, k):
    #Так как список начинается с 0 элемента, он не ипользуется,
    #а от размера списка данных (n) надо отнять 1. 
    
    i = 1 
    c_summ = 0
    
    while i < n-k:
        
        c_summ = c_summ+(input_data[int(i)]-M)*\
        (input_data[int(i+k)]-M)
        #Индексы списка должны быть типа int 
        #(или др. поддерживаемого).
            
        i = i+1
    
    gamma = (1/n)*c_summ
    
    return(gamma)

#Функция расчёта H методом CoLoRaDe.
def colorade(input_data, e, debug):
    
    print("Используется метод CoLoRaDe.")
    logging.info("Используется метод CoLoRaDe.")
    
    #Количество пакетов (элементов списка).
    #-1 для учёта неиспользуемого 0-го элемента.
    n = len(input_data)-1
    
    #Дебаг.
    if debug >= 1:
        print("n=" + str(n))
    
    #Мат. ожидание.
    M = (1/n)*sum(input_data)
    
    #Цикл расчёта H.
    #Последний элемент списка будет самый правильный.
    H = [0]
    i = 1
    
    while i <= n:
        k = i
        
        #АвтоКорреляционная Функция
        ACF = comp_gamma(input_data, M, n, k)/\
        comp_gamma(input_data, M, n, 0)
        
        #H_1 отдельно.
        if i==1:
            H.insert(int(i), (0.5+1/(2*math.log(2))*math.log(1+ACF)))
        
        #H_2 и далее.
        if i>1:
            
            #Дебаг
            if debug >= 2:
                print("H[i-1]=" + str(H[i-1]))
            
            #f(H_i)
            f_H = ACF-0.5*((k+1)**(2*H[int(i-1)])-2*k**(2*H[int(i-1)])+\
            (k-1)**(2*H[int(i-1)]))
        
            #f'(H_i)
            df_H = -0.5*(2*math.log(k+1)*(k+1)**(2*H[int(i-1)])-\
            (4*math.log(k))*(k)**(2*H[int(i-1)])+\
            (2*math.log(k-1))*(k-1)**(2*H[int(i-1)]))
            
            #HEAF(i+1), почти. 
            H.insert(int(i), (H[int(i-1)]-f_H/df_H))
            
            e_stop = abs(H[int(i)]-H[int(i-1)])
            if e_stop <= e: break
        
        #Дебаг.
        if debug >= 1:
            print("i=" + str(i))
        
        #Итерация цикла.
        i = i+1
        
        
    #Дебаг.
    if debug >= 1:
        print("АКФ: " + str(ACF))
        print("H=" + str(H))
    
    #Последний показатель Хёрста правильный.
    good_H = H[len(H)-1]
    
    print("H=" + str(good_H))
    print("e=" + str(e_stop))
    
    logging.info("H=" + str(good_H) + '\t' + "e=" + str(e_stop))
    
    return(good_H, e_stop)
