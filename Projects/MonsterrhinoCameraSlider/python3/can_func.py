'''
Author: Gregor Holzner
Company: Tratter Engineering SRL September 2020
Website: www.trattereng.com
'''

'''
Implementation protocol V2:
	-Addressing
		-Used frame format is extended (29 bit) Address 0-536.870.911
			
			
			
			
			
			- Bit 0-3 Nummer (0-15)
			- Bit 4-13	sub command (9 bit =512)	    ;select sub command
			- Bit 14-17	command (0-15)					;command
				0 ('s')									;Sytem
				1 ('m')									;Motor
				2 ('i')									;Input
				3 ('f')									;User function
			- Bit 18	error
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

		- get a value set RTR Bit in Can Protocol

	-Data Field
		-Byte MSB-0		user return function_ID (0-255)
						Bit 0-8 (0-127)					;return function_ID
			
		-Byte MSB-1 & MSB-7 <Data>		;length and type depending on the register


'''



from can import Message
from bitstring import BitStream, BitArray

def cmd_to_CAN(sub_command="0", motor_nr=1, usr_fnct_id=1, err=0, data=0, toAddress = 2, command="m", fromAddress = 1, respondMessage = 1):
        """
        Function to transform command into can frame to send it to monsterrhino
        :param cmd:
        :param sub_command:
        :param motor_nr:
        :param usr_fnct_id:
        :param err:
        :param data:
        :param toAddress:
        :param command:
        :param fromAddress:
        :param respondMessage:
        :return:
        """

        # error=0

        # c = fromAddress << 4

        # data field generation
        '''
        Byte MSB < command > (0 - 255) 'm/i/s/f'       command
		0 ('s') Sytem
		1 ('m')	Motor
		2 ('i') Input
		3 ('f') User function
        '''

        # print("Command: " + command)
        _cmd_list = ["s", "m", "i", "f"]

        try:
                command = [i for i, elem in enumerate(_cmd_list) if command in elem][0]
                # print("converted to " + str(command))
        except IndexError as error:
                print("ERROR: " + str(error))
                command = 0
        _subcmd_list = ["0","1","2","rm","tp", "cp", "mr","" ,"", "", "ms"]
        try:
                subCommand = [i for i, elem in enumerate(_subcmd_list) if sub_command in elem][0]
        except IndexError as error:
                print("ERROR: " + str(error))
                subCommand = 0
        # print("Subcommand converted to: " + str(subCommand))
        err=1
        address = (int(respondMessage) << 28) | ((int(fromAddress) & 0x1F) << 23) | ((int(toAddress) & 0x1F) << 18) | ((int(err) & 0x01) << 17) | ((int(command) & 0x0F) << 13) | ((int(subCommand) & 0x1F)) << 4 | ((int(motor_nr) & 0xF));

        '''
        -Byte MSB - 1 & MSB - 2 < subcommand > (12 bit); select sub function
        -Bit
        0 - 12(0 - 4095)				;subCommand
        "tp"    0
        "cp"    1
        "mo"    2
        "ms"    3
        '''

        _msb0 = usr_fnct_id

        # Byte MSB-4 to MSB-7 <Data>(32 bit)		;length and type depending on the register
        # print("data: " + str(data))
        if (data == "?"):
                data = 0
        data = int(data)
        _msb1 = data & int(0xFF)
        _msb2 = (data >> 8) & int(0xFF)
        _msb3 = (data >> 16) & int(0xFF)
        _msb4 = (data >> 24) & int(0xFF)
        _msb5 = 0
        _msb6 = 0
        _msb7 = 0
        data = [        _msb0,           # MSB
                        _msb1,          # MSB-1
                        _msb2,          # MSB-2
                        _msb3,          # MSB-3
                        _msb4,          # MSB-4
                        _msb5,          # MSB-5
                        _msb6,          # MSB-6
                        _msb7]          # MSB-7


        return address, data

