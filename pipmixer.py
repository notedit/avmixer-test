

import sys

import av

container = av.open('guigu_1.mp4')


for bbbb, frame in enumerate(container.decode(video=0)):
    frame = frame.to_rgb()
    small_frame = frame.reformat(frame.width/2,frame.height/2,frame.format.name)
    big_rgb_bytes = bytearray(frame.planes[0].to_bytes())
    small_rgb_bytes = bytearray(small_frame.planes[0].to_bytes())
    # just top right for now 
    w = frame.width * 3
    h = frame.height
    sw = small_frame.width * 3
    sh = small_frame.height
    for i in range(sh):
        big_rgb_bytes[i*w:i*w+sw] = small_rgb_bytes[i*sw:i*sw+sw]

    frame.planes[0].update_buffer(big_rgb_bytes)
    frame.to_image().save('%04d.jpg' % bbbb)
    if bbbb > 5:
        break
