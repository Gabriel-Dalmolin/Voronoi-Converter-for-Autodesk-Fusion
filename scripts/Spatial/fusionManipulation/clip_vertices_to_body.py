import adsk.core
import adsk.fusion

def clip_vertices_to_body(body: adsk.fusion.BRepBody, vertices):
    v = []
    measureMgr = adsk.core.Application.get().measureManager

    for vertex in vertices:
        p = adsk.core.Point3D.create(
            vertex[0],
            vertex[1],
            vertex[2]
        )

        containment = body.pointContainment(p)
        if containment == adsk.fusion.PointContainment.PointOutsidePointContainment:
            min_dist = measureMgr.measureMinimumDistance(body, p)
            v.append(min_dist.positionOne.asArray())
        else:
            v.append(p.asArray())

    return v