import USBloggerLib
import time
from datetime import datetime ,timezone, timedelta
from numpy import uint32, uint8, int8, uint16
import numpy as np
import struct
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import threading



import colorama
from colorama import Fore, Back, Style
colorama.init()
cred =      Fore.RED
cgreen =    Fore.GREEN
clgreen =   Fore.LIGHTGREEN_EX
cblue =     Fore.BLUE
cyellow =   Fore.YELLOW
clyellow =  Fore.LIGHTYELLOW_EX
clcyan =    Fore.LIGHTCYAN_EX
clmag =     Fore.LIGHTMAGENTA_EX
clblue =    Fore.LIGHTBLUE_EX
creset =    Fore.RESET

import os
import sys
try:
    #go to file directory
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass
filename = 'log.csv'

#############################################################################
# Создание изображения
width = 800
height = 500

image1 = Image.new("RGB", (width, height), "black")
draw1 = ImageDraw.Draw(image1)

width2 = 500
height2 = 200
image2 = Image.new("RGB", (width2, height2), "black")
draw2 = ImageDraw.Draw(image2)

def move_img(image):
    # сдвинуть содержимое draw на 1 пиксель влево, вправо оставить "черную" линию
    image.paste(image1, (-1, 0))

def draw_point(draw,y, r,g,b):
    x = width - 2
    y = int(height-y)
    draw.point((x, y), tuple([r,g,b]))

    



#define ADC_REFERENCE_VOLTAGE					1.224f
#define ADC_MAX									0x1000//0xFFF

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

