 #from Tkinter import *
#from PIL import Image, ImageTk
#import ImageOps
import numpy as np
from matplotlib import cm
import cv2
import time
#import tkFileDialog
import serial
import os
import platform
import tkinter as tk
from tkinter import *
from tkinter import ttk, Button, Label, Frame, OptionMenu, Text, filedialog
from PIL import Image, ImageTk
import threading
import can
from led import runLED, LED
import RPi.GPIO as GPIO


from can_func import cmd_to_CAN, uf_to_CAN, uv_from_CAN, sys_to_CAN
if "arm" in platform.platform():
    PC = False
else:
    PC = True

HOVERCOLER = 'gray'

class MyApp:
    def __init__(self):

        self.myContainer1 = tk.Tk()
        self.myContainer1.wm_attributes('-type', 'splash')
        self.myContainer1.title("Monsterrhino Printer")
        self.myContainer1.geometry("800x480")

        self.myContainer1.configure(bg="black")


        # Set up variables
        self.im_height = 1240  # Maximum step number of axis
        self.im_width = 2000  # Maximum step number of axis
        self.pix_per_step = 2

        self.pos = [0, 0, 0]
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.port_name = "/dev/ttyUSB0"

        self.laser_status = "off"
        self.laser_pin = 26;
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laser_pin, GPIO.OUT)
        self.laser(0);

        self.hight_factor = 0.66
        self.rot_count = 90
        self.homing = False
        # Show image
        self.tkpi = PhotoImage(file="images/monsterrhino.png")
        self.label = Label(self.myContainer1, image=self.tkpi, bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=0,
                                      highlightbackground="black", font="none 18")

        self.load_img = Button(self.myContainer1, text="Load Image!", command=self.new_img, bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 18")

        self.connect = Button(self.myContainer1, text="X", command=self.restart_app, bg='black', activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 18", fg= "red")

        self.status_bar = Label(self.myContainer1, text="Status")

        self.spinnbox_label = Label(self.myContainer1, text="Image height:", bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 8")

        self.go_zero = Button(self.myContainer1, text="Home", command=self.home_xy_axis, bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 18")

        self.res_label = Label(self.myContainer1, text="{}x{} px".format(self.im_height, self.im_width), bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 8")

        self.burn = Button(self.myContainer1, text="Start plotting!", command=self.start_printing, bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 18")

        self.xdir_label = Label(self.myContainer1, text="y_max = 1500 steps ------------> y", bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 8")
        self.rotate_img = Button(self.myContainer1, text="Rotate Image!", command=self.rotate_image)

        self.variable = StringVar(self.myContainer1)
        self.variable.set("700")  # default value
        self.drop_down = OptionMenu(self.myContainer1, self.variable, "500", "600", "700", "800", "900", "1000", "1100", "1200", "1300", "1400", "1500")
        self.drop_down.configure( bg='black', fg="white", activebackground=HOVERCOLER, borderwidth=2,
                                      highlightbackground="black", font="none 18")

        self.var1 = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.myContainer1, text='Curved', variable=self.var1, onvalue=1, offvalue=0, bg='black', activebackground=HOVERCOLER, borderwidth=0,
                                      highlightbackground="black", font="none 18", fg= "red")


        # Organize layout using grid
        self.label.place(x=520, y=440, anchor="s", height=430, width=500)
        self.load_img.place(x=140, y=90, anchor="s", height=80, width=240)
        self.spinnbox_label.place(x=100, y=115, anchor="s")
        self.drop_down.place(x=140, y=200, anchor="s", height=80, width=240)
        self.go_zero.place(x=140, y=285, anchor="s", height=80, width=240)
        self.burn.place(x=140, y=370, anchor="s", height=80, width=240)
        # self.checkbox.place(x=140, y=430, anchor="s")

        self.connect.place(x=770, y=50, anchor="s", height=40, width=40)

        self.xdir_label.place(x=140, y=470, anchor="s")
        # self.res_label.place(x=140, y=470, anchor="s")


        self.tc_receive_CAN_task = BackgroundTask(self.tc_receive_CAN)
        self.querry_y_pos_const_task = BackgroundTask(self.querry_y_pos_const)
        self.blink_led_task = BackgroundTask(self.blink_LED)
        self.print_task = BackgroundTask(self.draw_img_new)
        self.run = False

        if not PC:
            print("Startup CAN!")
            os.system("sudo /sbin/ip link set can0 up type can bitrate 1000000")  # brings up CAN
            self.can_bus = can.interface.Bus(bustype="socketcan", channel="can0",
                                             bitrate=1000000)
            time.sleep(0.1)

            # start receive task
            self.tc_receive_CAN_task.start()
            print("Start can querry task")


            self.led = LED()
            self.led.init_led()
            self.led.set_green()

        self.querry_y_pos_const_task.start()

    def start_printing(self):
        """Starts printing
        """
        self.print_task.start()

    def restart_app(self):
        """Restarts app, only from debugg area callable
        """
        os._exit(0)

    def tc_receive_CAN(self, par):
        """Starts receiver task to receive and set tc_status
        """
        try:
            print("-> Enter CAN receive loop!")
            while True:
                # Wait until a message is received.
                # print("----> Waiting...")
                message = self.can_bus.recv()

                # print("<---- Received...")
                # print("message length ---> " + str(len(message.data)))
                if len(message.data) > 1:
                    # print("enter if <-------<")
                    #print("ID length: ")
                    #print(message.arbitration_id.bit_length())
                    msb0 = '{0:x} '.format(message.data[0])
                    # print("id----> " + str(int(msb0, 16)))
                    id = int(msb0, 16)

                    msb1 = '{0:x} '.format(message.data[1])
                    # print("value----> " + str(int(msb1, 16)))
                    value = int(msb1, 16)

                    to_temp = int(message.arbitration_id) >> 18
                    to_can = int(to_temp & int('000001111', 2))
                    #print("To can ID: " + str(to_can))

                    s = ''
                    for i in range(message.dlc):
                        s += '{0:x} '.format(message.data[i])
                    #print('CAN receive---->  {}'.format(s))

                    # Lock status
                    if to_can == 1 and id == 35:
                        # Check if it is not the other value
                        # print("Y pos")
                        #self.pos[1] = value
                        self.y_current = value
                        #self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))


        except OSError:
            print('Cannot find PiCAN board')

    def new_img(self):
        folder_path = filedialog.askopenfilename()
        try:
            self.orig_im_cv2 = cv2.imread(folder_path)
            self.orig_im = Image.open(folder_path)
            self.orig_im = self.orig_im.convert('L')
            width, height = self.orig_im.size
            print("Original size: {} x {}".format(width, height))

            basewidth = 430
            wpercent = np.divide( basewidth, width)
            print("wpercent: " + str(wpercent))
            hsize = int(height*wpercent)

            print("basewidth {} hsize {}".format(basewidth, hsize))
            self.im = self.orig_im.resize((basewidth, hsize), Image.ANTIALIAS)

            self.spinnbox_label.configure(text="Orig. {}x{} px".format(width, height ))
            print("Set new image as label")
            self.tkpi = ImageTk.PhotoImage(self.im)
            self.label.config(image=self.tkpi)


        except:
            self.status_bar.configure(text="No valid image selected!")

    def stripe_img(self):
        print("stripe image")

    def laser(self, state):
        if state is 1:
            print("laser on")
            GPIO.output(self.laser_pin, 0)
        else:
            print("laser off")
            GPIO.output(self.laser_pin, 1)

    def x_move_relative(self, steps=100):
        """Moves to a given target position of the given motor
        """
        _steps = steps * 1

        print("Print straight!")
        address, data = cmd_to_CAN(command="m", sub_command="mr", motor_nr=2,
                                   usr_fnct_id=1, err=0, data=_steps, toAddress=2,
                                   fromAddress=1, respondMessage=1)
        if not PC:
            # Send CAN message
            self.send_CAN(address, data)

        address, data = cmd_to_CAN(command="m", sub_command="mr", motor_nr=2,
                                   usr_fnct_id=1, err=0, data=_steps, toAddress=2,
                                   fromAddress=1, respondMessage=1)
        if not PC:
            # Send CAN message
            self.send_CAN(address, data)

    def x_move_curve(self, steps=100):
        """Moves to a given target position of the given motor
        """
        print("Print curved!")
        address, data = uf_to_CAN(fromAddress=1, toAddress=2, respondMessage=1, usr_fnct_id=1,
                                  command="f", sub_command="s", uf_nr=1, par=2)
        if not PC:
            # Send CAN message
            print("curve")
            #self.send_CAN(address, data)

    def y_move_targetposition(self, pos=700):
        """Moves to a given target position of the given motor
        """
        _steps = pos * 1
        address, data = cmd_to_CAN(command="m", sub_command="tp", motor_nr=1,
                                   usr_fnct_id=1, err=0, data=_steps, toAddress=2,
                                   fromAddress=1, respondMessage=1)
        if not PC:
            # Send CAN message
            self.send_CAN(address, data)

    def home_xy_axis(self):
        """Homes x and y axis and moves back to starting position
        """
        if self.homing == False:
            address, data = uf_to_CAN(fromAddress=1, toAddress=2, respondMessage=1, usr_fnct_id=1,
                                      command="f", sub_command="s", uf_nr=1, par=4)
            if not PC:
                # Send CAN message
                self.send_CAN(address, data)

            self.querry_y_pos()

            self.homing = True
        self.laser(0)

    def querry_y_pos_const(self, par):
        """
        Variables:
        userFunctionVariable1 = 30      158
        userFunctionVariable2 = 31      159
        userFunctionVariable3 = 32      160
        userFunctionVariable4 = 33      161
        userFunctionVariable5 = 34      162
        userFunctionVariable6 = 35      163
        """
        # Start receive task
        # self.tc_receive_CAN_tc_row_task.start()

        # Transform CAN command 163 = ID 35
        # Transform CAN command 158 = ID 30
        while True:
            address, data = uv_from_CAN(fromAddress=1, toAddress=2, respondMessage=1, get_val=163, command=3,
                                        uf_nr=2, sub_command=35, data=0)

            # print("-------> Querry!")
            # Send CAN message
            if not PC:
                # Send CAN message
                self.send_CAN(address, data)

            time.sleep(0.02)

    def querry_y_pos(self):
        """
        Variables:
        userFunctionVariable1 = 30      158
        userFunctionVariable2 = 31      159
        userFunctionVariable3 = 32      160
        userFunctionVariable4 = 33      161
        userFunctionVariable5 = 34      162
        userFunctionVariable6 = 35      163
        """
        # Start receive task
        # self.tc_receive_CAN_tc_row_task.start()

        # Transform CAN command 163 = ID 35
        # Transform CAN command 158 = ID 30
        #while True:
        address, data = uv_from_CAN(fromAddress=1, toAddress=2, respondMessage=1, get_val=163, command=3,
                                    uf_nr=2, sub_command=35, data=0)
        # Send CAN message
        if not PC:
            # Send CAN message
            self.send_CAN(address, data)

        # self.myParent.after(20, self.querry_y_pos)
        #print("Querry!")
        #time.sleep(0.5)

    def send_CAN(self, address, data):
        """Translates command to CAN frame and sends it
        :param message: command to be translated and send over CAN
        """

        # Try to write the message
        try:
            msg = can.Message(arbitration_id=address, data=data, is_extended_id=True)
            # print(msg)

        except AttributeError as error:
            print("error:Create message")
            print(error)
            return

        # Try to send the message
        try:
            self.can_bus.send(msg)
            # print("Message sent on {}".format(self.can_bus.channel_info))
        except can.CanError:
            print("Message could NOT be sent!")

    def serial_connect(self):
        try:
            if self.ser.is_open == False:
                self.ser.port = self.port_name
                self.ser.open()
                if self.ser.is_open == True:
                    #self.connect.configure(text="Disconnect!", foreground="green")
                    self.status_bar.configure(text="CNC found!")
            elif self.ser.is_open == True:
                self.ser.close()
                if self.ser.is_open == False:
                    #self.connect.configure(text="Connect!", foreground="black")
                    self.status_bar.configure(text="Disconnected")
        except:
            self.connect.configure(text="No Device!", foreground="red")

    def move_step(self, axis, step=1):  # int(self.step_spinnbox.get())
        try:
            if self.ser.is_open == True:
                directions = ['x', 'y', 'z', 'c', 's', 'u']
                if directions.index(axis) < 3:
                    self.pos[directions.index(axis)] += step
                if directions.index(axis) >= 3:
                    self.pos[directions.index(axis) - 3] -= step
                self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
                self.ser.write(b'{}{}\n'.format(step, axis))
            elif self.ser.is_open == False:
                self.status_bar.configure(text="Serial not open!")
        except:
            self.status_bar.configure(text="No Device connected!")

    def set_zero(self):
        for i in range(3):
            self.pos[i] = 0
        self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))

    def move_zero(self):
        try:
            if self.ser.is_open == True:
                if self.pos[0] < 0:
                    self.ser.write(b'{}{}\n'.format(self.pos[0] * -1, "x"))
                    self.pos[0] = 0
                    self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
                elif self.pos[0] > 0:
                    self.ser.write(b'{}{}\n'.format(self.pos[0], "c"))
                    self.pos[0] = 0
                    self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
                elif self.pos[1] < 0:
                    self.ser.write(b'{}{}\n'.format(self.pos[1] * -1, "y"))
                    self.pos[1] = 0
                    self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
                elif self.pos[1] > 0:
                    self.ser.write(b'{}{}\n'.format(self.pos[1], "s"))
                    self.pos[1] = 0
                    self.pos_label.configure(text="x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
            elif self.ser.is_open == False:
                self.status_bar.configure(text="Serial not open!")
        except:
            self.status_bar.configure(text="No Device connected!")

    def rotate_image(
            self):  # rotation behavior not working properly yet, also mirror function introducing: ImageOps.rotate
        try:
            if self.rot_count == 360:
                self.rot_count = 0
            self.im = self.orig_im.rotate(self.rot_count)
            self.rot_count += 90

            width, height = self.im.size
            new_width = int(np.divide(width, int(self.pix_per_step_spinnbox.get())))
            new_height = int((new_width * height / width) * self.hight_factor)
            self.im = self.im.resize((new_width, new_height), Image.ANTIALIAS)

            self.tkpi = ImageTk.PhotoImage(self.im)
            self.label.config(image=self.tkpi)
            self.label.config(height=200, width=200)
        except:
            self.status_bar.configure(text="No image defined!")

    # def burn_image(self):
    #     try:
    #         if self.ser.is_open == True and self.pos[0] == 0 and self.pos[1] == 0:
    #             pix = np.array(self.im)
    #             pix = 255 - pix
    #             nrow, ncol = pix.shape
    #
    #             for r in range(nrow):
    #                 if self.pos[0] == 0:
    #                     print ("Forward x")
    #                     for c in range(ncol):
    #                         self.ser.write(
    #                             b'{}a\n'.format(int(np.multiply(pix[r, c], float(self.burn_time_factor.get())))))
    #                         time.sleep(
    #                             np.divide(np.multiply(pix[r, c], float(self.burn_time_factor.get())), 1000) + 0.15)
    #                         self.move_step("x", int(self.scale_val.get()))
    #                         time.sleep(0.1)
    #                 else:
    #                     print ("Backward x")
    #                     for c in reversed(range(ncol)):
    #                         self.ser.write(
    #                             b'{}a\n'.format(int(np.multiply(pix[r, c], float(self.burn_time_factor.get())))))
    #                         time.sleep(
    #                             np.divide(np.multiply(pix[r, c], float(self.burn_time_factor.get())), 1000) + 0.15)
    #                         self.move_step("c", int(self.scale_val.get()))
    #                         time.sleep(0.1)
    #
    #                 self.move_step("y", int(self.scale_val.get()))
    #                 time.sleep(0.10)
    #                 print ("x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
    #
    #             self.move_zero()
    #
    #         elif self.ser.is_open == False:
    #             self.status_bar.configure(text="Serial not open!")
    #     except:
    #         self.status_bar.configure(text="No Device connected!")
    #
    # def burn_image_with_skip(self):
    #     """
    #     Function to switch laser on and off and move through each pixel. White pixel are skipped
    #     """
    #     try:
    #         if self.ser.is_open == True and self.pos[0] == 0 and self.pos[1] == 0:
    #             pix = np.array(self.im)
    #             pix = 255 - pix
    #             nrow, ncol = pix.shape
    #
    #             for r in range(nrow):
    #                 ncol_count_f = 0
    #                 ncol_count_b = 0
    #                 if self.pos[0] == 0:
    #                     print ("Forward x")
    #                     print ("Row: %d" % r)
    #                     for c in range(ncol):
    #                         if pix[r, c] > 0:
    #                             self.move_step("x", int(self.scale_val.get()) * ncol_count_f)
    #                             time.sleep(0.1 * ncol_count_f)
    #                             self.ser.write(b'{}a\n'.format(int(np.multiply(pix[r, c],
    #                                                                            float(self.burn_time_factor.get())))))
    #                             time.sleep(
    #                                 np.divide(np.multiply(pix[r, c], float(self.burn_time_factor.get())), 1000) + 0.15)
    #                             ncol_count_f = 0
    #                         if c == (ncol - 1):
    #                             self.move_step("x", (ncol_count_f + 1) * int(self.scale_val.get()))
    #                             print ("Return to zero steps forward")
    #                             time.sleep(0.02 * ncol_count_f)
    #                         ncol_count_f += 1
    #
    #                 else:
    #                     print ("Backward x")
    #                     print ("Row: %d" % r)
    #                     for c in reversed(range(ncol)):
    #                         if pix[r, c] > 0:
    #                             self.move_step("c", int(self.scale_val.get()) * ncol_count_b)
    #                             time.sleep(0.1 * ncol_count_b)
    #                             self.ser.write(b'{}a\n'.format(int(np.multiply(pix[r, c],
    #                                                                            float(self.burn_time_factor.get())))))
    #                             time.sleep(
    #                                 np.divide(np.multiply(pix[r, c], float(self.burn_time_factor.get())), 1000) + 0.15)
    #                             ncol_count_b = 0
    #                         if c == 0:
    #                             self.move_step("c", self.pos[0])
    #                             print ("Return to zero steps backward")
    #                             time.sleep(0.02 * self.pos[0])
    #                         ncol_count_b += 1
    #
    #                 self.move_step("y", int(self.scale_val.get()))
    #                 time.sleep(0.10)
    #                 print ("x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
    #
    #             self.move_zero()
    #
    #         elif self.ser.is_open == False:
    #             self.status_bar.configure(text="Serial not open!")
    #     except:
    #         self.status_bar.configure(text="No Device connected!")
    #
    #
    # def burn_image_with_skip_jump(self):
    #     """
    #     Function to switch laser on and off and move through each pixel. White pixel are skipped
    #     """
    #     try:
    #         if self.pos[0] == 0 and self.pos[1] == 0:
    #             pix = np.array(self.im)
    #             pix = 255 - pix
    #             nrow, ncol = pix.shape
    #
    #             for c in range(ncol):
    #                 nrow_count_f = 0
    #                 nrow_count_b = 0
    #                 if self.pos[1] == 0:
    #                     print ("Forward y")
    #                     print ("Col: %d" % c)
    #                     for r in range(nrow):
    #                         if pix[r, c] > 0:
    #                             # self.move_step("y", int(self.scale_val.get()) * nrow_count_f)
    #                             #time.sleep(0.1 * nrow_count_f)
    #                             #self.ser.write(b'{}a\n'.format(int(np.multiply(pix[r, c], float(self.burn_time_factor.get())))))
    #                             #time.sleep(np.divide(np.multiply(pix[r, c], float(self.burn_time_factor.get())), 1000) + 0.15)
    #                             nrow_count_f = 0
    #                         if r == (nrow - 1):
    #                             #self.move_step("y", (nrow_count_f + 1) * int(self.scale_val.get()))
    #                             print ("Return to zero steps forward")
    #                             time.sleep(0.02 * nrow_count_f)
    #                         nrow_count_f += 1
    #
    #                 else:
    #                     print ("Backward y")
    #                     print ("Col: %d" % c)
    #                     for r in reversed(range(nrow)):
    #                         if pix[r, c] > 0:
    #                             self.move_step("s", int(self.scale_val.get()) * nrow_count_b)
    #                             time.sleep(0.1 * nrow_count_b)
    #                             self.ser.write(b'{}a\n'.format(int(np.multiply(pix[r, c],
    #                                                                            float(self.burn_time_factor.get())))))
    #                             time.sleep(
    #                                 np.divide(np.multiply(pix[r, c], float(self.burn_time_factor.get())), 1000) + 0.15)
    #                             nrow_count_b = 0
    #                         if r == 0:
    #                             self.move_step("s", self.pos[1])
    #                             print ("Return to zero steps backward")
    #                             time.sleep(0.02 * self.pos[1])
    #                         nrow_count_b += 1
    #
    #                 self.move_step("x", int(self.scale_val.get()))
    #                 time.sleep(0.10)
    #                 print ("x: {}  y: {}  z: {}".format(self.pos[0], self.pos[1], self.pos[2]))
    #
    #             self.move_zero()
    #
    #         elif self.ser.is_open == False:
    #             self.status_bar.configure(text="Serial not open!")
    #     except:
    #         self.status_bar.configure(text="No Device connected!")

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def wait_to_finish(self):
        self.y_current = 1
        while self.y_current != 0:
            # self.querry_y_pos()
            print("y current 1: " + str(self.y_current))
            time.sleep(0.2)

    def blink_LED(self, par):
        while True:
            if self.run == True:
                self.led.set_orange_green_mix()
                time.sleep(0.5)
                self.led.set_orange_green_mix2()
                time.sleep(0.5)

    def draw_img_new(self, par):

        if self.homing == True:

            print("Start printing ...")
            self.run = True
            if not PC:
                self.blink_led_task.start()

            wait_for_pen = 1.4

            or_nrow, or_ncol = self.orig_im_cv2.shape[:2]
            print("Original Nraws {} Original Ncols {}".format(or_nrow, or_ncol))

            print("Curved: " + str(self.var1.get()))
            # Get desired image height
            image_height = int(self.variable.get())

            print("image_height: " + str(image_height))
            scale_factor = np.divide(or_nrow, image_height)
            print("scale factor: " + str(scale_factor))
            image_width =  int(np.divide(or_ncol,  scale_factor))
            image_width = int(np.divide(image_width, 7))

            print("Image height set to: " + str(image_height) + " image width set to: "+ str(image_width))

            # image_height = 700
            invert = False        # draw black or white

            # self.orig_im_cv2 = self.image_resize(self.orig_im_cv2, height = image_height)

            self.orig_im_cv2 = cv2.resize(self.orig_im_cv2, (image_width, image_height))

            self.orig_im_cv2 = cv2.cvtColor(self.orig_im_cv2, cv2.COLOR_BGR2GRAY)
            __, self.orig_im_cv2 = cv2.threshold(self.orig_im_cv2, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            nrow, ncol= self.orig_im_cv2.shape[:2]
            c = ncol-1
            r = nrow
            print("Nraws {} Ncols {}".format(r, c))

            if invert:
                self.orig_im_cv2 = (255 - self.orig_im_cv2)

            # print(self.orig_im_cv2)
            # cv2.imshow("im", self.orig_im_cv2)
            # cv2.waitKey()

            img = self.orig_im_cv2
            positive = True
            prev_pix = 255

            for c in range(ncol - 1, -1, -1):
                print("c: " + str(c))
                if sum(img[:, c]) == ncol*255:
                    print("Empty line -- skip to next line!")
                    print("----")
                    prev_pix = 255

                else:
                    if positive:
                        print("Positive!")

                        for idx, pix in enumerate(reversed(img[:, c])):
                            # print(idx, pix)

                            # ----------------Plotting--------------------
                            if pix == prev_pix:
                                pass
                                # print("same color!")
                            elif pix < prev_pix:
                                # draw color is black
                                print((len(img[:, c]) - idx), pix)
                                print("Laser off - move to idx: {}!".format(idx))
                                if not PC:
                                    self.laser(0)
                                    # time.sleep(wait_for_pen)
                                    self.wait_to_finish()

                                    self.y_move_targetposition(idx)

                                    self.wait_to_finish()

                                    # time.sleep(wait_for_pen)

                            elif pix > prev_pix:
                                # draw color is white
                                print((len(img[:, c]) - idx), pix)
                                print("Laser on - move to idx: {}!".format(idx))
                                if not PC:
                                    self.laser(1)
                                    # time.sleep(wait_for_pen)
                                    self.wait_to_finish()

                                    self.y_move_targetposition(idx)

                                    self.wait_to_finish()

                                    # time.sleep(wait_for_pen)

                            if idx == len(img[:, c]) - 1:
                                # move to the end
                                print("Move to the end to idx: {}!".format(idx))
                                print((len(img[:, c]) - idx), pix)
                                if pix > 0:
                                    # draw color is black
                                    print("Laser off - move to idx: {}!".format(idx))
                                    if not PC:
                                        self.laser(0)
                                        # time.sleep(wait_for_pen)
                                        self.wait_to_finish()

                                        # self.y_move_targetposition(idx)

                                        # self.wait_to_finish()


                                elif pix == 0:
                                    # draw color is white
                                    print("Laser on - move to idx: {}!".format(idx))
                                    if not PC:
                                        self.laser(1)
                                        # time.sleep(wait_for_pen)
                                        self.wait_to_finish()

                                        self.y_move_targetposition(idx)

                                        self.wait_to_finish()

                                        # time.sleep(wait_for_pen)

                            prev_pix = pix
                            # ------------------------------------------

                        print("----")
                        positive = False
                        prev_pix = 255

                    else:
                        print("Negative!")

                        for idx, pix in enumerate(img[:, c]):
                            # print(idx, pix)

                            # ----------------Plotting--------------------
                            if pix == prev_pix:
                                pass
                                # print("same color!")
                            elif pix < prev_pix:
                                # draw color is black
                                print((len(img[:, c]) - idx), pix)
                                print("Laser off - move to idx: {}!".format((len(img[:, c]) - idx)))
                                if not PC:
                                    self.laser(0)
                                    # time.sleep(wait_for_pen)
                                    self.wait_to_finish()

                                    self.y_move_targetposition((len(img[:, c]) - idx))

                                    self.wait_to_finish()

                                    # time.sleep(wait_for_pen)

                            elif pix > prev_pix:
                                # draw color is white
                                print((len(img[:, c]) - idx), pix)
                                print("Laser on - move to idx: {}!".format((len(img[:, c]) - idx)))
                                if not PC:
                                    self.laser(1)
                                    # time.sleep(wait_for_pen)
                                    self.wait_to_finish()

                                    self.y_move_targetposition((len(img[:, c]) - idx))

                                    self.wait_to_finish()

                                    # time.sleep(wait_for_pen)

                            if idx == len(img[:, c]) - 1:
                                # move to the end
                                print((len(img[:, c]) - idx), pix)
                                print("Move to the end to idx: {}!".format((len(img[:, c]) - idx)))
                                if pix > 0:
                                    # draw color is black
                                    print("Laser off - move to idx: {}!".format((len(img[:, c]) - idx)))
                                    if not PC:
                                        self.laser(0)
                                        # time.sleep(wait_for_pen)
                                        self.wait_to_finish()

                                        # self.y_move_targetposition(0)

                                        # self.wait_to_finish()


                                elif pix == 0:
                                    # draw color is white
                                    print("Laser on - move to idx: {}!".format((len(img[:, c]) - idx)))
                                    if not PC:
                                        self.laser(1)
                                        # time.sleep(wait_for_pen)
                                        self.wait_to_finish()

                                        self.y_move_targetposition(0)

                                        self.wait_to_finish()

                                        # time.sleep(wait_for_pen)

                            prev_pix = pix
                            # ------------------------------------------

                        print("----")
                        positive = True
                        prev_pix = 255

                # X MOVE with wheels
                print("Move to next line!")
                print("Laser off!")
                self.laser(0)
                print("----> x ")
                # time.sleep(wait_for_pen)

                self.wait_to_finish()

                if not self.var1.get():
                    print("Straight print!")
                    self.x_move_relative(steps=6)
                    time.sleep(0.2)
                else:
                    print("Curve print!")
                    self.x_move_curve()
                    time.sleep(0.4)

            # Done
            # self.pos_label.configure(text="Done printing!")
            self.run = False
            time.sleep(0.5)
            self.led.set_blue()

            self.homing = False


class BackgroundTask():

    def __init__( self, taskFuncPointer ):
        self.__taskFuncPointer_ = taskFuncPointer
        self.__workerThread_ = None
        self.__isRunning_ = False

    def taskFuncPointer( self ) : return self.__taskFuncPointer_

    def isRunning( self ) :
        return self.__isRunning_ and self.__workerThread_.isAlive()

    def start( self ):
        if not self.__isRunning_ :
            self.__isRunning_ = True
            self.__workerThread_ = self.WorkerThread( self )
            # Kills thread on end of program
            self.__workerThread_.daemon = True

            self.__workerThread_.start()

    def stop( self ) : self.__isRunning_ = False

    class WorkerThread( threading.Thread ):
        def __init__( self, bgTask ):
            threading.Thread.__init__( self )
            self.__bgTask_ = bgTask

        def run( self ):
            try :
                self.__bgTask_.taskFuncPointer()( self.__bgTask_.isRunning )
            except Exception as e: print(e)
            self.__bgTask_.stop()




if __name__ == "__main__":
    # root = Tk()
    # root.geometry("800x480")

    myapp = MyApp()
    myapp.myContainer1.mainloop()
