#include "System.h"

int run_speed = 400;

void Sub1_Init(UserFunction *pUserFunction)
{
  // Motor Parameter

  g_Motor1.LoadMotorParameter();
  g_Motor1.SetMotorCurrent(200);
  g_Motor1.SetMotorCurrentHold(0);
  g_Motor1.Begin();
  // Speed 
  g_Motor1.ResetRampStatus();;
  g_Motor1.SetSW_ModeInt(g_Motor1.GetStartup_SWMode());
  g_Motor1.SetRampMode((MotorClass::RampMode)g_Motor1.GetStartup_RampMode());
  g_Motor1.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
  // 
//  pUserFunction->m_variable[5] = 0;
  Serial.println("Setup done!");

  return;
}


uint32_t RunStallGuard(UserFunction *pUserFunction){
   
    g_Motor1.SetRampMode(MotorClass::VELOCITY_MODE);
    TMC5160_Reg::COOLCONF_Register coolconf = g_Motor1.GetCOOLCONF();
    TMC5160_Reg::SW_MODE_Register swMode = g_Motor1.GetSW_Mode();
    g_Motor1.SetMaxSpeed(run_speed);
    g_Motor1.SetModeChangeSpeeds(0, 50, 0);
    coolconf.sgt = 5; // -64 .. 63
    g_Motor1.SetCOOLCONF(coolconf);
    swMode.sg_stop = 1;
    vTaskDelay(1000);
    g_Motor1.SetSW_Mode(swMode);
    Serial.println("SG Active Left!");
   
    return 1;
  
}

uint32_t RunStallGuardBackward(UserFunction *pUserFunction){
   
    g_Motor1.SetRampMode(MotorClass::VELOCITY_MODE);
    TMC5160_Reg::COOLCONF_Register coolconf = g_Motor1.GetCOOLCONF();
    TMC5160_Reg::SW_MODE_Register swMode = g_Motor1.GetSW_Mode();
    g_Motor1.SetMaxSpeed(-run_speed);
    g_Motor1.SetModeChangeSpeeds(0, 50, 0);
    coolconf.sgt = 5; // -64 .. 63
    g_Motor1.SetCOOLCONF(coolconf);
    swMode.sg_stop = 1;
    vTaskDelay(1000);
    g_Motor1.SetSW_Mode(swMode);
    Serial.println("SG Active Right!");
    return 1;
  
}

uint32_t RunBackAndForth(UserFunction *pUserFunction){

for (int i=0; i<10; i++){

  Sub1_Init(pUserFunction);
  vTaskDelay(10);
  
  RunStallGuard(pUserFunction);
  vTaskDelay(10);
  g_UserFunction[1].TiggerStart(3);
  vTaskDelay(50);
  
  while (g_UserFunction[1].m_variable[5] != 1){
//    Serial.print("variable: ");
//    Serial.println(g_UserFunction[3].m_variable[5]);
    vTaskDelay(10);
    };
    
  Serial.println("------------ Done running! ----------------");
  
  
  Sub1_Init(pUserFunction);
  vTaskDelay(10);
  
  RunStallGuardBackward(pUserFunction);
  
  vTaskDelay(10);
  g_UserFunction[1].TiggerStart(3);
  vTaskDelay(50);
  
  while (g_UserFunction[1].m_variable[5] != 1){
//    Serial.print("variable: ");
//    Serial.println(g_UserFunction[3].m_variable[5]);
    vTaskDelay(10);
    };
    
  Serial.println("------------ Done running 2! ----------------");
  Serial.print("i= ");
  Serial.println(i);
}
  
  return 1;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
  
  Sub1_Init(pUserFunction);
  if (par == 1) RunStallGuard(pUserFunction);
  if (par == 2) RunStallGuardBackward(pUserFunction);
  if (par == 3) RunBackAndForth(pUserFunction);
  
  return 1;
}
