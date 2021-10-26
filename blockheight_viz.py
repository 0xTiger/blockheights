import json
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

dat = lambda x: [v.get(x, 0) for v in layers.values()]
merge_dicts = lambda dicts: sum((Counter(d) for d in dicts), Counter())

cache_file = 'dataset.json'

print("Loading cache")
with open(cache_file) as f:
    cache = json.load(f)
    layers = cache['layers']

total_counts = merge_dicts(layers.values())
blocktypes = [{'id': id, 'data': dat(id), 'total': v} for id, v in total_counts.items()]
blocktypes = sorted(blocktypes, key=lambda x: -1*x['total'])

distribs = [blocktype['data'] for blocktype in blocktypes]
names = [blocktype['id'] for blocktype in blocktypes]
print(total_counts)

print("Plotting Data")
plt.style.use('ggplot')

fig, ax = plt.subplots()
plt.stackplot(range(256), distribs, labels=names)

fig2, ax2 = plt.subplots()

def animate(i):
    type = blocktypes[i]

    ax2.clear()
    ax2.plot(range(256), type['data'], label=type['id'], color='#111111')#, color=ore['color'])
    ax2.fill_between(range(256), type['data'], color='#111111')
    ax2.legend()

    try:
        imagebox = OffsetImage(mpimg.imread('textures/' + type['id'] + '.png'), zoom=5)
        ax2.add_artist(AnnotationBbox(imagebox, (0.985,0.9), xycoords='axes fraction', frameon=False, annotation_clip=True, box_alignment=(1,1)))
    except FileNotFoundError:
        try:
            imagebox = OffsetImage(mpimg.imread('textures/missing.png'), zoom=5)
            ax2.add_artist(AnnotationBbox(imagebox, (0.985,0.9), xycoords='axes fraction', frameon=False, annotation_clip=True, box_alignment=(1,1)))
        except:
            pass

    ax2.set_xlabel('y level')
    ax2.set_ylabel('Abundance')
    ax2.set_title('Distribution of each type \nof block in a minecraft world')

ani = animation.FuncAnimation(fig2, animate, frames=range(len(blocktypes)), interval=2000, repeat_delay=2000)
# ani.save("blockheights.mp4")
plt.show()
