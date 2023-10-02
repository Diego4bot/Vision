import pygame
import sys
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SQUARE_SIZE = 50
COLOR = (255, 255, 255)

# Create a window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Square properties
square_x = (WINDOW_WIDTH - SQUARE_SIZE) // 2
square_y = WINDOW_HEIGHT - SQUARE_SIZE - 2
square_speed = 5

# Capture webcam input Settings:
drawing_spec = mp_drawing.DrawingSpec
mp_drawing.DrawingSpec(thickness=1, circle_radius=1),

cap = cv2.VideoCapture(1)
# Webcam feed rectangle position and size
webcam_width, webcam_height = 640, 480
webcam_x, webcam_y = 10, 10

# Initialize FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Main game loop ____________________________________________________________________
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     # Check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
        # Ensure the square doesn't move beyond the left edge
        square_x = max(square_x, 0)
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
        # Ensure the square doesn't move beyond the right edge
        square_x = min(square_x, WINDOW_WIDTH - SQUARE_SIZE)

    # Capture webcam frame
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

 #  OpenCV writtable ________________________________________________________________  
    image.flags.writeable = False

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Changes Color from Blue 
    results = face_mesh.process(image) # Face_mesh process Camera 

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Process the image with FaceMesh
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# DRAW LANDMARKS_____________________________________________________________________
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:

# TESSELATION_______________________________________________     
        mp_drawing.draw_landmarks(
            image = image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
            #landmark_drawing_spec=None,
            #connection_drawing_spec=mp_drawing_styles
            #.get_default_face_mesh_iris_connections_style())
        
# / selfie-view / Shaking_________________________________________________________
    cv2.imshow('Face Mesh', cv2.flip(image, 1))
    #cv2.imshow('Face Mesh', image)    
    if cv2.waitKey(100) & 0xFF == 27:  # Shaking prevention
      break
    
    # Check for face detection _____________________________________________________
    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        # Get the X-coordinates of the left and right edges of the face
        left_edge_x = int(face_landmarks.landmark[10].x * WINDOW_WIDTH)
        right_edge_x = int(face_landmarks.landmark[10].x * WINDOW_WIDTH)

        # Calculate the square's new position based on the face landmarks
        square_x = left_edge_x + (right_edge_x - left_edge_x) / 2 - SQUARE_SIZE / 2
        

        # Ensure the square doesn't move beyond the left and right edges of the window
        square_x = max(0, min(square_x, WINDOW_WIDTH - SQUARE_SIZE))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the square
    pygame.draw.rect(screen, COLOR, (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))

    # Convert the OpenCV image to a Pygame image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    webcam_surface = pygame.surfarray.make_surface(image_rgb)

    # Resize the webcam feed to fit the desired rectangle size
    angle = -90
    webcam_surface = pygame.transform.scale(webcam_surface, (webcam_height/3, webcam_width/3))
    webcam_surface = pygame.transform.rotate (webcam_surface, angle) 
    # Blit the webcam feed onto the screen
    screen.blit(webcam_surface, (webcam_x, webcam_y))

    # Update the display
    pygame.display.flip()
    
# Release the camera and quit Pygame
cap.release()
pygame.quit()
sys.exit()
