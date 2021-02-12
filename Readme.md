# Monsterrhino Motion Examples

This documentation shows you easy and more complex ways to programm a Monsterrhino Motion.

## 1) Motor setup
*(~/ExamplesCpp/Example1_MotorSetup.cpp)*

To run a stepper motor, first you need to set up the main motor parameters like motor current, speed, acceleration and others.
As you can see in the following code every task needs to start in a "UserFunction":  

```C++
uint32_t MotorInit(uint32_t par, UserFunction* pUserFunction)
{
	g_Motor1.LoadMotorParameter();
	g_Motor1.SetMotorCurrent(100);
	g_Motor1.SetMotorCurrentHold(50);
	g_Motor1.Begin();
	g_Motor1.ResetRampStatus();
	g_Motor1.SetRampSpeeds(g_Motor1.GetStartup_RampSpeedsStart(),  g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()); //Start, stop, threshold speeds
	g_Motor1.SetAccelerations(g_Motor1.GetStartup_AccelerationsAMax(), g_Motor1.GetStartup_AccelerationsDMax(), g_Motor1.GetStartup_AccelerationsA1(), g_Motor1.GetStartup_AccelerationsD1()); //AMAX, DMAX, A1, D1

	return 1;
}

uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
  MotorInit(par, pUserFunction); //Motor initialization
  return 1;
}
```
## 2) Target position
*(~/ExamplesCpp/Example2_TargetPosition.cpp)*
With the motor-command **SetTargetPosition** you can choose a desired position of your motor, which it will reach.  

```C++  
uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
{
	MotorInit();									//Motor initialization

	g_Motor1.SetTargetPosition(100);			
	//Sets motor1 target position -> motor runs (unless its already at that position)

	return 1;
}
```
Similar motor-commands are:  
```C++  
g_Motor1.SetCurrentPosition(10);  //Sets current motor position to value 10

g_Motor1.SetMoveRelative(150);  //Motor moves 150 steps relative from current position


```
## 3) Homing
*(~/ExamplesCpp/Example3_Homing.cpp)*  
With the motor-command **SetTargetPosition** you can choose a desired position of your motor, which it will reach.  

```C++
static void HomingInit()
{
	g_Motor1.m_HomingParameters.mode = 1;
	g_Motor1.m_HomingParameters.rampSpeedHold = 150.0; //can not be more other wise it smashes into endswitch
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
```C++

}
```

### 1-Axis Homing

### 2-Axis Homing (simultaneously)

## Encoder



1     |2    |Address|Board ID
-     |-    |-     |-
LOW   |LOW  |   2  |0
HIGH  |LOW  |   3  |1
LOW   |HIGH |   4  |2
HIGH  |HIGH |   5  |3

## Examples

* Roboterarm
* 3D-printer

## TODO
