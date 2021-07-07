import io
import numpy as np
import time

from PIL import Image
import pyrealsense2 as rs


class Realsense:
    def __init__(self):
        """initiates the camera for use"""
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

        self.pipeline.start(config)
        self.align = rs.align(rs.stream.color)

    def get_frame(self):
        """Take a depth and colour frame"""
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        colour_frame = aligned_frames.get_color_frame()

        if not depth_frame or not colour_frame:
            return False, None, None

        depth_image = np.asanyarray(depth_frame.get_data())
        colour_image = np.asanyarray(colour_frame.get_data())

        return True, colour_image, depth_image

    def take_colour_photo(self):
        """returns a colour photo in a viewable rightside up format"""
        status, colour_image, depth_image = self.get_frame()
        r_colour_image = np.rot90(colour_image, 3)

        # TODO: check why image layers come back incorrectly
        bimg = Image.fromarray(r_colour_image, "RGB")
        b, g, r = bimg.split()
        img = Image.merge("RGB", (r, g, b))
        img.save("colour_photo.png")

        img_byte = io.BytesIO()
        img.save(img_byte, format="PNG")

        return img_byte.getvalue()

    def fill_depth_holes(self, depth_frame):
        """Fill any holes in the depth frame using filters"""
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        return filled_depth

    def take_colour_depth_photo(self):
        """returns a readable colour frame with aligned depth frame - no rotation"""
        status, colour_image, depth_image = self.get_frame()
        bimg = Image.fromarray(colour_image, "RGB")
        b, g, r = bimg.split()
        img = Image.merge("RGB", (r, g, b))
        img.save("colour_depth.png")

        img_byte = io.BytesIO()
        img.save(img_byte, format="PNG")
        corrected_depth = self.fill_depth_holes(depth_image)

        return img_byte.getvalue(), corrected_depth
