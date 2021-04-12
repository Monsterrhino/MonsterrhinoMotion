#include "System.h"


//g_UserFunction[0].m_variable[0] -> rotation speed
//g_UserFunction[0].m_variable[1] -> rotation start point angle
//g_UserFunction[0].m_variable[2] -> rotation end point angle
//g_UserFunction[0].m_variable[3] -> linear speed
//g_UserFunction[0].m_variable[4] -> table speed

int run_speed = 400;
int run_speed_bckwd = 120;
int rot_speed = 5;

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
  g_Motor2.LoadMotorParameter();
  g_Motor2.SetMotorCurrent(20);
  g_Motor2.SetMotorCurrentHold(0);
  g_Motor2.Begin();
  // Speed 
  g_Motor2.ResetRampStatus();

  g_Motor1.SetStartup_SenseResistor(220);
  g_Motor2.SetStartup_SenseResistor(220);

  g_Motor3.LoadMotorParameter();
  g_Motor3.SetStartup_SenseResistor(220);
  g_Motor3.SetMotorCurrent(200);
  g_Motor3.SetMotorCurrentHold(0);
  g_Motor3.Begin();
  // Speed 
  g_Motor3.ResetRampStatus();;
  g_Motor3.SetSW_ModeInt(0);
  g_Motor3.SetRampMode((MotorClass::RampMode)g_Motor1.GetStartup_RampMode());
  g_Motor3.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
  
  g_Motor3.SetStartup_SWMode(0); 
  g_Motor3.SetStartup_drvStrength(0);
  g_Motor3.SetStartup_bbmTime(8);
  g_Motor3.SetStartup_bbmClks(0);
// 


  Serial.println("Setup done!");

  return;
}


void Init_Var(UserFunction *pUserFunction){
    // x slider
  g_Motor1.SetCurrentPosition(0.0f);
  g_Motor1.SetTargetPosition(0.0f);
  
  g_UserFunction[0].m_variable[0] = 5;//-> rotation speed
  g_UserFunction[0].m_variable[1] = 330;//-> rotation start point angle 0-360
  g_UserFunction[0].m_variable[2] = 30;//-> rotation end point angle 0-360
  g_UserFunction[0].m_variable[3] = 50;//-> linear speed
  g_UserFunction[0].m_variable[4] = 50;//-> table speed

  
  g_Motor4.LoadMotorParameter();
  g_Motor4.SetStartup_SenseResistor(220);
  g_Motor4.SetMotorCurrent(50);
  g_Motor4.SetMotorCurrentHold(0);
  g_Motor4.Begin();

  // Speed 
  g_Motor4.ResetRampStatus();;
  g_Motor4.SetSW_ModeInt(0);
  g_Motor4.SetRampMode((MotorClass::RampMode)g_Motor1.GetStartup_RampMode());
  g_Motor4.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
  // 
  
  Serial.print("Init variable!");
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
    g_Motor1.SetMaxSpeed(-run_speed_bckwd);
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



uint32_t HomeCameraSlider(uint32_t par, UserFunction* pUserFunction){

  Sub1_Init(pUserFunction);
  vTaskDelay(10);
  
  RunStallGuard(pUserFunction);
  vTaskDelay(10);
  g_UserFunction[1].TiggerStart(3);
  vTaskDelay(50);
  
  while (g_UserFunction[1].m_variable[5] != 1){
    vTaskDelay(10);
    };

  Serial.println("------------ Done homing x! ----------------");

  // Reset to positioning mode
  g_Motor1.SetRampMode(MotorClass::POSITIONING_MODE);
  TMC5160_Reg::COOLCONF_Register coolconf = g_Motor1.GetCOOLCONF();
  TMC5160_Reg::SW_MODE_Register swMode = g_Motor1.GetSW_Mode();
  coolconf.sgt = 5; // -64 .. 63
  g_Motor1.SetCOOLCONF(coolconf);
  swMode.sg_stop = 1;
  vTaskDelay(1000);
  g_Motor1.SetSW_Mode(swMode);
  
  g_Motor1.SetMotorCurrent(30);
  g_Motor1.SetMotorCurrentHold(30);

  Serial.println("------------ Done resetting! ----------------");
  g_Motor2.SetMotorCurrent(10);
  g_Motor2.SetMotorCurrentHold(30);
  
  g_Motor2.SetMaxSpeed(100);
  g_Motor2.SetTargetPosition(10000);
  
  pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_INPUT1_RisingHigh);
  if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false;
  
  g_Motor2.SetCurrentPosition(0.0f);
  g_Motor2.SetTargetPosition(0.0f);

  g_Motor2.SetMoveRelative(40);
  g_Motor2.ResetRampStatus();
  pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_MOTOR2PosReached);
  if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false;
  
  Serial.println("------------ Done homing rotation! ----------------");

  Init_Var(pUserFunction);
  Serial.println("------------ Done init variable! ----------------");
  
  return 1;
  }


