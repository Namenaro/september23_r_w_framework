from leafs_selector import EvaluatedLeafs, GeneratorEvaluatedLeafs
from scene import Scene
from program import Program
from eval_r import REval

from copy import deepcopy

class Rostoc:
    def __init__(self, scene, w, program, r):
        self.w = w
        self.r = r
        self.scene = scene
        self.program = program


        self.leafs_coords = []
        self.leafs_ws = []
        self.parent_name = None

    def make_leafs(self, name, num_leafs):
        # делаем предсказание
        left_coord, right_coord, v, u_in_scene, parent_coord_in_scene, parent_name = self.program.get_prediction_for_name(
            self.scene, name)

        # по данному предсказанию находим num_leafs лучших листьев
        leafs_getter = GeneratorEvaluatedLeafs(self.scene, allowed_area_left=left_coord,
                                               allowed_area_right=right_coord, predicted_v=v,
                                               predicted_coord_in_scene=u_in_scene,
                                               name=name, parent_coord=parent_coord_in_scene, parent_name=parent_name)

        leafs_container = leafs_getter.generate()
        top_coords, top_ws, top_errs = leafs_container.get_winners_by_w(
            num_leafs)  # TODO есть 2 вариант этой функции (уже реализованых!)

        self.leafs_coords = top_coords
        self.leafs_ws = top_ws
        self.parent_name=parent_name

    def create_children_rostocs(self, name):
        children = []
        for i in range(len(self.leafs_ws)):
            leaf_w = self.leafs_ws[i]
            leaf_coord = self.leafs_coords[i]
            child_rostoc = self._create_child(leaf_w, leaf_coord, name)
            children.append(child_rostoc)
        return children


    def _create_child(self, leaf_w, leaf_coord, name):
        child_scene = deepcopy(self.scene)
        child_scene.add_point(leaf_coord, name)
        child_scene.add_parent(child_name=name, parent_name=self.parent_name)
        rostoc = Rostoc(scene=child_scene, w=self.w + leaf_w, program=self.program, r=0)
        return rostoc

    def get_w(self):
        return self.w

    def get_err(self):
        err = self.scene.get_err_sum()
        return err

    def get_lefs_coords(self):
        return self.leafs_coords

    def get_leafs_ws(self):
        return self.leafs_ws

    def get_R(self): # по всему сигналу, не учитывая условия перед добавлением каждой точки
        # считаем, что фиксированных нет, а интерполяция по всему сигналу
        eval = REval(fixed_coords=[], filled_scene_to_eval=self.scene, allowed_left=0, allowed_right=len(self.scene.signal)-1)
        R= eval.get_R()
        return R

    def get_r(self):
        return self.r
