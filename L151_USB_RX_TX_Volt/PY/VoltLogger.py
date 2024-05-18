import USBloggerLib
import time
from datetime import datetime ,timezone, timedelta
from numpy import uint32, uint8, int8, uint16
import numpy as np
import struct

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

#define ADC_REFERENCE_VOLTAGE					1.224f
#define ADC_MAX									0x1000//0xFFF

############################################################################
def sensors(data):
    RV_HI4 = 1000
    RV_LO4 = 1011

    RV_HI5 = 1000
    RV_LO5 = 1015

    RV_HI6 = 1000
    RV_LO6 = 1015

    RV_HI7 = 1000
    RV_LO7 = 1015

    try:
        elem_arr = [data[i:i+4] for i in range(0, len(data), 4)]

        vref  = struct.unpack('<f', bytes( elem_arr[0]  ))[0]
        temp  = struct.unpack('<f', bytes( elem_arr[1]  ))[0]
        adc0  = struct.unpack('<f', bytes( elem_arr[2]  ))[0]
        adc1  = struct.unpack('<f', bytes( elem_arr[3]  ))[0]
        adc2  = struct.unpack('<f', bytes( elem_arr[4]  ))[0]
        adc3  = struct.unpack('<f', bytes( elem_arr[5]  ))[0]
        adc6  = struct.unpack('<f', bytes( elem_arr[6]  ))[0]
        adc7  = struct.unpack('<f', bytes( elem_arr[7]  ))[0]
        adc8  = struct.unpack('<f', bytes( elem_arr[8]  ))[0]
        adc9  = struct.unpack('<f', bytes( elem_arr[9]  ))[0]
        adc18 = struct.unpack('<f', bytes( elem_arr[10] ))[0]
        adc19 = struct.unpack('<f', bytes( elem_arr[11] ))[0]
        adc20 = struct.unpack('<f', bytes( elem_arr[12] ))[0]
        adc21 = struct.unpack('<f', bytes( elem_arr[13] ))[0]

        #adc4 = adc4 * ( (RV_HI4 + RV_LO4) / RV_LO4 )
        #adc5 = adc5 * ( (RV_HI5 + RV_LO5) / RV_LO5 )
        #adc6 = adc6 * ( (RV_HI6 + RV_LO6) / RV_LO6 )
        #adc7 = adc7 * ( (RV_HI7 + RV_LO7) / RV_LO7 )

        print(cgreen, f'vref: {vref:7.4f}, '+
                      f'temp: {temp:7.4f}, '+
                      f'0: {adc0:6.4f}, '+    
                      f'1: {adc1:6.4f}, '+
                      f'2: {adc2:6.4f}, '+
                      f'3: {adc3:6.4f}, '+
                      f'6: {adc6:6.4f}, '+
                      f'7: {adc7:6.4f}, '+
                      f'8: {adc8:6.4f}, '+
                      f'9: {adc9:6.4f}, '+
                      f'18: {adc18:6.4f}, '+
                      f'19: {adc19:6.4f}, '+
                      f'20: {adc20:6.4f}, '+
                      f'21: {adc21:6.4f}')

        #if not os.path.exists(filename):
        #    file =  open(filename, mode='w') 
        #    file.write('Time;Vref;Adc0;Adc1;Adc2;Adc3;Adc4;Adc5;Adc6;Adc7\n')
        #    file.close()


        #now = datetime.now(timezone.utc)
        #formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        #file =  open(filename, mode='a') 
        #file.write(f'{formatted_time};{vref:.5f};{adc0:.5f};{adc1:.5f};{adc2:.5f};{adc3:.5f};{adc4:.5f};{adc5:.5f};{adc6:.5f};{adc7:.5f}\n')
        #file.close()

    except Exception as e:  
        print(e)

