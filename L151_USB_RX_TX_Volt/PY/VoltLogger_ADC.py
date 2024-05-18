import USBloggerLib
import time
from datetime import datetime ,timezone, timedelta
from numpy import uint32, uint8, int8, uint16
import numpy as np
import struct
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import threading
import math


import colorama
from colorama import Fore, Back, Style
colorama.init()


import os
import sys
try:
    #go to file directory
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass


#############################################################################
# Переменные
Sadc0  = 0
Sadc1  = 0
Sadc2  = 0
Sadc3  = 0
Sadc6  = 0
Sadc7  = 0
Sadc8  = 0
Sadc9  = 0
Sadc18 = 0
Sadc19 = 0
Sadc20 = 0
Sadc21 = 0

adc_zero = 0

#############################################################################
def zero_ADC():
    global in_cap
    global in_cap_count

    global in0_off
    global in1_off
    global in2_off
    global in3_off
    global in6_off
    global in7_off
    
    time.sleep(1)

    in0_off=0
    in1_off=0
    in2_off=0
    in3_off=0
    in6_off=0
    in7_off=0
    in_cap_count = 0
    in_cap = 1
    ADCdelay(20)
    

    time.sleep(3)
    try:
        in_cap = 0
        in0_off= in0_off / in_cap_count
        in1_off= in1_off / in_cap_count
        in2_off= in2_off / in_cap_count
        in3_off= in3_off / in_cap_count
        in6_off= in6_off / in_cap_count
        in7_off= in7_off / in_cap_count
        in_cap_count = 0 
        
    except:
        pass
    ADCdelay(30)

def zero_ADCth():
    thread = threading.Thread(target=zero_ADC, daemon = True)
    thread.start()


#############################################################################
# Создание изображения
width = 400
height = 800

image1 = Image.new("RGB", (width, height), "black")
draw1 = ImageDraw.Draw(image1)


# Создание окна Tkinter
root = tk.Tk()
root.title("Рисование точек")
canvas1 = tk.Canvas(root, width=width, height=height)

canvas1.grid(row=0, column=0,rowspan=2)





# Отображение изображения в окне Tkinter
img_tk1 = ImageTk.PhotoImage(image1)
canvas_image1 = canvas1.create_image(0, 0, anchor="nw", image=img_tk1)



##############################################################################
#     ######      #####       ###      #       #
#     #      #    #     #   #     #    #       #
#     #      #    #####     #######    #   #   #
#     #      #    #     #   #     #    # #   # #
#     ######      #     #   #     #    #       #
##############################################################################


def draw_img():
    while True:
        time.sleep(0.02)
        #############################################################################
        #graph IMG1
        
        w = 5
        bx = 10
        draw1.rectangle([(0, 0), (width, height)], fill=(0,0,0))

        draw1.line([(20, bx  ), (20, bx - Sadc0  )], fill=(255,  0,  0), width=w)
        draw1.line([(40, bx  ), (40, bx - Sadc1  )], fill=(255,  0,  0), width=w)
        draw1.line([(60, bx  ), (60, bx - Sadc2  )], fill=(255,  0,  0), width=w)
        draw1.line([(80, bx  ), (80, bx - Sadc3  )], fill=(255,  255,  0), width=w)
        draw1.line([(100,bx  ), (100,bx - Sadc6  )], fill=(255,  255,  0), width=w)
        draw1.line([(120,bx  ), (120,bx - Sadc7  )], fill=(255,  255,  0), width=w)
        draw1.line([(140,bx  ), (140,bx - Sadc8  )], fill=(255,  0,  255), width=w)
        draw1.line([(160,bx  ), (160,bx - Sadc9  )], fill=(255,  0,  255), width=w)
        draw1.line([(180,bx  ), (180,bx - Sadc18 )], fill=(255,  0,  255), width=w)
        draw1.line([(200,bx  ), (200,bx - Sadc19 )], fill=(255,  0,  255), width=w)
        draw1.line([(220,bx  ), (220,bx - Sadc20 )], fill=(100,  100,  100), width=w)
        draw1.line([(240,bx  ), (240,bx - Sadc21 )], fill=(100,  100,  100), width=w)


        # Обновление изображения в окне Tkinter
        img_tk1 = ImageTk.PhotoImage(image1)
        canvas1.itemconfig(canvas_image1, image=img_tk1)
        canvas1.image = img_tk1



