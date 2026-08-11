import traceback

import adsk.fusion
import adsk.core

def combine_bodies(root, bodies: adsk.core.ObjectCollection):
    combines = root.features.combineFeatures
    b1 = adsk.fusion.BRepBody.cast(bodies.item(0))
    bodies.removeByIndex(0)

    tempMgr = adsk.fusion.TemporaryBRepManager.get()

    i = 0
    ran_without_adding = 0
    while len(bodies) > 0:
        bbox = b1.boundingBox
        if i >= len(bodies):
            i = 0
            ran_without_adding += 1

        if ran_without_adding >= 3:
            break

        body = adsk.fusion.BRepBody.cast(bodies[i])

        bbox_2 = body.boundingBox
        if bbox.intersects(bbox_2):
            b1_copy = tempMgr.copy(b1)
            b2_copy = tempMgr.copy(body)
            try:
                success = tempMgr.booleanOperation(b1_copy,
                                            b2_copy,
                                            adsk.fusion.BooleanTypes.IntersectionBooleanType) #type: ignore

                if success and b1_copy.volume > 0:
                    objCollection = adsk.core.ObjectCollection.create()
                    objCollection.add(body)
                    bodies.removeByItem(body)

                    combineInput = combines.createInput(b1, objCollection) 
                    combineInput.isKeepToolBodies = False
                    combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation # type: ignore
                    combines.add(combineInput)

                    ran_without_adding = 0
            except Exception:
                bodies.removeByItem(body)
                body.deleteMe()
                pass

        i += 1

    return b1