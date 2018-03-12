
import av
import av.filter



inputpath = 'bird.mp4'

icntnr = av.open(inputpath)
ocntnr = av.open(inputpath + ".out.mp4", "w")


ivstrm = next((s for s in icntnr.streams if s.type == 'video'), None)


output_video_stream = ocntnr.add_stream('libx264',24)
output_video_stream.pix_fmt = "yuv420p"

graph = av.filter.Graph()


fchain = []
filter_ = graph.add_buffer(template=ivstrm)
print(filter_.inputs)
fchain.append(filter_)
fchain.append(graph.add("vflip"))
fchain[-2].link_to(fchain[-1])
fchain.append(graph.add("hflip"))
fchain[-2].link_to(fchain[-1])
fchain.append(graph.add("buffersink"))  # graph must end with buffersink...?
fchain[-2].link_to(fchain[-1])

for packet in icntnr.demux():
    for ifr in packet.decode():
        typ = packet.stream.type
        if typ == 'video':
            fchain[0].push(ifr)
            ofr = fchain[-1].pull()
            print(ofr)
            ofr.pts = None
            packet = output_video_stream.encode(ofr)
            print(packet)
            ocntnr.mux(packet)
            # for p in ostrms[typ].encode(ofr):
            #     print(p)
            #     ocntnr.mux(p)

ocntnr.close()
