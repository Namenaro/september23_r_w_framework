from eval_r import REval
from utils import HtmlLogger, StartSituationsGen, StartSituation, draw_ECG, draw_vertical_line
from scene import Scene

import matplotlib.pyplot as plt

def get_data():
    start_situation = StartSituationsGen().__next__()
    return start_situation.signal, start_situation.start_point


def make_exp_for_scene(fixed_points, filled_scene, log):
    fig, ax = plt.subplots()
    filled_scene.draw(ax)
    log.add_fig(fig)

    r_eval = REval(fixed_coords=fixed_points, filled_scene_to_eval=filled_scene, allowed_left=0, allowed_right=filled_scene.get_size())
    R = r_eval.get_R()
    log.add_text("R = " + str(R))
    print ("R= " + str(R))



if __name__ == '__main__':
    signal, start_point = get_data()

    log = HtmlLogger("R_LOG")
    fixed_points = [start_point]

    best_real_points = [14, 5, 37, 39]
    best_scene = Scene(signal)
    best_scene.fill_from_array_by_nearest_principle(fixed_points+best_real_points)
    make_exp_for_scene(fixed_points, best_scene, log)

    bad_real_points = [60, 70, 80, 90]
    bad_scene = Scene(signal)
    bad_scene.fill_from_array_by_nearest_principle(fixed_points + bad_real_points)
    make_exp_for_scene(fixed_points, bad_scene, log)