#############################################################################



#TODO: добавить функцию сглаживания координат



#define ADC_REFERENCE_VOLTAGE					1.224f
#define ADC_MAX									0x1000//0xFFF

############################################################################


def sensors_int(data):
    global Sadc0 
    global Sadc1 
    global Sadc2 
    global Sadc3 
    global Sadc6 
    global Sadc7 
    global Sadc8 
    global Sadc9 
    global Sadc18
    global Sadc19
    global Sadc20
    global Sadc21
    
    global adc_zero

    delta = 0.1


    ADC_REFERENCE_VOLTAGE				=	1.224
    ADC_MAX								=	0x1000

    try:
        elem_arr = [data[i:i+2] for i in range(0, len(data), 2)]

        vref  = elem_arr[0 ][1]  <<8 | elem_arr[0 ][0] 
        vadc =  ADC_REFERENCE_VOLTAGE * ADC_MAX / vref 
        temp  = elem_arr[1 ][1]  <<8 | elem_arr[1 ][0] 
        adc0  = int( vadc/ADC_MAX *(elem_arr[2 ][1]  <<8 | elem_arr[2 ][0])  *1224 )
        adc1  = int( vadc/ADC_MAX *(elem_arr[3 ][1]  <<8 | elem_arr[3 ][0])  *1224 )
        adc2  = int( vadc/ADC_MAX *(elem_arr[4 ][1]  <<8 | elem_arr[4 ][0])  *1224 )
        adc3  = int( vadc/ADC_MAX *(elem_arr[5 ][1]  <<8 | elem_arr[5 ][0])  *1224 )
        adc6  = int( vadc/ADC_MAX *(elem_arr[6 ][1]  <<8 | elem_arr[6 ][0])  *1224 )
        adc7  = int( vadc/ADC_MAX *(elem_arr[7 ][1]  <<8 | elem_arr[7 ][0])  *1224 )
        adc8  = int( vadc/ADC_MAX *(elem_arr[8 ][1]  <<8 | elem_arr[8 ][0])  *1224 )
        adc9  = int( vadc/ADC_MAX *(elem_arr[9 ][1]  <<8 | elem_arr[9 ][0])  *1224 )
        adc18 = int( vadc/ADC_MAX *(elem_arr[10][1]  <<8 | elem_arr[10][0])  *1224 )
        adc19 = int( vadc/ADC_MAX *(elem_arr[11][1]  <<8 | elem_arr[11][0])  *1224 )
        adc20 = int( vadc/ADC_MAX *(elem_arr[12][1]  <<8 | elem_arr[12][0])  *1224 )
        adc21 = int( vadc/ADC_MAX *(elem_arr[13][1]  <<8 | elem_arr[13][0])  *1224 )


        #калибровка нуля
        az = adc0
        
        if az < adc1:
            az = adc1
        if az < adc2:
            az = adc2
        if az < adc3:
            az = adc3
        if az < adc6:
            az = adc6
        if az < adc7:
            az = adc7
        if az < adc8:
            az = adc8
        if az < adc9:
            az = adc9
        if az < adc18:
            az = adc18
        if az < adc19:
            az = adc19
        # if az < Sadc20:
        #     az = Sadc20
        # if az < Sadc21:
        #     az = Sadc21

        adc_zero  += 0.05 * (az - adc_zero) 



        #установка в ноль по оффсетам
        adc0  -= adc_zero
        adc1  -= adc_zero
        adc2  -= adc_zero
        adc3  -= adc_zero
        adc6  -= adc_zero
        adc7  -= adc_zero
        adc8  -= adc_zero
        adc9  -= adc_zero
        adc18 -= adc_zero
        adc19 -= adc_zero
        adc20 -= adc_zero
        adc21 -= adc_zero

        Sadc0  += delta * (adc0 - Sadc0) 
        Sadc1  += delta * (adc1 - Sadc1) 
        Sadc2  += delta * (adc2 - Sadc2) 
        Sadc3  += delta * (adc3 - Sadc3) 
        Sadc6  += delta * (adc6 - Sadc6) 
        Sadc7  += delta * (adc7 - Sadc7) 
        Sadc8  += delta * (adc8 - Sadc8) 
        Sadc9  += delta * (adc9 - Sadc9) 
        Sadc18 += delta * (adc18 - Sadc18) 
        Sadc19 += delta * (adc19 - Sadc19) 
        Sadc20 += delta * (adc20 - Sadc20) 
        Sadc21 += delta * (adc21 - Sadc21) 
        
        
        
    





        print(Fore.GREEN, f'vref: {vadc:7.4f}, '+
                      f'temp: {temp:5d}, '+
                      f'0: {int(adc0):5d}, '+    
                      f'1: {int(adc1):5d}, '+
                      f'2: {int(adc2):5d}, '+
                      f'3: {int(adc3):5d}, '+
                      f'6: {int(adc6):5d}, '+
                      f'7: {int(adc7):5d}, '+
                      f'8: {int(adc8):5d}, '+
                      f'9: {int(adc9):5d}, '+
                      f'18: {int(adc18):5d}, '+
                      f'19: {int(adc19):5d}, '+
                      f'20: {int(adc20):5d}, '+
                      f'21: {int(adc21):5d}')


        

        # обновление изображения в окне Tkinter

        # img_tk3 = ImageTk.PhotoImage(image3)
        # canvas3.itemconfig(canvas_image3, image=img_tk3)
        # canvas3.image = img_tk3
    except Exception as e:  
        print(e)

