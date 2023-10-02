import cv2
import mediapipe as mp

# Load the Selfie Segmentation model from Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# Load the image
image_path = 'C:/Users/user/Documents/Vision MP/girlX.jpg'  # Replace with the path to your image
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run selfie segmentation on the image
with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
    results = selfie_segmentation.process(image)

    # Extract the segmentation mask from the result
    segmentation_mask = results.segmentation_mask

# Apply the segmentation mask to the original image
output_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
output_image[:, :, 3] = segmentation_mask

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Segmentation Mask', segmentation_mask)
cv2.imshow('Output Image', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
