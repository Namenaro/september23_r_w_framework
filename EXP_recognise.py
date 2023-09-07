# TODO сейчас весь фрейморк распознавания написан из предположения, что у всех точек, кроме первой, ЕСТЬ РОДИТЕЛЬ. И тестируемся именно на таких примерах
from utils import  HtmlLogger, StartSituationsGen, StartSituation
from recogniser import Recogniser
from program import Program, Resctiction


def get_program():
    sit_gen = StartSituationsGen()
    situation = sit_gen.__next__()
    signal = situation.signal
    first_v = signal[situation.start_point]


    program = Program()
    name1 = program.add_first_node(v=first_v)

    coord2 = 14
    v2 = signal[coord2]
    u2 = coord2 - situation.start_point
    restriction2 = Resctiction(left_name=None, right_name=name1)
    name2 = program.add_node(v=v2, u=u2, parent_name=name1, restriction=restriction2)

    coord3 = 37
    v3 = signal[coord3]
    u3 = coord3 - situation.start_point
    restriction3 = Resctiction(left_name=name1, right_name=None)
    name3 = program.add_node(v=v3, u=u3, parent_name=name1, restriction=restriction3)

    coord4 = 5
    v4 = signal[coord4]
    u4=coord4-coord2
    restriction4 = Resctiction(right_name=name2)
    name5 = program.add_node(v=v4, u=u4, parent_name=name2, restriction=restriction4)

    return program


if __name__ == '__main__':
    log = HtmlLogger("LOG_recogniser")
    sit_gen = StartSituationsGen()
    situation = sit_gen.__next__()
    signal = situation.signal
    program = get_program()
    program.print()
    recogniser = Recogniser(program, signal)
    recogniser.draw_rostocs(log)

    step_num = 1
    while True:
        success = recogniser.make_step()
        if success is False:
            break

        print("ШАГ " + str(step_num) + " : кол-во ростков ->  " + str(recogniser.get_num_rostocs()))
        log.add_text("ШАГ " + str(step_num) + " : кол-во ростков ->  " + str(recogniser.get_num_rostocs()))
        recogniser.draw_rostocs(log)
        step_num +=1