#include "System.h"

uint32_t last_m3 = 0;
uint32_t last_m4 = 0;


void updateCoordinates(uint32_t par, UserFunction* pUserFunction) {

	while (true) {
		uint32_t temp_4 = g_Motor4.GetCurrentPosition();
		uint32_t temp_3 = g_Motor3.GetCurrentPosition();

		if (temp_4 == last_m4 && temp_3 == last_m3) {
			//Serial.println("Not moving!");
			pUserFunction->m_variable[5] = 0;
		}
		else {
			//Serial.println("Moving!");
			pUserFunction->m_variable[5] = 1;
		}

		last_m3 = temp_3;
		last_m4 = temp_4;

		//Serial.print("Current y pos: ");
		//Serial.println(pUserFunction->m_variable[5]);
		vTaskDelay(50);
	}
}

uint32_t UserFunction2(uint32_t par, UserFunction* pUserFunction)
{
	updateCoordinates(par, pUserFunction);

	return 1;
}