tasks = {
         "252":sensors_int}

def usb_rx(data):
    global receivedTrg
    receivedTrg = 1
    try:
        tasks[str(data[0])](data[1:])
    except:
        pass
        #print(cgreen, data)   


############################################################################

def checkDevice(data, stp = 0):
    USBloggerLib.send([0x00,0b00000001])
    tasks['0']=checkDevice(data, stp=1)
    

def startADC():
    cmd = 0x01

    start_time = time.time()
    while (start_time + 10) > time.time():
        if USBloggerLib.send([cmd]):
            break
        else:
            time.sleep(0.5)

def startADC_cont():
    cmd = 0x02

    start_time = time.time()
    while (start_time + 10) > time.time():
        if USBloggerLib.send([cmd]):
            break
        else:
            time.sleep(0.5)

def ADC_int(d): # 1/0
    cmd = 0x03
    dat = d
    start_time = time.time()
    while (start_time + 10) > time.time():
        if USBloggerLib.send([cmd,dat]):
            break
        else:
            time.sleep(0.5)

def ADCdelay(d):
    cmd = 0x04
    dat = uint16(d)
    start_time = time.time()
    while (start_time + 10) > time.time():
        if USBloggerLib.send([cmd,uint8(dat>>8),uint8(dat)]):
            break
        else:
            time.sleep(0.5)


def adc_th():
    USBloggerLib.StartListener_BG(callback_fn=usb_rx)

    ADC_int(1)
    ADCdelay(50)

    startADC_cont()
    while 1:
        time.sleep(0.05)
        #startADC()  
        time.sleep(1)
############################################################################
### input type: data = [1,2,3,...]
############################################################################


###########################################################################
#
#   #      #     ######     ###    #      #          
#   # #  # #    #      #     #     # #    #         
#   #  #   #    #      #     #     #  #   #       
#   #      #    # #### #     #     #   #  #       
#   #      #    #      #     #     #    # #    
#   #      #    #      #    ###    #      #  
#
###########################################################################
        
if __name__ == "__main__":



    # Запуск потока для обновления изображения
    thread = threading.Thread(target=adc_th, daemon = True)
    thread.start()

    thread_win = threading.Thread(target=draw_img, daemon = True)
    thread_win.start()
    # Запуск главного цикла Tkinter
    root.mainloop()
    
