


# Есть некий сигнал. К нему даны n фиксированных точкек.
# Нужно составит ьраспределение интерполяционного качества для m точек, из которых
# n уже поставлены. Все m точек в интерполяторе по сигналу соединяются по приниципу ближайших соседей справа и слева.

class REval:
    def __init__(self, signal, fixed_coords, coords_real):
        self.signal = signal
        self.fixed_coords = fixed_coords
        self.coords_real = coords_real

        self.r_distr = self._get_r_distr()

    def _get_r_distr(self):
        return r_distr

    def get_R(self):
        return R