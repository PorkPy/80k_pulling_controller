import numpy as np
import next_state4 as state
import pickle as pickle
import goal_calc4 as goal
import ur_data_plus_joints2 as ur
#import ik_model2 as ik
#import a80k_model_predict2 as test
import command4 as comm

def beam_adjust():

    print("")
    print("Starting Beam Adjust")
    with open('pickle_send.pickle', "rb") as file2:
        pickle_out = pickle.load(file2)

    L_1, pull_angle = pickle_out
    print("pull_angle", pull_angle)
    print("L_1", L_1)


    L_1 = L_1 + 0.15
    if pull_angle > 80:
        pull_angle = pull_angle - 1.5
    elif pull_angle > 60:
        pull_angle = pull_angle - 1.5#0.2
    else:
        pull_angle = pull_angle - 1.5#0.1


    pickel_send = L_1, pull_angle
    with open('pickle_send.pickle', "wb") as file2:
        pickle.dump(pickel_send, file2, -1)

    force, x,y  = force_calc(pull_angle, L_1)
    print(x)
    print(y)
    return force, x,y


def force_calc(L_1 = 0.0, pull_angle = 0.0):
    print("")
    print("  Starting force_calc with L_1", L_1, " pull_angle", pull_angle)

    if L_1 == 0.0:
        # If this is the first iteration, there is not yet a pull angle or pull length.
        # Invoking state_calc(), returns the current x, y position, the iterative step
        # position in x,y, and the iterative step position as a pull angle and length.
        L_1, pull_angle, x,y , next_x_rel, next_y_rel= state.state_calc()


    # find x and y values from pull angle and length.
    x, y = goal.goal_pos_calc(pull_angle, L_1)



    # Use x and y to find joint angles from ik model.
    joints = comm.ik_predictor(x, y)
    trimmed_results = np.delete(joints, [1,3],1)

    if L_1 == 0.0:
        j0, j2, j4, j5, e0,e1,e2,e3,e4,e5,v0, v2,v4,v5, x, y = ur.where_now()

    else:
        j0 = trimmed_results[0][0]
        j2 = trimmed_results[0][1]
        j4 = trimmed_results[0][2]
        j5 = trimmed_results[0][3]

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

    force = comm.model( j0, j2, j4, j5)
                        #e0, e1, e2, e3, e4, e5,\
                        #v0, v2, v4, v5)


    # pickel_file = L_1,pull_angle
    # with open('pickle_L_1_pull_angle.pickle', "wb") as file3:
    #     pickle.dump(pickel_file, file3, -1)
    #force = force * 1.2
    print("force = ", force)
    return force, x,y # x and y used to break code if x and y are too large.

if __name__ == '__main__':
    force = force_calc(0.5,45)
