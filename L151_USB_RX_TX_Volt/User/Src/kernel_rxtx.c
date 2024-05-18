/*
 * au_logic.c
 *
 *  Created on: Mar 16, 2022
 *      Author: Heorenmaru
 */

#include "kernel.h"

#define DEVICE_CODE 0x0000U
#define DEVICE_VER 	0x00U

/////////////////////////////////////////////////////////////////////////////////
// HANDLERS and VARS
/////////////////////////////////////////////////////////////////////////////////
extern ADC_HandleTypeDef hadc;

#define ch_count  14
uint16_t adc_data[ch_count * 8] = { 0 };

#define T_TIMEOUT  1
#define T_OK 0


uint8_t continious = 0;
uint8_t adc_ok = 0;
uint8_t int_out = 1;
uint16_t adc_delay = 10;
/////////////////////////////////////////////////////////////////////////////////
// USB Receive logic
/////////////////////////////////////////////////////////////////////////////////



void usb_callback(uint8_t *arr, uint16_t len){



	////////////
	// DEV INFO
	// (STANDART COMMAND)
	if(arr[0] == 0 ){

		uint16_t *idBase0 = (uint16_t*)(UID_BASE);
		uint16_t *idBase1 = (uint16_t*)(UID_BASE + 0x02);
		uint32_t *idBase2 = (uint32_t*)(UID_BASE + 0x04);
		uint32_t *idBase3 = (uint32_t*)(UID_BASE + 0x08);

		usb_rst_cursor();
		usb_add_uint8(0x00);
		usb_add_uint16(idBase0);
		usb_add_uint16(idBase1);
		usb_add_uint32(idBase2);
		usb_add_uint32(idBase3);

		usb_add_uint16((uint8_t)DEVICE_CODE);
		usb_add_uint8((uint8_t)DEVICE_VER);

		usb_send_buff();

	}



	////////////////Start Convert Single mode
	if(arr[0] == 1 ){

		HAL_GPIO_WritePin(LEDR_GPIO_Port, LEDR_Pin, 0);
		HAL_GPIO_WritePin(LEDG_GPIO_Port, LEDG_Pin, 1);
		continious = 0;
		HAL_ADC_Start_DMA(&hadc, (uint32_t*)&adc_data, ch_count*8);

		usb_rst_cursor();
		usb_add_uint8(0x01);
		usb_add_uint8(0);

		usb_send_buff();
	}

	////////////////Start Convert Continious mode
	if(arr[0] == 2 ){

		HAL_GPIO_WritePin(LEDG_GPIO_Port, LEDG_Pin, 0);
		continious = 1;
		HAL_ADC_Start_DMA(&hadc, (uint32_t*)&adc_data, ch_count*8);



		usb_rst_cursor();
		usb_add_uint8(0x02);
		usb_add_uint8(0);

		usb_send_buff();
	}

	//////////////// int/float mode
	if(arr[0] == 3 ){

		if(arr[1]>0){
			int_out = 1;
		}else{
			int_out = 0;
		}

		usb_rst_cursor();
		usb_add_uint8(0x03);
		usb_add_uint8(0);

		usb_send_buff();
	}

	//////////////// adc delay
		if(arr[0] == 4 ){

			adc_delay = arr[1]<<8 | arr[2];

			usb_rst_cursor();
			usb_add_uint8(0x03);
			usb_add_uint8(0);

			usb_send_buff();
		}
}



/////////////////////////////////////////////////////////////////////////////////
// ADC
/////////////////////////////////////////////////////////////////////////////////

#define ADC_REFERENCE_VOLTAGE					1.224f
#define ADC_MAX									0x1000//0xFFF

