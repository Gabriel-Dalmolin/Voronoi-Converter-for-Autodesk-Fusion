import scipy
import scipy.spatial

import adsk.core
import adsk.fusion

from .get_body_interception import get_body_interception
from ..fusionManipulation.clip_vertices_to_body import clip_vertices_to_body

edges = []
lines = []

def create_edges(d, k, vertices):
    for i in range(len(d[k])): 
        j = i+1
        if j >= len(d[k]):
            j = 0

        v1 = vertices[d[k][i]]
        v2 = vertices[d[k][j]]


        if -1 in v1 or -1 in v2:
            continue

        p1 = adsk.core.Point3D.create(
            v1[0],
            v1[1],
            v1[2]
        )

        p2 = adsk.core.Point3D.create(
            v2[0],
            v2[1],
            v2[2]
        )


        line = adsk.core.Line3D.create(p1, p2)
        lines.append(line)

        edges.append([p1,p2])


def get_voronoi_edges(body, voronoi: scipy.spatial.Voronoi, ghost_index) -> tuple[list, list[list[adsk.core.Point3D]]]:
    vertices = voronoi.vertices
    vertices = clip_vertices_to_body(body, vertices)

    d = voronoi.ridge_dict

    for k in d:
        a = k[0]
        b = k[1]
        
        if a < ghost_index or b < ghost_index:
            create_edges(d, k, vertices)

    interceptions = get_body_interception(body, lines)

    return interceptions, edges