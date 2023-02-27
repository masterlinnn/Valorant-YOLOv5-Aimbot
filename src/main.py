import torch
from mss import mss
import numpy as np
import time
import math
import keyboard
from yaml import load, dump, Loader
import cv2
import serial
from pynput.mouse import Controller
from pynput import mouse

buttonX1 = False
buttonX2 = False

mouseController = Controller()
def on_click(x_, y_, button, pressed):
    global buttonX1, buttonX2
    if button == button.x1 and pressed:
        buttonX1 = True
    elif button == button.x1 and not pressed:
        buttonX1 = False
        
    if button == button.x2 and pressed:
        buttonX2 = True
    elif button == button.x2 and not pressed:
        buttonX2 = False
    # print("x: {} | y: {} | button: {} | pressed: {}".format(x_, y_, button, pressed))

mouse_listener = mouse.Listener(
    on_click=on_click
)
mouse_listener.start()

with open("config.yaml", "r") as yml:
    config = load(yml, Loader=Loader)


# Model
model = torch.hub.load(config["yolov5"]["path"], "custom", path=config["yolov5"]["model"], source="local").cuda()

try:
    arduino = serial.Serial(config["arduino"]["port"], int(config["arduino"]["baudrate"]),timeout=config["arduino"]["timeout"])
except:
    raise Exception("The arduino is not connected to PC or the Arduino's COM port is wrong.")

# Display
displaySize = (1920,1080)
size = 150
center = size / 2
top = int((displaySize[1] - size) / 2)
left = int((displaySize[0] - size) / 2)
monitor = {"top": top, "left": left, "width": size, "height": size}

def sendCode(code):
    encoded = str.encode(code)
    arduino.write(encoded)
    

with mss() as sct:
    while True:
        ss = np.array(sct.grab(monitor))

        df = model(ss, size=size).pandas().xyxy[0]

        try:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])

            head = (int(xmin + (xmax - xmin) / 2), int(ymin + (ymax - ymin) / 8))

            distance = (head[0] - center, head[1] - center)

            if keyboard.is_pressed(config["keyconfig"]["silent"]):
            # if buttonX1:
                # print("head", head[0], head[1])
                print("head dis", distance[0], distance[1])
                code = f",{distance[0]},{distance[1]},silent*"
                sendCode(code)
                time.sleep(0.01)
            if keyboard.is_pressed(config["keyconfig"]["shoot"]):
            # if buttonX2:
                # print("head", head[0], head[1])
                print("head dis", distance[0], distance[1])
                code = f",{distance[0]},{distance[1]},shoot*"
                sendCode(code)
                time.sleep(0.175)

        except:
            pass

        # cv2.imshow("", ss)
        # if(cv2.waitKey(1) == ord('l')):
        #     cv2.destroyAllWindows()
        #     break