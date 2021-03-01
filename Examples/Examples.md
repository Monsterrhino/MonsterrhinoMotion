---
title: "Monsterrhino Motion: EXAMPLES"
output: 
  bookdown::html_document2:
    toc: true
    toc_float: true
    fig_caption: true
---

# Getting started

MonsterrhinoMotion features three main ways to be controlled:  

## USB
UART is the simplest way to give commands. MonsterrhinoMotion can be controlled directly, out of the box, via UART-communication.  

Just open the serial command window and select the following settings and the COM-port of your MonsterrhinoMotion.  
After a successful connection with your MonsterrhinoMotion you can send commands as shown here:  
(**Attention:** Motion needs to be in normal mode **not** boot mode! Led is blinking)
```
m1tp 100  (Motor 1 target point 100 steps)
m3mr 200  (Motor 3 move relative 200 steps)
m2ma 100  (Motor 2 set motor current to 100mA)

m3ma ?    (Motor 3 returns motor current in mA)
m2cp ?    (MOtor 2 returns current position)
```
**Note:** A list of all UART-commands can be found in the documentation (~/Documentation).

## CAN
CAN is a commonly used communication system in automotive, automation and others.  
Due to its high reliability and higher speed than UART it can be used to communicate with the Motion from another Motion or, as an example, a RaspberryPi or Arduino (with their CAN-module).
For further information see the documentation (~/Documentation).

[TODO: Insert image of simple CAN functionality]: <>

## Programming the Motion
It is possible to program various functions on the Motion, this enables a fully autonomous and dynamic system.  
The main structure of the code consists of six "UserFunction" files (User_Function1.cpp) and the main file ("monsterrhinostep.ino").  

- **"monsterrhinostep.ino":** The "main" file is used to declare main initialization as interrupt actions. Its similar to the Arduino "void setup()"" function.  
- **"User_Function(X).cpp":** A total of six "UserFunctions" are used for programming actions. They can be executed simultaneously.

The following examples show you how to program easy movements of stepper motors, changing motor behavior,... .  

[TODO: Insert image of file blocks main, userfunc1,etc]: <>

# Programming examples

This documentation shows you easy and more complex ways to program a MonsterrhinoMotion.

## Motor setup
*(~/ExamplesCpp/Example1_MotorSetup.cpp)*

To run a stepper motor, first you need to set up the main motor parameters as motor current, speed, acceleration and others.
As you can see in the following code a task needs to start in one of the six "UserFunctions":  

```C++
void MotorInit()
{
	g_Motor1.LoadMotorParameter();		//Loads default motor values (SenseResitor, Current, ...)

	g_Motor1.SetMotorCurrent(100);		//Motor current in mA (0.001 Ampere)
	g_Motor1.SetMotorCurrentHold(50);	//Motor standstill current

	g_Motor1.Begin();					        				

	g_Motor1.ResetRampStatus();			  //Reset RampStatus flags and set ramp Speed/Acceleration to default
	g_Motor1.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
	g_Motor1.SetAccelerations(g_Motor1.GetStartup_AccelerationsAMax(), g_Motor1.GetStartup_AccelerationsDMax(), g_Motor1.GetStartup_AccelerationsA1(), g_Motor1.GetStartup_AccelerationsD1());
	
	return;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
  MotorInit(); //Motor initialization
  return 1;
}
```
In the following examples the function "MotorInit" is used but not shown.  

## Target position
*(~/ExamplesCpp/Example2_TargetPosition.cpp)*  

With the motor-command **SetTargetPosition** you can choose a desired position of your motor, which it will reach.  

```C++  
//FILE: "User_Function1.cpp"
uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	MotorInit();									
	//Motor initialization

	g_Motor1.SetTargetPosition(100);			
	//Sets motor1 target position -> motor runs (unless its already at that position)

	return 1;
}
```
Similar motor-commands are:  
```C++  
g_Motor1.SetCurrentPosition(10);  
//Sets current motor position to value 10; no motor movement

g_Motor1.SetMoveRelative(150);  
//Motor moves 150 steps relative from current position
```
## Homing
*(~/ExamplesCpp/Example3_Homing.cpp)*  

Homing is used to have a reference point in your mechanical system. After successful homing you have the start point of your system.  
As an example a 3d printer uses two-axis homing to get the XY-system start point (X=0, Y=0).  

In homing you can set various parameters to adjust speed, acceleration, offset and many more. This can be programmed as shown here:  
```C++
//FILE: "User_Function1.cpp"
void HomingInit()
{
	g_Motor1.m_HomingParameters.mode = 1;
	g_Motor1.m_HomingParameters.rampSpeedHold = 150.0;
	g_Motor1.m_HomingParameters.accelerationsD1 = 100.0;
	g_Motor1.m_HomingParameters.accelerationsA1 = 100.0;
	g_Motor1.m_HomingParameters.accelerationsAmax = 100.0;
	g_Motor1.m_HomingParameters.accelerationsDmax = 100.0;
	g_Motor1.m_HomingParameters.rampSpeed_2 = 80.0;
	g_Motor1.m_HomingParameters.rampSpeedStart = 60.0;
	g_Motor1.m_HomingParameters.homingOffset = 15.0;

	return;
}
```
After the homing initialization you can begin with the homing action:
```C++
//FILE: "User_Function1.cpp"
uint32_t Homing(uint32_t par, UserFunction* pUserFunction)
{
	//Reset ramp status and current/target position and wait 500ms to be sure
	g_Motor3.SetCurrentPosition(0);
	g_Motor3.SetTargetPosition(0);
	g_Motor3.ResetRampStatus();
	vTaskDelay(500);
	
	g_Motor3.MotorFunction_TiggerStart(MOTOR_FUNCTION_HOMING);
	pUserFunction->MotorHomingOk(LOCK_MOTOR3, par);

	return 1;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	MotorInit();	//Motor initialization
	HomingInit();	//Homing initialization

	Homing(par, pUserFunction);

	return 1;
}
```

## Input
*(~/ExamplesCpp/Example4_Input.cpp)*  

The MonsterrhinoMotion is able to read 12 digital inputs. These inputs can be set as an interrupt or can be controlled during a process manually.

An interrupt reacts either to a rising or falling edge of the input pin (LOW->HIGH or HIGH->LOW). If this event occurs a selected action can be chosen.  

In this example we use "input1" with a rising event (event is active when input changes from low to high). As action we choose the start of Userfunction2:
```C++
//FILE: "monsterrhinostep.ino"
void ExtraInit()
{
	g_Input1.SetRunRisingFunction(INPUT_RUN_USERFUNCTION_START_2);
}
```
More options for an interrupt declaration can be found in the documentation.

# CAN examples