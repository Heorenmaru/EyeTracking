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
raw_x = 0           # -1 .. 1
raw_y = 0           # -1 .. 1

smoth1_delta = 0    
smoth1_x = 0        # -1 .. 1
smoth1_y = 0        # -1 .. 1

smoth2_delta = 0
smoth2_x = 0        # -1 .. 1
smoth2_y = 0        # -1 .. 1

smoth3_delta = 0
smoth3_x = 0        # -1 .. 1
smoth3_y = 0        # -1 .. 1

# масштаб ADC
adcScale = 100

# положение точек
point1_pos = [-0.5, -0.5]
p1_vScale = 1
angle1_to_center = 0

point2_pos = [-0.5,    0]
p2_vScale = 1
angle2_to_center = 0

point3_pos = [-0.5, +0.5]
p3_vScale = 1
angle3_to_center = 0

point4_pos = [0.5,  -0.5]
p4_vScale = 1
angle4_to_center = 0

point5_pos = [0.5,     0]
p5_vScale = 1
angle5_to_center = 0

point6_pos = [0.5,  +0.5]
p6_vScale = 1
angle6_to_center = 0

# Raw data
p1Vec = 0
p2Vec = 0
p3Vec = 0
p4Vec = 0
p5Vec = 0
p6Vec = 0

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
height = 400

image1 = Image.new("RGB", (width, height), "black")
draw1 = ImageDraw.Draw(image1)

width2 = 500
height2 = 150


image2 = Image.new("RGB", (width2, height2), "black")
draw2 = ImageDraw.Draw(image2)

width3 = 300
height3 = 300

image3 = Image.new("RGB", (width3, height3), "black")
draw3 = ImageDraw.Draw(image3)

# Создание окна Tkinter
root = tk.Tk()
root.title("Рисование точек")
canvas1 = tk.Canvas(root, width=width, height=height)
canvas2 = tk.Canvas(root, width=width2, height=height2)
canvas3 = tk.Canvas(root, width=width3, height=height3)
canvas1.grid(row=0, column=0,rowspan=2)
canvas2.grid(row=0, column=1)
canvas3.grid(row=1, column=1)
# добавить кнопку и повесить команду zero_ADC()
button = tk.Button(root, text="zero_ADC", command=zero_ADCth)
button.grid(row=2, column=0)



# Отображение изображения в окне Tkinter
img_tk1 = ImageTk.PhotoImage(image1)
canvas_image1 = canvas1.create_image(0, 0, anchor="nw", image=img_tk1)

img_tk2 = ImageTk.PhotoImage(image2)
canvas_image2 = canvas2.create_image(0, 0, anchor="nw", image=img_tk2)

img_tk3 = ImageTk.PhotoImage(image3)
canvas_image3 = canvas3.create_image(0, 0, anchor="nw", image=img_tk3)



def move_img(image):
    # сдвинуть содержимое draw на 1 пиксель влево, вправо оставить "черную" линию
    image.paste(image1, (-1, 0))

