import adsk.fusion 
import adsk.core

def get_body_interception(body: adsk.fusion.BRepBody, edges: list[adsk.core.Line3D]):
    app = adsk.core.Application.get()

    vertices = []

    for face in body.faces:
        ps = []
        for edge in edges:
            surface = face.geometry
            points = edge.intersectWithSurface(surface)
            for vertex in points:
                point = adsk.core.Point3D.cast(vertex)
                if face.isPointOnFace(point):
                    ps.append(point)
        if len(ps) > 0:
            vertices.append([face, ps])
    return vertices