from scene import Scene
from utils import Distr

import random

######## СУТЬ:
# R это безразмерная универсальная величина, опирающяяся только на вероятности и
# оценивающая ценность породженного описания (не с точки зрения агента а по факту -
# это обратная связь от реальности). Служит для обратного обучающего сигнала: если
# агент уверен, что порождает описание с хорошим стродством, а R оказывается низка,
# то функцию замера сродства стоит дообучить.

######## ТЕХНИЧЕСКИЕ ДЕТАЛИ:
# Есть некий сигнал. К нему даны n фиксированных точкек.
# Нужно составить распределение интерполяционного качества для m точек, из которых
# n уже поставлены. Все m точек в интерполяторе по сигналу соединяются по приниципу ближайших соседей справа и слева.


# r ошибка интерполяции на данном сигнале при данных точках
# R вероятностная нетривиальность такой маленькой ошибки при такой вводной


class REval:
    def __init__(self, fixed_coords, filled_scene_to_eval, allowed_left, allowed_right):
        self.signal = filled_scene_to_eval.signal
        self.fixed_coords = fixed_coords
        self.num_coords_real = filled_scene_to_eval.get_num_of_points() - len(fixed_coords)
        self.real_r = filled_scene_to_eval.get_err_sum()

        self.allowed_left = allowed_left
        self.allowed_right = allowed_right

        self.r_distr = self._get_r_distr()


    def _get_r_distr(self):
        N=200
        rs_sample = []
        for _ in range(N):
            random_points = random.sample(range(self.allowed_left, self.allowed_right), self.num_coords_real)
            r = self._get_r(random_points)
            rs_sample.append(r)
        r_distr = Distr(rs_sample)
        return r_distr

    def get_R(self):
        R = self.r_distr.get_p_of_event(self.real_r, self.r_distr.get_mean())
        return R

    def _get_r(self, points):
        scene = Scene(self.signal)
        scene.fill_from_array_by_nearest_principle(points + self.fixed_coords)
        r = scene.get_err_sum()
        return r


