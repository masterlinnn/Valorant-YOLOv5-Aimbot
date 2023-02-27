import torch
from mss import mss
import numpy as np
import time
import math
import keyboard

# Model
model = torch.hub.load("../yolov5", "custom", "../models/valorant-v12.pt")

# Display
displaySize = (1920,1080)
size = 150
center = size / 2
top = int((displaySize[1] - size) / 2)
left = int((displaySize[0] - size) / 2)
monitor = {"top": top, "left": left, "width": size, "height": size}

screenshotCenter = [displaySize[0] / 2, displaySize[1] / 2]



closest_part_distance = 100000
closest_part = -1
with mss() as sct:
    while True:
        ss = np.array(sct.grab(monitor))

        df = model(ss, size=size).pandas().xyxy[0]

        for i in range(0,10):
            try:
                xmin = int(df.iloc[i,0])
                ymin = int(df.iloc[i,1])
                xmax = int(df.iloc[i,2])
                ymax = int(df.iloc[i,3])

                centerX = (xmax-xmin)/2+xmin 
                centerY = (ymax-ymin)/2+ymin

                distance = math.dist([centerX,centerY], screenshotCenter)

                if int(distance) < closest_part_distance:
                    closest_part_distance = distance
                    closest_part = i

            except:
                print("",end="")

        if keyboard.is_pressed("f"):
            xmin = df.iloc[closest_part,0]
            ymin = df.iloc[closest_part,1]
            xmax = df.iloc[closest_part,2]
            ymax = df.iloc[closest_part,3]
            head_center_list = [(xmax-xmin)/2+xmin,(ymax-ymin)/2+ymin]
            
            xdif = (head_center_list[0] - screenshotCenter[0])
            ydif = (head_center_list[1] - screenshotCenter[1])
            data = f"{int(xdif)}:{int(ydif)}"
            print(data)
