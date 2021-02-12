Changed in Readme_install:

-open Arduino IDE, for each libary inside the Libs folder go to ["Sketch->IncludeLibrary->Add .ZIP Library"] .. and select it
-Board: “Nucleo-64” (["Tools"]-> Board .. -> STM32 Boards -> Nucleo-64)
-Install Arduino Extension in Visual Studio: go to ["Extensions->Manage Extensions"] and Updates>Online, search for Arduino and install Arduino IDE for Visual Studio (Visual Micro)

Replace Dateien: 	replace path missing
			add
			"\Users\*username*\AppData\Local\Arduino15\packages\STM32\hardware\stm32\1.8.0\cores\arduino\stm32\usb\cdc" 	replace "usbd_cdc_if.c"
			"\Users\*username*\AppData\Local\Arduino15\packages\STM32\hardware\stm32\1.8.0\variants\NUCLEO_L476RG"		replace "variant.cc"
			"\Users\*username*\Documents\Arduino\libraries"									replace "monsterrhinoStep" folder 