def uf_to_CAN( fromAddress = 1, toAddress = 2, respondMessage = 1, usr_fnct_id = 1, command = "f", sub_command = "s", uf_nr = 6, par = 1):
        # data field generation
        '''
        -Byte MSB < command > (0 - 255) 'm/i/s/f'       ;command
        'm'		0						                ;Motor
        'i'		1							            ;Input
        's'		2							            ;Sytem
        'f'		3							            ;User function
        '''

        data = par

        # print("Command " + command + ":")
        _cmd_list = ["s", "m", "i", "f"]
        try:
                command = [i for i, elem in enumerate(_cmd_list) if command in elem][0]
        except IndexError as error:
                print("ERROR: " + str(error))
                command = 0

        # print(command)

        # print("Subcommand " + sub_command + ":")
        _subcmd_list = ["0", "s", "uvF1", "uv4", "uv5"]
        try:
                sub_command = [i for i, elem in enumerate(_subcmd_list) if sub_command in elem][0]
                # In case it is the uservariable float set to 40
                if sub_command == 2:
                        sub_command = 40
                if sub_command == 3:
                        sub_command = 33
                if sub_command == 4:
                        sub_command = 34

        except IndexError as error:
                print("ERROR: " + str(error))
                sub_command = 0

        # print(sub_command)

        err = 1
        address = (int(respondMessage) << 28) | ((int(fromAddress) & 0x1F) << 23) | ((int(toAddress) & 0x1F) << 18) | (
                        (int(err) & 0x01) << 17) | ((int(command) & 0x0F) << 13) | (int(sub_command) & 0x7F) << 4 | (
                  (int(uf_nr) & 0xF));

        '''
        -Byte MSB - 1 & MSB - 2 < subcommand > (12 bit); select sub function
        -Bit
        0 - 12(0 - 4095)				;subCommand
        "tp"    0
        "cp"    1
        "mo"    2
        "ms"    3
        '''
        _msb0 = usr_fnct_id

        # Byte MSB-4 to MSB-7 <Data>(32 bit)		;length and type depending on the register
        # data = 1

        # print("data: " + str(data))
        if (data == "?"):
                data = 0
        data = int(data)
        _msb1 = data & int(0xFF)
        _msb2 = (data >> 8) & int(0xFF)
        _msb3 = (data >> 16) & int(0xFF)
        _msb4 = (data >> 24) & int(0xFF)
        _msb5 = 0
        _msb6 = 0
        _msb7 = 0
        data = [_msb0,  # MSB
                _msb1,  # MSB-1
                _msb2,  # MSB-2
                _msb3,  # MSB-3
                _msb4,  # MSB-4
                _msb5,  # MSB-5
                _msb6,  # MSB-6
                _msb7]  # MSB-7

        return address, data

def uv_from_CAN( fromAddress = 1, toAddress = 2, respondMessage = 1, get_val = 128, command = 3, sub_command = 3, uf_nr = 6, data = 0):

        # data field generation
        '''
        -Byte MSB < command > (0 - 255) 'm/i/s/f'       ;command
        'm'		0						                ;Motor
        'i'		1							            ;Input
        's'		2							            ;Sytem
        'f'		3							            ;User function
        '''
        err = 1
        address = (int(respondMessage & int('1', 2)) << 28) |\
                  ((int(fromAddress) &  int('11111', 2)) << 23) | \
                  ((int(toAddress) &    int('11111', 2)) << 18) | \
                  ((int(err) &          int('1', 2)) << 17) | \
                  ((int(command) &      int('1111', 2)) << 13) | \
                  (int(sub_command) &   int('111111111', 2)) << 4 | \
                  ((int(uf_nr) &        int('1111', 2)));


        _msb0 = get_val #& int('00000001', 2)
        #print("msb0: " + str(_msb0))

        # Byte MSB-4 to MSB-7 <Data>(32 bit)		;length and type depending on the register
        # data = 1
        if (data == "?"):
                data = 0
        data = int(data)
        _msb1 = data & int(0xFF)
        _msb2 = (data >> 8) & int(0xFF)
        _msb3 = (data >> 16) & int(0xFF)
        _msb4 = (data >> 24) & int(0xFF)
        _msb5 = 0
        _msb6 = 0
        _msb7 = 0
        data = [_msb0,  # MSB
                _msb1, # MSB-1
                _msb2,  # MSB-2
                _msb3,  # MSB-3
                _msb4]  # MSB-4
                #_msb5,  # MSB-5
                #_msb6,  # MSB-6
                #_msb7]  # MSB-7

        # test = Message(is_extended_id=False, is_error_frame=False, arbitration_id=address, data=data)
        #print("Get uservariable...")
        return address, data

