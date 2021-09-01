#include "System.h"

bool initialized2 = false;


uint32_t MotorInit(uint32_t par, UserFunction* pUserFunction)
{
		g_Motor1.SetMotorCurrent(80);
		g_Motor1.SetMotorCurrentHold(50);

		g_Motor2.SetMotorCurrent(80);
		g_Motor2.SetMotorCurrentHold(50);

		g_Motor3.m_HomingParameters.mode = 2;
		g_Motor3.m_HomingParameters.rampSpeedHold = 250.0;
		g_Motor3.m_HomingParameters.rampSpeed_2 = 80.0;
		g_Motor3.m_HomingParameters.homingOffset = 50.0;

		g_Motor3.SetMotorCurrent(30);
		g_Motor3.SetMotorCurrentHold(10);

		g_Motor4.m_HomingParameters.mode = 2;
		g_Motor4.m_HomingParameters.rampSpeedHold = 250.0;
		g_Motor4.m_HomingParameters.rampSpeed_2 = 80.0;
		g_Motor4.m_HomingParameters.homingOffset = 50.0;

		g_Motor4.SetMotorCurrent(30);
		g_Motor4.SetMotorCurrentHold(10);

		initialized2 = true;
	
	return 1;

}

void SetMoveSpeed(uint32_t par, UserFunction* pUserFunction)
{
	g_Motor3.SetMaxSpeed(2000);
	g_Motor3.SetAcceleration(2500.0);

	g_Motor4.SetMaxSpeed(2000);			// 900
	g_Motor4.SetAcceleration(2500.0);  //700
	Serial.println("Set speed!");
	return;

}

uint32_t Homing3and4(uint32_t par, UserFunction* pUserFunction)
{
	g_Motor3.SetCurrentPosition(0);
	g_Motor3.SetTargetPosition(0);
	g_Motor3.ResetRampStatus();
	//vTaskDelay(500);

	g_Motor3.MotorFunction_TiggerStart(MOTOR_FUNCTION_HOMING);
	//pUserFunction->MotorHomingOk(LOCK_MOTOR3, par);
	
	g_Motor4.SetCurrentPosition(0);
	g_Motor4.SetTargetPosition(0);
	g_Motor4.ResetRampStatus();
	//vTaskDelay(500);

	g_Motor4.MotorFunction_TiggerStart(MOTOR_FUNCTION_HOMING);
	pUserFunction->MotorHomingOk(LOCK_MOTOR3 | LOCK_MOTOR4, par);

	g_Motor3.SetMaxSpeed(700);
	g_Motor3.SetAcceleration(900.0);

	g_Motor4.SetMaxSpeed(700);			
	g_Motor4.SetAcceleration(900.0);

	// y axis
	g_Motor4.SetMoveRelative(-1550);

	// x axis
	g_Motor3.SetMoveRelative(-850);

	
	//pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_MOTOR4PosReached);
	//if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false;

	pUserFunction->m_MotorIoEvent.SetAndCondition(MOTORIOEVENT_MOTOR3PosReached |MOTORIOEVENT_MOTOR4PosReached);
	if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false;


	g_Motor3.SetCurrentPosition(150);
	g_Motor3.SetTargetPosition(150);
	g_Motor4.SetCurrentPosition(0);
	g_Motor4.SetTargetPosition(0);

	g_Motor2.SetCurrentPosition(0);
	g_Motor2.SetTargetPosition(0);
	g_Motor1.SetCurrentPosition(0);
	g_Motor1.SetTargetPosition(0);

	// set speed
	SetMoveSpeed(par, pUserFunction);

	Serial.println("END");

	return 1;

}

uint32_t MoveCurve(uint32_t par, UserFunction* pUserFunction) {

	g_Motor1.SetMotorCurrent(100);
	g_Motor1.SetMotorCurrentHold(100);

	g_Motor2.SetMotorCurrent(100);
	g_Motor2.SetMotorCurrentHold(100);

	g_Motor1.SetCurrentPosition(0);	
	//g_Motor1.SetTargetPosition(0);
	g_Motor2.SetCurrentPosition(0);
	//g_Motor2.SetTargetPosition(0);

	g_Motor1.ResetRampStatus();
	g_Motor2.ResetRampStatus();

	g_Motor1.SetMoveRelative(2.8f);
	g_Motor2.SetMoveRelative(-1.4f);

	pUserFunction->m_MotorIoEvent.SetAndCondition(MOTORIOEVENT_MOTOR1PosReached | MOTORIOEVENT_MOTOR2PosReached);
	if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false;

	Serial.println("Moved curved stepps");

	return 1;

}


uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	if (initialized2 == false) MotorInit(par, pUserFunction);
	if (par == 1) Homing3and4(par, pUserFunction);
	if (par == 2) MoveCurve(par, pUserFunction);
	return 1;
}
