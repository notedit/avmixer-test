

import av
import av.filter
from av.audio import AudioFrame

av.logging.set_level(av.logging.VERBOSE)


args = "sample_rate=%d:sample_fmt=%s:channel_layout=%s:time_base=%d/%d:channels=2" % (
    44100, 's16',
    'stereo',
    1, 44100,
)

graph = av.filter.Graph()

fchain = []
fchain.append(graph.add('abuffer',args))
fchain.append(graph.add('volume','volume=0.5'))
fchain[-2].link_to(fchain[-1])
fchain.append(graph.add('abuffersink'))
fchain[-2].link_to(fchain[-1])

graph.configure()

iframe = AudioFrame('s16', 'stereo', 2048)
iframe.sample_rate = 44100
iframe.time_base = '1/44100'


fchain[0].push(iframe)

oframe = fchain[-1].pull()


