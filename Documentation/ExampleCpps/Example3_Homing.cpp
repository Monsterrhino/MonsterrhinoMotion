#include "System.h"

/*
* Monsterrhino Motion Examples
* Example 3: Homing
* V1.0
* 26.02.2021
* Author D.D.
*/

void MotorInit()
{
	g_Motor3.LoadMotorParameter();		//Loads default motor values (SenseResitor, Current, ...)

	g_Motor3.SetMotorCurrent(100);		//Motor current in mA (0.001 Ampere)
	g_Motor3.SetMotorCurrentHold(50);	//Motor standstill current

	g_Motor3.Begin();					//				

	g_Motor3.ResetRampStatus();			//Reset RampStatus flags
	g_Motor3.SetRampSpeeds(g_Motor3.GetStartup_RampSpeedsStart(), g_Motor3.GetStartup_RampSpeedsStop(), g_Motor3.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
	g_Motor3.SetAccelerations(g_Motor3.GetStartup_AccelerationsAMax(), g_Motor3.GetStartup_AccelerationsDMax(), g_Motor3.GetStartup_AccelerationsA1(), g_Motor3.GetStartup_AccelerationsD1()); //AMAX, DMAX, A1, D1

	return;
}
void HomingInit()
{
	g_Motor3.m_HomingParameters.mode = 1;
	g_Motor3.m_HomingParameters.rampSpeedHold = 5.0;
	//g_Motor3.m_HomingParameters.accelerationsD1 = 100.0;
	//g_Motor3.m_HomingParameters.accelerationsA1 = 100.0;
	//g_Motor3.m_HomingParameters.accelerationsAmax = 100.0;
	//g_Motor3.m_HomingParameters.accelerationsDmax = 100.0;
	g_Motor3.m_HomingParameters.rampSpeed_2 = 5.0;
	//g_Motor3.m_HomingParameters.rampSpeedStart = 60.0;
	g_Motor3.m_HomingParameters.homingOffset = 15.0;

	g_Motor3.SetMaxSpeed(5);
	g_Motor3.SetAcceleration(5);

	return;
}

uint32_t Homing(uint32_t par, UserFunction* pUserFunction)
{
	//Reset ramp status and current/target position and wait 500ms to ensure
	g_Motor3.SetCurrentPosition(0);
	g_Motor3.SetTargetPosition(0);
	g_Motor3.ResetRampStatus();
	vTaskDelay(500);

	//
	g_Motor3.MotorFunction_TiggerStart(MOTOR_FUNCTION_HOMING);
	pUserFunction->MotorHomingOk(LOCK_MOTOR3, par);

	g_Motor3.SetMaxSpeed(5);
	g_Motor3.SetAcceleration(100);

	Serial.println("yAxis homing done!");
	return 1;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	MotorInit();	//Motor initialization
	HomingInit();	//Homing initialization

	Homing(par, pUserFunction);

	return 1;
}

/*
*
*/