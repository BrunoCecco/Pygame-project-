import math, heapq, time


# Still possible to optimise ordering of neighbours by minimal distance of next step
def neighbours(w, h, x, y, gX, gY):
    nbs = []

    if gX > x:
        if x < w-1:
            nbs.append([x+1,y])
        if x > 0:
            nbs.append([x-1,y])
    else:
        if x > 0:
            nbs.append([x-1,y])
        if x < w-1:
            nbs.append([x+1,y])
        
    if gY > y:
        if y < h-1:
            nbs.append([x,y+1])
        if y > 0:
            nbs.append([x,y-1])
    else:
        if y > 0:
            nbs.append([x,y-1])
        if y < h-1:
            nbs.append([x,y+1])
    return nbs


def store(path):
    global BESTLEN, BESTPATH
    
    if BESTLEN > len(path):
        BESTLEN = len(path)
        BESTPATH = path


def isadjacent(path, p1):
    for p2 in path[:-2]:
        if (p1[0] == p2[0] and abs(p1[1]-p2[1]) == 1) or \
                 (p1[1] == p2[1] and abs(p1[0]-p2[0]) == 1):
            return True
    return False


def worm(path, w, h, gX, gY, obstacles):
    global BESTLEN, NW
    
    if len(path) > BESTLEN:
        return

    NW += 1    
    # print("Worm %5d: %d - %s" % (NW, len(path), path))
    last = path[-1]
    nbs = neighbours(w, h, last[0], last[1], gX, gY)
    for p in nbs:
        if p[0] == gX and p[1] == gY:
            npath = path.copy()
            npath.append(p)
            store(npath)
            return
        elif (p in obstacles) or (p in path) or isadjacent(path, p):
            continue
        else:
            npath = path.copy()
            npath.append(p)
            worm(npath, w, h, gX, gY, obstacles)           


def bfp(w, h, sX, sY, gX, gY, obstacles):
    global NW, BESTPATH
    starttime = time.time()
    path = [[sX, sY]]
    worm(path, w, h, gX, gY, obstacles)
    endtime = time.time()
    print("Completed (%d,%d) grid in %.3f (%d worms) - Path = %d %s" % (w, h, endtime - starttime, NW, BESTLEN, BESTPATH))


for n in range(4, 11):
    global BESTLEN, NW
    BESTLEN = 999999
    NW = 0
    bfp(n, n, 0, 0, n-1, n-1, [])

