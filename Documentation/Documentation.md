---
title: "Monsterrhino Motion: DOCUMENTATION"
output: 
  bookdown::html_document2:
    toc: true
    toc_float: true
    fig_caption: true
---

<!-- ![](Images/Monsterrhino_Images/logo.png){width=20%}  -->

<p align="center">
  <img width="100" src="Images/Monsterrhino_Images/logo.png">
</p>

<p align="center">
  <img width="500" src="Images/Motion_Illustrated.png">
</p>



# General
**Monsterrhino Motion** is an independent stepper motor controller.  
It can run up to 4 stepper motors at once - in parallel. The powerful MCU combined with our advanced firmware (multitasking capable - up to 6 user tasks) allows you to control stepper motors in the most simple way - you can program it with the Arduino IDE or with more advanced IDEs. Our firmware allows you to program the card at a high level e.g. you tell the motor to rotate continuously, make a 100 steps, etc. Further key features are limit switch connectors for each motor, encoder connectors, digital sensor inputs and digital/analog outputs. 
The CAN interface offers reliable high performance communication with other devices such as Monsterrhino Motion, Monsterrhino Control, Raspberry Pi, Arduino and many more.

Specs:  

- **4** Stepper motors
- **12** digital inputs
- **1** digital output
- **3** analog outputs
- **



## Programming the Motion
It is possible to program various functions on the Motion, this enables a fully autonomous and dynamic system.  
The main structure of the code consists of six "UserFunction" files (User_Function1.cpp) and the main file ("monsterrhinostep.ino").  

The following image shows you the **main structure** of the files used to program the Motion:

![](Images/ProgrammingStructure.png)

**Note:** The loop function is **not used**, because all processes and actions are programmed in the "Userfunctions" that can be executed simultaneously.

### "monsterrhinostep.ino"-file
This file is used for main initialization.  
Example:
```C++
#include <Wire.h>
#include  "PortIni.h"

void ExtraInit()
{
	g_Input1.SetRunRisingFunction(INPUT_RUN_USERFUNCTION_START_2 + 1);
	//set Input1 interrupt at rising edge, Start userfunction 2 with parameter par=1
}
//------------------------------------------------------------------------------
void setup() {
	// Init IO
	g_System.Init(ExtraInit);
	ExtraInit();
}
```

### User Function
The six "UserFunction"-files can be programmed for any action. They can be started and stopped by inputs, CAN-commands, UART-commands or other userfunctions.  

```
Serial commands:
f1s1
//Start UserFunction1 with parameter par=1
f2s2
//Start UserFunction2 with parameter par=2 (even if function1 is not finished)
f1t
//Stop UserFunction1
```

Functions to start or stop other UserFunctions are:
  
```C++
TODO
```

# Motor control
## Ramp behavior

![Ramp behaviour (Datasheet TMC5160/A)](Images/TMC5160_rampBeh.png)

Following the ramp behavior you can adjust the parameters:  

* **Acceleration:** Start(A1) and Max(Amax)
* **Deceleration:** Final(D1) and Max(Dmax)
* **MaxSpeed:** From 0 to ?
* **RampSpeed:** Start,Stop,Hold  

An example to set these parameters (with the startup values) is shown here.
```C++
g_Motor1.SetRampSpeeds(
g_Motor1.GetStartup_RampSpeedsStart(), g_Motor1.GetStartup_RampSpeedsStop(), g_Motor1.GetStartup_RampSpeedsHold()
); //V1,VMAX, VSTOP

g_Motor1.SetAccelerations(
g_Motor1.GetStartup_AccelerationsAMax(), g_Motor1.GetStartup_AccelerationsDMax(), g_Motor1.GetStartup_AccelerationsA1(), g_Motor1.GetStartup_AccelerationsD1()
); //AMAX, DMAX, A1, D1
```

**Note:** Value *Vstart* is default zero.  
**See also:** Serial [Motor commands] ramp mode (*m1rs,m1rc, m1as*)

## Ramp mode
```C++
g_Motor1.SetRampMode(MotorClass::RampMode::POSITIONING_MODE);
g_Motor1.SetRampMode(MotorClass::RampMode::VELOCITY_MODE);
g_Motor1.SetRampMode(MotorClass::RampMode::HOLD_MODE);
```