def sys_to_CAN(sub_command="sytemReboot", motor_nr=0, usr_fnct_id=0, err=0, data=0, toAddress = 2, command="s", fromAddress = 1, respondMessage = 0):
        """
        Function to transform command into can frame to send it to monsterrhino
        :param cmd:
        :param sub_command:
        :param motor_nr:
        :param usr_fnct_id:
        :param err:
        :param data:
        :param toAddress:
        :param command:
        :param fromAddress:
        :param respondMessage:
        :return:
        """

        '''
        Byte MSB < command > (0 - 255) 'm/i/s/f'       command
		0 ('s') Sytem
		1 ('m')	Motor
		2 ('i') Input
		3 ('f') User function
		
		
					- Bit 0-3 Nummer (0-15)
			- Bit 4-13	sub command (9 bit =512)	    ;select sub command
			- Bit 14-17	command (0-15)					;command
				0 ('s')									;Sytem
				1 ('m')									;Motor
				2 ('i')									;Input
				3 ('f')									;User function
			- Bit 18	error							; active low
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
				
		SubCommand_System:
		 systemSN = 1,						//
		 systemFirmareTime = 2,				//
		 sytemHV = 3,						//
		 sytemSV = 4,						//
		 sytemSaveConguration = 5,			//
		 sytemRestoreConguration = 6,		//
		 sytemDefaultConguration = 7,		//
		 sytemFactoryDefaultConguration = 8,//
		 sytemProgrammKey = 9,				//
		 sytemReboot = 10,					//
		 systemDebugLevel =11,				//
		 systemStartUpDebugLevel = 12,		//
		 systemCanAdd =13,					//
		 systemStartUpCanAdd = 14,			//
		 systemCanSpeed = 15,				//
		 systemStartUpCanSpeed =16,			//
		 systemDipSwitch=17,				//
		 systemDoor=18,						//
		 systemPWM=19,						//
		 systemStartUpPWM=20,
		 systemPWM_Frequency = 21,
		 systemStartUpPWM_Frequency = 22,
        '''

        # print("Command: " + command)
        _cmd_list = ["s", "m", "i", "f"]

        try:
                command = [i for i, elem in enumerate(_cmd_list) if command in elem][0]
                # print("converted to " + str(command))
        except IndexError as error:
                print("ERROR: " + str(error))
                command = 0
        _subcmd_list = ["","systemSN",	"systemFirmareTime", "sytemHV", "sytemSV", "sytemSaveConguration", "sytemRestoreConguration",
		 "sytemDefaultConguration", "sytemFactoryDefaultConguration", "sytemProgrammKey", "sytemReboot", "systemDebugLevel",
		 "systemStartUpDebugLevel", "systemCanAdd", "systemStartUpCanAdd", "systemCanSpeed", "systemStartUpCanSpeed",
		 "systemDipSwitch", "systemDoor", "systemPWM", "systemStartUpPWM", "systemPWM_Frequency", "systemStartUpPWM_Frequency"]

        try:
                subCommand = [i for i, elem in enumerate(_subcmd_list) if sub_command in elem][0]
        except IndexError as error:
                print("ERROR: " + str(error))
                subCommand = 0
        # print("Subcommand converted to: " + str(subCommand))
        err=1
        address = (int(respondMessage) << 28) | ((int(fromAddress) & 0x1F) << 23) | ((int(toAddress) & 0x1F) << 18) |\
                  ((int(err) & 0x01) << 17) | ((int(command) & 0x0F) << 13) | ((int(subCommand) & 0x1F)) << 4 | \
                  ((int(motor_nr) & 0xF));

        _msb0 = usr_fnct_id

        # Byte MSB-4 to MSB-7 <Data>(32 bit)		;length and type depending on the register
        # print("data: " + str(data))
        if (data == "?"):
                data = 0
        data = int(data)
        _msb1 = data & int(0xFF)
        _msb2 = (data >> 8) & int(0xFF)
        _msb3 = (data >> 16) & int(0xFF)
        _msb4 = (data >> 24) & int(0xFF)
        _msb5 = 0
        _msb6 = 0
        _msb7 = 0
        data = [        _msb0,           # MSB
                        _msb1,          # MSB-1
                        _msb2,          # MSB-2
                        _msb3,          # MSB-3
                        _msb4,          # MSB-4
                        _msb5,          # MSB-5
                        _msb6,          # MSB-6
                        _msb7]          # MSB-7

        return address, data

if __name__ == '__main__':

        # address, data = sys_to_CAN(sub_command="sytemReboot", motor_nr=0, usr_fnct_id=0, err=0, data=0, toAddress = 2, command="s", fromAddress = 1, respondMessage = 0)
        # print(address, data)

        print(int('110000', 2))
