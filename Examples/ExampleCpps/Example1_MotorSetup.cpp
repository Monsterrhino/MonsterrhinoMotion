#include "System.h"

/*
* Monsterrhino Motion Examples
* Example 1: Motor setup
* V1.0
* 11.02.2021
* Author D.D.
*/

void MotorInit()
{
	g_Motor1.LoadMotorParameter();
	g_Motor1.SetMotorCurrent(100);
	g_Motor1.SetMotorCurrentHold(50);
	g_Motor1.Begin();
	g_Motor1.ResetRampStatus();
	g_Motor1.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
	g_Motor1.SetAccelerations(g_Motor1.GetStartup_AccelerationsAMax(), g_Motor1.GetStartup_AccelerationsDMax(), g_Motor1.GetStartup_AccelerationsA1(), g_Motor1.GetStartup_AccelerationsD1()); //AMAX, DMAX, A1, D1

	return;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	MotorInit();									//Motor initialization
	return 1;
}