in1_max = 0
in1_min = 0
in2_max = 0
in2_min = 0
in3_max = 0
in3_min = 0
def sensors_int(data):
    global in1_max
    global in1_min
    global in2_max
    global in2_min
    global in3_max
    global in3_min

    RV_HI4 = 1000
    RV_LO4 = 1011

    RV_HI5 = 1000
    RV_LO5 = 1015

    RV_HI6 = 1000
    RV_LO6 = 1015

    RV_HI7 = 1000
    RV_LO7 = 1015

    try:
        elem_arr = [data[i:i+2] for i in range(0, len(data), 2)]

        vref  = elem_arr[0][0]  <<8 | elem_arr[0][1] 
        temp  = elem_arr[1][0]  <<8 | elem_arr[1][1] 
        adc0  = elem_arr[2][0]  <<8 | elem_arr[2][1] 
        adc1  = elem_arr[3][0]  <<8 | elem_arr[3][1] 
        adc2  = elem_arr[4][0]  <<8 | elem_arr[4][1] 
        adc3  = elem_arr[5][0]  <<8 | elem_arr[5][1] 
        adc6  = elem_arr[6][0]  <<8 | elem_arr[6][1] 
        adc7  = elem_arr[7][0]  <<8 | elem_arr[7][1] 
        adc8  = elem_arr[8][0]  <<8 | elem_arr[8][1] 
        adc9  = elem_arr[9][0]  <<8 | elem_arr[9][1] 
        adc18 = elem_arr[10][0] <<8 | elem_arr[10][1]
        adc19 = elem_arr[11][0] <<8 | elem_arr[11][1]
        adc20 = elem_arr[12][0] <<8 | elem_arr[12][1]
        adc21 = elem_arr[13][0] <<8 | elem_arr[13][1]

        #adc4 = adc4 * ( (RV_HI4 + RV_LO4) / RV_LO4 )
        #adc5 = adc5 * ( (RV_HI5 + RV_LO5) / RV_LO5 )
        #adc6 = adc6 * ( (RV_HI6 + RV_LO6) / RV_LO6 )
        #adc7 = adc7 * ( (RV_HI7 + RV_LO7) / RV_LO7 )
        dtl = 3.0

        if adc0>in1_max:
            in1_max = adc0
        else:
            in1_max -= dtl

        if adc1>in2_max:
            in2_max = adc1
        else:
            in2_max -= dtl

        if adc2>in3_max:
            in3_max = adc2
        else:
            in3_max -= dtl
######
        if adc0<in1_min:
            in1_min = adc0
        else:
            in1_min += dtl

        if adc1<in2_min:
            in2_min = adc1
        else:
            in2_min += dtl
        
        if adc2<in3_min:
            in3_min = adc2
        else:
            in3_min += dtl
        

        print(cgreen, f'vref: {vref:5d}, '+
                      f'temp: {temp:5d}, '+
                      f'0: {adc0:5d}, '+    
                      f'1: {adc1:5d}, '+
                      f'2: {adc2:5d}, '+cyellow+
                      f'in1H: {int(in1_max):5d}, '+#f'3: {adc3:5d}, '+
                      f'in1L: {int(in1_min):5d}, '+clcyan+#f'6: {adc6:5d}, '+
                      f'in2H: {int(in2_max):5d}, '+#f'7: {adc7:5d}, '+
                      f'in2L: {int(in2_min):5d}, '+clmag+#f'8: {adc8:5d}, '+
                      f'in3H: {int(in3_max):5d}, '+#f'9: {adc9:5d}, '+
                      f'in3L: {int(in3_min):5d}, '+clgreen+#f'18: {adc18:5d}, '+
                      f'in1 d: {int(in1_max-in1_min):5d}, '+#f'19: {adc19:5d}, '+
                      f'in2 d: {int(in2_max-in2_min):5d}, '+#f'20: {adc20:5d}, '+
                      f'in3 d: {int(in3_max-in3_min):5d}, '#f'21: {adc21:5d}')
        )

        #if not os.path.exists(filename):
        #    file =  open(filename, mode='w') 
        #    file.write('Time;Vref;Adc0;Adc1;Adc2;Adc3;Adc4;Adc5;Adc6;Adc7\n')
        #    file.close()


        #now = datetime.now(timezone.utc)
        #formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        #file =  open(filename, mode='a') 
        #file.write(f'{formatted_time};{vref:.5f};{adc0:.5f};{adc1:.5f};{adc2:.5f};{adc3:.5f};{adc4:.5f};{adc5:.5f};{adc6:.5f};{adc7:.5f}\n')
        #file.close()

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


############################################################################
### input type: data = [1,2,3,...]
############################################################################
if __name__ == "__main__":



    USBloggerLib.StartListener_BG(callback_fn=usb_rx)

    ADC_int(0)
    


    while 1:
        time.sleep(0.010)
        startADC()
