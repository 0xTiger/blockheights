import argparse
import json
import os
from collections import Counter
from itertools import product
from timeit import default_timer as timer

from anvil import Chunk, Region

parser = argparse.ArgumentParser()
parser.add_argument('--world', required=True, help='Name, (not path) of the minecraft world directory')
parser.add_argument('--out', default='out.json', help='Path to output data file')
parser.add_argument('--spiral', action='store_true', help='Set flag to scrape regions in a spiral order')
args = parser.parse_args()

ord = lambda x: x[0]*32 + x[1]

def spiral_step(t):
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


linearPath = not args.spiral # Determines which regions are chosen for scanning and in which order
world_folder = os.path.join(minecraft_path, '.minecraft/saves', args.world)

try:
    print("Loading cache")
    with open(args.out) as f:
        cache = json.load(f)
        layers = {int(k): Counter(v) for k, v in cache['layers'].items()}
        latest_c, start_region = cache['latest']['chunk'], cache['latest']['region']
except FileNotFoundError:
    print("FileNotFoundError: starting anew")
    layers = {y: Counter() for y in range(-64, 320)}
    latest_c, start_region = (0, 0), (0, 0)


def iter_regions(start_region=None, spiral_path=False):
    x, z = (0, 0) if start_region is None else start_region
    yield x, z
    while True:
        if spiral_path:
            x, z = spiral_step((x, z))
        else:
            z += 1
        yield x, z


print(f'Starting in r: {start_region}, c: {latest_c}')
for a, b in iter_regions(start_region=start_region): # Steps through regions
    print(f'In region: ({a}, {b})')
    region = Region.from_file(f'{world_folder}/region/r.{a}.{b}.mca')

    for c in product(range(32),range(32)): # Steps through chunks
        start = timer()
        if Region.chunk_location(region, *c)[0] != 0 and ord(c) > ord(latest_c):
            chunk = Chunk.from_region(region, *c)
        else:
            print(f"Failed: {c}, skipping without saving")
            continue
        
        for coords in product(range(16), range(-64, 320), range(16)): # Steps through induvidual blocks
            x, y, z = coords
            block = chunk.get_block(*coords)
            layers[y][block.id] += 1

        latest_c = c

        with open(args.out, 'w') as o:
            json.dump({'latest': {'region': start_region, 'chunk': latest_c},
                        'layers': layers}, o, indent=2)
        end = timer()
        print(f'Scraped: {c} in {end - start:.3f}s')
    latest_c = (0, 0)
