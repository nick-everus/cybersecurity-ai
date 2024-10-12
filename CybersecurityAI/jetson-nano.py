import pyds
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Create the pipeline
pipeline = Gst.parse_launch("filesrc location=video.mp4 ! decodebin ! nvstreammux name=mux batch-size=1 ! nvinfer config-file-path=yolo_config.txt ! nvvidconv ! nveglglessink")

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Wait for EOS or errors
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS | Gst.MessageType.ERROR)

# Stop the pipeline
pipeline.set_state(Gst.State.NULL)