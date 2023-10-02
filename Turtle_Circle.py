
import turtle

# Define the function that is linked to the circle
def circle_function():
    print('Circle clicked')

# Create a turtle screen and a turtle object
screen = turtle.Screen()
turtle = turtle.Turtle()

# Draw a circle on the screen
turtle.penup()
turtle.goto(5, 5)
turtle.pendown()
turtle.circle(200)

# Set the mouse callback function for the turtle object
turtle.onclick(circle_function)

# Start the turtle event loop
turtle.mainloop()

import threading

def pre():    
    print('Before delay')

timer = threading.Timer(3,pre)
timer.start()
print('After delay')