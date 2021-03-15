---
title: "Monsterrhino Motion"
output: 
  bookdown::html_document2:
    toc: true
    toc_float: true
    fig_caption: true
---

# Introduction
The Monsterrhino Motion card is an independent stepper motor driver card to power and control up to 4 stepper motors that comes with a pre-installed firmware.
You can use Monsterrhino Motion in different ways depending on the complexity of your project: 

- Use the pre-installed firmware by sending commands **over a serial USB port** using a variety of predefined functions
- Use the pre-installed firmware by sending commands **over CAN bus** using a variety of predefined functions
- Program functions and actions with the **provided Arduino library** and upload directly to the card

In the simplest case you can just connect 24V, a stepper motor and a USB cable to the Monsterrhino Motion and you are ready to move the motor.

The key features of the stepper driver card are:

- up to 4 stepper motors
- two limit switches per motor
- encoder for each stepper motor
- up 12 digital inputs (24V)
- 1 digital output (24V)
- 3 PWM outputs (open collector)
- 2 CAN bus connector 
- USB C connector
- micro USB connector
- analog emergency power-off circuit that can be bridged with a jumper


![](Documentation/Images/Monsterrhino_Motion_Datasheet.png)


# USB serial communication

## Connect to Monsterrhino Motion

Install the Arduino IDE on your computer (https://www.arduino.cc/en/software). Open the Arduino IDE on your computer. Select the right port under **Tools->Port** e.g. /dev/ttyACM0 or COM5. Open the serial monitor by clicking on the magnifying glass symbol. Set **115200 baud** and line ending to **Both NL & CR**. Press the reset button on the Monsterrhino Motion than your ready to type your first command. If you have Motor 1 connected you can for example type: **m1mr 100** into the serial monitor and hit enter - now Motor 1 should move 100 steps. The meaning of this command is: **m1** - motor 1, **mr** move relative, **100** - hundred steps. With **m1mr -100** you can move 100 steps into the other direction. 


## Commands
The bold commands can be combined with the commands from the list below e.g.:

- **m1tp 100** - motor 1 move to target position 100
- **m4ma 200** - motor 4 set motor current to 200 mA
- **m3smp** - motor 3 save motor parameters
- **m2cp ?** - request motor 2 current position

The questionmark can generally be used to request parameters.

Motor |**m**    |**motor**
---         | :-:     | :-:
TargetPosition |tp|targetpos
CurrentPosition|cp|currentpos
Mode|mo|mode
MaxSpeed|ms|maxspeed
CurrentSpeed|cs|currentspeed
Register|r|register
RampSpeeds|rs|rampspeeds
Acceleration|ac|acceleration
Accelerations|as|accelerations
Stop|s|stop
Enable|en|enable
Disable|di|disable
EncoderPosition|ep|encoderposition 
LatchedPosition|lp|latchedposition
LatchedEncoderPosition|le|latchedencoder
MotorDriveStatus|mds|motordrvstatus
MotorRampStat|mrs|motorrampstat
gStat|gs|gstat
MotorCurrent|ma|currentma
Freewheelingmode|fwm| freewheelingmode
ModeChangeSpeeds|mcs| modechangespeeds
Switch Mode|swm|swmode
Save|sv|save
SaveMotorParameter|smp|savemotorparameter
Test|test
Load|ld|load
Startup|st|startup 

**Input**|i|input
---         | :-:     | :-:
InputFunction|if|inputfunction
StartUp|st|startup

**Functions**|f|function
---         | :-:     | :-:
Start|s|start
Stop|t|stop
Variable|v|variable
Float|f|float
Startup|st|startup
Unlock|u|unlook

Mode|mo|mode ->
	? (get) 
	p or positioning 
	v or velocity
	h or hold

# CAN bus communication
Commands can also be send over the CAN bus, therefore it is necessary to set the correct bits in the CAN frame.Following a description of the bits within the CAN frame.

	21-28 ID  (8 Bit 0-255 0=broadcast 1-9 Bus controller )
	15-20 Function (6 Bit )
	9-14 Nr (6 Bit )
	2-8  Sub Function (7 Bit)
	1   RTR respond
	
	Implementation protocol V2:
	-Addressing
		  - Used frame format is extended (29 bit) Address 0-536.870.911
			- Bit 0-3 Nummer (0-15)
			- Bit 4-13	sub command (9 bit =512)	    ;select sub command
			- Bit 14-17	command (0-15)					;command
				0 ('s')									;Sytem
				1 ('m')									;Motor
				2 ('i')									;Input
				3 ('f')									;User function
			- Bit 18	error						; active low
			-Bit 19-23	to Address
				0										;is a Broadcast message				
				2-31									;to Address
			-Bit 24-28	from Address
				0										;Bus controller
				2-31									;from Address
			- Bit 29	dentifies respond message
				0										;respond message
				1										;send message
			- Address range:
				Address 0 = broadcast message
				Address 1 = Bus controller
				available address range for client is 2-31

		

	-Data Field
		-Byte MSB-0		user return function_ID (0-127)
						Bit 0-7 (0-127)					;return function_ID
						Bit 7							; Set 1 = Get Value
		-Byte MSB-1 & MSB-7 <Data>		;length and type depending on the register

	


		- subCommand of motor command
			0;	emergency stop
				-no data
			1;	stop
				-no data
			2;	enable/disable driver
				-data type <byte>
					0:disabel driver
					1:enable driver
			3;  RampMode (uint8) <Set><Get>											RampMode
				-data type <uint8>
					0:																Positioning mode (using all A, D and V parameters)
					1:																Velocity mode to positive VMAX (using AMAX acceleration)
					2:																Velocity mode to negative VMAX (using AMAX acceleration)
					3:																Hold mode (velocity remains unchanged,unless stop event occurs)
			4;	TargetPosition (int48) <Set><Get>									the target position (step*1000) /!\ Set all other motion profile parameters before
				-data type <double*1000>
			5;	TargetPosition Register (int32) <Set><Get>							the target position (micro steps) /!\ Set all other motion profile parameters before
				-data type <int32>
			6;	MoveRelative(int32) <Set>											Move motor relative (steps*1000)
				-data type <double*1000>
			7;	MoveRelative Register(int32) <Set>									Move motor relative (micro steps)
				-data type <int32>
			8;	CurrentPosition (int48) <Set><Get>					 				the current internal position (steps*1000)
				-data type <double*1000>
			9;	CurrentPosition Register (int32) <Set><Get>					 		the current internal position (micro steps)
				-data type <micro steps>
			10;	Max Speed (uint32) <Set>											the max speed VMAX
				-data type <float*1000>
			11;	Max Speed Register (uint32) <Set><Get>								Register max speed VMAX
				-data type <uint32>
			12; Ramp speed Start(uint32) <Set><Get>									the start ramp speed
				-data type <float*1000>
			13;	Ramp speed Start Register (uint32) <Set><Get>						Register Ramp speed Start
				-data type <uint32>
			14; Ramp speed Stop(uint32) <Set><Get>									the stop ramp speed
				-data type <float*1000>
			15;	Ramp speed Stop Register (uint32) <Set><Get>						Register Ramp speed Stop
				-data type <uint32>
			16; Ramp speed Hold(uint32) <Set><Get>									the hold ramp speed
				-data type <float*1000>
			17;	Ramp speed Hold Register (uint32) <Set><Get>						Register Ramp speed Hold
				-data type <uint32>
			18;	get Current Speed(uint32)	<Get>									Return the current speed
				-data type <float*1000>
			19;	get Current Speed Register (uint32) <Get>							Return the current  speed Register 
				-data type <uint32>
			20; Acceleration AMAX(uint32) <Set><Get>								 ramp accelerations AMAX
				-data type <float*1000>
			21;	 Acceleration AMAX Register(uint32) <Set><Get>						Register  Acceleration AMAX
				-data type <uint32>
			22; Acceleration DMAX (uint32) <Set><Get>								ramp accelerations DMAX
				-data type <float*1000>
			23;	 Acceleration DMAX Register(uint32) <Set><Get>						Register  Acceleration DMAX
				-data type <uint32>
			24; Acceleration A1(uint32) <Set><Get>									ramp accelerations A1
				-data type <float*1000>
			25;	 Acceleration A1 Register(uint32) <Set><Get>						Register  Acceleration A1
				-data type <uint32>
			26; Acceleration D1(uint32) <Set><Get>									ramp accelerations D1
				-data type <float*1000>
			27;	 Acceleration D1 Register(uint32) <Set><Get>						Register  Acceleration D1
				-data type <uint32>
			28; ModeChangeSpeeds pwmThrs(uint32) <Set><Get>							mode change speeds pwmThrs
				-data type <float*1000>
			28;	 ModeChangeSpeeds pwmThrs Register(uint32) <Set><Get>				Register  ModeChangeSpeeds pwmThrs
				-data type <uint32>
			30; ModeChangeSpeeds coolThrs(uint32) <Set><Get>						mode change speeds coolThrs
				-data type <float*1000>
			21;	 ModeChangeSpeeds coolThrs Register(uint32) <Set><Get>				Register ModeChangeSpeeds coolThrs
				-data type <uint32>
			32; ModeChangeSpeeds highThrs(uint32) <Set><Get>						mode change speeds highThrs
				-data type <float*1000>
			33;	 ModeChangeSpeeds highThrs Register(uint32) <Set><Get>				Register ModeChangeSpeeds highThrs
				-data type <uint32>
			34;	Encoder Position (int48) <Set><Get>									the current encoder position (micro steps)
				-data type <double*1000>
			35;	Encoder Position Register(uint32) <Set><Get>						the current encoder position (steps*1000)
				-data type <uint32>
			36;	Latched Position (int48) <Set><Get>									the current latched position (micro steps)
				-data type <double*1000>
			37;	Latched Position Register(uint32) <Set><Get>						the Latched position (steps*1000)
				-data type <uint32>
			38;	LatchedEncoderPosition (int48) <Set><Get>							the current latched encoder position (steps*1000)
				-data type <double*1000>
			39;	LatchedEncoderPosition Register(int32) <Set><Get>					the current latched encoder position (uSteps)
				-data type <int32>


			50;	EncoderResolution_motorSteps (int32) <Set><Get>						the number of steps per turn for the motor
				-data type <int32>
			51;	EncoderResolution_encResolution (int32) <Set><Get>					the actual encoder resolution (pulses per turn)
				-data type <int32>
			
			53;	EncoderIndexConfiguration (uint8 bit bit bit bit ) <Set>			Configure the encoder N event context.
				-data type <uint8>													sensitivity : set to one of ENCODER_N_NO_EDGE, ENCODER_N_RISING_EDGE, ENCODER_N_FALLING_EDGE, ENCODER_N_BOTH_EDGES
				-data type <bit>													nActiveHigh : choose N signal polarity (true for active high)
				-data type <bit>													ignorePol : if true, ignore A and B polarities to validate a N event
				-data type <bit>													aActiveHigh : choose A signal polarity (true for active high) to validate a N event
				-data type <bit>													bActiveHigh : choose B signal polarity (true for active high) to validate a N event
				-data type <bit>
			54;	EncoderLatching(uint8) <Set>										Enable/disable encoder and position latching on each encoder N event (on each revolution)
				-data type <uint8>
			55;	isEncoderDeviationDetected(uint8) <Get>								Check if a deviation between internal pos and encoder has been detected
				-data type <uint8>
			56; clearEncoderDeviationFlag() <Set>									Clear encoder deviation flag (deviation condition must be handled before)
				-no data
			57; EncoderAllowedDeviation (int32) <Set>								Encoder Allowed Deviation
				-data type <uint32>
			58; SW_Mode (uint16) <Set><Get>											Reference Switch & StallGuard2 Event Configuration Register; See the TMC 5160 datasheet page 43
				-data type <uint16>
			59; DRV STATUS(uint32) <Get>											StallGuard2 Value and Driver Error Flags; datasheet page 56
				-data type <uint32>
			60; GetRampStatus(uint16) <Get><Reset>									RAMP_STAT � Ramp & Reference Switch Status Register; datasheet page 44
				-data type <uint16>
			61; GetGstat(uint8) <Get><Reset>										Global status flags
				-data type <uint8>



			67; SenseResistor(uint16) <Set><Get>									sense Resistor in mOhms 0=automatic
					-data type <uint16>
			68; MotorCurrent(uint16) <Set><Get>										Motor Current in mA
					-data type <uint16>
			69; MotorCurrentReduction(uint16) <Set><Get>							Motor current reduction in mA
					-data type <uint16>
			70; Motor Freewheeling Mode(uint8) <Set><Get>							Motor freewheeling mode
					-data type <uint8>
						FREEWHEEL_NORMAL   = 0x00,									Normal operation
						FREEWHEEL_ENABLED  = 0x01,									Freewheeling
						FREEWHEEL_SHORT_LS = 0x02,									Coil shorted using LS drivers
						FREEWHEEL_SHORT_HS = 0x03									Coil shorted using HS drivers
			71; Iholddelay(uint8) <Set><Get>										Controls the number of clock cycles for motor power down after a motion as soon as standstill is
																					detected (stst=1) and TPOWERDOWN has expired.The smooth transition avoids a motor jerk upon power down.
						-data type <uint8>
							0:														instant power down
							1..15:													Delay per current reduction step in multiple	of 2^18 clocks
			72; PWM_OFS(uint8) <Set><Get>											user defined PWM amplitude offset (0-255) related to full
						-data type <uint8>
																					motor current (CS_ACTUAL=31) in stand still.(Reset default=30)
			73; PWM_GRAD(uint8) <Set><Get>											Velocity dependent gradient for PWM amplitude: PWM_GRAD * 256 / TSTEP
																					This value is added to PWM_AMPL to compensate for	the velocity-dependent motor back-EMF.
						-data type <uint8>
			74; StepperDirection(uint8) <Set><Get>									Velocity motor  Stepper Direction
						-data type <uint8>

			75; UnLook Motor(uint8) <Set><Get>										Unlock Motor
				-data type <uint8>	
																This value is added to PWM_AMPL to compensate for	the velocity-dependent motor back-EMF.


			90; Homing Mode(uint8) <Set/Start><Get>									Start homing
						-data type <uint8>
							1: // endswitsh left
							2: // endswitsh right
			91; Homing timeOut (uint32) <Set><Get>									homing time to fail
						-data type <uint32>
			92; Homing maxPos (uint32) <Set><Get>									maximal deviation Posipion to fail
						-data type <uint32>
			93; Homing rampSpeed (uint32) <Set><Get>								rampSpeed for the homing process
						-data type <float*1000>
			94; Homing rampSpeed Register (uint32) <Set><Get>						Register rampSpeed for the homing process
						-data type <uint32>
			95; Homing rampSpeed_2(uint32) <Set><Get>								rampSpeed phase 2
						-data type <float*1000>
			96; Homing rampSpeed_2 Register (uint32) <Set><Get>						Register rampSpeed_2 for the homing process phase 2
						-data type <uint32>
			97; Homing Offset(uint48) <Set><Get>									homing offset(microstep)
						-data type <float*1000>
			98; Homing Offset Register (uint32) <Set><Get>							Register homing offset(microstep)
						-data type <uint32>
			99; Homing rampSpeedStart(uint32) <Set><Get>							homing ramp speed start
						-data type <double*1000>
			100; Homing rampSpeedStart Register (uint32) <Set><Get>					Register rampSpeedStart()
						-data type <uint32>
			101; Homing rampSpeedStop(uint32) <Set><Get>							homing ramp speed stop
						-data type <float*1000>
			102; Homing rampSpeedStop Register (uint32) <Set><Get>					Register rampSpeedStop()
						-data type <uint32>
			103; Homing rampSpeedHold(uint32) <Set><Get>							homing ramp speed hold
						-data type <float*1000>
			104; Homing rampSpeedHold Register (uint32) <Set><Get>					Register rampSpeedHold()
						-data type <uint32>
			105; Homing accelerationsAmax(uint32) <Set><Get>						homing accelerations Amax
						-data type <float*1000>
			106; Homing accelerationsAmax Register (uint32) <Set><Get>				Register accelerationsAmax()
						-data type <uint32>
			107; Homing accelerationsDmax(uint32) <Set><Get>			 			homing accelerations Dmax
						-data type <float*1000>
			108; Homing accelerationsDmax Register (uint32) <Set><Get>				Register accelerationsDmax()
						-data type <uint32>
			109 ;Homing accelerationsA1(uint32) <Set><Get>							homing accelerations A1
						-data type <float*1000>
			110; Homing accelerationsA1 Register (uint32) <Set><Get>				Register accelerationsA1()
						-data type <uint32>
			111;Homing accelerationsD1(uint32) <Set><Get>			 				homing accelerations D1
						-data type <float*1000>
			112; Homing accelerationsD1 Register (uint32) <Set><Get>				Register accelerationsD1()
						-data type <uint32>
										

			128;Startup  drvStrength(uint32) <Set><Get>			 					Startup Selection of gate driver current. Adapts the gate driver current to the gate charge of the external MOSFETs.
				-data type <uint8>
					00: weak
					01: weak+TC (medium above OTPW level)
					10: medium
					11: strong
						
			129;Startup  bbmClks(uint32) <Set><Get>			 						Startup 0..15: Digital BBM time in clock cycles (typ. 83ns).The longer setting rules (BBMTIME vs. BBMCLKS).
					-data type <uint16>
						(Reset Default: OTP 4 or 2)
			130;Startup  bbmTime(uint32) <Set><Get>			 						Startup Break-Before make delay
				-data type <uint8>
					0=shortest (100ns) � 16 (200ns) � 24=longest (375ns)
					>24 not recommended, use BBMCLKS instead
			131;Startup  Iholddelay(uint8) <Set><Get>								Startup	Iholddelay
						-data type <uint8>
			132;Startup  SenseResistor(uint16) <Set><Get>							Startup sense resistor in mOhms 0=automatic
					-data type <uint16>
			133;Startup  MotorCurrent(uint16) <Set><Get>							Startup motor current in mA
					-data type <uint16>
			134;Startup  MotorCurrentReduction(uint16) <Set><Get>					Startup motor current reduction in mA
					-data type <uint16>
			135;Startup  Motor Freewheeling Mode(uint8) <Set><Get>					Startup motor freewheeling mode
					-data type <uint8>
			136;Startup  PWM_OFS(uint8) <Set><Get>									Startup	user defined PWM amplitude offset (0-255) related to full
						-data type <uint8>
			137;Startup  PWM_GRAD(uint8) <Set><Get>									Startup	Velocity dependent gradient for PWM amplitude: PWM_GRAD * 256 / TSTEP
						-data type <uint8>
			138;Startup  StepperDirection(uint8) <Set><Get>							Startup	Velocity motor  Stepper Directio
						-data type <uint8>
			139;Startup  MaxSpeed (uint32) <Set><Get>								Startup	the max speed VMAX
				-data type <float*1000>
			140;Startup  MaxSpeed Register (uint32) <Set><Get>						Register Startup  MaxSpeed
						-data type <uint32>
			141;Startup  StartRampSpeed(uint32) <Set><Get>							Startup	the start ramp speed
				-data type <float*1000>
			142;Startup  StartRampSpeed Register (uint32) <Set><Get>				Register Startup  start ramp speed
						-data type <uint32>
			143;Startup  StopRampSpeed(uint32) <Set><Get>							Startup	the stop ramp speed
				-data type <float*1000>
			144;Startup  StopRampSpeed Register (uint32) <Set><Get>					Register Startup  stop ramp speed
						-data type <uint32>
			145;Startup  HoldRampSpeed(uint32) <Set><Get>							Startup	the hold ramp speed
				-data type <float*1000>
			146;Startup  HoldRampSpeed Register (uint32) <Set><Get>					Register Startup  hold ramp speed
					-data type <uint32>
			147;Startup  Acceleration maxAccel(uint32) <Set><Get>					Startup	ramp accelerations AMAX
				-data type <float*1000>
			148;Startup  Acceleration maxAccel Register (uint32) <Set><Get>			Register Startup  Acceleration maxAccel
					-data type <uint32>
			149;Startup  Acceleration maxDecel(uint32) <Set><Get>					Startup	ramp accelerations DMAX
				-data type <float*1000>
			150;Startup  Acceleration maxDecel Register (uint32) <Set><Get>			Register Startup  Acceleration maxDecel
					-data type <uint32>
			151;Startup  Acceleration startAccel(uint32) <Set><Get>					Startup	ramp accelerations A1
				-data type <uifloat*1000nt32>
			152;Startup  Acceleration startAccel Register (uint32) <Set><Get>		Register Startup  Acceleration startAccel
					-data type <uint32>
			153;Startup  Acceleration stopAccel(uint32) <Set><Get>					Startup	ramp accelerations D1
				-data type <float*1000>
			154;Startup  Acceleration stopAccel Register (uint32) <Set><Get>		Register Startup  Acceleration stopAccel
					-data type <uint32>
			155;Startup  ModeChangeSpeeds pwmThrs(uint32) <Set><Get>				Startup	mode change speeds pwmThrs
				-data type <float*1000>
			156;Startup  ModeChangeSpeeds pwmThrs Register (uint32) <Set><Get>		Register Startup  ModeChangeSpeeds pwmThrs
					-data type <uint32>
			157;Startup  ModeChangeSpeeds coolThrs(uint32) <Set><Get>				Startup	mode change speeds coolThrs
				-data type <float*1000>
			158;Startup  ModeChangeSpeeds coolThrs Register (uint32) <Set><Get>		Register Startup  ModeChangeSpeeds coolThrs
					-data type <uint32>
			159;Startup  ModeChangeSpeeds highThrs(uint32) <Set><Get>				Startup	mode change speeds highThrs
				-data type <float*1000>
			160;Startup  ModeChangeSpeeds highThrs Register (uint32) <Set><Get>		Register Startup  ModeChangeSpeeds highThrs
					-data type <uint32>
			161;Startup  EncoderResolution_motorSteps (int32) <Set><Get>		Startup	the number of steps per turn for the motor
				-data type <int32>
			162;Startup  EncoderResolution_encResolution (int32) <Set><Get>		Startup	the actual encoder resolution (pulses per turn)
				-data type <int32>
			
			164;Startup  EncoderIndexConfiguration (uint8 bit bit bit bit ) <Set><Get>		Startup	Configure the encoder N event context.
				-data type <uint8>													sensitivity : set to one of ENCODER_N_NO_EDGE, ENCODER_N_RISING_EDGE, ENCODER_N_FALLING_EDGE, ENCODER_N_BOTH_EDGES
				-data type <bit>													nActiveHigh : choose N signal polarity (true for active high)
				-data type <bit>													ignorePol : if true, ignore A and B polarities to validate a N event
				-data type <bit>													aActiveHigh : choose A signal polarity (true for active high) to validate a N event
				-data type <bit>													bActiveHigh : choose B signal polarity (true for active high) to validate a N event
				-data type <bit>													Startup	Enable/disable encoder and position latching on each encoder N event (on each revolution)
			
			166;Startup  EncoderAllowedDeviation (int32) <Set><Get>				Startup	Encoder Allowed Deviation
				-data type <uint32>
			167;Startup  SW_Mode (uint16) <Set><Get>							Startup	Reference Switch & StallGuard2 Event Configuration Register; See the TMC 5160 datasheet page 43
				-data type <uint16>
			168;Startup  RampMode (uint8) <Set><Get>							Startup	 RampMode
				-data type <uint8>
					0:															Positioning mode (using all A, D and V parameters)
					1:															Velocity mode to positive VMAX (using AMAX acceleration)
					2:															Velocity mode to negative VMAX (using AMAX acceleration)
					3:															Hold mode (velocity remains unchanged,unless stop event occurs)
				"HomingMode","HomingOffset","HomingMaxPos","HomingTimeout","HomingSpeed_2","HomingDmax"
			169;Startup  Homing Mode(uint8) <Set><Get>							Startup	homing mode
						-data type <uint8>
			170;Startup  Homing Offset(int48) <Set><Get>						Startup	homing offset(microstep)
						-data type <double*1000>
			171;Startup  Homing Offset Register (int32) <Set><Get>				Register Startup	homing offset(microstep)
						-data type <int32>
			172;Startup  Homing timeOut (uint32) <Set><Get>						Startup	homing time to fail
						-data type <uint32>
			173;Startup  Homing maxPos (int32) <Set><Get>						Startup	homing maximal deviation Posipion to fail
						-data type <int32>
			174;Startup  Homing rampSpeed_2(uint32) <Set><Get>					Startup	homing rampSpeed phase 2
						-data type <float*1000>
			175;Startup  Homing rampSpeed_2 Register (int32) <Set><Get>			Register homing Startup	rampSpeed_2
						-data type <int32>
			176;Startup  Homing accelerationsDmax(uint32) <Set><Get>			Startup	homing accelerations Dmax
						-data type <float*1000>
			175;Startup  Homing accelerationsDmax Register (int32) <Set><Get>	Register homing Startup	accelerationsDmax
						-data type <int32>
			512..768	Maping Motor Register
						-data type <int32/uint32>

			- subCommand of userFunction 
				1; start user function(uint8)  <Set><Get>							Start userFunction whith sub user function data
					-data type <uint8>
				2; stop user function
			   30; userFunctionVariable1(uint32)  <Set><Get>						Set/Get userFunction variable 1
			   31; userFunctionVariable2(uint32)  <Set><Get>						Set/Get userFunction variable 2
			   32; userFunctionVariable3(uint32)  <Set><Get>						Set/Get userFunction variable 3
			   33; userFunctionVariable4(uint32)  <Set><Get>						Set/Get userFunction variable 4
			   34; userFunctionVariable5(uint32)  <Set><Get>						Set/Get userFunction variable 5
			   35; userFunctionVariable6(uint32)  <Set><Get>						Set/Get userFunction variable 6
			   40; userFunction Variable1 float(uint48)(uint48/1000= double )  <Set><Get>					Set/Get userFunction float variable 1
			   41; userFunction Variable2 float(uint48)(uint48/1000= double )  <Set><Get>					Set/Get userFunction float variable 2
			   42; userFunction Variable3 float(uint48)(uint48/1000= double )  <Set><Get>					Set/Get userFunction float variable 3
			   43; userFunction Variable4 float(uint48)(uint48/1000= double )  <Set><Get>					Set/Get userFunction float variable 4

			   50; Startup  start user function(uint8)  <Set><Get>					Startup userFunction whith sub user function data

			   60; Startup userFunction Variable1(uint32)  <Set><Get>				Startup Set/Get userFunction variable 1
			   61; Startup userFunction Variable2(uint32)  <Set><Get>				Startup Set/Get userFunction variable 2
			   62; Startup userFunction Variable3(uint32)  <Set><Get>				Startup	Set/Get userFunction variable 3
			   63; Startup userFunction Variable4(uint32)  <Set><Get>				Startup	Set/Get userFunction variable 4
			   64; Startup userFunction Variable5(uint32)  <Set><Get>				Startup	Set/Get userFunction variable 5
			   65; Startup userFunction Variable6(uint32)  <Set><Get>				Startup	Set/Get userFunction variable 6
			   70; Startup userFunction Variable1 float(uint48)(uint48/1000= double )  <Set><Get>			Startup	Set/Get userFunction float variable 1
			   71; Startup userFunction Variable2 float(uint48)(uint48/1000= double )  <Set><Get>			Startup	Set/Get userFunction float variable 2
			   72; Startup userFunction Variable3 float(uint48)(uint48/1000= double )  <Set><Get>			Startup	Set/Get userFunction float variable 3
			   73; Startup userFunction Variable4 float(uint48)(uint48/1000= double )  <Set><Get>			Startup	Set/Get userFunction float variable 4

			- subCommand of input											<Input1..6 and laser1..2 >
				1 inputFaling(uint32)	<Set><Get>									Input Faling INPUT_RUN_USERFUNCTION
					-data type <uint32>
				2 inputRising(uint32)	<Set><Get>									Input Rising INPUT_RUN_USERFUNCTION
					-data type <uint32>
				3 Startup inputFaling(uint32)	<Set><Get>							Startup Input Faling INPUT_RUN_USERFUNCTION
					-data type <uint32>
				4 Startup inputRising(uint32)	<Set><Get>							Startup Input Rising INPUT_RUN_USERFUNCTION
					-data type <uint32>

				5 GetInputState <uint8><Get>										Get the state of input
					-data type <uint8>

				descipion of INPUT_RUN_USERFUNCTION:
				all fuctions can cominate 
				INPUT_RUN_USERFUNCTION_START_1						0x0001xx	; Start userfunction 1 whit sub function xx
				INPUT_RUN_USERFUNCTION_START_2						0x000200	; Start userfunction 2 whit sub function xx
				INPUT_RUN_USERFUNCTION_START_3						0x000400	; Start userfunction 3 whit sub function xx
				INPUT_RUN_USERFUNCTION_START_4						0x000800	; Start userfunction 4 whit sub function xx
				INPUT_RUN_USERFUNCTION_START_5						0x001000	; Start userfunction 4 whit sub function xx
				INPUT_RUN_USERFUNCTION_START_6						0x002000	; Start userfunction 4 whit sub function xx

				INPUT_RUN_USERFUNCTION_STOP_1						0x010100	; Stop userfunction 1
				INPUT_RUN_USERFUNCTION_STOP_2						0x010200	; Stop userfunction 2
				INPUT_RUN_USERFUNCTION_STOP_3						0x010400	; Stop userfunction 3
				INPUT_RUN_USERFUNCTION_STOP_4						0x010800	; Stop userfunction 4
				INPUT_RUN_USERFUNCTION_STOP_5						0x011000	; Stop userfunction 5
				INPUT_RUN_USERFUNCTION_STOP_6						0x012000	; Stop userfunction 6

				INPUT_RUN_MOTOR_STOP_1								0x020100	; Motor Stop 1
				INPUT_RUN_MOTOR_STOP_2								0x020200	; Motor Stop 2
				INPUT_RUN_MOTOR_STOP_3								0x020200	; Motor Stop 3
				INPUT_RUN_MOTOR_STOP_4								0x020400	; Motor Stop 4

				INPUT_RUN_MOTOR_EMERGENCYSTOP_1						0x022100	; EMERGENCYSTOP Motor  1
				INPUT_RUN_MOTOR_EMERGENCYSTOP_2						0x022200	; EMERGENCYSTOP Motor  1
				INPUT_RUN_MOTOR_EMERGENCYSTOP_3						0x022400	; EMERGENCYSTOP Motor  1
				INPUT_RUN_MOTOR_EMERGENCYSTOP_4						0x022800	; EMERGENCYSTOP Motor  1

# Monsterrhino Motion library installation guide 

## Install Java Runtime Environment

### For Windows
* download the Java Runtime Environment from the official Website - https://www.java.com/en/download/manual.jsp (or get it from the Software folder)
* install it by running the executable (.exe) file


### For Ubuntu
* install the Java Runtime Environment by executing the following command in your terminal: ```sudo apt install openjdk-8-jre```


## Prepare Arduino IDE:
* Download and install the Arduino IDE from the official page: https://www.arduino.cc/en/Main/Software (or get it from the Software folder)

* Start the Arduino IDE and add **Stm32duino** to it by doing the following steps:
  + add the following line under **File->Preferences** in the section **Additional Boards Manager URLs**: `https://raw.githubusercontent.com/stm32duino/BoardManagerFiles/master/STM32/package_stm_index.json`  
  + go to **Tools->Board->Boards Manager** and search for **STM32 Cores**, choose version **1.8.0** and press *Install*  


## Install STM32CubeProgrammer:
  
* Download **STM32CubeProgrammer** from the official page: https://www.st.com/en/development-tools/stm32cubeprog.html (or get it from the Software folder)

  ### For Windows
  * install it by running the executable (.exe) file
  
  ### For Ubuntu
  * using Ubuntu the **STM32CubeProgrammer** can be installed by executing the install script from a terminal - *cd* to the location of the file, then run it: ```./SetupSTM32CubeProgrammer-2.5.0.linux```
  
  ### For both
  * you can install it using the default settings; during the installation process, also complete the driver installation that will pop up


## Add the Monsterrhino application to the Arduino IDE:

* open Arduino IDE, for each libary inside the Libs folder go to **Sketch->IncludeLibrary->Add .ZIP Library ..** and select it
* open the Monsterrhino application in your Arduino IDE: **File->Examples->MonsterrhinoStep**
* adjust the Arduino IDE tool settings (**Tools**) like follows
  + Board: "Nucleo-64" (**Tools -> Board .. -> STM32 Boards -> Nucleo-64**)
  + Board part number: "Nucleo L476RG"
  + USB support (if available): "CDC (generic 'Serial' supersede U(S)ART-)"
  + Upload method: "STM32CubeProgrammer (DFU)"  
  
* replace the files on your computer with the files you find inside the **ToReplace** folder
  + **usbd_cdc_if.c**:  
  "C:\\Users\\*username*\\AppData\\Local\\Arduino15\\packages\\STM32\\hardware\\stm32\\1.8.0\\cores\\arduino\\stm32\\usb\\cdc"
  + **variant.c**:  
  "C:\\Users\\*username*\\AppData\\Local\\Arduino15\\packages\\STM32\\hardware\\stm32\\1.8.0\\variants\\NUCLEO_L476RG"
  + **monsterrhinoStep**-Folder:  
  "\\Users\\*username*\\Documents\\Arduino\\libraries"


## Use Monsterrhino directly in your Arduino IDE
* once Monsterrhino is connected to your computer and the reset button on it is pushed, the system should recognize your USB device
* now choose the correct Port **Settings -> Port** inside the Arduino IDE
* open the serial monitor **Settings -> Serial monitor**, set Baud to **115200**, set line endings to **NL and CR**
* you can now send commands to your Monsterrhino using the serial monitor


## Upload the Monsterrhino application to your Monsterrhino
  
### For Ubuntu
*change the #include arduino.h to #include Arduino.h in all the header files of the MonsterrhinoStep library
  
### For both
* connect your computer to your Monsterrhino, push the reset button while holding down the debug button on your Monsterrhino
* compile and upload the Monsterrhino application using your Arduino IDE



# Set up Visual Studio to use with Monsterrhino
* the above setup of Arduino IDE has to be completed before setting up Visual Studio
* download and install Visual Studio (or get it from the Software folder), add the workload **desktop development with c++** during the installation process  https://docs.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=vs-2019, you may skip the registering process as it is optional
* install Arduino Extension in Visual Studio: go to **Extension -> ManageExtensions -> Online**, search for **Arduino** and install **Arduino IDE for Visual Studio (Visual Micro)** (you will have to close Visual Studio during the installation process)
* open the location configuration **Extensions -> vMicro -> General -> Configure Arduino IDE Location(s)** and enter the correct paths, it should look similar to the example in the image:  

  ![](Documentation/Images/config.jpg){width=50%}  

* open project **monsterrhinostep** (/Documents/Arduino/monsterrhinostep.sln) in Visual Studio
* adjust the vMicro settings (**Extensions -> vMicro**) to the same values as you did in your Arduino IDE (see **adjust the Arduino IDE settings like follows** above)
* reopen Visual Studio, open **Extensions -> vMicro -> ViewPortMonitor ** (Monsterrhino needs to be connected to your computer to be able to open it), switch the setting **line endings** to **Both CR & LF**
* you can now use the ViewPortMonitor to connect to your Monsterrhino and directly send commands 
* to use Visual Studio to compile and upload your code to your Monsterrhino, you first have to restart it in debug mode (keep debug button pushed while pressing the reset button)



