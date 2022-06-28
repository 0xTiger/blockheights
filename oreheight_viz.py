import json
from collections import Counter

import matplotlib.pyplot as plt

YRANGE = range(-64, 320)
flatten = lambda l: [item for sublist in l for item in sublist]
merge_dicts = lambda dicts: sum((Counter(d) for d in dicts), Counter())

cache_file = 'out.json'

with open(cache_file) as f:
    cache = json.load(f)
    layers = {int(k):v for k,v in cache['layers'].items()}
total_counts = merge_dicts(layers.values())
allblocktypes = total_counts.keys()

ores = [
    {'ids': ['coal_ore', 'deepslate_coal_ore'], 'color': '#141212'},
    {'ids': ['iron_ore', 'deepslate_iron_ore'], 'color': '#f2b28a'},
    {'ids': ['copper_ore', 'deepslate_copper_ore'], 'color': '#db5825'},
    {'ids': ['redstone_ore', 'deepslate_redstone_ore'], 'color': '#ff0000'},
    {'ids': ['gold_ore', 'deepslate_gold_ore'], 'color': '#fce232'},
    {'ids': ['lapis_ore', 'deepslate_lapis_ore'], 'color': '#112fb8'},
    {'ids': ['diamond_ore', 'deepslate_diamond_ore'], 'color': '#33ffeb'},
    {'ids': ['emerald_ore', 'deepslate_emerald_ore'], 'color': '#18d921'},
]
ore_names = [ore['ids'][0].split('_')[0] for ore in ores]

pltdata = []
for ore in ores:
    ids = ore['ids']
    ore['data'] = [sum(v.get(id, 0) for id in ids) for v in layers.values()]
    pltdata.append(flatten([[y]*count for y, count in zip(YRANGE, ore['data'])]))

maxhs = [max(ore['data']) for ore in ores]
totals = [sum(ore['data']) for ore in ores]
widthss = list(map(lambda x: x / max(maxhs), maxhs))
print(totals)

plt.style.use('ggplot')
fig, ax = plt.subplots()
parts = ax.violinplot(pltdata, widths=widthss, showextrema=False)
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(ores[i]['color'])
    pc.set_alpha(1)
ax.grid(visible=False, axis='x')
ax.set_xticks(list(range(1, len(ore_names) + 1)))
ax.set_xticklabels(ore_names, rotation=30, ha='right')
ax.set_xlim(0.25, len(ore_names) + 0.75)
ax.set_xlabel('Ore type')
ax.set_ylabel('y level')
ax.set_title('How common are different ores\nin each layer of a minecraft world', fontname='Calibri', fontsize=20)

fig2, ax2 = plt.subplots()
for ore in ores:
    ax2.plot(YRANGE, ore['data'], label=ore['ids'][0], color=ore['color'])
ax2.legend()

plt.show()
