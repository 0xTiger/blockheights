import json
import anvil27
from itertools import product
from timeit import default_timer as timer

def dict_merge(dicts):
    neodict = {}
    for k, v in reduce(lambda x,y: x + y, [d.items() for d in dicts]):
        if k in neodict.keys():
            neodict[k] += v
        else:
            neodict[k] = v
    return neodict

ord = lambda x: x[0]*32 + x[1]

def spiral_iter(t):
    x, y = t
    #Starts (0,0) -> (1,0) and continues anti-clockwise
    if x > y > -1*x: y += 1 #Walk UP
    elif y >= x and y > -1*x: x -= 1 #Walk LEFT
    elif x < y <= -1*x: y -= 1 #Walk DOWN
    elif y <= x and y <= -1*x: x += 1 #Walk RIGHT
    return (x, y)

cache_file = 'assets\\mc\\blockheights.json'
world_folder = 'C:\\Users\\tigeer\\AppData\\Roaming\\.minecraft\\saves\\manual'
linearPath = True #Determines which regions are chosen for scanning and in which order

try:
    print("Loading cache")
    with open(cache_file) as f:
        cache = json.load(f)
        layers = {int(k):v for k,v in cache['layers'].items()}
        latest_c, latest_r = cache['latest']['chunk'], cache['latest']['region']
except:
    print("Loading cache failed, starting anew")
    layers = {y: {} for y in range(256)}
    latest_c, latest_r = (0, 0), (0, 0)


print("Starting in r: (%d, %d), c: (%d, %d)" % (latest_r[0], latest_r[1], latest_c[0], latest_c[1]))
while True: #Steps through regions
    a , b = latest_r
    region = anvil27.Region.from_file(world_folder + '\\region\\r.'+str(a)+'.'+str(b)+'.mca')

    for c in product(range(32),range(32)): #Steps through chunks
        start = timer()
        if anvil27.Region.chunk_location(region, *c)[0] != 0 and ord(c) > ord(latest_c):
            chunk = anvil27.Chunk.from_region(region, *c)
        else:
            print("Failed: (%d, %d), skipping without saving" % (c[0], c[1]))
            continue

        for coords in product(range(16), range(256), range(16)): #Steps through induvidual blocks
            x, y, z = coords
            block = chunk.get_block(*coords)
            if block.id in layers[y]:
                layers[y][block.id] += 1
            else:
                layers[y][block.id] = 1

        latest_c = c
        end = timer()

        with open(cache_file, 'w') as o:
            json.dump({'latest': {'region': latest_r, 'chunk': latest_c},
                        'layers': layers}, o, indent=2)

        print("Scraped: (%d, %d) in %.3fs, saved cache @ %s" % (c[0], c[1], end - start, cache_file))

    if linearPath:
        latest_r = (a, b + 1)
        latest_c = (0, 0)
    else:
        latest_r = spiral_iter(latest_r)
        latest_c = (0, 0)
    print("Moving to region: (%d, %d)" % latest_r)
