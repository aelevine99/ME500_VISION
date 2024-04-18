import cv2
import subprocess
from inference_sdk import InferenceHTTPClient

# Initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="wUU8rX5LcogWMC67u43g"
)

# Main loop; infers sequentially until you press "q"
while True:
    # On "q" keypress, exit
    def signal_handler(sig, frame):
        print("Ctrl+C detected. Exiting...")
        exit(0)

    # Get the current image from the webcam
    subprocess.run(["fswebcam", "-r", "1280x720", "--jpeg", "100", "--save", "/home/me500/fdmVision/image.jpg"])
    img = cv2.imread("/home/me500/fdmVision/image.jpg")

    # Perform inference using the Roboflow Infer API
    result = CLIENT.infer(img, model_id="fdm-failures-spaghetti/1")

    # Parse the inference results
    predictions = result['predictions']

    for prediction in predictions:
        # Extract prediction information
        print(prediction)
        class_name = prediction['class']
        x, y = int(prediction['x']), int(prediction['y'])
        print(x,y)
        width, height = int(prediction['width']), int(prediction['height'])
        print(width,height)
        confidence = int(prediction['confidence'])
        print(confidence)

        # Draw bounding box on the image
        topLeft = (int(x-width/2),int(y+height/2))
        print(topLeft)
        bottomRight = (int(x+width/2),int(y-height/2))
        print(bottomRight)
        cv2.rectangle(img, topLeft, bottomRight, (0, 255, 0), 2)
        cv2.putText(img, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        annotatedImagePath = "/home/me500/fdmVision/annotated_image.jpg"
        cv2.imwrite(annotatedImagePath,img)
        exit(0)
