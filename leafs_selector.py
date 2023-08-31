from eval_w import WEval
from eval_r import REval
from utils import HtmlLogger, StartSituationsGen, StartSituation, draw_ECG, draw_vertical_line, PointsCloud
from scene import Scene

import matplotlib.pyplot as plt
from random import randrange
from copy import deepcopy

def get_data():
    start_situation = StartSituationsGen().__next__()
    return start_situation.signal, start_situation.start_point


class EvaluatedLeafs:
    def __init__(self, coords, errs, ws, Rs=None):
        self.coords = coords
        self.errs = errs
        self.ws = ws
        self.Rs = Rs

    def _get_top_by_w(self, m):
        if m <= len(self.ws):
            best_w_indexes = sorted(range(len(self.ws)), key=lambda i: self.ws[i], reverse=True)[:m] # от больших к меньшим
            return best_w_indexes
        return sorted(range(len(self.ws)), key=lambda i: self.ws[i], reverse=True)



    def get_winners(self,num_winners, num_preselected_by_w):
        best_w_indexes = self._get_top_by_w(num_preselected_by_w)
        new_errs, new_ws, new_coords = self._subselect_by_index_list(best_w_indexes)
        best_by_err_indexes = sorted(range(len(new_errs)), key=lambda i: new_errs[i])[:num_winners]   # от меньших к большим, т.к. ошибку хотим маленькую

        top_coords = list([new_coords[i] for i in best_by_err_indexes])
        top_ws = list([new_ws[i] for i in best_by_err_indexes])
        top_errs = list([new_errs[i] for i in best_by_err_indexes])
        return top_coords, top_ws, top_errs


    def _subselect_by_index_list(self, indexes_list):
        new_errs = list([self.errs[i] for i in indexes_list])
        new_ws = list([self.ws[i] for i in indexes_list])
        new_coords = list([self.coords[i] for i in indexes_list])
        return new_errs, new_ws, new_coords


class GeneratorEvaluatedLeafs:
    def __init__(self, prev_scene, allowed_area_left, allowed_area_right,  predicted_v, predicted_coord_in_scene, name, parent_coord, parent_name):
        self.prev_scene = prev_scene  # там поставлены все узлы, распознаванныке к данному шагу. Эту сцену нельзя менять

        self.alowed_area_left = allowed_area_left
        self.alowed_area_right = allowed_area_right

        self.predicted_v = predicted_v
        self.predicted_coord_in_scene = predicted_coord_in_scene
        self.name = name

        self.parent_coord = parent_coord
        self.parent_name = parent_name

    def _get_extrs_allowed(self):
        extrs = self.prev_scene.get_extrms_in_interval(self.alowed_area_left, self.alowed_area_right)
        return extrs

    def _eval_Rs(self, candidates):
        Rs =[]

        fixed_points = self.prev_scene.get_points_coords()
        for coord_candidate in candidates:
            scene_with_candidate = deepcopy(self.prev_scene)
            scene_with_candidate. add_point(coord=coord_candidate, name=self.name)
            scene_with_candidate.add_parent(self.name, self.parent_name)
            r_eval = REval(fixed_coords=fixed_points, filled_scene_to_eval=scene_with_candidate,
                           allowed_left=self.alowed_area_left, allowed_right=self.alowed_area_right)
            R = r_eval.get_R()
            Rs.append(R)
        return Rs

    def _eval_rs(self, candidates):
        errs =[]
        for coord_candidate in candidates:
            scene_with_candidate = deepcopy(self.prev_scene)
            scene_with_candidate. add_point(coord=coord_candidate, name=self.name)
            scene_with_candidate.add_parent(self.name, self.parent_name)
            err = scene_with_candidate.get_err_sum()
            errs.append(err)
        return errs

    def _eval_ws(self, candidates):
        ws = []
        for coord_candidate in candidates:
            weval = WEval(full_signal=self.prev_scene.signal, parent_coord=self.parent_coord,
                          real_coord=coord_candidate, predicted_coord=self.predicted_coord_in_scene,
                          predicted_v=self.predicted_v, v_weight=0.5)
            w = weval.get_W()
            ws.append(w)
        return ws

    def generate(self):
        extrs_coords = self._get_extrs_allowed()
        errs = self._eval_rs(extrs_coords)
        ws = self._eval_ws(extrs_coords)
        evaluated_leafs = EvaluatedLeafs(coords=extrs_coords, errs=errs, ws=ws)
        return evaluated_leafs


if __name__ == '__main__':
    log = HtmlLogger("Leafs_LOG")


