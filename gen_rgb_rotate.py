from __future__ import division

import math

import av
from av.video.frame import VideoFrame
from PIL import Image


width = 320
height = 240
duration = 96

path = 'rgb_rotate.mov'
output = av.open(path, 'w')


stream = output.add_stream("libx264", 24)
#stream.width = width
#stream.height = height
stream.pix_fmt = "yuv420p"

for frame_i in range(duration):

    frame = VideoFrame(width, height, 'rgb24')
    image = Image.new('RGB', (width, height), (
        int(255 * (0.5 + 0.5 * math.sin(frame_i / duration * 2 * math.pi))),
        int(255 * (0.5 + 0.5 * math.sin(frame_i / duration * 2 * math.pi + 2 / 3 * math.pi))),
        int(255 * (0.5 + 0.5 * math.sin(frame_i / duration * 2 * math.pi + 4 / 3 * math.pi))),
    ))
    frame.planes[0].update_buffer(image.tobytes())

    packet = stream.encode(frame)
    if packet:
        output.mux(packet)


# Done!
output.close()
