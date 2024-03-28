import cv2
from inference_sdk import InferenceHTTPClient

# Initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="wUU8rX5LcogWMC67u43g"
)

# Open webcam
video = cv2.VideoCapture(0)

# Main loop; infers sequentially until you press "q"
while True:
    # On "q" keypress, exit
    if cv2.waitKey(1) == ord('q'):
        break

    # Get the current image from the webcam
    ret, img = video.read()

    # Perform inference using the Roboflow Infer API
    result = CLIENT.infer(img, model_id="fdm-failures-spaghetti/1")

    # Parse the inference results
    predictions = result['predictions']

    # Visualize the annotated image
    for prediction in predictions:
        # Extract prediction information
        class_name = prediction['class']
        x_min, y_min, x_max, y_max = prediction['boundingBox']

        # Draw bounding box on the image
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(img, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the annotated image
    cv2.imshow('Annotated Image', img)

# Release resources when finished
video.release()
cv2.destroyAllWindows()
