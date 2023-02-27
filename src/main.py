import torch
from mss import mss
import numpy as np
import time
import math
import keyboard
from yaml import load, dump, Loader
import cv2
import serial

with open("config.yaml", "r") as yml:
    config = load(yml, Loader=Loader)


# Model
model = torch.hub.load(config["yolov5"]["path"], "custom", path=config["yolov5"]["model"], source="local")

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
                # print("head", head[0], head[1])
                # print("head dis", distance[0], distance[1])
                code = f",{head[0]},{head[1]},silent*"
                sendCode(code)

        except:
            pass

        # cv2.imshow("", ss)
        # if(cv2.waitKey(1) == ord('l')):
        #     cv2.destroyAllWindows()
        #     break