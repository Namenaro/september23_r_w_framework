from rostok import Rostoc


class LateralInhibitionSystem:
    def __init__(self, rosctocs):
        self.rostocs = rosctocs # их будем прореживать (удялть лишние)


    def run_inhibition(self, procent=0.8):
        indexes_to_remove = set()
        # будем сравнивать каждй росток с каждым, кроме себя самого
        num_rostocs = len(self.rostocs)
        for i in range(num_rostocs):
            for j in range(i+1, num_rostocs):
                rostoc1 = self.rostocs[i]
                rostoc2 = self.rostocs[j]

                coords1 = rostoc1.get_lefs_coords()
                ws1 = rostoc1.get_leafs_ws()

                coords2 = rostoc2.get_lefs_coords()
                ws2 = rostoc2.get_leafs_ws()

                need_delete_1, need_delete_2 = decise(coords1, coords2, ws1 , ws2, procent)
                if need_delete_1:
                    indexes_to_remove.add(i)
                if need_delete_2:
                    indexes_to_remove.add(j)


        self.rostocs = [i for j, i in enumerate(self.rostocs) if j not in indexes_to_remove]


def decise(coords1, coords2, ws1 , ws2, threshold=0.8):

    need_delete_1 = False
    need_delete_2 = False

    m1 = measure_intersection_procent(coords1, coords2)
    m2 = measure_intersection_procent(coords2, coords1)

    if max(m1, m2)<threshold:
        return need_delete_1, need_delete_2   # никого не удаляем

    best_w1 =max(ws1)
    best_w2 = max(ws2)

    if best_w1>best_w2:   #TODO возможно нужно сравнивать w-шки только из перечечения?
        need_delete_2 = True
        return need_delete_1, need_delete_2

    need_delete_2=True
    return need_delete_1, need_delete_2


def measure_intersection_procent(coords1, coords2):
    # сколько записей из coords1 присутсвуют в coords2
    num_of_1_in_2 =0
    for coord in coords1:
        if coord in coords2:
            num_of_1_in_2 +=1

    procent = num_of_1_in_2/len(coords1)
    return procent

