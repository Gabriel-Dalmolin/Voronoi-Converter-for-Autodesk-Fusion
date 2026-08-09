import adsk.core
import adsk.fusion

import math

def revolve_vertices(
        root: adsk.fusion.Component, 
        radius, 
        vertices: list[adsk.core.Point3D], 
        bodies: adsk.core.ObjectCollection):

    sketch = root.sketches.add(root.xYConstructionPlane)
    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs

    for vertex in vertices:
        x = vertex.x
        y = vertex.y
        z = vertex.z

        p1 = sketch.modelToSketchSpace(adsk.core.Point3D.create(x + radius,y,z))
        p2 = sketch.modelToSketchSpace(adsk.core.Point3D.create(x - radius,y,z)) 

        line = axis = lines.addByTwoPoints(p1, p2)
        arc = arcs.addByCenterStartEnd(sketch.modelToSketchSpace(vertex), p1, p2)

        profile = sketch.profiles.item(0)
        
        revolves = root.features.revolveFeatures
        revolveInput = revolves.createInput(
            profile,
            axis, 
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation #type: ignore
        )

        revolveAngle = adsk.core.ValueInput.createByReal(math.pi)
        revolveInput.setAngleExtent(True, revolveAngle)
        
        b = revolves.add(revolveInput).bodies
        for i in b:
            bodies.add(i)

        line.deleteMe()
        arc.deleteMe()