There are three different ramp modes:  

* **[Positioning mode]:** Motor turns til it reached its target point.  
* **[Velocity mode]:** Motor velocity to max speed.
* **[Hold mode]:** Velocity remains unchanged, unless stop event occurs. 

**See also:** Serial [Motor commands] ramp mode (*m1rm (v,p,h or ?)*)

### Positioning mode

This is the normal mode for a stepper motor.
These two functions describe the main action that can be programmed:  

* **TargetPosition**
* **MoveRelative**  

```C++
g_Motor1.SetTargetPosition(200.0);  
//Set target position to 200 steps (double value)
g_Motor1.SetMoveRelative(10.0);     
//Set target position 10 steps relative from current position
```

### Velocity mode  
In this mode the motor turns with the maximum speed.
```C++
g_Motor1.SetRampMode(MotorClass::RampMode::VELOCITY_MODE)
//Set ramp mode to "VelocityMode"
g_Motor1.SetMaxSpeed(100);
//Set maximum speed to 100 steps/sec
```

**Note:** When changed to this mode, max speed is zero. To begin set **max speed** to a value greather than 0.  

### Hold mode

In this mode velocity remains unchanged, unless a stop event occurs.
If you change velocity after ramp mode was set to hold mode nothing happens.

## Startup parameters

Motors have many values that are set default after reset.  
These values can be set with serial [Motor commands] or in the code. After you change one of the startup values you need to save the parameters with the serial command "s save".  
The command "m1st ?" returns a list of all parameters.

```
Serial commands:
m1st sr 100   
//Set motor1 startup value of senseResisor to 100 Ohm
s save        //System save
```

In the following list you can find all motor startup values. They can be read or set with these two functions:
**SetStartup_** or **GetStartup_**  
```C++
g_Motor1.SetStartup_SenseResistor(200);
//Set startup value for motor1 senseResistor to 200 Ohms
```

Function|Description
---|------
drvStrength           |
bbmTime               |
bbmClks               |
SenseResistor         |Resistor for current measuring in mOhm
MotorCurrent          |Motor current in mA
MotorCurrentReduction |
Freewheeling          |Reduce motor current to 0mA in standstill
Iholddelay            |
PwmofsInitial         |
PwmGradInitial        |
StepperDirection      |Direction of stepper motor
MotorSteps            |Full steps of stepper motor
PWMThrsInt            |
PWMThrs               |
COOLThrsInt           |
COOLThrs              |
HighThrs              |
HighThrsInt           |
SWMode                |see [Limit switch]
RampMode              |see [Ramp mode]
RampMaxSpeed          |Vmax ([Ramp behavior])
RampMaxSpeedInt       |Vmax integer ([Ramp behavior])
RampSpeedsStartInt    |Vstart integer ([Ramp behavior])
RampSpeedsStart       |Vstart ([Ramp behavior])
RampSpeedsHoldInt     |V1 integer ([Ramp behavior])
RampSpeedsHold        |V1 ([Ramp behavior])
RampSpeedsStopInt     |Vstop integer ([Ramp behavior])
RampSpeedsStop        |Vstop ([Ramp behavior])
AccelerationsAMaxInt  |Maximal acceleration integer
AccelerationsAMax     |Maximal acceleration
AccelerationsDMaxInt  |Maximal deceleration integer
AccelerationsDMax     |Maximal deceleration
AccelerationsA1Int    |Initial acceleration integer
AccelerationsA1       |Initial acceleration
AccelerationsD1Int    |Initial deceleration integer
AccelerationsD1       |Initial deceleration
HomingMode            |See parameter "mode" in [Homing]
HomingOffsetInt       |Homing offset integer
HomingOffset          |Homing offset
HomingMaxPos          |Homing max. position
HomingTimeout         |Homing timeout
HomingSpeed2Int       |Homing speed second contact integer
HomingSpeed2          |Homing speed second contact
HomingDmaxInt         |Homing max deceleration integer
HomingDmax            |Homing max deceleration
COOLCONF              |
                      |
EncoderResolution     |
EncoderAlloweddeviation|
EncoderSetup          |
EncoderInverted       |

## Limit switch

![](Images/LS.gif)

It is possible to use various types for limit sensing:  

