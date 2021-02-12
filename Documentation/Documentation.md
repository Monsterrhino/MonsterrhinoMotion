# Readme - Monsterrhino Stepper controller

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
**Examples:**  
```C++
g_Input1.SetRunFallingFunction(INPUT_RUN_MOTOR_STOP_1);
//Stop motor 1 at falling edge on input 1

g_Input2.SetRunRisingFunction(INPUT_RUN_MOTOR_STOP_2_3_4);
//Stop motor 2,3 and 4 at rising edge on input 2

g_Input3.SetRunRisingFunction(INPUT_RUN_MOTOR_STOP_1_2_3_4);
//Stop motor 1,2,3 and 4 at rising edge on input 3

g_Input4.SetRunFallingFunction(INPUT_RUN_USERFUNCTION_1 + 2); 
//Start user function 1 sub 2 at falling edge on input 4
```  
**see also:** Input serial commands

# User Functions

## Variables
Each UserFunction has a total of **12 public variables** with two types (uint32, double) each 6.  These variables have the ability to be read and/or set over CAN communication.
This variables can be used in CAN-communication.
```C++
pUserFunction->m_variable[0] = 0; //m_variable[0]=0 of current UserFunction
pUserFunction->m_variableFloat[4] = 3.45;
```

## Events  
Events provide the machine to react on different actions depending on motor status, user function status, input status and time.  

```C++
pUserFunction->m_MotorIoEvent.SetOrCondition(MOTORIOEVENT_MOTOR1PosReached);
//TODO: Add other examples
```

## Ramp mode
```C++
g_Motor1.SetRampMode(MotorClass::RampMode::VELOCITY_MODE)
```
 

There are three different ramp modes:  

* **Positioning**: Motor turns til it reached its target point.  
* **Velocity**: Motor velocity to max speed (using Amax).
* **Hold**: Velocity remains unchanged, unless stop event occurs. 

Motor control features different parameters to adjust ramp properties.  
Such as:  

* **Acceleration:** Start(A1) and Max(Amax)
* **Deceleration:** Final(D1) and Max(Dmax)
* **MaxSpeed:** From 0 to ?
* **RampSpeed:** Start,Stop,Hold  

**See also:** Serial commands for motor ramp mode (*m1rm (v,p,h or ?)*)
**TODO:** Graph

### Positioning Mode  

There are different options:  

* **TargetPosition**
* **MoveRelative**  

```C++
g_Motor1.SetTargetPosition(200.0);  //Set target position to 200 steps (double value)
g_Motor1.SetMoveRelative(10.0);     //Set target position 10 steps relative from current position
```

### Velocity Mode  

When changed to this mode, max speed is zero. To begin set **max speed** to a value greather than 0.  

### Hold Mode

Velocity remains unchanged, unless stop event occurs.

## Homing
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

TODO: Latched pos ?, Graph

## Limit switch
It is possible to use various types for limit sensing:  

* **Limit switch:** Two limit switches per motor, can be of any type (mechanical, inductive, ...).  
Connection through the corresponding JST-XH connector CN[6,8,10,12] (for Motor 1,2,3,4)  
* **Latch:** TODO  
* **Stall_Guard:** The motor stops at a set force on the motor shaft.

Properties for motor limit switch config are set with following parameters:  

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

# Motor

## Special functions  

Special functions are stall guard, coolStepping, power stage tuning and stealth chop.



## Parameter

Motors have many values that are set default after reset.  
The motor class has instances for each motor.  
```C++
g_Motor1.SetMaxSpeed(300);    //motor1
```
Motor startup parameter functions: 
**SetStartup_** or **GetStartup_**  

Function|Description
---|------
drvStrength           |
bbmTime               |
bbmClks               |
SenseResistor         |Resistor for current measuring in mOhm
MotorCurrent          |Motor current in mA
MotorCurrentReduction |
Freewheeling          |
Iholddelay            |
PwmofsInitial         |
PwmGradInitial        |
StepperDirection      |
MotorSteps            |
PWMThrsInt            |
PWMThrs               |
COOLThrsInt           |
COOLThrs              |
HighThrs              |
HighThrsInt           |
SWMode                |
RampMode              |
RampMaxSpeed          |
RampMaxSpeedInt       |
RampSpeedsStartInt    |
RampSpeedsStart       |
RampSpeedsHoldInt     |
RampSpeedsHold        |
RampSpeedsStopInt     |
RampSpeedsStop        |
AccelerationsAMaxInt  |
AccelerationsAMax     |Maximal Acceleration
AccelerationsDMaxInt  |
AccelerationsDMax     |Maximal Deceleration
AccelerationsA1Int    |
AccelerationsA1       |Initial Acceleration
AccelerationsD1Int    |
AccelerationsD1       |Initial Deceleration
HomingMode            |
HomingOffsetInt       |
HomingOffset          |Homing Offset
HomingMaxPos          |
HomingTimeout         |
HomingSpeed2Int       |
HomingSpeed2          |
HomingDmaxInt         |
HomingDmax            |
COOLCONF              |
                      |
EncoderResolution     |
EncoderAlloweddeviation|
EncoderSetup          |
EncoderInverted       |

# Communication
This board offers two main types of communication:  

* **Serial:** U(S)ART is used to communicate with lower speed.
* **CAN:**  CAN (common in automotive) is used to communicate faster and without failure.

## Serial U(S)ART

Serial communication is possible via USB. The following properties should be set to ensure correct data transfer:

* U(S)ART support: generic 'Serial'
* Line ending: Both CR & LF

The serial command is build as follows:  
[mainFunction][Nr][subFunction] (+optional: [value/subFunction2] [value])

function|subfunction1|subfunction1|subfunction2
-|--|---         |-----
m|tp  |targetpos         |(value)
m|cp  |currentpos        |(value)
m|rm  |rampmode          |(value)
m|ms  |maxspeed          |(value)
m|cs  |currentspeed      |(value) only get
m|r   |register          |Controller Register?
m|rs  |rampspeeds        |(3 values: start,stop,hold)
m|ac  |acceleration      |(value) for A1,Amax,D1,Dmax
m|as  |accelerations(    |(5 values: A1,D1,hold,Amax,Dmax)
m|s   |stop              |(value) TODO: no output in serial and afterwards problems
m|en  |enable            |(value)
m|ep  |encoderposition   |TODO
m|lp  |latchedposition   |TODO
m|le  |latchedencoder    |TODO
m|mr  |moverelative      |(value)
m|mds |motordrvstatus    |(?), other functions to set/get drive status
m|mrs |motorrampstat     |(?), other functions to set/get ramp status
m|gs  |gstat             |(?), other functions
m|ma  |currentma         |(value)
m|fwm |freewheelingmode  |(value)
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
-|----|------------------|-----------------------   
i|if  |inputfunction     |
i|st  |startup           |
-|----|------------------|-----------------------
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

Switch 1 (SW1, CAN TERM) activates CAN termination resistor (120 Ohm).
Switch 2 (SW2, BOARD ID) indicates CAN address (BoardID+2) as follows:

1     |2    |Address|Board ID
-     |-    |-     |-
LOW   |LOW  |   2  |0
HIGH  |LOW  |   3  |1
LOW   |HIGH |   4  |2
HIGH  |HIGH |   5  |3

**Note**:  
Address 0 is reserved for a broadcast message.  
Address 1 is reserved for other devices.  

# TODO

## Main functions 

* Outputs (Digital/Analog)

## Special functions  

* Stealth chop
* Power stage tuning
* Stealth guard
* Analog in
* SPI/I2C

## Examples

* Roboterarm
* 3D-printer