def draw_point(draw,y, r,g,b):
    x = width - 2
    y = int(height-y)
    draw.point((x, y), tuple([r,g,b]))


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
        draw_point(draw1, in0+height/2, 255,0,0)
        draw_point(draw1, in1+height/2, 255,255,0)
        draw_point(draw1, in2+height/2, 0,255,0)

        draw_point(draw1, in3+height/2, 0,255,255)
        draw_point(draw1, in6+height/2, 255,255,255)
        draw_point(draw1, in7+height/2, 255,0,255)

        # Обновление изображения в окне Tkinter
        img_tk1 = ImageTk.PhotoImage(image1)
        canvas1.itemconfig(canvas_image1, image=img_tk1)
        canvas1.image = img_tk1
        move_img(image1)

        #############################################################################
        # bar IMG2
        # рисование линий в draw2 цвета rgb
        h = 30
        w = 5
        bx = int(width2/3)



        draw2.rectangle([(0, 0), (width2, height2)], fill=(0,0,0))
        draw2.line([(bx, 0), (bx, height2)], fill=(127,127,127), width=1)
        draw2.line([(bx+bx, 0), (bx+bx, height2)], fill=(127,127,127), width=1)


        draw2.line([(bx, h  ), (bx - in0, h  )], fill=(255,  0,  0), width=w)
        draw2.line([(bx, h*2), (bx - in1, h*2)], fill=(255,255,  0), width=w)
        draw2.line([(bx, h*3), (bx - in2, h*3)], fill=(0,  255,  0), width=w)

        draw2.line([(bx+bx, h  ), (bx+bx + in3, h  )], fill=(0,  255,255), width=w)
        draw2.line([(bx+bx, h*2), (bx+bx + in6, h*2)], fill=(255,255,255), width=w)
        draw2.line([(bx+bx, h*3), (bx+bx + in7, h*3)], fill=(255,  0,255), width=w)


        #middle horizontal
        l_md = (in0+in1+in2)/3
        r_md = (in3+in6+in7)/3

        x = l_md-r_md
        y1m = (in0+in3)/2
        y2m = (in1+in6)/2
        y3m = (in2+in7)/2

        y = y1m-y3m

        draw2.line([(bx,    h*4), (bx    - l_md,    h*4)], fill=(127,127,127), width=w)
        draw2.line([(bx+bx, h*4), (bx+bx + r_md,    h*4)], fill=(127,127,127), width=w)

        draw2.line([(int(width2/2 + (l_md-r_md)*4), 0), (int(width2/2 + (l_md-r_md)*4), height2)], fill=(127,127,127), width=1)

        draw2.line([0, (int(height2/2 + (y)*2)), (width2, int(height2/2 + (y)*2) )], fill=(127,127,0), width=1)


        # Обновление изображения3 в окне Tkinter





        img_tk2 = ImageTk.PhotoImage(image2)
        canvas2.itemconfig(canvas_image2, image=img_tk2)
        canvas2.image = img_tk2

        #############################################################################
        # рисование курсора IMG3    
        # рисуем 6 точек и ветора от них к центру
        draw3.rectangle([(0, 0), (width3, height3)], fill=(0,0,0))

        centerx = width3/2
        centery = height3/2
        

        point1_pxpos_x = int(centerx+centerx*point1_pos[0])
        point1_pxpos_y = int(centery+centery*point1_pos[1])

        point2_pxpos_x = int(centerx+centerx*point2_pos[0])
        point2_pxpos_y = int(centery+centery*point2_pos[1])

        point3_pxpos_x = int(centerx+centerx*point3_pos[0])
        point3_pxpos_y = int(centery+centery*point3_pos[1])

        point4_pxpos_x = int(centerx+centerx*point4_pos[0])
        point4_pxpos_y = int(centery+centery*point4_pos[1])

        point5_pxpos_x = int(centerx+centerx*point5_pos[0])
        point5_pxpos_y = int(centery+centery*point5_pos[1])

        point6_pxpos_x = int(centerx+centerx*point6_pos[0])
        point6_pxpos_y = int(centery+centery*point6_pos[1])
        
        draw3.ellipse((point1_pxpos_x-2, point1_pxpos_y-2, point1_pxpos_x+2, point1_pxpos_y+2), fill=(255,0,0))
        draw3.ellipse((point2_pxpos_x-2, point2_pxpos_y-2, point2_pxpos_x+2, point2_pxpos_y+2), fill=(0,255,0))
        draw3.ellipse((point3_pxpos_x-2, point3_pxpos_y-2, point3_pxpos_x+2, point3_pxpos_y+2), fill=(0,0,255))
        draw3.ellipse((point4_pxpos_x-2, point4_pxpos_y-2, point4_pxpos_x+2, point4_pxpos_y+2), fill=(255,255,0))
        draw3.ellipse((point5_pxpos_x-2, point5_pxpos_y-2, point5_pxpos_x+2, point5_pxpos_y+2), fill=(0,255,255))
        draw3.ellipse((point6_pxpos_x-2, point6_pxpos_y-2, point6_pxpos_x+2, point6_pxpos_y+2), fill=(255,0,255))

        
        #рисуем линию от каждой точки длиной x с учетом угла
        s = 80
        draw3.line([point1_pxpos_x, point1_pxpos_y, point1_pxpos_x + p1Vec*s*math.cos(math.radians(angle1_to_center)), point1_pxpos_y + p1Vec*s*math.sin(math.radians(angle1_to_center))], fill=(255,0,0))
        draw3.line([point2_pxpos_x, point2_pxpos_y, point2_pxpos_x + p2Vec*s*math.cos(math.radians(angle2_to_center)), point2_pxpos_y + p2Vec*s*math.sin(math.radians(angle2_to_center))], fill=(0,255,0))
        draw3.line([point3_pxpos_x, point3_pxpos_y, point3_pxpos_x + p3Vec*s*math.cos(math.radians(angle3_to_center)), point3_pxpos_y + p3Vec*s*math.sin(math.radians(angle3_to_center))], fill=(0,0,255))
        draw3.line([point4_pxpos_x, point4_pxpos_y, point4_pxpos_x + p4Vec*s*math.cos(math.radians(angle4_to_center)), point4_pxpos_y + p4Vec*s*math.sin(math.radians(angle4_to_center))], fill=(255,255,0))
        draw3.line([point5_pxpos_x, point5_pxpos_y, point5_pxpos_x + p5Vec*s*math.cos(math.radians(angle5_to_center)), point5_pxpos_y + p5Vec*s*math.sin(math.radians(angle5_to_center))], fill=(0,255,255))
        draw3.line([point6_pxpos_x, point6_pxpos_y, point6_pxpos_x + p6Vec*s*math.cos(math.radians(angle6_to_center)), point6_pxpos_y + p6Vec*s*math.sin(math.radians(angle6_to_center))], fill=(255,0,255))

        # рисуем курсоры
        # RAW
        draw3.line([centerx+centerx*raw_x, 0,   centerx+centerx*raw_x, height3], fill=(127,0,0), width=1)
        draw3.line([0, centery+centery*raw_y, width3, centery+centery*raw_y], fill=(127,0,0), width=1)
        
        # smooth 1
        draw3.line([centerx+centerx*smoth1_x, 0,   centerx+centerx*smoth1_x, height3], fill=(0,127,127), width=1)
        draw3.line([0, centery+centery*smoth1_y, width3, centery+centery*smoth1_y], fill=(0,127,127), width=1)

        # smooth 2
        draw3.line([centerx+centerx*smoth2_x, 0,   centerx+centerx*smoth2_x, height3], fill=(0,127,0), width=1)
        draw3.line([0, centery+centery*smoth2_y, width3, centery+centery*smoth2_y], fill=(0,127,0), width=1)

        # smooth 3
        draw3.line([centerx+centerx*smoth3_x, 0,   centerx+centerx*smoth3_x, height3], fill=(127,127,127), width=1)
        draw3.line([0, centery+centery*smoth3_y, width3, centery+centery*smoth3_y], fill=(127,127,127), width=1)

        img_tk3 = ImageTk.PhotoImage(image3)
        canvas3.itemconfig(canvas_image3, image=img_tk3)
        canvas3.image = img_tk3

