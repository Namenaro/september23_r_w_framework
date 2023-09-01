from eval_w import WEval
from utils import HtmlLogger, StartSituationsGen, StartSituation, draw_ECG, draw_vertical_line, PointsCloud
from scene import Scene

import matplotlib.pyplot as plt
from random import randrange

def get_data():
    start_situation = StartSituationsGen().__next__()
    return start_situation.signal, start_situation.start_point



def make_exp_for_prediction(u_predicted, log):
    signal, start_point = get_data()
    # идеальное предсказание первого шага


    v_predicted = signal[u_predicted]
    print("v_pred = " + str(v_predicted))

    # перебираем все экстремумы сигнала на сцене, и для каждого меряем u_w, v_w, w
    scene = Scene(signal)

    candidates = scene.get_all_extemums_of_signal()
    uws = []
    vws = []
    names = []
    for i in range(len(candidates)):
        coord_candidate = candidates[i]
        name = i
        names.append(name)
        weval = WEval(full_signal=signal, parent_coord=start_point,
                      real_coord=coord_candidate, predicted_coord=u_predicted,
                      predicted_v=v_predicted, v_weight=0.5)
        uw = weval.get_w_u()
        vw = weval.get_w_v()

        uws.append(uw)
        vws.append(vw)

    # отрисовываем кандидатов на плоскости u_w, v_w
    points_cloud = PointsCloud(xs=uws, ys=vws, names=names)
    fig, ax = plt.subplots()
    points_cloud.draw_on_01(ax)
    ax.set_title('Внутренная оценка кандидатов:')
    ax.set_xlabel('u_w')
    ax.set_ylabel('v_w')
    log.add_fig(fig)

    # отрисовываем w на самом сигнале ЭКГ (вместе с предсказанием), причем выоста вертикальной линии равна max_val*w
    fig, ax = plt.subplots()
    draw_ECG(ax, signal=signal)

    draw_vertical_line(ax, x=u_predicted, y=v_predicted, label="prediction", color="orange")

    max_v = max(signal)
    for i in range(len(candidates)):
        coord_candidate = candidates[i]
        name = names[i]
        w = uws[i] + vws[i]
        draw_vertical_line(ax, x=coord_candidate, y=max_v * w, color="green")
        ax.annotate(str(name), (coord_candidate - 0.5, randrange(0, 150)), fontsize=7)
    plt.legend()
    log.add_fig(fig)


if __name__ == '__main__':
    log = HtmlLogger("W_LOG_with_parent")
    make_exp_for_prediction(u_predicted=14, log=log)

    log.add_text("Среднее предсказание")
    make_exp_for_prediction(u_predicted=37, log=log)

    log.add_text("Плохое предсказание")
    make_exp_for_prediction(u_predicted=80, log=log)







