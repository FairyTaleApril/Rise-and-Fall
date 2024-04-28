import numpy as np

from RenderingPipeline.RayTracingTools.Intersection import *


class BVHNode:
    def __init__(self):
        self.split_axis = 0
        self.first_prim_offset = 0
        self.n_primitives = 0
        self.Bound = None
        self.left = None
        self.right = None
        self.obj = None


class BVH:
    def __init__(self):
        self.leaf_nodes = None
        self.total_leaf_nodes = None
        self.total_primitives = None
        self.interior_nodes = None

    def detext_intersect(self, ray):
        inter = Intersection()

        return inter


