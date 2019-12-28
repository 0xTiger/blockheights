import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

flatten = lambda l: [item for sublist in l for item in sublist]
dat = lambda x: [(v[x] if x in v else 0) for _,v in layers.items()]

def dict_merge(dicts):
    neodict = {}
    for k, v in reduce(lambda x,y: x + y, [d.items() for d in dicts]):
        if k in neodict.keys():
            neodict[k] += v
        else:
            neodict[k] = v
    return neodict

cache_file = 'dataset.json'

print("Loading cache")
with open(cache_file) as f:
    cache = json.load(f)
    layers = {int(k):v for k,v in cache['layers'].items()}

total_counts = dict_merge([v for k,v in layers.items()])
blocktypes = [{'id': k, 'data': dat(k), 'total': v} for k,v in total_counts.items()]
blocktypes = sorted(blocktypes, key=lambda x: -1*x['total'])

distribs = [blocktype['data'] for blocktype in blocktypes]
names  = [blocktype['id'] for blocktype in blocktypes]
print(names)

print("Plotting Data")
plt.style.use('ggplot')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

plt.stackplot(range(256), distribs, labels=names)

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)

def animate(i):
    type = blocktypes[i]

    ax2.clear()
    ax2.plot(range(256), type['data'], label=type['id'], color='#111111')#, color=ore['color'])
    ax2.fill_between(range(256), type['data'], color='#111111')
    ax2.legend()

    try:
        imagebox = OffsetImage(mpimg.imread('textures\\' + type['id'] + '.png'), zoom=3)
        ax2.add_artist(AnnotationBbox(imagebox, (0.870,0.8), xycoords='axes fraction', frameon=False, annotation_clip=True))
    except:
        imagebox = OffsetImage(mpimg.imread('textures\\missing.png'), zoom=3)
        ax2.add_artist(AnnotationBbox(imagebox, (0.870,0.8), xycoords='axes fraction', frameon=False, annotation_clip=True))

    plt.xlabel('y level')
    plt.ylabel('Abundance')
    plt.title('Distribution of each type \nof block in a minecraft world')

ani = animation.FuncAnimation(fig2, animate, frames=range(len(blocktypes)), interval=500, repeat_delay=2000)
ani.save("blockheights.mp4")
plt.show()
