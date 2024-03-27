# import a utility function for loading Roboflow models
from inference import get_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2

# load local image or video feed 
image_file = "Roboflow_Integration\people-walking.jpg" #going to change this to webcame capture
image = cv2.imread(image_file)

# load our model and API key
model = "fdm-failures-spaghetti"
modelAPIKey = "wUU8rX5LcogWMC67u43g"

# run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
results = model.infer(image) #not sure if this is best, working on it

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

# create supervision annotators
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotate the image with our inference results
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

# display the image
sv.plot_image(annotated_image)