############################################################################
def sensors(data):
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

    try:
        elem_arr = [data[i:i+4] for i in range(0, len(data), 4)]

        vref  = struct.unpack('<f', bytes( elem_arr[0]  ))[0]
        temp  = struct.unpack('<f', bytes( elem_arr[1]  ))[0]
        adc0  = struct.unpack('<f', bytes( elem_arr[2]  ))[0]*1224
        adc1  = struct.unpack('<f', bytes( elem_arr[3]  ))[0]*1224
        adc2  = struct.unpack('<f', bytes( elem_arr[4]  ))[0]*1224
        adc3  = struct.unpack('<f', bytes( elem_arr[5]  ))[0]*1224
        adc6  = struct.unpack('<f', bytes( elem_arr[6]  ))[0]*1224
        adc7  = struct.unpack('<f', bytes( elem_arr[7]  ))[0]*1224
        adc8  = struct.unpack('<f', bytes( elem_arr[8]  ))[0]*1224
        adc9  = struct.unpack('<f', bytes( elem_arr[9]  ))[0]*1224
        adc18 = struct.unpack('<f', bytes( elem_arr[10] ))[0]*1224
        adc19 = struct.unpack('<f', bytes( elem_arr[11] ))[0]*1224
        adc20 = struct.unpack('<f', bytes( elem_arr[12] ))[0]*1224
        adc21 = struct.unpack('<f', bytes( elem_arr[13] ))[0]*1224

        
        if in_cap>0:
            in0_off +=adc0
            in1_off +=adc1
            in2_off +=adc2
            in3_off +=adc3
            in6_off +=adc6
            in7_off +=adc7
            in_cap_count += 1

        adc0  -= in0_off
        adc1  -= in1_off
        adc2  -= in2_off
        adc3  -= in3_off
        adc6  -= in6_off
        adc7  -= in7_off


        if adc0>in0:
            in0+= delta * abs(in0 - adc0)
        else:
            in0-= delta * abs(in0 - adc0) 

        if adc1>in1:
            in1+= delta * abs(in1 - adc1)
        else:
            in1-= delta * abs(in1 - adc1) 

        if adc2>in2:
            in2+= delta * abs(in2 - adc2) 
        else:
            in2-= delta * abs(in2 - adc2) 

        if adc3>in3:
            in3+= delta * abs(in3 - adc3)
        else:
            in3-= delta * abs(in3 - adc3)
        
        if adc6>in6:
            in6+= delta * abs(in6 - adc6)
        else:
            in6-= delta * abs(in6 - adc6)

        if adc7>in7:
            in7+= delta * abs(in7 - adc7)
        else:
            in7-= delta * abs(in7 - adc7) 


        print(cgreen, f'vref: {vref:7.4f}, '+
                      f'temp: {temp:7.4f}, '+
              clcyan, f'0: {in0:7.4f}, '+    
                      f'1: {in1:7.4f}, '+
                      f'2: {in2:7.4f}, '+
                      f'3: {in3:7.4f}, '+
                      f'6: {in6:7.4f}, '+
                      f'7: {in7:7.4f}, '+
                      f'8: {adc8:7.4f}, '+
                      f'9: {adc9:7.4f}, '+
                      f'18: {adc18:7.4f}, '+
                      f'19: {adc19:7.4f}, '+
                      f'20: {adc20:7.4f}, '+
                      f'21: {adc21:7.4f}')



    except Exception as e:  
        print(e)


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
    # RV_HI4 = 1000
    # RV_LO4 = 1011

    # RV_HI5 = 1000
    # RV_LO5 = 1015

    # RV_HI6 = 1000
    # RV_LO6 = 1015

    # RV_HI7 = 1000
    # RV_LO7 = 1015

    ADC_REFERENCE_VOLTAGE				=	1.224
    ADC_MAX								=	0x1000

    try:
        elem_arr = [data[i:i+2] for i in range(0, len(data), 2)]

        vref  = elem_arr[0 ][1]  <<8 | elem_arr[0 ][0] 
        temp  = elem_arr[1 ][1]  <<8 | elem_arr[1 ][0] 
        adc0  = int( (elem_arr[2 ][1]  <<8 | elem_arr[2 ][0])   )
        adc1  = int( (elem_arr[3 ][1]  <<8 | elem_arr[3 ][0])   )
        adc2  = int( (elem_arr[4 ][1]  <<8 | elem_arr[4 ][0])   )
        adc3  = int( (elem_arr[5 ][1]  <<8 | elem_arr[5 ][0])   )
        adc6  = int( (elem_arr[6 ][1]  <<8 | elem_arr[6 ][0])   )
        adc7  = int( (elem_arr[7 ][1]  <<8 | elem_arr[7 ][0])   )
        adc8  = int( (elem_arr[8 ][1]  <<8 | elem_arr[8 ][0])   )
        adc9  = int( (elem_arr[9 ][1]  <<8 | elem_arr[9 ][0])   )
        adc18 = int( (elem_arr[10][1]  <<8 | elem_arr[10][0])   )
        adc19 = int( (elem_arr[11][1]  <<8 | elem_arr[11][0])   )
        adc20 = int( (elem_arr[12][1]  <<8 | elem_arr[12][0])   )
        adc21 = int( (elem_arr[13][1]  <<8 | elem_arr[13][0])   )



        if in_cap>0:
            in0_off +=adc0
            in1_off +=adc1
            in2_off +=adc2
            in3_off +=adc3
            in6_off +=adc6
            in7_off +=adc7
            in_cap_count += 1

        adc0  -= in0_off
        adc1  -= in1_off
        adc2  -= in2_off
        adc3  -= in3_off
        adc6  -= in6_off
        adc7  -= in7_off
        vref = ADC_REFERENCE_VOLTAGE * ADC_MAX / vref

        # in0 = adc0
        # in1 = adc1
        # in2 = adc2
        # in3 = adc3
        # in6 = adc6
        # in7 = adc7

        if adc0>in0:
            in0+= delta * abs(in0 - adc0)
        else:
            in0-= delta * abs(in0 - adc0) 

        if adc1>in1:
            in1+= delta * abs(in1 - adc1)
        else:
            in1-= delta * abs(in1 - adc1) 

        if adc2>in2:
            in2+= delta * abs(in2 - adc2) 
        else:
            in2-= delta * abs(in2 - adc2) 

        if adc3>in3:
            in3+= delta * abs(in3 - adc3)
        else:
            in3-= delta * abs(in3 - adc3)
        
        if adc6>in6:
            in6+= delta * abs(in6 - adc6)
        else:
            in6-= delta * abs(in6 - adc6)

        if adc7>in7:
            in7+= delta * abs(in7 - adc7)
        else:
            in7-= delta * abs(in7 - adc7) 


    
        draw_point(draw1, in0+height/2, 255,0,0)
        draw_point(draw1, in1+height/2, 255,255,0)
        draw_point(draw1, in2+height/2, 0,255,0)

        draw_point(draw1, in3+height/2, 0,255,255)
        draw_point(draw1, in6+height/2, 255,255,255)
        draw_point(draw1, in7+height/2, 255,0,255)

        print(cgreen, f'vref: {vref:3f}, '+
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


        # Обновление изображения в окне Tkinter
        img_tk1 = ImageTk.PhotoImage(image1)
        canvas1.itemconfig(canvas_image1, image=img_tk1)
        canvas1.image = img_tk1
        move_img(image1)

        # рисование линий в draw2 цвета rgb
        h = 30
        w = 5
        bx = int(width2/3)
        if in0>100:
            in0 = 100
        if in0<-80:
            in0 = -80

        if in1>100:
            in1 = 100
        if in1<-80:
            in1 = -80

        if in2>100:
            in2 = 100
        if in2<-80:
            in2 = -80   
        
        if in3>100:
            in3 = 100
        if in3<-80:
            in3 = -80
        
        if in6>100:
            in6 = 100
        if in6<-80:
            in6 = -80
        
        if in7>100:
            in7 = 100
        if in7<-80:
            in7 = -80
        
        draw2.rectangle([(0, 0), (width2, height2)], fill=(0,0,0))
        draw2.line([(bx, 0), (bx, height2)], fill=(127,127,127), width=1)
        draw2.line([(bx+bx, 0), (bx+bx, height2)], fill=(127,127,127), width=1)

        
        draw2.line([(bx, h), (bx - in0, h)], fill=(255,0,0), width=w)
        draw2.line([(bx, h*2), (bx - in1, h*2)], fill=(255,255,0), width=w)
        draw2.line([(bx, h*3), (bx - in2, h*3)], fill=(0,255,0), width=w)

        draw2.line([(bx+bx, h), (bx+bx + in3, h)], fill=(0,255,255), width=w)
        draw2.line([(bx+bx, h*2), (bx+bx + in6, h*2)], fill=(255,255,255), width=w)
        draw2.line([(bx+bx, h*3), (bx+bx + in7, h*3)], fill=(255,0,255), width=w)
        # Обновление изображения в окне Tkinter
        img_tk2 = ImageTk.PhotoImage(image2)
        canvas2.itemconfig(canvas_image2, image=img_tk2)
        canvas2.image = img_tk2

    except Exception as e:  
        print(e)

tasks = {"253":sensors,
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
def adc_th():
    USBloggerLib.StartListener_BG(callback_fn=usb_rx)

    ADC_int(0)
    ADCdelay(50)

    thread = threading.Thread(target=zero_ADC, daemon = True)
    thread.start()
    startADC_cont()
    while 1:
        time.sleep(0.05)
        #startADC()  
        time.sleep(1)
############################################################################
### input type: data = [1,2,3,...]
############################################################################
if __name__ == "__main__":

    # Создание окна Tkinter
    root = tk.Tk()
    root.title("Рисование точек")
    canvas1 = tk.Canvas(root, width=width, height=height)
    canvas2 = tk.Canvas(root, width=width2, height=height2)
    canvas1.pack()
    canvas2.pack()
    # добавить кнопку и повесить команду zero_ADC()
    button = tk.Button(root, text="zero_ADC", command=zero_ADCth)
    button.pack()



    # Отображение изображения в окне Tkinter
    img_tk1 = ImageTk.PhotoImage(image1)
    canvas_image1 = canvas1.create_image(0, 0, anchor="nw", image=img_tk1)

    img_tk2 = ImageTk.PhotoImage(image2)
    canvas_image2 = canvas2.create_image(0, 0, anchor="nw", image=img_tk2)

    # Запуск потока для обновления изображения
    thread = threading.Thread(target=adc_th, daemon = True)
    thread.start()

    # Запуск главного цикла Tkinter
    root.mainloop()
    
