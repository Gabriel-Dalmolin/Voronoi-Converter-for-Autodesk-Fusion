import math


import adsk.core
import adsk.fusion

import traceback

from .sweep_edge import sweep_edge
from .revolve_vertices import revolve_vertices

bodies = adsk.core.ObjectCollection.create()
seeds = []

def create_edges(root: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius):
    for edge in body.edges:
        sweep_edge(root, 2 * radius, edge, edge.startVertex.geometry, bodies)


def create_vertices(root: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius):
    vertices = []
    for vertex in body.vertices:
        seeds.append(vertex.geometry.asArray())
        vertices.append(vertex.geometry)
    revolve_vertices(root, 2 * radius, vertices, bodies)


def create_wireframe(root: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius: float):
    create_edges(root, body, radius)
    create_vertices(root, body, radius)        

    return bodies, seeds