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

    def recursive_build(self, objects):
        node = BVHNode()

        bounds = None
        for obj in objects:
            if bounds is None:
                bounds = obj.Bound
            else:
                bounds = Bound.union(bounds, obj.Bound)

        if len(objects) == 1:
            node.Bound = objects[0].Bound
            node.obj = objects[0]
            node.left = None
            node.right = None
            return node
        elif len(objects) == 2:
            node.left = self.recursive_build([objects[0]])
            node.right = self.recursive_build([objects[1]])

            node.Bound = Bound.union(node.left.Bound, node.right.Bound)
            return node
        else:
            centroid_bounds = None
            for obj in objects:
                if centroid_bounds is None:
                    centroid_bounds = obj.Bound.get_centroid()
                else:
                    centroid_bounds = Bound.union(centroid_bounds, obj.Bound.get_centroid())

            dim = centroid_bounds.max_extent()
            objects.sort(key=lambda f: f.Bound.get_centroid()[dim])

            beginning = objects[:len(objects)//2]
            middling = objects[len(objects)//2:]
            ending = objects

            left_shapes = beginning
            right_shapes = middling

            assert len(objects) == (len(left_shapes) + len(right_shapes))

            node.left = self.recursive_build(left_shapes)
            node.right = self.recursive_build(right_shapes)

            node.Bound = Bound.union(node.left.Bound, node.right.Bound)

        return node

    

    def BVH_detect_intersect(self, ray):
        inter = Intersection()

        if not self.root:
            return inter

        inter = self.recursive_detext_intersect(self.root, ray)
        return inter


    def recursive_detect_intersect(self, node: BVHNode, ray):
        inter = node.Bound.detect_intersect(ray)

        if not inter.happened:
            return inter

        if not node.left and not node.right:
            return inter

        hit_left = self.recursive_detext_intersect(node.left, ray)
        hit_right = self.recursive_detext_intersect(node.right, ray)

        return hit_left if abs(hit_left.t) < abs(hit_right.t) else hit_right