* **Limit switch:** Two limit switches per motor, can be of any type (mechanical, inductive, ...).  
Connection through the corresponding JST-XH connector CN[6,8,10,12] (for Motor 1,2,3,4)  
* **Sensorless:** The motor stops at a set force on the motor shaft.

Properties for motor limit switch configuration are set with following parameters:  

* **stop_l_enable:**  Enable automatic motor stop during active left reference switch input
* **stop_r_enable:**  Enable automatic motor stop during active right reference switch input
* **pol_stop_l:** Sets the active polarity of the left reference switch input (1=inverted, low active, a low level on REFL stops the motor)
* **pol_stop_r:** Sets the active polarity of the right reference switch input (1=inverted, low active, a low level on REFR stops the motor
* **swap_lr:**  Swap the left and the right reference switch inputs
* **latch_l_inactive:** Activate latching of the position to XLATCH upon an inactive going edge on REFL
* **latch_r_inactive:** Activate latching of the position to XLATCH upon an inactive going edge on REFR
* **latch_l_active:** Activate latching of the position to XLATCH upon an active going edge on REFL
* **latch_r_active:** Activate latching of the position to XLATCH upon an active going edge on REFR
* **en_latch_encoder:** Latch encoder position to ENC_LATCH upon reference switch event
* **sg_stop:** Enable stop by stallGuard2 (also available in dcStep mode). Disable to release motor after stop event.
* **en_softstop:** Enable soft stop upon a stop event (uses the deceleration ramp settings)

Example:  
```
Serial commands:
m1swm sle 1   
//Motor1 stop left enable
m1swm sre 1   
//Motor1 stop right enable
m1tp 10000
//Motor turns to targetPos 10000
//if the right limit switch is activated the motor stops (position not reached!)
```
or  
```C++
TMC5160_Reg::SW_MODE_Register swMode;
swMode.stop_l_enable = 1;
//stop left enable
swMode.stop_r_enable = 1;
//stop right enable
g_Motor1.SetSW_Mode(swMode);
//set selected options for motor1 swMode

g_Motor1.SetTargetPosition(1000);
//Set target position to 1000
```

## Special functions  

Special functions are stall guard, coolStepping, power stage tuning and stealth chop.

## Events
Events provide the machine to react on different actions depending on motor status, user function status, input status and time.  

```C++
pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_MOTOR1PosReached);
//TODO: Add other examples
```
# Homing

![](Images/Homing.gif)

Homing has four main steps:  

1) **First contact** with limit switch  
2) Get **safety distance**: Go away 50 steps from first contact (with changed direction)  
3) **Second contact** with **slower** speed (*rampSpeed_2*)  
4) **Offset** after second contact (*homingOffset*, with changed direction)  

Homing can be configured with the following parameters:  

```C++
g_Motor1.m_HomingParameters.mode = 1;
g_Motor1.m_HomingParameters.rampSpeedHold = 200.0;
g_Motor1.m_HomingParameters.homingOffset = 15.0;
```  
* **mode:** homing on the left (1) or right (2) side. 0 is homing off.
* **timeOut:** Timeout without successful homing
* **maxPos:** Maximal position without successful homing  (in microsteps)
* **rampSpeed:** Initial speed in homing (step 1); default is Default_Startup_MaxSpeed
* **rampSpeed_2:** Speed in step 3: second contact
* **homingOffset:** Offset from actual switch position
* **rampSpeedStart:** 
* **rampSpeedStop:**  
* **rampSpeedHold:**  
* **accelerationsAmax:** Maximum acceleration
* **accelerationsDmax:**  Maximum deceleration
* **accelerationsA1:**  Start acceleration
* **accelerationsD1:**  Finish deceleration

**Note:**  
In step 2, if switch is still pressed after 50 steps, this step will repeat.  
In step 3, motor turns 100 steps til it reaches the limit switch, otherwise there is a homing error.
The motor gets set in POSITIONING MODE when homing. 
Step 4 speed is startup_maxSpeed.

TODO: Latched pos ?

## Normal homing
When setting the "MOTOR_FUNCTION_HOMING" start-trigger, the motor begins homing with the **pre-selected** parameters.  
The next command is to keep the motor locked until the homing event is finished.  

