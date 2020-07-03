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
v.1.1.6a от 03.07.2020.
"""

#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль math для математики.
import math


#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %H:%M:%S |')


#Функция для расчёта ковариации в методе CoLoRaDe.
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

#Функция расчёта H методом CoLoRaDe. (HEAF)
def colorade(input_data, e, debug):
    
    print("Используется метод CoLoRaDe.")
    logging.info("Используется метод CoLoRaDe.")
    
    #Количество пакетов (элементов списка).
    #-1 для учёта неиспользуемого 0-го элемента.
    n = len(input_data)-1
    
    #Дебаг.
    if debug >= 1:
        print("n=" + str(n))
    
    #Математическое ожидание.
    M = (1/n)*sum(input_data)
    
    #Цикл расчёта H и перед ним инициализация переменных.
    H = [0]
    ACF = [0]
    f_H = [0]
    df_H = [0]
    e_current = [0, 0]
    i = 1
    
    while i <= n:
        k = i
        
        #Дебаг.
        if debug >= 1:
            print("i=" + str(i))
        
        #АвтоКорреляционная Функция (ковариация/дисперсию)
        ACF.insert(int(i), comp_gamma(input_data, M, n, k)/\
        comp_gamma(input_data, M, n, 0))
        #Возможно, лучше считать отдельно.
        
        #H_1 отдельно.(k!=1)
        if i==1:
            H.insert(int(i), (0.5+1/(2*math.log(2))*\
            math.log(1+ACF[int(i)])))
        
        #H_2 и далее.
        if i>1:
            
            #Дебаг
            if debug >= 2:
                print("H[i-1]=" + str(H[i-1]))
            
            #f(H_i)
            f_H.insert(int(i), ACF[int(i)]-0.5*((k+1)**(2*H[int(i-1)])-\
            2*k**(2*H[int(i-1)])+(k-1)**(2*H[int(i-1)])))
            
            if debug >= 2:
                print("f(H_" + str(i) + ")=" + str(f_H))
            
            #f'(H_i), k!=1.
            df_H.insert(int(i), -0.5*(2*math.log(k+1)*\
            (k+1)**(2*H[int(i-1)])-(4*math.log(k))*\
            (k)**(2*H[int(i-1)])+\
            (2*math.log(k-1))*(k-1)**(2*H[int(i-1)])))
            
            #HEAF(i).
            H.insert(int(i), (H[int(i-1)]-f_H[int(i-1)]/df_H[int(i-1)]))
            
            if debug >= 1:
                print("H_" + str(i) + "=" + str(H[int(i)]))
            
            #Остановка расчётов.
            e_current.insert(int(i), abs(H[int(i)]-H[int(i-1)]))
            
            if e_current[int(i)] <= e: break
            #Без 1, т.к. для него не считается (e[1]=0).
            
        #Итерация цикла.
        i = i+1
        
        
    #Дебаг.
    if debug >= 1:
        print("АКФ: " + str(ACF))
        #print("H=" + str(H))
    
    #Вывод значений. Возможно, надо сделать отключаемым.
    print("H=" + str(H))
    print("e=" + str(e_current))
    
    logging.info("H=" + str(H) + '\t' + "e=" + str(e_current))
    
    return(H, e_current)
    
    """    
    Для предотвращения ошибок переполнения float и деления на 0 (df_H)
    надо увеличить эпсилон (уменьшить требуемую точность вычисления).
    
    В статье большой набор входных данных (1000 значений) разбили на 
    сэмплы по 200 значений (оптимально, по мнению автора).
    По большой выборке проходило окно определённого размера (N точек).
    Для каждого получившегося сэмпла (точек в окне) вычислялся H 
    (до установленной точности) и брался минимальный из полученных H.
    Потом окно сдвигалось (на размер себя же?) и вычисления повторялись. 
    По полученным данным можно было строить график.
    
    H не должен быть отрицательным!
    """
