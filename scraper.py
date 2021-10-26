import os
import json
from anvil import Region, Chunk
from itertools import product
from collections import Counter
from timeit import default_timer as timer

ord = lambda x: x[0]*32 + x[1]

def spiral_iter(t):
    x, y = t
    # Starts (0,0) -> (1,0) and continues anti-clockwise
    if x > y > -1*x: y += 1 # Walk UP
    elif y >= x and y > -1*x: x -= 1 # Walk LEFT
    elif x < y <= -1*x: y -= 1 # Walk DOWN
    elif y <= x and y <= -1*x: x += 1 # Walk RIGHT
    return (x, y)

if os.name == 'nt':
    minecraft_path = os.environ.get("LOCALAPPDATA")
elif os.name == 'posix':
    minecraft_path = os.environ.get("HOME")


world = 'myworld'
cache_file = 'dataset2.json'
linearPath = True #Determines which regions are chosen for scanning and in which order


world_folder = os.path.join(minecraft_path, '.minecraft/saves', world)
try:
    print("Loading cache")
    with open(cache_file) as f:
        cache = json.load(f)
        layers = {int(k):Counter(v) for k,v in cache['layers'].items()}
        latest_c, latest_r = cache['latest']['chunk'], cache['latest']['region']
except FileNotFoundError:
    print("FileNotFoundError: starting anew")
    layers = {y: Counter() for y in range(256)}
    latest_c, latest_r = (0, 0), (0, 0)

print(f'Starting in r: {latest_r}, c: {latest_c}')
while True: # Steps through regions
    a , b = latest_r
    region = Region.from_file(f'{world_folder}/region/r.{a}.{b}.mca')

    for c in product(range(32),range(32)): # Steps through chunks
        start = timer()
        if Region.chunk_location(region, *c)[0] != 0 and ord(c) > ord(latest_c):
            chunk = Chunk.from_region(region, *c)
        else:
            print(f"Failed: {c}, skipping without saving")
            continue
        
        for coords in product(range(16), range(256), range(16)): # Steps through induvidual blocks
            x, y, z = coords
            block = chunk.get_block(*coords)
            layers[y][block.id] += 1

        latest_c = c
        end = timer()

        with open(cache_file, 'w') as o:
            json.dump({'latest': {'region': latest_r, 'chunk': latest_c},
                        'layers': layers}, o, indent=2)

        print(f'Scraped: {c} in {end - start:.3f}s, saved cache @ {cache_file}')

    if linearPath:
        latest_r = (a, b + 1)
        latest_c = (0, 0)
    else:
        latest_r = spiral_iter(latest_r)
        latest_c = (0, 0)
    print(f'Moving to region: {latest_r}')
