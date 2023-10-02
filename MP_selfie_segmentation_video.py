"""
#MEDIAPIPE,maskSegmentation Mediapipe and cv2 in Video

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# Initialize the camera
cap = cv2.VideoCapture(1)

# Initialize the hair segmentation model
with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image
        results = selfie_segmentation.process(image)

        # Extract the hair mask
        mask = results.segmentation_mask

        # Convert the data type of the mask to 8-bit unsigned
        mask = mask.astype('uint8')

        # Apply the mask to the original image
        add_mask = cv2.bitwise_and(image, image, mask=mask)

        # Show the results
        cv2.imshow('Original Image', image)
        cv2.imshow('Mask', mask)
        cv2.imshow('Core', add_mask)

        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()





import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# Initialize the camera
cap = cv2.VideoCapture(1)

# Initialize the hair segmentation model
model_selection = 1  # Change this to select the desired model (0 or 1)
mask_scope = 0.2     # Adjust this value to control the mask scope (0.0 to 1.0)
mask_threshold = 0.5 # Adjust this value to control the mask threshold (0.0 to 1.0)

with mp_selfie_segmentation.SelfieSegmentation(model_selection=model_selection) as selfie_segmentation:

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image
        results = selfie_segmentation.process(image)

        # Extract the hair mask
        mask = results.segmentation_mask

        # Create a custom mask based on threshold
        custom_mask = np.zeros_like(mask)
        custom_mask[mask >= mask_threshold] = 1

        # Apply the custom mask to the original image
        add_mask = cv2.bitwise_and(image, image, mask=custom_mask.astype('uint8'))

        # Show the results
        cv2.imshow('Original Image', image)
        cv2.imshow('Mask', custom_mask * 255)  # Display the mask as a grayscale image
        cv2.imshow('Core', add_mask)

        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


"""

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# Initialize the camera
cap = cv2.VideoCapture(1)

# Initialize the hair segmentation model
model_selection = 1  # Change this to select the desired model (0 or 1)
mask_threshold = 0.5 # Adjust this value to control the mask threshold (0.0 to 1.0)
mask_fade = 1       # Adjust this value to control the mask fade size

with mp_selfie_segmentation.SelfieSegmentation(model_selection=model_selection) as selfie_segmentation:

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image
        results = selfie_segmentation.process(image)

        # Extract the hair mask
        mask = results.segmentation_mask

        # Create a custom mask based on threshold
        custom_mask = np.zeros_like(mask)
        custom_mask[mask >= mask_threshold] = 1

        # Create a mask for the fade effect
        mask_fade_effect = cv2.GaussianBlur(custom_mask, (0, 0), mask_fade)
        custom_mask = cv2.addWeighted(custom_mask, 1, mask_fade_effect, -1, 0)

        # Apply the custom mask to the original image
        add_mask = cv2.bitwise_and(image, image, mask=custom_mask.astype('uint8'))

        # Show the results
        cv2.imshow('Original Image', image)
        cv2.imshow('Mask', custom_mask * 255)  # Display the mask as a grayscale image
        cv2.imshow('Core', add_mask)

        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
