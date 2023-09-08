from utils import IdGenedator, get_mini_ECG, draw_ECG, InterpolationSegment, ExtremumFinder

import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import  statistics

class Point:
    def __init__(self, coord):
        self.parents_names = []
        self.coord = coord

    def add_parent(self, parent_name):
        self.parents_names.append(parent_name)

    def get_coord(self):
        return self.coord



class Scene:
    def __init__(self, signal):
        self.signal = signal
        self.mean = statistics.mean(signal)
        self.names_to_points = {}
        self.indexes_to_names = {}

        self.idgen = IdGenedator()

        self.coords_to_predictions = {}  # над любой точкой сцены самое новое предсказание (хронологичски добавленное)
        for coord in range(len(self.signal)):
            self.coords_to_predictions[coord] = 0 #self.mean

        self.coords_of_extrms = self.get_all_extemums_of_signal()

    def get_index_by_name(self, name):
        return self.names_to_points[name].get_coord()

    def get_name_by_index(self, index):
        return self.indexes_to_names.get(index, None)

    def get_points_coords(self):
        points_coords = list([val.coord for val in self.names_to_points.values()])
        return points_coords

    def add_point(self, coord, name=None):
        if name is None:
            name = self.idgen.get_id()
        self.names_to_points[name] = Point(coord)
        self.indexes_to_names[coord]=name
        self.coords_to_predictions[coord] = self.signal[coord]
        return name

    def get_size(self):
        return len(self.signal)

    def get_or_create_point(self, index):
        name_in_index = self.get_name_by_index(index)
        if name_in_index is not None:
            return name_in_index

        new_point_name = self.add_point(index)
        return new_point_name

    def add_parent(self, child_name, parent_name):
        self.names_to_points[child_name].add_parent(parent_name)

        index1 = self.get_index_by_name(child_name)
        index2 = self.get_index_by_name(parent_name)
        self._register_new_segment(index1, index2)

    def _register_new_segment(self, index1, index2):
        seg = InterpolationSegment(index1, self.signal[index1], index2, self.signal[index2])
        vals = seg.get_vals_from_left()
        indexes = seg.get_indexes_from_left()

        for i in range(len(vals)):
            coord = indexes[i]
            val = vals[i]

            self.coords_to_predictions[coord] = val

        #self._recalc_prediction_btw_segments() # TODO без этого на ненакрытых интерполяцией будет ноль

    def _recalc_prediction_btw_segments(self): # TODO это можно сделать разными способами. Можно написать тут pass
        # перебираем точки начиная с самой левой
        # для текущей точки берем ближайшую справа
        # проверяем состоит ли эта пара в отношениях родитель ребенок
        # если нет, то на сегменте между ними считаем среднее и перезаписываем предсказание всем точкам на сегменте

        points_coords = self.get_points_coords()
        soted_coords_from_left = sorted(points_coords) #по возрастанию
        for i in range(len(soted_coords_from_left)-1):
            left_point = soted_coords_from_left[i]
            right_point = soted_coords_from_left[i+1]
            poin_name1 = self.get_name_by_index(left_point)
            point_name2 = self.get_name_by_index(right_point)
            if self._are_point_linked_into_segment(point_name2, poin_name1):
                continue
            if right_point - left_point == 1:
                continue
            mean = self.get_mean_in_area_include_borders(point_left=left_point+1, point_right=right_point-1)
            for coord in range(left_point+1, right_point):
                self.coords_to_predictions[coord] = mean

        # тдельно обрабатываем сегмент левее самой левой и правее самой правой
        if soted_coords_from_left[0]>1:
            mean = self.get_mean_in_area_include_borders(point_left=0, point_right=soted_coords_from_left[0]-1)
            for coord in range(0, soted_coords_from_left[0]):
                self.coords_to_predictions[coord] = mean

        if soted_coords_from_left[-1]<len(self.signal)-1:
            mean = self.get_mean_in_area_include_borders(point_left=soted_coords_from_left[-1]+1, point_right=len(self.signal)-1)
            for coord in range(soted_coords_from_left[-1]+1, len(self.signal)):
                self.coords_to_predictions[coord] = mean

    def get_mean_in_area_include_borders(self, point_left, point_right):
        sum = 0
        for coord in range(point_left, point_right+1):
            sum += self.signal[coord]
        n = point_right - point_left + 1
        mean = sum/n
        return mean

    def _are_point_linked_into_segment(self, point_name1, point_name2):
        parents_of_1 = self.names_to_points[point_name1].parents_names
        if point_name2 in parents_of_1:
            return True
        parents_of_2 = self.names_to_points[point_name2].parents_names
        if point_name1 in parents_of_2:
            return True
        return False


    def get_prediction(self):
        pointwise_prediction = []
        for coord in range(len(self.signal)):
            pointwise_prediction.append(self.coords_to_predictions[coord])

        return pointwise_prediction

    def get_error_pointwise(self):
        errs = []
        prediction = self.get_prediction()
        for i in range(len(prediction)):
            errs.append(abs(self.signal[i] - prediction[i]))
        return errs

    def get_err_max_index(self):
        errs = self.get_error_pointwise()
        whorst_index = errs.index(max(errs))
        return whorst_index


    def get_err_sum(self):
        return sum(self.get_error_pointwise())

    def get_left_nearest_point(self, index):
        non_empty_indexes = self.indexes_to_names.keys()
        left_indexes = list([other_index for other_index in non_empty_indexes if other_index<index])
        if len(left_indexes) == 0:
            return None
        sorted_left_non_empy_indexes = sorted(left_indexes, reverse=True) #по убыванию
        nearest_index = sorted_left_non_empy_indexes[0]
        name_of_nearest = self.indexes_to_names[nearest_index]
        return self.names_to_points[name_of_nearest]

    def get_left_nearest_point_name(self, index):
        non_empty_indexes = self.indexes_to_names.keys()
        left_indexes = list([other_index for other_index in non_empty_indexes if other_index<index])
        if len(left_indexes) == 0:
            return None
        sorted_left_non_empy_indexes = sorted(left_indexes, reverse=True) #по убыванию
        nearest_index = sorted_left_non_empy_indexes[0]
        name_of_nearest = self.indexes_to_names[nearest_index]
        return name_of_nearest

    def get_right_nearest_point(self, index):
        non_empty_indexes = self.indexes_to_names.keys()
        right_indexes = list([other_index for other_index in non_empty_indexes if other_index > index])
        if len(right_indexes) == 0:
            return None
        sorted_right_non_empy_indexes = sorted(right_indexes)  # по возрастанию
        nearest_index = sorted_right_non_empy_indexes[0]
        name_of_nearest = self.indexes_to_names[nearest_index]
        return self.names_to_points[name_of_nearest]

    def get_right_nearest_point_name(self, index):
        non_empty_indexes = self.indexes_to_names.keys()
        right_indexes = list([other_index for other_index in non_empty_indexes if other_index > index])
        if len(right_indexes) == 0:
            return None
        sorted_right_non_empy_indexes = sorted(right_indexes)  # по возрастанию
        nearest_index = sorted_right_non_empy_indexes[0]
        name_of_nearest = self.indexes_to_names[nearest_index]
        return name_of_nearest

    def get_all_extemums_of_signal(self):
        finder = ExtremumFinder(self.signal)
        coords_of_extrms = finder.get_coords_extremums()
        return coords_of_extrms

    def get_vs_in_interval(self, left_coord, right_coord):
        return self.signal[left_coord: right_coord+1]

    def get_all_maxes_of_err(self):
        finder = ExtremumFinder(signal=self.get_error_pointwise())
        indexes = finder.get_coords_maxes()
        return indexes

    def get_extrms_in_interval(self, index1, index2):
        left = index1
        right = index2
        if index1>index2:
            left = index2
            right = index1
        coords_extrms = []
        for index in self.coords_of_extrms:
            if index>=left and index<=right:
                coords_extrms.append(index)
        return coords_extrms

    def get_start_id(self):
        return 0

    def get_num_of_points(self):
        return len(self.names_to_points)

    ########################################################################
    def draw(self, ax):
        draw_ECG(ax, self.signal)
        self.draw_points(ax)
        self.draw_preiction(ax)
        self.draw_err(ax)
        #self.draw_extremums()
        ax.legend(fancybox=True, framealpha=0.5)

    def draw_extremums(self):
        indexes = self.get_extrms_in_interval(0, len(self.signal)-1)
        vals = [self.signal[index] for index in indexes]
        plt.scatter(indexes, vals, label="кстремумы сигнала")

    def draw_points(self, ax):
        for name, point in self.names_to_points.items():
            ax.vlines(x=point.coord, ymin=0, ymax=max(self.signal), colors='orange', lw=1, alpha=0.5)
            text(point.coord, max(self.signal)/2, str(name), rotation=0, verticalalignment='center')

    def draw_preiction(self, ax):
        ax.plot(self.get_prediction(),  'green',ls="--", label='предсказание')

    def draw_err(self, ax):
        ax.plot(self.get_error_pointwise(), 'red', label='ошибка', alpha=0.2)
        #whorst_index = self.get_err_max_index()
        #ax.vlines(x=whorst_index, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)
        #text(whorst_index, max(self.signal) / 2, str("худшее"), rotation=0, verticalalignment='center', color='red')


    def draw_situation_for_index(self, ax, index):
        ax.vlines(x=index, ymin=0, ymax=max(self.signal), colors='blue', lw=1, alpha=0.5, label="ТЕСТОВАЯ т.")

        nearest_left_point = self.get_left_nearest_point(index)
        if nearest_left_point is not None:
            l_index = nearest_left_point.coord
            ax.vlines(x=l_index, ymin=0, ymax=max(self.signal), colors='blue', lw=5, alpha=0.2, label="ближайший левый оп.")

        nearest_right_point = self.get_right_nearest_point(index)
        if nearest_right_point is not None:
            r_index = nearest_right_point.coord
            ax.vlines(x=r_index, ymin=0, ymax=max(self.signal), colors='blue', lw=5, alpha=0.2,
                      label="ближайший правый оп.")

    def fill_from_array_by_nearest_principle(self, coords_arr):
        names = []
        for coord in coords_arr:
            name = self.add_point(coord)
            names.append(name)

        for i in range(len(names)):
            name = names[i]
            coord = coords_arr[i]
            left_point_name = self.get_left_nearest_point_name(coord)
            if left_point_name is not None:
                self.add_parent(name, left_point_name)
            right_point_name = self.get_right_nearest_point_name(coord)
            if right_point_name is not None:
                self.add_parent(name, right_point_name)



if __name__ == '__main__':
    signal = get_mini_ECG()


    scene = Scene(signal)
    name_1 = scene.add_point(coord=105)
    name_2 = scene.add_point(coord=94)
    scene.add_parent(parent_name=name_1, child_name=name_2)

    name_3 = scene.add_point(coord=53)
    scene.add_parent(parent_name=name_1, child_name=name_3)


    fig, axs = plt.subplots()
    scene.draw(axs)
    #scene.draw_situation_for_index(axs, index=50)

    plt.show()



