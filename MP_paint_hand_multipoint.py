import tkinter as tk
import cv2
import mediapipe as mp
from PIL import ImageTk, Image

# Create the main window
window = tk.Tk()
window.title("Paint Program")

# Create a canvas for drawing
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Variables for drawing
draw_color = "black"
brush_size = 5
last_x = None
last_y = None

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Initialize the video capture
cap = cv2.VideoCapture(1)

# Create a new window for displaying the camera feed
camera_window = tk.Toplevel(window)
camera_window.title("Camera Feed")

# Create a label for displaying the video feed
video_label = tk.Label(camera_window)
video_label.pack()

# Function to handle mouse events
def on_mouse_down(event):
    global last_x, last_y
    last_x = event.x
    last_y = event.y

def on_mouse_drag(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, fill=draw_color, width=brush_size)
    last_x = event.x
    last_y = event.y

# Function to handle hand landmarks
def handle_hand_landmarks(frame, results):
    global last_x, last_y
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * canvas_width)
                y = int(landmark.y * canvas_height)

                # Draw a circle at each hand landmark position
                canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

        if len(results.multi_hand_landmarks) > 0:
            index_finger_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * canvas_width)
            y = int(index_finger_tip.y * canvas_height)

            # Draw a line on the canvas
            if last_x is not None and last_y is not None:
                canvas.create_line(last_x, last_y, x, y, fill=draw_color, width=brush_size)

            # Update the last position
            last_x = x
            last_y = y


# Function to change the brush color
def change_color(new_color):
    global draw_color
    draw_color = new_color

# Function to change the brush size
def change_size(new_size):
    global brush_size
    brush_size = new_size

# Create color buttons
color_buttons = [
    ("Black", "black"),
    ("Red", "red"),
    ("Green", "green"),
    ("Blue", "blue"),
]
for text, color in color_buttons:
    button = tk.Button(window, text=text, bg=color, command=lambda c=color: change_color(c))
    button.pack(side=tk.LEFT, padx=5)

# Create size buttons
size_buttons = [
    (5, "Small"),
    (10, "Medium"),
    (15, "Large"),
]
for size, label in size_buttons:
    button = tk.Button(window, text=label, command=lambda s=size: change_size(s))
    button.pack(side=tk.LEFT, padx=5)

# Bind mouse events to canvas
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)

# Function to update the video frame
def update_frame():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror-like effect

    # Convert the frame to RGB for Mediapipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hand landmarks
    results = hands.process(frame_rgb)
    handle_hand_landmarks(frame, results)

    # Convert the frame back to BGR for display in Tkinter
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame_image = Image.fromarray(frame_bgr)
    frame_tk = ImageTk.PhotoImage(image=frame_image)

    # Update the video label in the camera window
    video_label.configure(image=frame_tk)
    video_label.image = frame_tk

    # Schedule the next frame update
    window.after(10, update_frame)

# Start updating the video frame
update_frame()

# Start the Tkinter event loop
window.mainloop()

# Release the video capture
cap.release()