#############################################################################
# масштабирование векторов
def vector_scale(a0,a1,a2,a3,a6,a7):
    global p1Vec 
    global p2Vec
    global p3Vec
    global p4Vec
    global p5Vec
    global p6Vec

    p1Vec = 1/adcScale * a0
    p2Vec = 1/adcScale * a1
    p3Vec = 1/adcScale * a2
    p4Vec = 1/adcScale * a3
    p5Vec = 1/adcScale * a6
    p6Vec = 1/adcScale * a7

    if p1Vec > 1:
        p1Vec = 1
    if p2Vec > 1:
        p2Vec = 1
    if p3Vec > 1:
        p3Vec = 1
    if p4Vec > 1:
        p4Vec = 1
    if p5Vec > 1:
        p5Vec = 1
    if p6Vec > 1:
        p6Vec = 1
    
    if p1Vec < -1:
        p1Vec = -1
    if p2Vec < -1:
        p2Vec = -1
    if p3Vec < -1:
        p3Vec = -1
    if p4Vec < -1:
        p4Vec = -1
    if p5Vec < -1:
        p5Vec = -1
    if p6Vec < -1:
        p6Vec = -1

# #сглаживание координат
# def vector_smooth(vec, delta):

#     res+= delta * (adc0 - in0) 
#     in1+= delta * (adc1 - in1)
#     in2+= delta * (adc2 - in2)
#     in3+= delta * (adc3 - in3)
#     in6+= delta * (adc6 - in6)
#     in7+= delta * (adc7 - in7)
    
