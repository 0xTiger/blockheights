import json
import matplotlib.pyplot as plt
from collections import Counter

flatten = lambda l: [item for sublist in l for item in sublist]
merge_dicts = lambda dicts: sum((Counter(d) for d in dicts), Counter())

cache_file = 'dataset.json'

print("Loading cache")
with open(cache_file) as f:
    cache = json.load(f)
    layers = {int(k):v for k,v in cache['layers'].items()}

total_counts = merge_dicts(layers.values())
allblocktypes = total_counts.keys()
# print(allblocktypes)

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
    ore['data'] = [v.get(id, 0) for v in layers.values()]
    pltdata.append(flatten([[y]*count for y, count in enumerate(ore['data'])]))

maxhs = [max(ore['data']) for ore in ores]
totals = [sum(ore['data']) for ore in ores]
print(totals)
widthss = list(map(lambda x: x / max(maxhs), maxhs))

print("Plotting Data")
plt.style.use('ggplot')
fig, ax = plt.subplots()

def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(list(range(1, len(labels) + 1)))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Ore type')

parts = ax.violinplot(pltdata, widths=widthss, showmeans=False, showmedians=False,
                        showextrema=False)

for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(ores[i]['color'])
    pc.set_alpha(1)

set_axis_style(ax, list(map(lambda x: x.split('_')[0], [ore['id'] for ore in ores])))
ax.set_ylabel('y level')
ax.set_title('How common are different ores\nin each layer of a minecraft world', fontname='Calibri', fontsize=20)

fig2, ax2 = plt.subplots()

for ore in ores:
    ax2.plot(range(256), ore['data'], label=ore['id'], color=ore['color'])
ax2.legend()

plt.show()
