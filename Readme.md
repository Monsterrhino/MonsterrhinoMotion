# Monsterrhino Motion

## Introduction
The Monsterrhino Motion card is an independent stepper motor driver card to power and control up to 4 stepper motors that comes with a pre-installed firmware.
You can use Monsterrhino Motion in different ways depending on the complexity of your project: 

- Use the pre-installed library by sending commands **over a serial USB port** using a variety of predefined functions (see below)
- Use the pre-installed library by sending commands **over CAN bus** using a variety of predefined functions (see in the MonsterrhinoControl documentation)
- Program functions and actions with the **provided Arduino library** and upload directly to the card

In the simplest case all you need to do is **just connect 24V, a stepper motor and a USB cable** to the Monsterrhino Motion and you are ready to move the motor - **plug and play**.

The key features of the MonsterrhinoMotion stepper driver card are:

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


## MonsterrhinoMotion pinout

![](Documentation/Images/Monsterrhino_Motion_Datasheet.png)


## USB serial communication

## Connect to Monsterrhino Motion

Install the Arduino IDE on your computer (https://www.arduino.cc/en/software). Open the Arduino IDE on your computer. 

+ Select the right port under **Tools->Port** e.g. /dev/ttyACM0 or COM5. 
+ Open the serial monitor and set **115200 baud** and line ending to **Both NL & CR**. 

Press the reset button on the Monsterrhino Motion than your ready to type your first command. If you have Motor 1 connected you can for example type: **m1mr 100** into the serial monitor and hit enter - now Motor 1 should move 100 steps. The meaning of this command is: **m1** - motor 1, **mr** move relative, **100** - hundred steps. With **m1mr -100** you can move 100 steps into the other direction. 


## Commands
The MonsterrhinoMotion commands are combinations of commands from the list below. They are composed of the classifier: **m, i or f**. A number after the classifier letter selects the desired motor, input, or function: Motor 1 = **m1**, Userfunction 1 = **f1**. The classifier is followed by a function such as targetposition = **tp** and a number.

- **m1tp 100** - motor 1 move to target position 100
- **m4ma 200** - motor 4 set motor current to 200 mA
- **m3smp** - motor 3 save motor parameters
- **m2cp ?** - request motor 2 current position

The questionmark can generally be used to request a current value e.g. Motor 1 what is the current position = **m1tp ?**.

Motor |**m**    |**motor** | Setting
---         | :-:     | :-: | :-:
TargetPosition |tp|targetpos |
CurrentPosition|cp|currentpos|
Rampmode|rm|rampmode |	p or positioning, v or velocity, h or hold
Motor current|ma|currentma |
MaxSpeed|ms|maxspeed |
CurrentSpeed|cs|currentspeed|
Register|r|register|
RampSpeeds|rs|rampspeeds|
Acceleration|ac|acceleration|
Accelerations|as|accelerations|
Stop|s|stop|
Enable|en|enable|
Disable|di|disable|
EncoderPosition|ep|encoderposition |
LatchedPosition|lp|latchedposition|
LatchedEncoderPosition|le|latchedencoder|
MotorDriveStatus|mds|motordrvstatus|
MotorRampStat|mrs|motorrampstat|
gStat|gs|gstat|
MotorCurrent|ma|currentma|
Freewheelingmode|fwm| freewheelingmode|
ModeChangeSpeeds|mcs| modechangespeeds|
Switch Mode|swm|swmode|
Save|sv|save|
SaveMotorParameter|smp|savemotorparameter|
Test|test|
Load|ld|load|
Startup|st|startup |

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




## Monsterrhino Motion library installation guide 

### Install Java Runtime Environment

#### For Windows
* download the Java Runtime Environment from the official Website - https://www.java.com/en/download/manual.jsp (or get it from the Software folder)
* install it by running the executable (.exe) file


#### For Ubuntu
* install the Java Runtime Environment by executing the following command in your terminal: ```sudo apt install openjdk-8-jre```


### Prepare Arduino IDE:
* Download and install the Arduino IDE from the official page: https://www.arduino.cc/en/Main/Software (or get it from the Software folder)

* Start the Arduino IDE and add **Stm32duino** to it by doing the following steps:
  + add the following line under **File->Preferences** in the section **Additional Boards Manager URLs**: `https://raw.githubusercontent.com/stm32duino/BoardManagerFiles/master/STM32/package_stm_index.json`  
  + go to **Tools->Board->Boards Manager** and search for **STM32 Cores**, choose version **1.8.0** and press *Install*  


### Install STM32CubeProgrammer:
  
* Download **STM32CubeProgrammer** from the official page: https://www.st.com/en/development-tools/stm32cubeprog.html (or get it from the Software folder)

  ### For Windows
  * install it by running the executable (.exe) file
  
  ### For Ubuntu
  * using Ubuntu the **STM32CubeProgrammer** can be installed by executing the install script from a terminal - *cd* to the location of the file, then run it: ```./SetupSTM32CubeProgrammer-2.5.0.linux```
  
  ### For both
  * you can install it using the default settings; during the installation process, also complete the driver installation that will pop up


### Add the Monsterrhino application to the Arduino IDE:

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


### Use Monsterrhino directly in your Arduino IDE
* once Monsterrhino is connected to your computer and the reset button on it is pushed, the system should recognize your USB device
* now choose the correct Port **Settings -> Port** inside the Arduino IDE
* open the serial monitor **Settings -> Serial monitor**, set Baud to **115200**, set line endings to **NL and CR**
* you can now send commands to your Monsterrhino using the serial monitor


### Upload the Monsterrhino application to your Monsterrhino
  
#### For Ubuntu
*change the #include arduino.h to #include Arduino.h in all the header files of the MonsterrhinoStep library
  
#### For both
* connect your computer to your Monsterrhino, push the reset button while holding down the debug button on your Monsterrhino
* compile and upload the Monsterrhino application using your Arduino IDE



## Set up Visual Studio to use with Monsterrhino
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