```C++
g_Motor3.MotorFunction_TiggerStart(MOTOR_FUNCTION_HOMING);
pUserFunction->MotorHomingOk(LOCK_MOTOR3, par);
```
## Sensorless homing
It is also possible to home without limit switches using StallGuard2.  
TODO

# Input
  
**Interrupts** are used to perform an action when the selected input is triggered, either on the **falling** or **rising** edge.  
The following function can be coded in the **ExtraInit-Function** (monsterrhinostep.ino). In this case the interrupt is activated after a reset.

```C++
g_Input1.SetRunFallingFunction(INPUT_RUN_MOTOR_STOP_1);
```
**Actions:**
These are the defined values for an action, beginning with **INPUT_RUN_**:  
  
- NONE  
- USERFUNCTION_START_*[UserFunctionNr]* + *[SubFunctionNr]*  
- USERFUNCTION_STOP_*[UserFunctionNr]*  +	*[SubFunctionNr]*  
- MOTOR_STOP_[MOTOR_NR]  
- MOTOR_EMERGENCYSTOP_[MOTOR_NR] 
    
**Note:** All combinations are possible when using a motor action.  
 
```C++
g_Input1.SetRunFallingFunction(INPUT_RUN_MOTOR_STOP_1);
//Stop motor 1 at falling edge on input 1

g_Input2.SetRunRisingFunction(INPUT_RUN_MOTOR_STOP_2_3_4);
//Stop motor 2,3 and 4 at rising edge on input 2

g_Input3.SetRunRisingFunction(INPUT_RUN_MOTOR_STOP_1_2_3_4);
//Stop motor 1,2,3 and 4 at rising edge on input 3

g_Input4.SetRunFallingFunction(INPUT_RUN_USERFUNCTION_1 + 2); 
//Start user function 1 sub 2 (parameter Par=2) at falling edge on input 4
```  
The state of an input can also be read with the digitalRead-function.  
```C++
if(digitalRead(g_Input1)==1){
  Serial.print("Hello world");
}
```
Example:
![](Images/Input.gif)
```C++
//FILE "monsterrhinostep.ino":
void ExtraInit(){
  g_Input1.SetRunFallingFunction(INPUT_RUN_MOTOR_STOP_1);
  g_Motor1.SetTargetPosition(1000);
  return;
}

//FILE "User_Function1.cpp":
uint32_t UserFunction1(uint32_t par, UserFunction* pUserFunction)
  g_Motor1.SetTargetPosition(0);
  return 1;
}

```
**see also:** [Input commands]

# Communication
This board offers two main types of communication:  

* **Serial:** U(S)ART is used to communicate with lower speed.
* **CAN:**  CAN (common in automotive) is used to communicate faster and without failure.

## Serial U(S)ART

UART is the simplest way to give commands. MonsterrhinoMotion can be controlled directly, out of the box, via UART-communication.  

Just open the serial command window and select the following settings and the COM-port of your MonsterrhinoMotion.  
After a successful connection with your MonsterrhinoMotion you can send commands as shown here:  

Serial communication is possible via USB. The following properties should be set to ensure correct data transfer:

* U(S)ART support: generic 'Serial'
* Line ending: Both CR & LF
* Baud rate: 115200

The serial command is build as follows:  

function + Nr + subFunction (+optional: value/subFunction2 + value)

```
m1tp 100  (Motor 1 target point 100 steps)
m3mr 200  (Motor 3 move relative 200 steps)
m2ma 100  (Motor 2 set motor current to 100mA)

m3ma ?    (Motor 3 returns motor current in mA)
m2cp ?    (MOtor 2 returns current position)
```
**Attention:** Motion needs to be in normal mode **not** boot mode! Led is blinking


### Motor commands

