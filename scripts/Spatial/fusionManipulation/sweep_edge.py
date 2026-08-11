import adsk.fusion
import adsk.core

def sweep_edge(
        root: adsk.fusion.Component, 
        radius, 
        edge: adsk.fusion.BRepEdge | adsk.fusion.SketchCurve, 
        vertex: adsk.core.Point3D,
        bodies: adsk.core.ObjectCollection):
    
    planes = root.constructionPlanes

    planeInput = planes.createInput()
    distance = adsk.core.ValueInput.createByReal(0)
    planeInput.setByDistanceOnPath(edge, distance)
    plane = planes.add(planeInput)

    sketch = root.sketches.add(plane)
    circles = sketch.sketchCurves.sketchCircles

    sketchPoint = sketch.modelToSketchSpace(vertex)
    circle = circles.addByCenterRadius(sketchPoint, radius)

    path = root.features.createPath(edge)

    profile = sketch.profiles.item(0)
    sweeps = root.features.sweepFeatures
    sweepInput = sweeps.createInput(profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) #type: ignore
    
    b = sweeps.add(sweepInput).bodies
    for i in b:
        bodies.add(i)
    
    sketch.deleteMe()
    plane.deleteMe()