void calc_voltage_int()
{

	uint32_t vref_adc 	= 0 ;
	uint32_t temp 	= 0 ;
	uint32_t chf_arr[ch_count-2] = {0};

	for (uint8_t i = 0; i < 8*ch_count; i = i + ch_count) {
		vref_adc 	+= adc_data[i];
		temp 		+= adc_data[i+1];
		for (uint8_t j = 2; j <= ch_count; j++ ){
			chf_arr[j-2] += adc_data[i + j];
		}

	}

	vref_adc 	= (uint32_t) vref_adc 	/ 8;
	temp 		= (uint32_t) temp 	/ 8;
	for (uint8_t j = 0; j < ch_count-2; j++ ){
		chf_arr[j] = (uint32_t)  chf_arr[j] / 8;
	}


	//voltage = (float) adc_2 * ( (RV_HI + RV_LO) / RV_LO );
	//current = (float) ( adc_3 / (1 + (RA_HI/RA_LO)) ) / R_SHUNT;   //(float)3/3*adc_3
	//power = voltage*current;
	usb_rst_cursor();
	usb_add_uint8(0xFC);
	usb_add_uint16(vref_adc);
	usb_add_uint16(temp);
	for (uint8_t j = 0; j < ch_count-2; j++ ){
		usb_add_uint16((uint16_t) chf_arr[j]);
	}
	usb_send_buff();
	HAL_GPIO_WritePin(LEDR_GPIO_Port, LEDR_Pin, 1);

}

void calc_voltage()
{

	float vref_adc 	= 0 ;
	float temp 	= 0 ;
	float chf_arr[ch_count-2] = {0};

	for (uint8_t i = 0; i < 8*ch_count; i = i + ch_count) {
		vref_adc 	+= adc_data[i];
		temp 		+= adc_data[i+1];
		for (uint8_t j = 2; j <= ch_count; j++ ){
			chf_arr[j-2] += adc_data[i + j];
		}

	}

	vref_adc 	= vref_adc 	/ 8;
	temp 		= temp 	/ 8;
	for (uint8_t j = 0; j < ch_count-2; j++ ){
		chf_arr[j] = chf_arr[j] / 8;
	}


	vref_adc 	=  ADC_MAX * ADC_REFERENCE_VOLTAGE / vref_adc;

	for (uint8_t j = 0; j < ch_count-2; j++ ){
		chf_arr[j] = vref_adc / ADC_MAX * chf_arr[j] ;
	}




	//voltage = (float) adc_2 * ( (RV_HI + RV_LO) / RV_LO );
	//current = (float) ( adc_3 / (1 + (RA_HI/RA_LO)) ) / R_SHUNT;   //(float)3/3*adc_3
	//power = voltage*current;
	usb_rst_cursor();
	usb_add_uint8(0xFD);
	usb_add_float(&vref_adc);
	usb_add_float(&temp);
	for (uint8_t j = 0; j < ch_count-2; j++ ){
		usb_add_float(&chf_arr[j]);
	}
	usb_send_buff();
	HAL_GPIO_WritePin(LEDR_GPIO_Port, LEDR_Pin, 1);
}


void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{

    if(hadc->Instance == ADC1)
    {
        HAL_ADC_Stop_DMA(hadc); // это необязательно
        if(int_out > 0){
        	calc_voltage_int();
        }else{
        	calc_voltage();
        }
		adc_ok = 1;
        

    }
}





/////////////////////////////////////////////////////////////////////////////////
// INIT
/////////////////////////////////////////////////////////////////////////////////


void kernel_init() {

    //////////////////////////////////
    // Hardware Check

	HAL_Delay(2000);
	HAL_GPIO_WritePin(LEDR_GPIO_Port, LEDR_Pin, 1);
	HAL_GPIO_WritePin(LEDG_GPIO_Port, LEDG_Pin, 1);
	HAL_GPIO_WritePin(LEDB_GPIO_Port, LEDB_Pin, 0);

}


/////////////////////////////////////////////////////////////////////////////////
// MAIN
/////////////////////////////////////////////////////////////////////////////////



void kernel_main() {
	usb_set_callback(&usb_callback);
	kernel_init();





    while(1)
    {
		if (adc_ok>0){
			adc_ok = 0;
			if (continious > 0){
        		HAL_ADC_Start_DMA(&hadc, (uint32_t*)&adc_data, ch_count*8);
        	}
			HAL_Delay(adc_delay);
		}
		

    }
}