uint32_t SetStartPosCameraSlider(uint32_t par, UserFunction* pUserFunction)
{ 
  // reset position
  g_Motor1.SetCurrentPosition(0.0f);
  g_Motor1.SetTargetPosition(0.0f);

  g_Motor2.SetCurrentPosition(0.0f);
  g_Motor2.SetTargetPosition(0.0f);
  g_Motor1.SetMaxSpeed( g_UserFunction[0].m_variable[3]);
  

  

  uint32_t start_angle = g_UserFunction[0].m_variable[1];
  Serial.print("Start angle: ");
  Serial.println(start_angle);
  float start_angle_f = (float) start_angle;
  
  if (start_angle >= 180){
    start_angle_f = (360-start_angle);
    start_angle_f = - start_angle_f;
    Serial.print("Start angle negative: ");
    Serial.println(start_angle_f);
    }
  
  float start_stepps = (start_angle_f/1.8)*5.88;  // Gear ratio 1:5.88
  Serial.print("Start stepps: ");
  Serial.println(start_stepps);
  
  // Go to rotation starting position
  g_Motor2.SetMoveRelative(start_stepps);
  g_Motor2.ResetRampStatus();
  pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_MOTOR2PosReached);
  if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false;

  Serial.println("Ready on start position!");
  
  return 1;
  }


uint32_t RunCameraSlider(uint32_t par, UserFunction* pUserFunction)
{ 

  
  g_Motor1.SetMotorCurrent(30);
  g_Motor1.SetMotorCurrentHold(30);
  // x slider
  g_Motor1.SetCurrentPosition(0.0f);
  g_Motor1.SetTargetPosition(0.0f);
  
  g_Motor1.SetMaxSpeed(g_UserFunction[0].m_variable[3]);
  g_Motor1.SetMoveRelative(-2000);

  // Rotation
  
  uint32_t stop_angle = g_UserFunction[0].m_variable[2];
  Serial.print("Stop angle: ");
  Serial.println(stop_angle);
  float stop_angle_f = (float) stop_angle;
  
  float stop_stepps = (stop_angle_f/1.8)*5.88;  // Gear ratio 1:5.88
  Serial.print("Start stepps: ");
  Serial.println(stop_stepps);
  
  g_Motor2.SetMaxSpeed(g_UserFunction[0].m_variable[0]*0.1
  );

  Serial.println("------------ Running! ----------------");
  
  g_Motor2.SetTargetPosition(stop_stepps);
  g_Motor1.ResetRampStatus();
  g_Motor2.ResetRampStatus();
  pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_MOTOR1PosReached | MOTORIOEVENT_MOTOR2PosReached);
  if (pUserFunction->WaitEvent() == USERFUNCTIONEVENT_EXIT) return false; 
   
  g_Motor4.SetMaxSpeed(0);
  g_Motor2.Stop();
  Serial.println("------------ Finished moving! ----------------");
  
  return 1;
  
}  


uint32_t StartTable(uint32_t par, UserFunction* pUserFunction)
{ 
  //Set ramp mode to "VelocityMode"
  g_Motor4.SetRampMode(MotorClass::RampMode::VELOCITY_MODE);
  g_Motor4.SetMaxSpeed(g_UserFunction[0].m_variable[4]);
  return 1;
  }


uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
  
  Sub1_Init(pUserFunction);

  
  if (par == 1) HomeCameraSlider(par, pUserFunction);
  if (par == 2) Init_Var(pUserFunction);
  if (par == 3) SetStartPosCameraSlider(par, pUserFunction);
  if (par == 4) RunCameraSlider(par, pUserFunction);
  if (par == 5) StartTable(par,pUserFunction);


  if (par == 6) RunStallGuardBackward(pUserFunction);
  if (par == 7) RunBackAndForth(pUserFunction);
  if (par == 8) RunStallGuard(pUserFunction);

  Serial.print("Subcmd: ");
  Serial.println(par);
  
  return 1;
}
