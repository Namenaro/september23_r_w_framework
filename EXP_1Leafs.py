from utils import HtmlLogger, StartSituationsGen, StartSituation, draw_ECG, draw_vertical_line, PointsCloud
from scene import Scene
from leafs_selector import EvaluatedLeafs, GeneratorEvaluatedLeafs

import matplotlib.pyplot as plt
from random import randrange


def make_exp(start_situation, log):
    signal = start_situation.signal
    parent_coord = start_situation.start_point
    prev_scene = Scene(signal)
    parent_name = prev_scene.add_point(parent_coord)
    predicted_v = -102.0
    predicted_coord_in_scene = 14

    allowed_area_left = 0
    allowed_area_right = len(signal)
    leafs_generator = GeneratorEvaluatedLeafs(prev_scene=prev_scene,
                                              allowed_area_left=allowed_area_left,
                                              allowed_area_right=allowed_area_right,
                                              predicted_v=predicted_v,
                                              predicted_coord_in_scene=predicted_coord_in_scene,
                                              name=2,
                                              parent_coord=parent_coord,
                                              parent_name=parent_name)

    evaluated_leafs = leafs_generator.generate()

    top_coords, top_ws, top_errs = evaluated_leafs.get_winners(num_winners=3, num_preselected_by_w=7)

    fig, ax = plt.subplots()
    draw_ECG(ax, signal)
    draw_vertical_line(ax, x=parent_coord, y=signal[parent_coord], color="red")
    max_v = max(signal)
    for i in range(len(top_coords)):
        coord_candidate = top_coords[i]
        w = top_ws[i]
        draw_vertical_line(ax, x=coord_candidate, y=max_v * w, color="green")
        ax.annotate(str(i), (coord_candidate - 0.5, randrange(0, 150)), fontsize=7)
    plt.legend()
    log.add_text("best w = " + str(top_ws[0]) + ", best err = " + str(top_errs[0]))
    log.add_fig(fig)

if __name__ == '__main__':
    log = HtmlLogger("Leafs_LOG")
    sit_gen = StartSituationsGen()
    # ОБУЧАЮЩАЯ СЦЕНА (для нее написано хардкодное предсказание)
    log.add_text("ETALON SITUATION:")
    start_situation = sit_gen.__next__()
    make_exp(start_situation, log)

    for situation in sit_gen:
        make_exp(situation, log)