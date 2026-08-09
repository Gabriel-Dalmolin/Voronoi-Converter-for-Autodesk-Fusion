import traceback

import adsk.core
import adsk.fusion

from .sweep_edge import sweep_edge
from .revolve_vertices import revolve_vertices

revolved_points = []

def sweep_voronoi_edges(root: adsk.fusion.Component, bodies, edges: list[list[adsk.core.Point3D]], radius):
    sketch = root.sketches.add(root.xYConstructionPlane)

    adsk.core.Application.get().log("Sweeping edges")
    for e in edges:
        p1 = e[0]
        p2 = e[1]

        curve = sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)

        if curve.length < 1e-4:
            adsk.core.Application.get().log(f"Skipping short edge: {curve.length}")
            continue

        sweep_edge(root, radius, curve, p1, bodies)

        if p1 not in revolved_points:
            revolved_points.append(p1)
        if p2 not in revolved_points:
            revolved_points.append(p2)

    adsk.core.Application.get().log("Sweeping vertices")
    revolve_vertices(root, radius, revolved_points, bodies)

    sketch.deleteMe()