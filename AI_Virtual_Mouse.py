# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:06:28 2024

@author: Shraddha
"""

#Step 1: Video Capture
#Step 2: Detect hand
#Step 3: Separate index finger
#Step 4: Move the mouse pointer using index finger
#Step 5: CLicking using virtual mouse 

import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0) #0 is to capture the first video source
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils #to draw the landmarks on the hand
screen_width, screen_height = pyautogui.size() #Gives the dimension of the screen

index_y = 0

while True:
    _, frame = cap.read() #capture frame
    frame = cv2.flip(frame, 1) #flip on the y axis = 1, x axis = 0 i.e. change direction
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convert color of the frame
    output = hand_detector.process(rgb_frame) #Process the rgb frame using hand_detector
    hands = output.multi_hand_landmarks #Marks the points on the hand
    
    if hands: 
       
        for hand in hands:
           drawing_utils.draw_landmarks(frame, hand) #to draw the landmark on the hand in the frame
           landmarks = hand.landmark #gives landmarks on the hand
           
           for id, landmark in enumerate(landmarks): 
               x = int(landmark.x * frame_width)
               y = int(landmark.y * frame_height)
               print(x,y) #coordinates of the 8th landmark
               
               if id == 8:
                   cv2.circle(img = frame, center = (x,y), radius = 15, color=(0,255,255) ) #Draws circle around the landmark of the tip of the index finger
                   index_x = screen_width / frame_width * x  #cursor covers the whole screen and not just the frame
                   index_y = screen_height / frame_height * y 
                   pyautogui.moveTo(index_x,index_y)
                   
               if id == 4:
                  cv2.circle(img = frame, center = (x,y), radius = 15, color=(255,0,0) ) #Draws circle around the landmark of the tip of the thumb
                  thumb_x = screen_width / frame_width * x #cursor covers the whole screen and not just the frame
                  thumb_y = screen_height / frame_height * y
               
            
                  print('Outside', abs(index_y - thumb_y))
                        
                  if abs(index_y - thumb_y) < 30 : 
                      pyautogui.click()
                      pyautogui.sleep(1)
                    
   
    cv2.imshow('Virtual Mouse', frame) #to display the image
    cv2.waitKey(1)
    

