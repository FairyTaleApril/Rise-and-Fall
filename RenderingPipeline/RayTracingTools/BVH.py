import numpy as np
from enum import Enum

from RenderingPipeline.RayTracingTools.Intersection import *


class SplitMethod(Enum):
    NAIVE = 1
    SAH = 2


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
        self.root = None
        self.leaf_nodes = None
        self.total_leaf_nodes = None
        self.total_primitives = None
        self.interior_nodes = None

    def detext_intersect(self, ray):
        inter = Intersection()

        if not self.root:
            return inter

        inter = self.recursive_detext_intersect(self.root, ray)
        return inter

    def recursive_detext_intersect(self, node: BVHNode, ray):
        inter = node.Bound.detect_intersect(ray)

        if not inter.happened:
            return inter

        if not node.left and not node.right:
            return inter

        hit_left = self.recursive_detext_intersect(node.left, ray)
        hit_right = self.recursive_detext_intersect(node.right, ray)

        return hit_left if abs(hit_left.t) < abs(hit_right.t) else hit_right
