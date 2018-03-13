

import av
import av.filter
from av.audio import AudioFrame

av.logging.set_level(av.logging.VERBOSE)

audio1 = 'result.wav'
audio2 = 'audio2.mp3'

audio_out = 'audio_out.mp3'

container1 = av.open(audio1)
container2 = av.open(audio2)

at = next((s for s in container1.streams if s.type == 'audio'), None)


print(at)

container_out = av.open(audio_out, "w")

out_stream = container_out.add_stream(template=at)


args = "sample_rate=%d:sample_fmt=%s:channel_layout=%s:time_base=%d/%d" % (
    44100, 's16',
    'stereo',
    1, 44100,
)

print(args)

graph = av.filter.Graph()

fchain = []
fchain.append(graph.add('abuffer',args))
fchain.append(graph.add('abuffersink'))
fchain[-2].link_to(fchain[-1])


# for packet in container1.demux():
#     for ifr in packet.decode():
#         print(ifr)
#         typ = packet.stream.type
#         if typ == 'audio':
#             #print(ifr)
#             fchain[0].push(ifr)
#             #print('push')
#             ofr = fchain[-1].pull()
#             # print(ofr)

resampler = av.AudioResampler('s16', 'stereo',44100)

iframe = AudioFrame('s16', 'stereo', 1024,False)
iframe.sample_rate = 44100
iframe.time_base = '1/44100'
iframe.pts = 0

oframe = resampler.resample(iframe)

print(oframe)

print('channels', len(oframe.layout.channels), oframe.samples)


fchain[0].push(iframe)



