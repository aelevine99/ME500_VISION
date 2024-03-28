#I found this online, and it make be faster than making individual calls to the API
from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes

pipeline = InferencePipeline.init (
    model_id = "fdm-failures-spaghetti/1",
    video_reference=0,
    on_prediction=render_boxes,
)

pipeline.start()
pipeline.join()
