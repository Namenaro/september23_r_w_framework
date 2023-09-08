import random
from utils import Distr

class REvalNegFirst:
    def __init__(self, signal, real_err):
        err_sample = []
        for _ in range(100):
            v12 = random.sample(signal, 2)
            err = abs(v12[0] - v12[1])
            err_sample.append(err)

        err_distr = Distr(err_sample)

        mean = err_distr.get_mean()
        if real_err > mean:
            self.R_neg = - err_distr.get_p_of_event(real_err, mean)
        else:
            self.R_neg =  err_distr.get_p_of_event(real_err, mean)

    def get_R_neg(self):
        return self.R_neg


class REvalNeg:
    def __init__(self, scene_with_candidate, err_distr, alowed_area_left, alowed_area_right):
        self.scene_with_candidate = scene_with_candidate
        self.err_distr = err_distr
        self.alowed_area_left = alowed_area_left
        self.alowed_area_right = alowed_area_right

    def get_R_neg(self):

        real_errs = self.scene_with_candidate.get_error_pointwise()

        # для каждой ошибки считатем ее веоятность (с плюсом "настолько хорошую" и с минусом "настолько плохую") и суммируем это все
        rs = []
        expected_err = self.err_distr.get_mean()
        for coord in range(self.alowed_area_left, self.alowed_area_right):
            real_err = real_errs[coord]
            if real_err > expected_err:
                # плохо
                p_neg = - self.err_distr.get_p_of_event(real_err, expected_err)
            else:
                p_neg = self.err_distr.get_p_of_event(real_err, expected_err)
            rs.append(p_neg)

        R_neg = sum(rs)
        return R_neg