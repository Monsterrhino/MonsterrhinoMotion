
import tkinter as tk
from tkinter import *
from tkinter import ttk, Button, Label, Frame, OptionMenu, Text, filedialog
from math import pi, cos, sin
from PIL import Image, ImageTk
from tkinter import colorchooser
import threading
import serial
import glob
import numpy as np
import time

BUTTON_IMGS = ["images/rotate_bwd.png",     # 0
               "images/rotate_fwd.png",     # 1
               "images/step_bwd.png",       # 2
               "images/step_fwd.png",       # 3
               "images/tab1_active_old.png", # 4
               "images/stop.png",           # 5
               "images/color_btn.png",      # 6
               "images/on.png",             # 7
               "images/off.png"             # 8
               ]

class MyApp:
    def __init__(self):
        self.myContainer1 = tk.Tk()
        # self.myContainer1.wm_attributes('-type', 'splash')
        self.myContainer1.title("MonsterrhinoMotion Bug")
        self.myContainer1.geometry("800x480")
        self.myContainer1.configure(bg="black")
        self.speed = 200
        self._connected = False

        # Connect to serial port
        _temp_po = Image.open(BUTTON_IMGS[8])
        self._con_img = ImageTk.PhotoImage(_temp_po)
        self._con = Button(self.myContainer1, image=self._con_img, command=self.connect_to_serial_port)
        self._con.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18")
        self._con.place(x=740, y=80, anchor="s")

        # Run left
        _temp_po = Image.open(BUTTON_IMGS[0])
        self._left_img = ImageTk.PhotoImage(_temp_po)
        self._left = Button(self.myContainer1, image=self._left_img, command=self.run_right)
        self._left.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18")
        self._left.place(x=150, y=300, anchor="s")

        # Run right
        _temp_po = Image.open(BUTTON_IMGS[1])
        self._right_img = ImageTk.PhotoImage(_temp_po)
        self._right = Button(self.myContainer1, image=self._right_img, command=self.run_left)
        self._right.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18")
        self._right.place(x=430, y=300, anchor="s")

        # Step forward
        _temp_po = Image.open(BUTTON_IMGS[3])
        self._fwd_img = ImageTk.PhotoImage(_temp_po)
        self._fwd = Button(self.myContainer1, image=self._fwd_img, command=self.run_backward)
        self._fwd.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18")
        self._fwd.place(x=290, y=195, anchor="s")

        # Step backward
        _temp_po = Image.open(BUTTON_IMGS[2])
        self._bwd_img = ImageTk.PhotoImage(_temp_po)
        self._bwd = Button(self.myContainer1, image=self._bwd_img, command=self.run_straight)
        self._bwd.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18")
        self._bwd.place(x=290, y=410, anchor="s")

        # Stop
        _temp_po = Image.open(BUTTON_IMGS[5])
        self._stop_img = ImageTk.PhotoImage(_temp_po)
        self._stop = Button(self.myContainer1, image=self._stop_img, command=self.stop)
        self._stop.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18")
        self._stop.place(x=290, y=305, anchor="s")

        # Speed scale
        self._scale_label = Label(self.myContainer1)
        self._scale_label.config(text="Speed")
        self._scale_label.place(x=180, y=75, anchor="s")
        self._scale_label.config(bg='black', fg="white", activebackground='white', borderwidth=1,
               highlightbackground="black", font="none 18")

        self._scale = Scale(self.myContainer1, from_=0, to=300,
                                     orient=tk.HORIZONTAL)
        self._scale.set(200)
        self._scale.config(bg='black', fg="white", activebackground='black', borderwidth=0,
                                        highlightbackground="black", font="none 18", command=self.set_speed)
        self._scale.place(x=280, y=70, anchor="s")

        # Color
        _temp_po = Image.open(BUTTON_IMGS[6])
        self._color_img = ImageTk.PhotoImage(_temp_po)
        self._color = Button(self.myContainer1, image=self._color_img, text="Select color",
                        command=self.choose_color)
        self._color.config(bg='black', fg="white", activebackground='white', borderwidth=1,
                          highlightbackground="black", font="none 18")
        self._color.place(x=630, y=310, anchor="s")

        # Random color button
        self._rand_color = Button(self.myContainer1, text="Random color",
                        command=self.choose_color)
        self._rand_color.config(bg='black', fg="white", activebackground='white', borderwidth=1,
                          highlightbackground="black", font="none 18", command=self.random_color)
        self._rand_color.place(x=630, y=380, anchor="s")

        self.port_name_label = Label(self.myContainer1, text='Select port: ')
        self.port_name_label.config(bg='black', fg="white", activebackground='white', borderwidth=1,
                          highlightbackground="black", font="none 12")
        self.port_name_label.place(x=460, y=70, anchor="s")
        # creating a entry for input
        # name using widget Entry
        self.port_name_var = StringVar()

        self.ports_list = self.serial_ports()
        self.port_name_var.set(self.ports_list[0])
        print(self.serial_ports())
        self.name_entry = tk.OptionMenu(self.myContainer1, self.port_name_var, *self.ports_list)
        self.name_entry.config(bg='black', fg="white", activebackground='white', borderwidth=1,
                          highlightbackground="black", font="none 12")
        self.name_entry.place(x=600, y=75, anchor="s")


    def set_speed(self, par):
        print(self._scale.get())
        self.speed = self._scale.get()

    def random_color(self):
        color = list(np.random.choice(range(256), size=3))
        self.color( color[0], color[1], color[2])
        print("Update random color!")
        self.myContainer1.after(2000, self.random_color)

    def choose_color(self):
        # variable to store hexadecimal code of color
        self.color_code = colorchooser.askcolor(title="Choose color")
        self.r = int(self.color_code[0][0])
        self.g = int(self.color_code[0][1])
        self.b = int(self.color_code[0][2])
        print(self.r, self.g, self.b)
        self.color(self.r, self.g, self.b)

    def connect_to_serial_port(self):
        if self._connected != True:
            print("Connect to serial!")

            self.ser = serial.Serial()
            # ser.port = "/dev/ttyUSB0"
            self.ser.port = self.port_name_var.get()
            # ser.port = "/dev/ttyS2"

            self.ser.baudrate = 115200
            self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
            self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
            self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
            # ser.timeout = None          #block read
            self.ser.timeout = 1  # non-block read
            # ser.timeout = 2              #timeout block read
            self.ser.xonxoff = False  # disable software flow control
            self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
            self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
            self.ser.writeTimeout = 2  # timeout for write

            # open serial port
            self.ser.open()

            # set continuous move
            self.continuous_move()

            _temp_po = Image.open(BUTTON_IMGS[7])
            self._con_img = ImageTk.PhotoImage(_temp_po)
            self._con.config(image = self._con_img)
            self._connected = True

        elif self._connected == True:
            _temp_po = Image.open(BUTTON_IMGS[8])
            self._con_img = ImageTk.PhotoImage(_temp_po)
            self._con.config(image=self._con_img)
            print("Serial close!")
            self.close_port()
            self._connected = False

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def close_port(self):
        self.ser.close()

    def write_to_monsterrhinomotion(self, cmd):
        if self.ser.isOpen:
            print("Write: " + str(cmd))
            message = "{}\n\r".format(cmd)
            self.ser.write(str.encode(message))

    def continuous_move(self):
        self.write_to_monsterrhinomotion("m2rm v")
        self.write_to_monsterrhinomotion("m1rm v")
        self.write_to_monsterrhinomotion("m3rm v")
        self.write_to_monsterrhinomotion("m4rm v")

    def run_straight(self):
        self.write_to_monsterrhinomotion("m2ms {}".format(self.speed))
        self.write_to_monsterrhinomotion("m1ms {}".format(self.speed))
        self.write_to_monsterrhinomotion("m3ms {}".format(-self.speed))
        self.write_to_monsterrhinomotion("m4ms {}".format(-self.speed))

    def run_left(self):
        self.write_to_monsterrhinomotion("m2ms {}".format(self.speed))
        self.write_to_monsterrhinomotion("m1ms {}".format(self.speed))
        self.write_to_monsterrhinomotion("m3ms {}".format(self.speed*0.4))
        self.write_to_monsterrhinomotion("m4ms {}".format(self.speed*0.4))

    def run_right(self):
        self.write_to_monsterrhinomotion("m2ms {}".format(-self.speed))
        self.write_to_monsterrhinomotion("m1ms {}".format(-self.speed))
        self.write_to_monsterrhinomotion("m3ms {}".format(-self.speed*0.4))
        self.write_to_monsterrhinomotion("m4ms {}".format(-self.speed*0.4))

    def run_backward(self):
        self.write_to_monsterrhinomotion("m2ms {}".format(-self.speed))
        self.write_to_monsterrhinomotion("m1ms {}".format(-self.speed))
        self.write_to_monsterrhinomotion("m3ms {}".format(self.speed))
        self.write_to_monsterrhinomotion("m4ms {}".format(self.speed))

    def stop(self):
        self.write_to_monsterrhinomotion("m2ms {}".format(0))
        self.write_to_monsterrhinomotion("m1ms {}".format(0))
        self.write_to_monsterrhinomotion("m3ms {}".format(0))
        self.write_to_monsterrhinomotion("m4ms {}".format(0))

    def color(self, r, g, b):
        print("Set color to: {} {} {}".format(r, g, b))
        self.write_to_monsterrhinomotion("s pf 100")                      #frequency (Hz)
        self.write_to_monsterrhinomotion("s pw3 {}".format(r))        #PWM (Pulse-width modulation)
        self.write_to_monsterrhinomotion("s pw2 {}".format(g))        #PWM (Pulse-width modulation)
        self.write_to_monsterrhinomotion("s pw1 {}".format(b))        #PWM (Pulse-width modulation)

class BackgroundTask():

    def __init__(self, taskFuncPointer):
        self.__taskFuncPointer_ = taskFuncPointer
        self.__workerThread_ = None
        self.__isRunning_ = False


    def taskFuncPointer(self):
        return self.__taskFuncPointer_

    def isRunning(self):
        return self.__isRunning_ and self.__workerThread_.isAlive()

    def start(self):
        if not self.__isRunning_:
            
            self.__isRunning_ = True
            self.__workerThread_ = self.WorkerThread(self)
            # Kills thread on end of program
            self.__workerThread_.daemon = True

            self.__workerThread_.start()

    def stop(self):
        self.__isRunning_ = False

    class WorkerThread(threading.Thread):
        def __init__(self, bgTask):
            threading.Thread.__init__(self)
            self.__bgTask_ = bgTask

        def run(self):
            try:
                self.__bgTask_.taskFuncPointer()(self.__bgTask_.isRunning)
            except Exception as e:
                print(e)
            self.__bgTask_.stop()


if __name__ == "__main__":
    myapp = MyApp()
    myapp.myContainer1.mainloop()