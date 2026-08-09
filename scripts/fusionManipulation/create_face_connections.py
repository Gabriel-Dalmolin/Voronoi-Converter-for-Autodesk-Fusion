import math

import adsk.core
import adsk.fusion

from .sweep_edge import sweep_edge
import random

CONNECTION_CHANCE = 0.1

def create_face_connections(
        root: adsk.fusion.Component, 
        bodies, 
        interceptions: list[tuple[adsk.fusion.BRepFace, list[adsk.core.Point3D]]], 
        radius, 
        random_edge = True):
    for i in interceptions:
        face = i[0]
        points = i[1]

        sketch = root.sketches.add(root.xYConstructionPlane)
        lines = sketch.sketchCurves.sketchLines

        for p1 in points:
            edges = face.edges
            edge = edges.item(0)

            if random_edge:
                n_edges = len(edges)
                edge = edges.item(random.randint(0, n_edges-1))    
            else:
                distance = math.inf
                for e in edges:
                    a = p1.distanceTo(e.startVertex.geometry)
                    b = p1.distanceTo(e.endVertex.geometry)

                    if a < distance or b < distance:
                        if a < b:
                            distance = a
                        else:
                            distance = b
                        edge = e
                if (random.uniform(0, 1) < CONNECTION_CHANCE):
                    rp = points[random.randint(0, len(points) - 1)]
                    if rp != p1:
                        l = lines.addByTwoPoints(rp, p1)
                        sweep_edge(root, radius, l, rp, bodies)


            success, start, end = edge.evaluator.getParameterExtents()
            success_, p2 = edge.evaluator.getPointAtParameter(random.uniform(start, end))

            line = lines.addByTwoPoints(p1, p2)

            sweep_edge(root, radius, line, p1, bodies)

        sketch.deleteMe()
