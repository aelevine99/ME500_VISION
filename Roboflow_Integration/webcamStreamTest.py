#I found this online, and it may be faster than making individual calls to the API. Still worth looking into if you you'd like to optimize the Roboflow methods
from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes

pipeline = InferencePipeline.init (
    model_id = "fdm-failures-spaghetti/1",
    video_reference=0,
    on_prediction=render_boxes,
)

pipeline.start()
pipeline.join()
