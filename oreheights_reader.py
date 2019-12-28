import json
import numpy as np
import matplotlib.pyplot as plt


flatten = lambda l: [item for sublist in l for item in sublist]

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
allblocktypes = [k for k,v in total_counts.items()]
print(allblocktypes)

ores = [{'id': 'coal_ore', 'color': '#141212'},
        {'id': 'iron_ore', 'color': '#f2b28a'},
        {'id': 'redstone_ore', 'color': '#ff0000'},
        {'id': 'gold_ore', 'color': '#fce232'},
        {'id': 'lapis_ore', 'color': '#112fb8'},
        {'id': 'diamond_ore', 'color': '#33ffeb'},
        {'id': 'emerald_ore', 'color': '#18d921'}]

pltdata = []
for ore in ores:
    id = ore['id']
    ore['data'] = [(v[id] if id in v else 0) for _,v in layers.items()]
    pltdata.append(flatten([[k]*v[id] for k,v in layers.items() if id in v]))

maxhs = [max(ore['data']) for ore in ores]
totals = [sum(ore['data']) for ore in ores]
print(totals)
widthss = map(lambda x: float(x) / max(maxhs), maxhs)

print("Plotting Data")
plt.style.use('ggplot')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Ore type')

parts = ax.violinplot(
        pltdata, widths=widthss, showmeans=False, showmedians=False,
        showextrema=False)

i = 0
for pc in parts['bodies']:
    pc.set_facecolor(ores[i]['color'])
    pc.set_alpha(1)
    i += 1

set_axis_style(ax, map(lambda x: x.split('_')[0], [ore['id'] for ore in ores]))
plt.ylabel('y level')
plt.title('How common are different ores\nin each layer of a minecraft world', fontname='Calibri', fontsize=20)

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)

for ore in ores:
    plt.plot(range(256), ore['data'], label=ore['id'], color=ore['color'])
plt.legend()

plt.show()
