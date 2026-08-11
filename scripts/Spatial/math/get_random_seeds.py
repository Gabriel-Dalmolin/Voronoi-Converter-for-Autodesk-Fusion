import random
import traceback

from scipy.stats import qmc

import adsk.core
import adsk.fusion

def get_random_seeds(body: adsk.fusion.BRepBody, radius, lloyd):
    seeds = []

    bbox = body.boundingBox
    min_p = bbox.minPoint
    max_p = bbox.maxPoint

    dx = max_p.x - min_p.x
    dy = max_p.y - min_p.y
    dz = max_p.z - min_p.z

    opt = None
    if lloyd:
        opt = "lloyd"
    n_radius = radius/100
    poisson = qmc.PoissonDisk(
        d=3,
        radius=n_radius,
        optimization=opt)
    
    samples = poisson.fill_space()

    for s in samples:
        p = adsk.core.Point3D.create(
            min_p.x + (s[0] * dx),
            min_p.y + (s[1] * dy),
            min_p.z + (s[2] * dz)
        )
        if body.pointContainment(p) == adsk.fusion.PointContainment.PointInsidePointContainment:
            seeds.append(p.asArray())

    return seeds