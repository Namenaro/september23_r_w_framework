from rostok import Rostoc
from inhibition_system import LateralInhibitionSystem
from utils import ExtremumFinder, HtmlLogger
from scene import Scene
from eval_w import WEvalFirstPoint
from eval_r import REval
from eval_r_neg import REvalNegFirst

import matplotlib.pyplot as plt


class Recogniser:
    def __init__(self, program, signal):
        self.program = program
        self.signal = signal

        self.NUM_CHILDREN_of_rostoc = 1
        self.NUM_ROSTOCS = 1
        self.NUM_INITIAL_ROSCTOCS = 1

        self.current_recog_step_num = 0

        self.ROSTOCS = []
        self._init_rostocs()


    def make_step(self): # после него полностью обновляется массив self.ROSTOCS
        SUCCESS = True
        self.current_recog_step_num += 1
        if self.check_stop_criteria():
            return not SUCCESS


        inhibition = LateralInhibitionSystem(self.ROSTOCS)
        name = self.program.get_ith_name(self.current_recog_step_num)

        # нинциализируем черновые листья
        for old_rostoc in self.ROSTOCS:
            old_rostoc.make_leafs(name, num_leafs=self.NUM_CHILDREN_of_rostoc)

        # производим торможение родительских ростков по похежести генерируемых ими листьев
        inhibition.run_inhibition(procent=0.8)


        #генерируем ростков-детей для выживших после торможения ростков-родителей
        all_cildren_rostocs = []
        for old_rostoc in self.ROSTOCS:
            childdren_of_rosctoc = old_rostoc.create_children_rostocs(name)
            all_cildren_rostocs = all_cildren_rostocs + childdren_of_rosctoc

        # отбираем топ лучших ростков-детей
        self.ROSTOCS = self._get_top_childen_rostocs(all_cildren_rostocs) # TODO сейчас соревнование  только по w, но можно по R или err
        return SUCCESS

    def check_stop_criteria(self):
        if self.current_recog_step_num == len(self.program):
            return True

        if len(self.ROSTOCS) == 0:
            return True

        return False

    def _init_rostocs(self):
        name = self.program.get_ith_name(self.current_recog_step_num)
        coords = ExtremumFinder(self.signal).get_top_N_maxes(
            self.NUM_INITIAL_ROSCTOCS)  # TODO не максимумы, а экстремумы (максимумы модуля сигнала)
        predicted_v = self.program.get_v(name)

        for coord in coords:
            w_evaluator = WEvalFirstPoint(self.signal, real_coord=coord, predicted_v=predicted_v)
            w = w_evaluator.get_W()

            scene = Scene(self.signal)
            scene.add_point(coord, name)

            R_evaluator = REval(fixed_coords=[], filled_scene_to_eval=scene, allowed_left=0, allowed_right=len(self.signal)-1)
            R = R_evaluator.get_R()

            R_neg_evaluator = REvalNegFirst(signal=self.signal, real_err=abs(predicted_v - self.signal[coord]))
            R_neg = R_neg_evaluator.get_R_neg()
            rostoc = Rostoc(scene, w, self.program, R, R_neg=R_neg)
            self.ROSTOCS.append(rostoc)

    def get_num_rostocs(self):
        return len(self.ROSTOCS)

    def _get_top_childen_rostocs(self, all_cildren_rostocs):
        ws = list([rost.get_w()] for rost in all_cildren_rostocs)


        if self.NUM_ROSTOCS < len(ws):
            best_w_indexes = sorted(range(len(ws)), key=lambda i: ws[i], reverse=True)[
                                 :self.NUM_ROSTOCS]  # от больших к меньшим

        else:
            best_w_indexes = sorted(range(len(ws)), key=lambda i: ws[i], reverse=True)

        children_winners = list([ all_cildren_rostocs[i] for i in best_w_indexes])
        return children_winners

    def draw_rostocs(self, log):
        for rostoc in self.ROSTOCS:
            fig, ax = plt.subplots()
            rostoc.scene.draw(ax)
            log.add_text("w = " + str(rostoc.get_w()) + " , R_neg = " + str(rostoc.get_Rneg()) + " , R_ad = " + str(rostoc.get_Ra()) + " , R_naive = " + str(rostoc.get_naive_R()))
            log.add_fig(fig)