#     smoth1_x = smoth1_x*0.5 + raw_x*0.5
#     smoth1_y = smoth1_y*0.5 + raw_y*0.5
#     smoth2_x = smoth2_x*0.5 + raw_x*0.5
#     smoth2_y = smoth2_y*0.5 + raw_y*0.5
#     smoth3_x = smoth3_x*0.5 + raw_x*0.5
#     smoth3_y = smoth3_y*0.5 + raw_y*0.5
#расчет координат по сумме векторов
def vector_sum():
    global angle1_to_center
    global angle2_to_center
    global angle3_to_center
    global angle4_to_center
    global angle5_to_center
    global angle6_to_center

    global raw_x
    global raw_y
    global smoth1_x
    global smoth1_y
    global smoth2_x
    global smoth2_y
    global smoth3_x
    global smoth3_y


    #расчет угла от точки до центра 
    angle1_to_center = math.degrees(math.atan2(point1_pos[1], point1_pos[0]))
    angle2_to_center = math.degrees(math.atan2(point2_pos[1], point2_pos[0]))
    angle3_to_center = math.degrees(math.atan2(point3_pos[1], point3_pos[0]))
    angle4_to_center = math.degrees(math.atan2(point4_pos[1], point4_pos[0]))
    angle5_to_center = math.degrees(math.atan2(point5_pos[1], point5_pos[0]))
    angle6_to_center = math.degrees(math.atan2(point6_pos[1], point6_pos[0]))

    #расчет суммы векторов
    #TODO: x = math.cos(angle), y = math.sin(angle)
    raw_x = -( p1Vec*p1_vScale*math.cos(angle1_to_center) 
             + p2Vec*p2_vScale*math.cos(angle2_to_center) 
             + p3Vec*p3_vScale*math.cos(angle3_to_center) 
             + p4Vec*p4_vScale*math.cos(angle4_to_center) 
             + p5Vec*p5_vScale*math.cos(angle5_to_center) 
             + p6Vec*p6_vScale*math.cos(angle6_to_center))
    
    raw_y = -( p1Vec*p1_vScale*math.sin(angle1_to_center) 
             + p2Vec*p2_vScale*math.sin(angle2_to_center) 
             + p3Vec*p3_vScale*math.sin(angle3_to_center) 
             + p4Vec*p4_vScale*math.sin(angle4_to_center) 
             + p5Vec*p5_vScale*math.sin(angle5_to_center) 
             + p6Vec*p6_vScale*math.sin(angle6_to_center))

                                                                                                                                                                                                          

    delta = 0.25
    smoth1_x+= delta * (raw_x - smoth1_x)
    smoth1_y+= delta * (raw_y - smoth1_y)

    smoth2_x+= delta * (smoth1_x - smoth2_x)
    smoth2_y+= delta * (smoth1_y - smoth2_y)

    smoth3_x+= delta * (smoth2_x - smoth3_x)
    smoth3_y+= delta * (smoth2_y - smoth3_y)

    pass

#TODO: добавить функцию сглаживания координат



#define ADC_REFERENCE_VOLTAGE					1.224f
#define ADC_MAX									0x1000//0xFFF

############################################################################

in0=0
in1=0
in2=0
in3=0
in6=0
in7=0

in0_off=0
in1_off=0
in2_off=0
in3_off=0
in6_off=0
in7_off=0
in_cap = 0
in_cap_count = 0
def sensors_int(data):
    global in0
    global in1
    global in2
    global in3
    global in6
    global in7

    global in_cap_count

    global in0_off
    global in1_off
    global in2_off
    global in3_off
    global in6_off
    global in7_off

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
        if in_cap>0:
            in0_off +=adc0
            in1_off +=adc1
            in2_off +=adc2
            in3_off +=adc3
            in6_off +=adc6
            in7_off +=adc7
            in_cap_count += 1

        #установка в ноль по оффсетам
        adc0  -= in0_off
        adc1  -= in1_off
        adc2  -= in2_off
        adc3  -= in3_off
        adc6  -= in6_off
        adc7  -= in7_off
        
        vector_scale(adc0,adc1,adc2,adc3,adc6,adc7)
        vector_sum()

        #сглаживание сигнала
        #TODO: DEPRECATED

        in0+= delta * (adc0 - in0) 
        in1+= delta * (adc1 - in1)
        in2+= delta * (adc2 - in2)
        in3+= delta * (adc3 - in3)
        in6+= delta * (adc6 - in6)
        in7+= delta * (adc7 - in7)




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
    
