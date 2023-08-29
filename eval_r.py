from scene import Scene
from utils import Distr


# Есть некий сигнал. К нему даны n фиксированных точкек.
# Нужно составит ьраспределение интерполяционного качества для m точек, из которых
# n уже поставлены. Все m точек в интерполяторе по сигналу соединяются по приниципу ближайших соседей справа и слева.


# r ошибка интерполяции на данном сигнале при данных точках
# R вероятностная нетривиальность такой маленькой ошибки при такой вводной


class REval:
    def __init__(self, fixed_coords, filled_scene_to_eval):
        self.signal = filled_scene_to_eval.signal
        self.fixed_coords = fixed_coords
        self.num_coords_real = filled_scene_to_eval.num_points()
        self.real_r = filled_scene_to_eval.get_err_sum()

        self.r_distr = self._get_r_distr()


    def _get_r_distr(self):
        N=200
        rs_sample = []
        for _ in range(N):
            random_points =
            r = self._get_r(random_points)
            rs_sample.append((r))
        r_distr = Distr(rs_sample)
        return r_distr

    def get_R(self):
        R = self.r_distr.p_event_more_eq_than_val(self.real_r)
        return R

    def _get_r(self, points):
        # сортируем токчки, теперь у каждой (кроме конечных есть ближайший сосед слева и справа)
        scene = Scene()

