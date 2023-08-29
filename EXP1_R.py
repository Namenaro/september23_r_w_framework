from eval_r import REval
from utils import HtmlLogger, StartSituationsGen, StartSituation, draw_ECG, draw_vertical_line

import matplotlib.pyplot as plt

def get_data():
    start_situation = StartSituationsGen().__next__()
    return start_situation.signal, start_situation.start_point


def make_exp_for_points(fixed_points, real_points_list, signal, log):
    fig, ax = plt.subplots()
    draw_ECG(ax, signal)
    draw_vertical_line(ax, x=start_point, y=max(signal), label="start_point")
    log.add_fig(fig)

    r_eval = REval(signal, fixed_coords=fixed_points, coords_real=real_points_list)
    R = r_eval.get_R()
    log.add_text("R = " + R)
    print ("R= " + R)


if __name__ == '__main__':
    signal, start_point = get_data()

    log = HtmlLogger("R_LOG")

    fixed_coords = [start_point]
    best_real_points = [15, 5, 37, 39]
    make_exp_for_points(fixed_coords, real_points_list=best_real_points, signal=signal, log=log)

    bad_real_points = [60, 70, 80, 90]
    make_exp_for_points(fixed_coords, real_points_list=bad_real_points, signal=signal, log=log)
