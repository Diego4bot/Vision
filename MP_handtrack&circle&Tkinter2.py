#Change color of disk when touched in Tkinter Frame 

import cv2
import mediapipe as mp 
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import pygame

# Initialize Pygame mixer
pygame.mixer.init()
#sound 0
pygame.mixer.music.load('C:/Users/user/Documents/Vision MP/Breathe2.mp3')
#sound 1
pygame.mixer.music.load('C:/Users/user/Documents/Vision MP/Breathe2.mp3')
#sound 2
pygame.mixer.music.load('C:/Users/user/Documents/Vision MP/Breathe2.mp3')

mp_drawing=mp.solutions.drawing_utils
mp_drawing_style=mp.solutions.drawing_styles
mphands=mp.solutions.hands

# Define the function that draws a circle
def draw_circle(image, center, radius, color):
    color = tuple(map(int, color))
    cv2.circle(image, center, radius, color, -1)
 
# Define the function that is linked to the circle
def circle_function_1():
    global circle_color_1
    if np.array_equal(circle_color_1, np.array([0, 0, 255])):
        circle_color_1 = np.array([0, 255, 0])    
        channel1 = pygame.mixer.Channel(0)
        channel1.play(pygame.mixer.Sound('Breathe2.mp3'))
    else:
        circle_color_1 = np.array([0, 0, 255]) 

def circle_function_2():
    global circle_color_2
    if np.array_equal(circle_color_2, np.array([0, 0, 255])):
        circle_color_2 = np.array([0, 255, 0])
        channel2 = pygame.mixer.Channel(1)
        channel2.play(pygame.mixer.Sound('Breathe2.mp3'))
    else:
        circle_color_2 = np.array([0, 0, 255])    

def circle_function_3():
    global circle_color_3
    if np.array_equal(circle_color_3, np.array([0, 0, 255])):
        circle_color_3 = np.array([0, 255, 0])
        channel3 = pygame.mixer.Channel(2)
        channel3.play(pygame.mixer.Sound('Breathe2.mp3'))
    else:
        circle_color_3 = np.array([0, 0, 255])  

def circle_function_4():
    global circle_color_4
    if np.array_equal(circle_color_4, np.array([0, 0, 255])):
        circle_color_4 = np.array([0, 255, 0])
    else:
        circle_color_4 = np.array([0, 0, 255])    

def circle_function_5():
    global circle_color_5
    if np.array_equal(circle_color_5, np.array([0, 0, 255])):
        circle_color_5 = np.array([0, 255, 0])
    else:
        circle_color_5 = np.array([0, 0, 255])                            

# Define the function to capture and process the video feed
def capture_feed():
    data, image = cap.read()
    #flip the image
    #supressed for tkinter
    #image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB) 
    
    image = cv2.flip(image,1) 
    
    #storing the results
    results = hands.process(image)
    image_width, image_height = image.shape[1], image.shape[0]
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    # Draw the circle on the image

    draw_circle(image, (100, 100), 30, circle_color_1)
    draw_circle(image, (200, 100), 30, circle_color_2)
    draw_circle(image, (300, 100), 30, circle_color_3)
    draw_circle(image, (400, 100), 30, circle_color_4)
    draw_circle(image, (500, 100), 30, circle_color_5)
    
    dist_value = 50

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                distance = cv2.norm((int(landmark.x * image_width), int(landmark.y * image_height)), (100, 100))
                if distance < dist_value:
                    # Call the function that is linked to the first circle
                    
                    circle_function_1()

                distance = cv2.norm((int(landmark.x * image_width), int(landmark.y * image_height)), (200, 100))
                if distance < dist_value:
                    # Call the function that is linked to the second circle
                    
                    circle_function_2()

                distance = cv2.norm((int(landmark.x * image_width), int(landmark.y * image_height)), (300, 100))
                if distance < dist_value:
                    # Call the function that is linked to the third circle
                    
                    circle_function_3()

                distance = cv2.norm((int(landmark.x * image_width), int(landmark.y * image_height)), (400, 100))
                if distance < dist_value:
                    # Call the function that is linked to the fourth circle
                    
                    circle_function_4()

                distance = cv2.norm((int(landmark.x * image_width), int(landmark.y * image_height)), (500, 100))    
                if distance < dist_value:
                    # Call the function that is linked to the fourth circle
                    
                    circle_function_5()    

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,mphands.HAND_CONNECTIONS)

    # Convert the image to PIL format and display it in the label
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    label.config(image=image)
    label.image = image

    # Call the function again after 1 millisecond
    root.after(1, capture_feed)

# Create a tkinter window and a frame inside it
root = tk.Tk()
root.title("Handtrack")
frame = tk.Frame(root)
frame.pack()

# Create a label inside the frame to display the video feed
label = tk.Label(frame)
label.pack()

# Create a video capture object and a hands object
cap = cv2.VideoCapture(1)
hands = mphands.Hands()

# Set the initial color of the circle to red
circle_color_1 = np.array([0, 0, 255])
circle_color_2 = np.array([0, 0, 255])
circle_color_3 = np.array([0, 0, 255])
circle_color_4 = np.array([0, 0, 255])
circle_color_5 = np.array([0, 0, 255])

# Call the function to capture and process the video feed
capture_feed()

# Start the tkinter event loop
root.mainloop()

# Release the video capture object
cap.release()