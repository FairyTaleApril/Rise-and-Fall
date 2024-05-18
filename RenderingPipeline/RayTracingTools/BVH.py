from RenderingPipeline.RayTracingTools.Intersection import *
from RenderingPipeline.RayTracingTools.Bound import *


class BVHNode:
    def __init__(self):
        self.bound = None
        self.triangle_mesh = None
        self.left = None
        self.right = None


class BVH:
    def __init__(self, triangle_meshes):
        self.num_node = 0
        self.num_triangle_meshes = len(triangle_meshes)

        self.root = self.recursive_build(triangle_meshes)
        print('\rBuilding BVH: 100.0%')

    def recursive_build(self, triangle_meshes):
        node = BVHNode()

        if len(triangle_meshes) == 1:
            node.bound = triangle_meshes[0].bound
            node.triangle_mesh = triangle_meshes[0]

            self.num_node += 1
            print('\rBuilding BVH: {:.1f}%'.format(100 * self.num_node / self.num_triangle_meshes), end='')
        elif len(triangle_meshes) == 2:
            node.left = self.recursive_build([triangle_meshes[0]])
            node.right = self.recursive_build([triangle_meshes[1]])
            node.bound = union_bound(node.left.bound, node.right.bound)
        else:
            centroid_bounds = None
            for triangle_mesh in triangle_meshes:
                centroid_bounds = union_bound_point(centroid_bounds, triangle_mesh.bound.get_centroid())

            dim = centroid_bounds.max_extent()
            triangle_meshes.sort(key=lambda f: f.bound.get_centroid()[dim])

            node.left = self.recursive_build(triangle_meshes[:len(triangle_meshes) // 2])
            node.right = self.recursive_build(triangle_meshes[len(triangle_meshes) // 2:])

            node.bound = union_bound(node.left.bound, node.right.bound)
        return node

    def detect_intersect(self, ray) -> Intersection:
        inter = self.recursive_detect_intersect(self.root, ray)
        return inter

    def recursive_detect_intersect(self, node: BVHNode, ray) -> Intersection:
        inter = Intersection()

        if not node.bound.detect_intersect(ray):
            return inter

        if not node.left and not node.right:
            inter = node.triangle_mesh.detect_intersect(ray)
            return inter

        hit_left = self.recursive_detect_intersect(node.left, ray)
        hit_right = self.recursive_detect_intersect(node.right, ray)

        if not hit_left.happened and not hit_right.happened:
            return inter
        elif hit_left.happened and hit_right.happened:
            return hit_left if abs(hit_left.t) < abs(hit_right.t) else hit_right
        elif hit_left.happened:
            return hit_left
        else:
            return hit_right
