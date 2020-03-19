import numpy as np
import next_state2
import pickle as pickle
import goal_calc2 as goal


def beam_adjust():

    print("")
    print("Starting Beam Adjust")
    with open('pickle_send.pickle', "rb") as file2:
        pickle_out = pickle.load(file2)

    L_1, pull_angle = pickle_out
    print("pull_angle", pull_angle)
    print("L_1", L_1)


    L_1 = L_1 + 0.05
    if pull_angle > 80:
        pull_angle = pull_angle - 0.4
    elif pull_angle > 60:
        pull_angle = pull_angle - 0.5#0.2
    else:
        pull_angle = pull_angle - 0.5#0.1


    pickel_send = L_1, pull_angle
    with open('pickle_send.pickle', "wb") as file2:
        pickle.dump(pickel_send, file2, -1)

    force = force_calc(L_1, pull_angle)

    force = force
    return force



def force_calc(L_1 = 0.0, pull_angle = 0.0):
    print("")
    print("  Starting force_calc with L_1", L_1, " pull_angle", pull_angle)

    if L_1 == 0.0:
        L_1, pull_angle, x ,y, next_x_rel, next_y_rel= next_state2.state_calc()


    import test3_prediction as test

    force = test.model(pull_angle)


    pickel_file = L_1,pull_angle
    with open('pickle_L_1_pull_angle.pickle', "wb") as file3:
        pickle.dump(pickel_file, file3, -1)

    return force

if __name__ == '__main__':
    force = force_calc(0.5,45)
