import math
import random

import adsk.core
import adsk.fusion

MARGIN_MULTIPLIER = 0.5
MAX_DISTANCE = 2 # Max distance between regular ghost points in centimeters 

seeds = []

def gen_regular_points(min_p, max_p, dx, mx, nx, dy, my, ny, dz, mz, nz):
    for i in range(ny):  # p and n to create the positive and negative version of the ghost points
        for j in range(nz):
            p = [max_p.x + mx, min_p.y + (i+1)*dy/(ny+1), min_p.z + (j+1)*dz/(nz+1)]
            n = [min_p.x - mx, min_p.y + (i+1)*dy/(ny+1), min_p.z + (j+1)*dz/(nz+1)]
            seeds.append(p) # i and j gets added 1 so that we dont multiply by 0 and 
            seeds.append(n) # one of the points gets on top of the wireframe

    for i in range(nx):  
        for j in range(nz):
            p = [min_p.x + (i+1)*dx/(nx+1), max_p.y + my, min_p.z + (j+1)*dz/(nz+1)]
            n = [min_p. x + (i+1)*dx/(nx+1), min_p.y - my, min_p.z + (j+1)*dz/(nz+1)]
            seeds.append(p) # n gets added one because if not, it would be split into without counting the edges, so,
            seeds.append(n) # we need n+1 regions to n regions, and we want n points splitting those regions create n division points
    
    for i in range(nx):  
        for j in range(ny):
            p = [min_p.x + (i+1)*dx/(nx+1), min_p.y + (j+1)*dy/(ny+1), max_p.z + mz]
            n = [min_p.x + (i+1)*dx/(nx+1), min_p.y + (j+1)*dy/(ny+1), min_p.z - mz]
            seeds.append(p)  
            seeds.append(n)

    return 

def gen_random_points(body: adsk.fusion.BRepBody, min_p: adsk.core.Point3D, max_p: adsk.core.Point3D, mx, my, mz, n_seeds):
    c = 0 
    while c < n_seeds:
        p = adsk.core.Point3D.create(
            random.uniform(min_p.x - mx, max_p.x + mx),
            random.uniform(min_p.y - my, max_p.y + my),
            random.uniform(min_p.z - mz, max_p.z + mz)
        )

        if body.pointContainment(p) == adsk.fusion.PointContainment.PointOutsidePointContainment:
            seeds.append(p.asArray())
            c += 1

def gen_ghost_points(body: adsk.fusion.BRepBody):
    bbox = body.boundingBox
    min_p = bbox.minPoint
    max_p = bbox.maxPoint

    dx = (max_p.x - min_p.x)
    dy = (max_p.y - min_p.y)
    dz = (max_p.z - min_p.z)

    mx = dx*MARGIN_MULTIPLIER
    my = dy*MARGIN_MULTIPLIER
    mz = dz*MARGIN_MULTIPLIER
    
    nx = math.ceil(dx / MAX_DISTANCE) # Number of regular ghost points in each direction 
    ny = math.ceil(dy / MAX_DISTANCE)
    nz = math.ceil(dz / MAX_DISTANCE)


    gen_regular_points(min_p, max_p, dx, mx, nx, dy, my, ny, dz, mz, nz)
    gen_random_points(body, min_p, max_p, mx, my, mz, 2 * (nx + ny + nz))

    return seeds


    

    


