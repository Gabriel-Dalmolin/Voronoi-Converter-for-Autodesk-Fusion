import adsk.core
import adsk.fusion 


def intersect_bodies(root: adsk.fusion.Component, target: adsk.fusion.BRepBody, tool: adsk.fusion.BRepBody, keepTools = False):
    combines = root.features.combineFeatures

    intersectionCollection = adsk.core.ObjectCollection.create()
    intersectionCollection.add(tool)
    intersectionInput = combines.createInput(target, intersectionCollection)
    intersectionInput.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation # type: ignore
    intersectionInput.isKeepToolBodies = keepTools
    combines.add(intersectionInput)
