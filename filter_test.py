
import av
import av.filter


setWidthHeight = False

inputpath = 'bird.mp4'

in_contain = av.open(inputpath)
out_contain = av.open(inputpath + ".out.mp4", "w")


in_video_stream = next((s for s in in_contain.streams if s.type == 'video'), None)


out_video_stream = out_contain.add_stream('libx264',24)
out_video_stream.pix_fmt = "yuv420p"


print('width ', out_video_stream.width, 'height ', out_video_stream.height)

graph = av.filter.Graph()
fchain = []
fchain.append(graph.add_buffer(template=in_video_stream))
fchain.append(graph.add("vflip"))
fchain[-2].link_to(fchain[-1])
fchain.append(graph.add("hflip"))
fchain[-2].link_to(fchain[-1])
fchain.append(graph.add("buffersink"))  # graph must end with buffersink...?
fchain[-2].link_to(fchain[-1])


resize_chain = []
resize = av.filter.Graph()
resize_chain.append(resize.add_buffer(template=in_video_stream))
resize_chain.append(resize.add('scale','w=200:h=100'))
resize_chain[-2].link_to(resize_chain[-1])
resize_chain.append(resize.add('buffersink'))
resize_chain[-2].link_to(resize_chain[-1])


overlay_chain = []
overlay = av.filter.Graph()
main_input = overlay.add_buffer(template=in_video_stream)
overlay_input = overlay.add_buffer(template=in_video_stream)
overlay_filter = overlay.add('overlay','main_w-overlay_w-10:main_h-overlay_h-10')

print(overlay_filter.inputs)

main_input.link_to(overlay_filter,0,0)
overlay_input.link_to(overlay_filter,0,1)

buffer_sink = overlay.add('buffersink')
overlay_filter.link_to(buffer_sink)



for packet in in_contain.demux(in_video_stream):
    for ifr in packet.decode():
        print('width ', ifr.width, 'height ', ifr.height)
        if not setWidthHeight:
            out_video_stream.width = ifr.width
            out_video_stream.height = ifr.height
            setWidthHeight = True
        fchain[0].push(ifr)
        ofr = fchain[-1].pull()
        ofr.pts = None

        # test resize

        resize_chain[0].push(ifr)
        outfr = resize_chain[-1].pull()

        print('resize width ',outfr.width, 'height ', outfr.height)

        packet = out_video_stream.encode(ofr)
        out_contain.mux(packet)

out_contain.close()
