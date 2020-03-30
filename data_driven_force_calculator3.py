import numpy as np
import next_state3
import pickle as pickle
import goal_calc2 as goal
import ur_data_plus_joints as ur
import ik_model as ik
import a80k_model_predict as test



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



    force = force_calc(pull_angle, L_1)

    force = force
    return force



def force_calc(L_1 = 0.0, pull_angle = 0.0):
    print("")
    print("  Starting force_calc with L_1", L_1, " pull_angle", pull_angle)

    if L_1 == 0.0:
        L_1, pull_angle, x ,y, next_x_rel, next_y_rel= next_state3.state_calc()

    # find x and y values from pull angle and length.
    x, y = goal.goal_pos_calc(pull_angle, L_1)

    # Use x and y to find joint angles from ik model.
    joints = ik.ik_predictor(x, y)

    print(joints)



    if L_1 == 0.0:
        j0, j2, j4, j5, e0,e1,e2,e3,e4,e5,v0, v2,v4,v5, x, y = ur.where_now()

    else:
        j0 = joints[0][0]
        j2 = joints[0][1]
        j4 = joints[0][2]
        j5 = joints[0][3]

        # using the mean values for effort accros 80k samples
        e0 = 0.056
        e1 = -5.338
        e2 = -2.337
        e3 = -0.429
        e4 = 0.067
        e5 = -0.009

        # using the mean values for velocity accros 80k samples
        v0 = 0.006
        v2 = -0.006
        v4 = -0.000
        v5 = -0.011

    force = test.model( j0, j2, j4, j5, \
                        e0, e1, e2, e3, e4, e5,\
                        v0, v2, v4, v5)


    pickel_file = L_1,pull_angle
    with open('pickle_L_1_pull_angle.pickle', "wb") as file3:
        pickle.dump(pickel_file, file3, -1)

    print(force)
    return force

if __name__ == '__main__':
    force = force_calc(0.5,45)
