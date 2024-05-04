import numpy as np
from Global import *
from RenderingPipeline.RayTracingTools.Intersection import *

import numpy as np
from math import fabs
import Object  # You need to create or import this module for loading OBJ files
import Material
from Bound import Bounds3  # You need to define this class for bounding box calculations
from BVH import BVHAccel  # You need to define this class for bounding volume hierarchy acceleration structure

def ray_triangle_intersect(v0, v1, v2, orig, dir, tnear, u, v):
    edge1 = v1 - v0
    edge2 = v2 - v0
    pvec = np.cross(dir, edge2)
    det = np.dot(edge1, pvec)
    if det == 0 or det < 0:
        return False

    tvec = orig - v0
    u = np.dot(tvec, pvec)
    if u < 0 or u > det:
        return False

    qvec = np.cross(tvec, edge1)
    v = np.dot(dir, qvec)
    if v < 0 or u + v > det:
        return False

    invDet = 1 / det

    tnear = np.dot(edge2, qvec) * invDet
    u *= invDet
    v *= invDet

    return True

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def point(self, t):
        return self.origin + t * self.direction


class Object:
    def intersect(self, ray):
        raise NotImplementedError()

    def intersect(self, ray, tnear, index):
        raise NotImplementedError()

    def get_intersection(self, ray):
        raise NotImplementedError()

    def get_surface_properties(self, P, I, index, uv, N, st):
        raise NotImplementedError()

    def eval_diffuse_color(self, st):
        raise NotImplementedError()

    def get_bounds(self):
        raise NotImplementedError()

class Intersection:
    def __init__(self):
        self.happened = False
        self.coords = None
        self.normal = None
        self.obj = None
        self.uv_coords = None

class TriangleMesh:
    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material
        self.e1 = v1 - v0
        self.e2 = v2 - v0
        self.N = normalize(np.cross(self.e1, self.e2))
        self.area = 0.5 * np.linalg.norm(np.cross(self.e1, self.e2))

    def detect_intersect(self, ray):
        inter = Intersection()

        ray_cross_e2 = np.cross(ray.direction, self.e2)
        det = np.dot(self.e1, ray_cross_e2)

        if abs(det) < epsilon:
            return inter

        inv_det = 1.0 / det
        s = ray.origin - self.v0
        u = inv_det * np.dot(s, ray_cross_e2)

        if u < 0 or u > 1:
            return inter

        s_cross_e1 = np.cross(s, self.e1)
        v = inv_det * np.dot(ray.direction, s_cross_e1)

        if v < 0 or u + v > 1:
            return inter

        t = inv_det * np.dot(self.e2, s_cross_e1)

        if t > epsilon:
            inter.happened = True
            inter.coords = ray.point(t)
            inter.normal = self.N
            inter.obj = self
            inter.uv_coords = [u, v]
        return inter

    def intersect(self, ray):
        return True

    def intersect(self, ray, tnear, index):
        return False

    def get_bounds(self):
        return Bounds3(self.v0, self.v1).union(self.v2)

    def eval_diffuse_color(self, st):
        return np.array([0.5, 0.5, 0.5])


class MeshTriangle(Object):
    def __init__(self, filename):
        # Load mesh from OBJ file
        loader = objloader.Loader()
        loader.load_file(filename)

        assert len(loader.loaded_meshes) == 1
        mesh = loader.loaded_meshes[0]

        min_vert = np.array([float('inf'), float('inf'), float('inf')])
        max_vert = np.array([-float('inf'), -float('inf'), -float('inf')])

        self.triangles = []
        for i in range(0, len(mesh.vertices), 3):
            face_vertices = []
            for j in range(3):
                vert = np.array([mesh.vertices[i + j].position.x,
                                 mesh.vertices[i + j].position.y,
                                 mesh.vertices[i + j].position.z]) * 60.0
                face_vertices.append(vert)

                min_vert = np.minimum(min_vert, vert)
                max_vert = np.maximum(max_vert, vert)

            # new_mat = Material(MaterialType.Diffuse, np.array([0.5, 0.5, 0.5]), np.array([0, 0, 0]))
            new_mat = Material.init()
            new_mat.Kd = 0.6
            new_mat.Ks = 0.0
            new_mat.specular_exponent = 0

            self.triangles.append(TriangleMesh(face_vertices[0], face_vertices[1], face_vertices[2], new_mat))

        self.bounding_box = Bounds3(min_vert, max_vert)

        ptrs = []
        for tri in self.triangles:
            ptrs.append(tri)

        self.bvh = BVHAccel(ptrs)

    def intersect(self, ray):
        return True


    def intersect(self, ray, tnear, index):
        intersect = False
        for k in range(len(self.triangles)):
            v0 = self.triangles[k].v0
            v1 = self.triangles[k].v1
            v2 = self.triangles[k].v2
            t, u, v = 0, 0, 0
            if ray_triangle_intersect(v0, v1, v2, ray.origin, ray.direction, t, u, v) and t < tnear:
                tnear = t
                index = k
                intersect |= True

        return intersect

    def get_bounds(self):
        return self.bounding_box

    def get_surface_properties(self, P, I, index, uv, N, st):
        v0 = self.triangles[index].v0
        v1 = self.triangles[index].v1
        v2 = self.triangles[index].v2
        e0 = np.normalize(v1 - v0)
        e1 = np.normalize(v2 - v1)
        N = np.normalize(np.cross(e0, e1))
        st0 = self.stCoordinates[self.vertexIndex[index * 3]]
        st1 = self.stCoordinates[self.vertexIndex[index * 3 + 1]]
        st2 = self.stCoordinates[self.vertexIndex[index * 3 + 2]]
        st = st0 * (1 - uv.x - uv.y) + st1 * uv.x + st2 * uv.y

    def eval_diffuse_color(self, st):
        scale = 5
        pattern = ((st.x * scale) % 1 > 0.5) ^ ((st.y * scale) % 1 > 0.5)
        return lerp(np.array([0.815, 0.235, 0.031]), np.array([0.937, 0.937, 0.231]), pattern)



