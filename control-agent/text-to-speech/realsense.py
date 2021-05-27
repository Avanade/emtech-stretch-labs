import pyrealsense2 as rs
import numpy as np
import time
import math

from PIL import Image
import io

import speech

def take_photo():
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    profile = pipeline.start(config)
    # Get the sensor once at the beginning. (Sensor index: 1)
    sensor = pipeline.get_active_profile().get_device().query_sensors()[1]
    # Set the exposure anytime during the operation
    sensor.set_option(rs.option.exposure, 80.000)

    # We will be removing the background of objects more than
    #  clipping_distance_in_meters meters away
    clipping_distance_in_meters = 1.5 
    
    time.sleep(2)#or the picture will look green

    align_to = rs.stream.color
    align = rs.align(align_to)

    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)
    color_frame = aligned_frames.get_color_frame()

    color_image = np.asanyarray(color_frame.get_data())
    r_color_image = np.rot90(color_image,3)

    bimg = Image.fromarray(r_color_image,'RGB')
    b,g,r = bimg.split()
    img = Image.merge("RGB",(r,g,b))
    img.save('test.png')

    img_byte = io.BytesIO()
    img.save(img_byte,format='PNG')

    return(img_byte.getvalue())


