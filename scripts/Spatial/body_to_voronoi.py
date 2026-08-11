import traceback

import scipy
import scipy.spatial

import adsk.core
import adsk.fusion

from .math.gen_mirrored_ghost_points import gen_mirrored_ghost_points
from .math.get_random_seeds import get_random_seeds
from .math.gen_ghost_points import gen_ghost_points
from .math.get_voronoi_edges import get_voronoi_edges
from .fusionManipulation.combine_bodies import combine_bodies
from .fusionManipulation.intersect_bodies import intersect_bodies
from .fusionManipulation.create_wireframe import create_wireframe
from .fusionManipulation.sweep_voronoi_edges import sweep_voronoi_edges
from .fusionManipulation.create_face_connections import create_face_connections

def body_to_voronoi(root: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius, size, lloyd):
    try: 
        app = adsk.core.Application.get()

        bodies = adsk.core.ObjectCollection.create()
        seeds = []

        wireframe_bodies, vertices = create_wireframe(root, body, radius)
        for b in wireframe_bodies:
            bodies.add(b)

        seeds += get_random_seeds(body, size, lloyd)

        ghost_index = len(seeds)

        seeds += gen_mirrored_ghost_points(seeds, body)

        voronoi = scipy.spatial.Voronoi(seeds)

        app.log("Getting voronoi edges")
        interceptions, edges = get_voronoi_edges(body, voronoi, ghost_index)
        
        app.log("Sweeping edges")
        sweep_voronoi_edges(root, bodies, edges, radius)

        obj_collection = adsk.core.ObjectCollection.create()
        for b in bodies:
            obj_collection.add(b)

        target = adsk.fusion.BRepBody.cast(obj_collection.item(0))

        app.log("Combining bodies")
        combine_bodies(root, obj_collection)

        app.log("Intersecting bodies")
        intersect_bodies(root, target, body)

    except:
        adsk.core.Application.get().log(traceback.format_exc())