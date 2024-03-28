import roboflow

rf = roboflow.Roboflow(api_key="wUU8rX5LcogWMC67u43g")

project = rf.workspace().project("fdm-failures-spaghetti")
model = project.version("1").model

# optionally, change the confidence and overlap thresholds
# values are percentages
model.confidence = 50
model.overlap = 25

#define local image
image = "Roboflow_Integration\spaghetti-test.jpg"

# predict on a local image
prediction = model.predict(image)

# Plot the prediction in an interactive environment
prediction.plot()

# Convert predictions to JSON
print(prediction.json())