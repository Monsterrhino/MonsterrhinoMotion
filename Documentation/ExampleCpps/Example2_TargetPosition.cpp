#include "System.h"

/*
* Monsterrhino Motion Examples
* Example 2: TargetPosition
* V1.0
* 11.02.2021
* Author D.D.
*/

void MotorInit()
{
	g_Motor1.LoadMotorParameter();		//Loads default motor values (SenseResitor, Current, ...)

	g_Motor1.SetMotorCurrent(100);		//Motor current in mA (0.001 Ampere)
	g_Motor1.SetMotorCurrentHold(50);	//Motor standstill current

	g_Motor1.Begin();					//				

	g_Motor1.ResetRampStatus();			//Reset RampStatus flags
	g_Motor1.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
	g_Motor1.SetAccelerations(g_Motor1.GetStartup_AccelerationsAMax(), g_Motor1.GetStartup_AccelerationsDMax(), g_Motor1.GetStartup_AccelerationsA1(), g_Motor1.GetStartup_AccelerationsD1()); //AMAX, DMAX, A1, D1
	return;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	MotorInit();						//Motor initialization

	g_Motor1.SetTargetPosition(100);	//Sets motor 1 target position to 100 -> motor runs (unless it´s already at that position)

	return 1;
}

/*
* Similar motor-functions are:
* g_Motor1.SetCurrentPosition(10);
* g_Motor1.SetMoveRelative(150);
*/