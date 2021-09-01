#include "System.h"

/*
 * ZirkonZahn Scanner
 * 
 * Last function in this file is "UserFunction1(par,pUserfunction)", this function is called when a button is pressed. Parameter "par" decides what function is executed (see "if" calls in userfunction1)
 * 
 * pose(..)-Function makes it possible to give a pose (x,z,a,b)
 * pose1(..)-Function makes it possible to give a pose (x,z,a) and set the speed for b-axis
 * 
 * Motors should be homed automatically for each other function (not testet perfectly).
 * NEVER move a motor manually and then start a function, always make HomeAll before.
 */


//X: R+ L-
//Z: U+ D-
//A: CW+ CCW-
//B: CH+ ROT-

//Speed limitation for each axis
#define X_SPEED         300
#define Y_SPEED         300

//Offset steps for each axis
#define X_OS   -65
#define Y_OS   -20

//Accelerations
#define X_ACC           1500
#define Y_ACC           1500

//Motor current
#define X_MA  100
#define Y_MA  100

//limits for pose
#define X_LIM   10
#define Y_LIM   10

//steps for full axis
#define X_FULL   20
#define Y_FULL   10

#define X_START -10
#define Y_START 4

// Motor 1 -> y axis rotate table
// Motor 2 -> x axis positive down

// Y +U -D
// X -R +L

bool x_homed = false;
bool y_homed = false;

bool all_homed = false;
bool first_homed = false;

bool flip = true;

//Initalize motors
void InitMotors(UserFunction* pUserFunction)
{
    g_Motor1.ResetRampStatus();
    g_Motor2.ResetRampStatus();
    
    // Motor 1 -> y axis
    g_Motor1.m_HomingParameters.mode = 2;
    g_Motor1.m_HomingParameters.rampSpeedHold = Y_SPEED/2;
    g_Motor1.m_HomingParameters.rampSpeed_2 = Y_SPEED/4;
    g_Motor1.m_HomingParameters.homingOffset = Y_OS;
    g_Motor1.m_HomingParameters.rampSpeed = Y_SPEED;
    g_Motor1.m_HomingParameters.accelerationsDmax = Y_ACC;
    g_Motor1.m_HomingParameters.accelerationsD1 = Y_ACC;
    g_Motor2.m_HomingParameters.multiple_homing = false;

    g_Motor1.SetMotorCurrent(Y_MA);
    g_Motor1.SetMotorCurrentHold(30);
    g_Motor1.SetMaxSpeed(Y_SPEED);
    g_Motor1.SetAcceleration(Y_ACC);

    // Motor 2 -> x axis
    g_Motor2.m_HomingParameters.mode = 2;
    g_Motor2.m_HomingParameters.rampSpeedHold = X_SPEED/2;
    g_Motor2.m_HomingParameters.rampSpeed_2 = X_SPEED/4;
    g_Motor2.m_HomingParameters.homingOffset = X_OS;
    g_Motor2.m_HomingParameters.rampSpeed = X_SPEED;
    g_Motor2.m_HomingParameters.accelerationsDmax = Y_ACC;
    g_Motor2.m_HomingParameters.accelerationsD1 = Y_ACC;
    g_Motor2.m_HomingParameters.multiple_homing = false;

    g_Motor2.SetMotorCurrent(X_MA);
    g_Motor2.SetMotorCurrentHold(30);
    g_Motor2.SetMaxSpeed(X_SPEED);
    g_Motor2.SetAcceleration(X_ACC);

    Serial.println("Init motors done");

    // Set limit switch enabled left and right
    TMC5160_Reg::SW_MODE_Register swMode;
    swMode.stop_l_enable = 1;
    //stop left enable
    swMode.stop_r_enable = 1;
    //stop right enable
    //g_Motor2.SetSW_Mode(swMode);
    return;
}

uint32_t homeX(uint32_t par, UserFunction* pUserFunction) {

    InitMotors(pUserFunction);
    Serial.println("X homing started...");

    // Start homing
    g_Motor2.MotorFunction_TriggerStart(MOTOR_FUNCTION_HOMING);
    pUserFunction->MotorHomingOk(LOCK_MOTOR2, par);
    
    Serial.println("X homing done!");
    x_homed = true;
    return 1;
}

uint32_t homeY(uint32_t par, UserFunction* pUserFunction) {

    InitMotors(pUserFunction);
    Serial.println("Y homing started...");

    // Start homing
    g_Motor1.MotorFunction_TriggerStart(MOTOR_FUNCTION_HOMING);
    pUserFunction->MotorHomingOk(LOCK_MOTOR1, par);
    
    Serial.println("Y homing done!");
    y_homed = true;
    return 1;
}

uint32_t homeAll_1(uint32_t par, UserFunction* pUserFunction) {

    homeX(par,pUserFunction);
    homeY(par,pUserFunction);
    all_homed = true;
    return 1;
}

