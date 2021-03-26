
#include "System.h"
#include "CanMessage.h"
#include <Can.h>
#include <CCmdDecode.h>
#include <CommandUsb.h>
#include <EEprom.h>
#include <Input.h>
#include <Motor.h>
#include <MotorIoEvent.h>

#include <User_Function.h>

#include <Can.h>
#include "ResourceLock.h"



/**
******************************************************************************
* @file    SteppControler.ino
* @author  ErKa
* @brief   
******************************************************************************
* @attention
*
* Copyright(c) 2020 3CI.
* All rights reserved.
*
* This software component is licensed by Tratter under BSD 3 - Clause license,
*the "License"; You may not use this file except in compliance with the
* License.You may obtain a copy of the License at :
*opensource.org / licenses / BSD - 3 - Clause
*
******************************************************************************
*/




#include <Wire.h>
#include  "PortIni.h"



void ExtraInit()
{
	Serial.println("Init ok");
	g_UserFunction[1].TiggerStart(0);
 
	//start things depending on board
//	g_Input1.SetRunFalingFunction(INPUT_RUN_USERFUNCTION_START_1 + 1);
//	g_Input2.SetRunFalingFunction(INPUT_RUN_USERFUNCTION_START_1 + 2);
//	g_Input3.SetRunFalingFunction(INPUT_RUN_USERFUNCTION_START_1 + 3);
//	g_Input4.SetRunFalingFunction(INPUT_RUN_USERFUNCTION_START_1 + 4);
//	g_Input5.SetRunFalingFunction(INPUT_RUN_USERFUNCTION_START_1 + 5);
}



//------------------------------------------------------------------------------
void setup() {
	// Init IO
	g_System.Init(ExtraInit);
}

//------------------------------------------------------------------------------
// WARNING idle loop has a very small stack (configMINIMAL_STACK_SIZE)
// loop must never block
void loop() {
	
	
	
	// Not used.
}
