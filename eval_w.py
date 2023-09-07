
class WEval:
    def __init__(self, full_signal, parent_coord, real_coord, predicted_coord, predicted_v, v_weight):
        self.signal_covered = self._get_signal_covered1(full_signal, parent_coord, real_coord, predicted_coord)

        self.v_range, self.u_range =self.get_v_u_ranges1(full_signal, parent_coord, real_coord, predicted_coord, predicted_v)

        self.u_err = abs(real_coord - predicted_coord)
        self.v_err = abs(full_signal[real_coord] - predicted_v)

        self.v_weight = v_weight
        self.u_weight = 1 - v_weight


    def get_v_u_ranges(self, full_signal, parent_coord, real_coord, predicted_coord, predicted_v):
        v_range = max(self.signal_covered) - min(self.signal_covered)
        u_range = len(self.signal_covered)
        return v_range, u_range

    def get_v_u_ranges1(self, full_signal, parent_coord, real_coord, predicted_coord, predicted_v):
        parent_val = full_signal[parent_coord]
        v_range = abs(parent_val - predicted_v)
        u_range = abs(parent_coord - predicted_coord)
        return v_range, u_range

    def _get_signal_covered1(self, full_signal, parent_coord, real_coord, predicted_coord):
        dist_to_real = abs(parent_coord - real_coord)
        dist_to_predicted = abs(parent_coord - predicted_coord)
        if dist_to_predicted > dist_to_real:
            signal_covered = full_signal[min(parent_coord, predicted_coord): max(parent_coord, predicted_coord)]
        else:
            signal_covered = full_signal[min(parent_coord, real_coord): max(parent_coord, real_coord)]
        return signal_covered

    def _get_signal_covered2(self, full_signal, parent_coord, real_coord, predicted_coord):
        return full_signal



    def get_W(self):
        w_u = self.get_w_u()
        w_v = self.get_w_v()
        return w_v + w_u

    def get_w_u(self):
        if self.u_err == 0:
            return 1*self.u_weight
        w_u = 1 - (self.u_err/ (self.u_err + self.u_range))
        return w_u*self.u_weight

    def get_w_v(self):
        if self.v_err == 0:
            return 1 * self.v_weight
        w_v = 1 - (self.v_err / (self.v_err + self.v_range))
        return w_v*self.v_weight



class WEvalFirstPoint:
    def __init__(self, full_signal, real_coord, predicted_v):
        self.real_v = full_signal[real_coord]
        self.v_err = abs(self.real_v - predicted_v)

    def get_w_v(self):
        w_v = 1 - (self.v_err / (self.v_err + abs(self.real_v)))
        return w_v

    def get_w_u(self):
        return None

    def get_W(self):
        return self.get_w_v()


class WEvalNoParent:
    def __init__(self, full_signal,  real_coord, predicted_coord, predicted_v):
        left = min(real_coord, predicted_coord)
        right = max(real_coord, predicted_coord)
        self.signal_covered = full_signal[left:right]

        self.v_range = max(self.signal_covered) - min(self.signal_covered)
        self.u_range = len(self.signal_covered)

        self.u_err = abs(real_coord - predicted_coord)
        self.v_err = abs(full_signal[real_coord] - predicted_v)

    def get_W(self):
        w_u = self.get_w_u()
        w_v = self.get_w_v()
        return w_v + w_u

    def get_w_u(self):
        w_u = 1 - (self.u_err/ (self.u_err + self.u_range))
        return w_u

    def get_w_v(self):
        w_v = 1 - (self.v_err / (self.v_err + self.v_range))
        return w_v