function|subfunction1|subfunction1|subfunction2/value
-|--|---         |-----
m|tp  |targetpos         |(value) or (?)
m|cp  |currentpos        |(value) or (?)
m|rm  |rampmode          |v,p,h or (?)
m|ms  |maxspeed          |(value) or (?)
m|cs  |currentspeed      |(?)
m|r   |register          |Controller Register?
m|rs  |rampspeeds        |(3 values: start,stop,hold), (?) for more information
m|ac  |acceleration      |(value) for A1,Amax,D1,Dmax, (?) for more information
m|as  |accelerations(    |(5 values: A1,D1,hold,Amax,Dmax), (?) for more information
m|s   |stop              |(value) TODO: no output in serial and afterwards problems
m|en  |enable            |(value) or (?)
m|ep  |encoderposition   |TODO
m|lp  |latchedposition   |TODO
m|le  |latchedencoder    |TODO
m|mr  |moverelative      |(value)
m|mds |motordrvstatus    |(?), other functions to set/get drive status
m|mrs |motorrampstat     |(?), other functions to set/get ramp status
m|gs  |gstat             |(?), other functions
m|ma  |currentma         |(value) or (?)
m|fwm |freewheelingmode  |1,0 or (?)
m|mcs |modechangespeeds  |(3 values: pwmThrs, coolThrs, highThrs)
m|swm |swmode            |(?), other functions with value afterwards (s.a. LimitSW section)
m|cc  |coolconf          |(?), other functions
m|smp |savemotorparameter|-
m|iv  |icversion         |(?)
m|ld  |load              |default or defaultall TODO:?
m|st  |startup           |(?), other functions to set/get startup values
m|ho  |homing            |(?), other functions to set/get homing values
m|tsc |tunesteathchop    |-
m|tps |tunestallguard    |-

### Input commands

function|subfunction1|subfunction1|subfunction2
-|--|---         |-----  
i|if  |inputfunction     |
i|st  |startup           |

### System commands

function|subfunction1|subfunction1|subfunction2
-|--|---         |-----  
s|sv  |softwareversion   |(?)
s|hv  |hardwareversion   |(?)
s|do  |door              |TODO
s|bi  |bordid            |(?) according to SW2, binary [0-3]
s|ft  |firmwaredaytime   |(?) return compile time
s|st  |startup           |(?), other functions to set/get startup system values
s|pw  |pwm +[AnalogPort] |(value) [0-255]
s|pf  |pwmfrequency + [Aport]|(value)
s|sv  |save              |-
s|reset|reboot           |-
s|ca  |canadress         |(value)
s|cs  |canspeed          |(value)
s|ld  |load              |-
s|d   |debug             |-

## CAN

CAN is a commonly used communication system in automotive, automation and others.  
Due to its high reliability and higher speed than UART it can be used to communicate with the Motion from another Motion or, as an example, a RaspberryPi or Arduino (with their CAN-module).  

Up to 4 Monsterrhino boards can be connected via CAN to communicate with each other. It is also possible to connect other devices that support CAN communication.  

CAN functions can be used in user functions as following:  

```c++
pUserFunction->RemoteCommand_Motor_SetTargetPosition(3, 1, 200);
//Set target position of motor 1 on board with address 3 to value 200
//address: 3; motorNr:1; Value:200

pUserFunction->RemoteCommand_UserFunction_SetStart(2, 2, 1);
//Start user function 2 sub function 2 on board with address 2
//address: 2; functionNr:2; subFunction:1

uint32_t testVariable = 0;
pUserFunction->RemoteCommand_UserFunction_GetVariable(4, 1, 5, testVariable);
//Get user function variable 5 of user function 1 on board with address 4 and write to testVariable
//address: 5; functionNr:1; functionVar:5; testVariable: variable with return value
```
The remoteCommand function supports all serial command functions.  
In addition you can get and set **user function variables** via remoteCommand as shown above.

### Board setup for CAN  

Switch 1 (SW1, CAN TERM) activates CAN termination resistor (120 Ohm) (1 is active).  
Switch 2 (SW2, BOARD ID) indicates CAN address (BoardID+2) as follows:

SW2_1     |SW2_2    |Address|Board ID
-----|------|------|-----
LOW   |LOW  |   2  |0
HIGH  |LOW  |   3  |1
LOW   |HIGH |   4  |2
HIGH  |HIGH |   5  |3

**Note**:  
Address 0 is reserved for a broadcast message.  
Address 1 is reserved for other devices.  

### Variables
Each [User Function] has a total of **12 public variables** with two types (uint32, double) each 6.  These variables have the ability to be read and/or be set over CAN communication.  
This variables can be used in CAN-communication.
```C++
pUserFunction->m_variable[0] = 0; //m_variable[0]=0 of current UserFunction
pUserFunction->m_variableFloat[4] = 3.45;
```
**Note:** *m_variable[6]* is **no** variable because each Userfunction offers six of each type.  
0-5 equals a total of 6.
