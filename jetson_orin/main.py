import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

import threading

# Global variables
sensor_id = int(os.environ.get('CAMERA_ID', '0'))
audio_card_id = os.environ.get('MICROPHONE_ID', '0,0')
port_number = int(os.environ.get('PORTNUMBER', '8000'))
folder_location = "/tmp/recordings/"
print(sensor_id, audio_card_id, port_number)

# Gstreamer
Gst.init(None)

loop = None

def video_stream_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    framerate=30,
    flip_method=0,
    rtmp_uri="rtmp://0.0.0.0/live/video"
    ):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1, format=NV12 ! "
        "nvvidconv flip-method=%d ! "
        "x264enc ! "
        "flvmux name=mux ! "
        "rtmpsink location=%s "
        %(
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            rtmp_uri,
        )
    )

def audio_stream_pipeline(
    audio_card_id='0,0',
    rtmp_uri="rtmp://0.0.0.0/live/audio"
    ):
    return (
        "alsasrc device=hw:%s ! "
        "audioconvert ! "
        "audioresample ! "
        "voaacenc ! "
        "flvmux name=mux ! "
        "rtmpsink location=%s "
        %(
            audio_card_id,
            rtmp_uri,
        )
    )

video_stream_pipeline = Gst.parse_launch(video_stream_pipeline(sensor_id=sensor_id))
audio_stream_pipeline = Gst.parse_launch(audio_stream_pipeline(audio_card_id=audio_card_id))

def start_stream_pipeline():
    global video_stream_pipeline
    global audio_stream_pipeline
    video_stream_pipeline.set_state(Gst.State.PLAYING)
    audio_stream_pipeline.set_state(Gst.State.PLAYING)
    time.sleep(1)

def stop_stream_pipeline():
    global video_stream_pipeline
    global audio_stream_pipeline
    if video_stream_pipeline is not None:
        video_stream_pipeline.set_state(Gst.State.NULL)
    if audio_stream_pipeline is not None:
        audio_stream_pipeline.set_state(Gst.State.NULL)
    time.sleep(1)

def video_record_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    framerate=30,
    flip_method=0,
    filename=folder_location+"video.flv",
    ):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1, format=NV12 ! "
        "nvvidconv flip-method=%d ! "
        "x264enc ! "
        "flvmux name=mux ! "
        "filesink location=%s "
        %(
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            filename,
        )
    )

def audio_record_pipeline(
    audio_card_id='0,0',
    filename=folder_location+"audio.flv",
    ):
    return (
        "alsasrc device=hw:%s ! "
        "audioconvert ! "
        "audioresample ! "
        "voaacenc ! "
        "flvmux name=mux ! "
        "filesink location=%s "
        %(
            audio_card_id,
            filename,
        )
    )


video_record_pipeline = Gst.parse_launch(video_record_pipeline(sensor_id=sensor_id))
audio_record_pipeline = Gst.parse_launch(audio_record_pipeline(audio_card_id=audio_card_id))

def start_record_pipeline():
    global video_record_pipeline
    global audio_record_pipeline
    video_record_pipeline.set_state(Gst.State.PLAYING)
    audio_record_pipeline.set_state(Gst.State.PLAYING)
    time.sleep(1)

def stop_record_pipeline():
    global video_record_pipeline
    global audio_record_pipeline
    if video_record_pipeline is not None:
        video_record_pipeline.set_state(Gst.State.NULL)
    if audio_record_pipeline is not None:
        audio_record_pipeline.set_state(Gst.State.NULL)
    time.sleep(1)

# FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global loop
    loop = GObject.MainLoop()
    threading.Thread(target=loop.run).start()
    time.sleep(1)

@app.get("/stream_start")
async def start():
    start_stream_pipeline()
    return {"message": "Live stream pipeline started"}

@app.get("/stream_stop")
async def stop():
    stop_stream_pipeline()
    return {"message": "Live stream pipeline stopped"}

@app.get("/record_start")
async def start():
    start_record_pipeline()
    return {"message": "Record pipeline started"}

@app.get("/record_stop")
async def stop():
    stop_record_pipeline()
    return {"message": "Record pipeline stopped"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port_number)