uint32_t homeAll(uint32_t par, UserFunction* pUserFunction) {

    InitMotors(pUserFunction);
    Serial.println("XY homing started...");

    // Start homing
    g_Motor1.MotorFunction_TriggerStart(MOTOR_FUNCTION_HOMING);
    g_Motor2.MotorFunction_TriggerStart(MOTOR_FUNCTION_HOMING);
    pUserFunction->MotorHomingOk(LOCK_MOTOR1, par);
    pUserFunction->MotorHomingOk(LOCK_MOTOR2, par);
    
    Serial.println("XY homing done!");
    x_homed = true;
    y_homed = true;
    all_homed = true;
    first_homed = true;
    return 1;
}

uint32_t homeAll_2(uint32_t par, UserFunction* pUserFunction) {

    InitMotors(pUserFunction);
    Serial.println("XY homing started...");

    // Start homing
    g_Motor1.MotorFunction_TriggerStart(MOTOR_FUNCTION_HOMING);
    g_Motor2.MotorFunction_TriggerStart(MOTOR_FUNCTION_HOMING);
    pUserFunction->MotorHomingOk(LOCK_MOTOR1, par);
    pUserFunction->MotorHomingOk(LOCK_MOTOR2, par);
    
    Serial.println("XY homing done!");
    x_homed = true;
    y_homed = true;
    all_homed = true;
    first_homed = true;

    pose(par,pUserFunction,X_START, Y_START);
    g_Motor1.SetCurrentPosition(0);
    g_Motor1.SetTargetPosition(0);
    g_Motor2.SetCurrentPosition(0);
    g_Motor2.SetTargetPosition(0);

    x_homed = true;
    y_homed = true;
    all_homed = true;
    first_homed = true;
    return 1;
}

void checkState(double x,double y){
    //to check if we are in homed position
    if(x==0){
      x_homed = true;
    }else{
      x_homed = false;
    }

    if(y==0){
      y_homed = true;
    }else{
      y_homed = false;
    }
    
    if((x_homed)&&(y_homed)){
      all_homed = true;
    }else{
      all_homed = false;
    }
}

uint32_t pose(uint32_t par, UserFunction* pUserFunction, double x_pos, double y_pos) {

    if(abs(x_pos)>X_LIM) {Serial.print("X pos over limit:");Serial.println(x_pos); x_pos=0;}
    if(abs(y_pos)>Y_LIM) {Serial.print("Y pos over limit:");Serial.println(y_pos); y_pos=0;}
    
    InitMotors(pUserFunction);
    Serial.println("New pose:");
    Serial.print("x->");Serial.println(x_pos);
    Serial.print("y->");Serial.println(y_pos);

    g_Motor1.SetMaxSpeed(Y_SPEED*2);
    g_Motor2.SetMaxSpeed(Y_SPEED*2);
    
    g_Motor1.SetTargetPosition(y_pos);
    g_Motor2.SetTargetPosition(x_pos);

    if (pUserFunction->SetTargetPosition_MotorWait(g_Motor1, y_pos) == USERFUNCTIONEVENT_EXIT) return false;
    if (pUserFunction->SetTargetPosition_MotorWait(g_Motor2, x_pos) == USERFUNCTIONEVENT_EXIT) return false;
    
    Serial.println("Pose movement done!");

    checkState(x_pos,y_pos);
    
    return 1;
}

void rect(uint32_t par, UserFunction* pUserFunction, double x_pos, double y_pos){
  pose(par, pUserFunction,x_pos,y_pos);
  pose(par, pUserFunction,x_pos,-y_pos);
  pose(par, pUserFunction,-x_pos,-y_pos);
  pose(par, pUserFunction,-x_pos,y_pos);
  pose(par, pUserFunction,x_pos,y_pos);
  //pose(par, pUserFunction,0,0);
}

void raute(uint32_t par, UserFunction* pUserFunction, double x_pos, double y_pos){
  pose(par, pUserFunction,x_pos,0);
  pose(par, pUserFunction,0,-y_pos);
  pose(par, pUserFunction,-x_pos,0);
  pose(par, pUserFunction,0,y_pos);
  pose(par, pUserFunction,x_pos,0);
  //pose(par, pUserFunction,0,0);
}

uint32_t demo1(uint32_t par, UserFunction* pUserFunction) {

    if(!all_homed){
      homeAll(par,pUserFunction);
    }
    Serial.println("Demo 1 started...");
    //pose(par, pUserFunction, x_pos,y_pos);
    
    //X: R+ L-
    //Y: U+ D-
    double y_pos = 1.5;
    double x_pos = 4;
    long del = 0;
    
    for(int i=0; i<5;i++){
      rect(par, pUserFunction,x_pos,y_pos);
    }

    vTaskDelay(1000);
    
    for(int i=0; i<5;i++){
      raute(par, pUserFunction,x_pos,y_pos);
    }

    vTaskDelay(1000);
    pose(par, pUserFunction,0,0);
    Serial.println("Demo 1 done!");
    return 1;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
    
    if (par == 1) homeX(par, pUserFunction);
    if (par == 2) homeY(par, pUserFunction);
    if (par == 3) homeAll(par, pUserFunction);
    if (par == 4) homeAll_2(par, pUserFunction);
    if (par == 5) demo1(par, pUserFunction);
    if (par == 6) pose(par, pUserFunction,10,10);
    return 1;
}
