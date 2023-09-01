from scene import Scene
from utils import IdGenedator

class Resctiction:
    def __init__(self,  left_name=None, right_name =None):
        self.left_name = left_name
        self.right_name = right_name


    def apply_to_scene(self, scene):
        if self.left_name is not None:
            left_coord = scene.get_index_by_name(self.left_name)
        else:
            left_coord = 0

        if self.right_name is not None:
            right_coord = scene.get_index_by_name(self.right_name)
        else:
            right_coord = scene.get_size()
        return left_coord, right_coord

class Program:
    def __init__(self):
        self.recogn_order = []

        self.name_to_parent_name = {}
        self.name_to_val = {}
        self.name_to_resctriction = {}
        self.name_to_u = {}

        self.idgen = IdGenedator()



    def add_first_node(self, v):
        name = self.idgen.get_id()
        self.name_to_parent_name[name] = None
        self.name_to_val[name] = v
        self.name_to_resctriction[name] = None
        self.name_to_u[name] = None

    def add_node(self, v, parent_name, u, restriction):
        name = self.idgen.get_id()
        self.name_to_parent_name[name] = parent_name
        self.name_to_val[name] = v
        self.name_to_resctriction[name] = restriction
        self.name_to_u[name] = u

    def __len__(self):
        return len(self.recogn_order)

    def get_prediction_for_name(self, scene, name):
        parent_name = self.name_to_parent_name[name]
        parent_coord_in_scene = scene.get_index_by_name(parent_name)
        left_coord, right_coord = self.name_to_resctriction[name].apply_to_scene(scene)
        v = self.name_to_val[name]
        u_from_parent = self.name_to_u[name]
        u_in_scene = parent_coord_in_scene + u_from_parent
        return left_coord, right_coord, v, u_in_scene, parent_coord_in_scene, parent_name
