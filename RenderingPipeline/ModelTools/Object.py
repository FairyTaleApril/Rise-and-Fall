import trimesh


class Object:
    def __init__(self):
        self.obj = None
        self.faces = None
        self.vertices = None

        self.bound = None

    def read_obj(self, filepath):
        self.obj = trimesh.load(filepath)

    def set_obj(self, obj):
        self.obj = obj
