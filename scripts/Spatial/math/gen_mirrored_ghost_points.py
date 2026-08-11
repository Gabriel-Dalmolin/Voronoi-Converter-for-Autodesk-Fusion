import adsk.core
import adsk.fusion

def gen_mirrored_ghost_points(
        seeds: list[list[int]],
        body: adsk.fusion.BRepBody
) -> list[list[int]]:  
    app = adsk.core.Application.get()
    measureMgr = app.measureManager

    bbox = body.boundingBox
    
    new_seeds = []

    for seed in seeds:
        for face in body.faces:
            point = adsk.core.Point3D.create( # P
                seed[0],
                seed[1],
                seed[2]
            )
            
            result = measureMgr.measureMinimumDistance(face, point)
            min_dist_point = result.positionTwo # Q

            v = [
                    2 * min_dist_point.x - point.x, # Since Q is a middle point of P and the mirrored version, 
                    2 * min_dist_point.y - point.y, # Q = (P + M)/2
                    2 * min_dist_point.z - point.z, # 2Q - P = M
                ]

            p = adsk.core.Point3D.create(
                v[0],
                v[1],
                v[2]
            )

            if bbox.contains(p):
                if body.pointContainment(p) == adsk.fusion.PointContainment.PointInsidePointContainment:
                    continue

            new_seeds.append(v)

    return new_seeds