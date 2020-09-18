#this can be expanded to include robot pose.

import os
import ur_data_plus_joints2 as ur
import next_state4 as state
import goal_calc4 as goal
import data_driven_force_calculator4 as forcex
import glob
import pickle as pickle
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import time
import pandas as pd

# Load inverse kinematics model
with open('/home/ur10pc/Desktop/robot_data/pickle/ik_model2.pkl','rb') as ik:
        ik_model = pickle.load(ik)

# Load Saved force prediction Model
with open('/home/ur10pc/Desktop/robot_data/pickle/80k_model2.pkl','rb') as f:
        pipeline = pickle.load(f)


#############################################################################################

def model(j0, j2, j4, j5):
          #e0, e1, e2, e3, e4, e5,\
          #v0, v2, v4, v5):

    print("Starting 80k model!!!!!")
    # # Construct dummy data frame to house
    dataw = pd.DataFrame([[ j0, j2, j4, j5]],
    #                         e0, e1, e2, e3, e4, e5,\
    #                         v0, v2, v4, v5]],
                 columns=["joint_0",    "joint_2", "joint_4", "joint_5"])
    #             "effot_joint_0",   "effot_joint_1",   "effot_joint_2",   "effot_joint_3",   "effot_joint_4",   "effot_joint_5",
    #             "vel_joint_0", "vel_joint_2", "vel_joint_4", "vel_joint_5"])

    # # Data has 'no' added synthetic data- previous controller did.
    # data0 = pd.read_csv('/home/ur10pc/Desktop/robot_data2/80k_data/data_sample.csv', delimiter=',')
    # data0 = pd.DataFrame(data0)

    # # Append new data-point to existing data for regularisation
    # data0 = data0.append(dataw, ignore_index = True, sort=False)

    # # Regularisation over data including new datapoint.
    # from sklearn.preprocessing import StandardScaler
    # data = data0.drop('Force Vec', axis=1)
    # scaler = StandardScaler()
    # scaler.fit(data)
    # data2 = scaler.transform(data)
    # data2 = pd.DataFrame(data2)
    # data2.columns= ["j0", "j2", "j4", "j5",
    #                 "e0","e1","e2","e3","e4","e5",
    #                 "v0","v2","v4","v5"]

    #  # Make New Prediction On New datapoint
    # sample = data2#.drop('force', axis=1)#features[-1:]
    # sample = sample[-1:]


    result = pipeline.predict(dataw)
    result = result[0]
    print('hello',result)

    return result

###########################################################################################


def ik_predictor(x, y):

    print("Starting ik model*****")

    z = 0.0436 # This doesn't change as the task space is a plane.

    sample = pd.DataFrame([[x, y, z]], columns=['x', 'y', 'z'])
    #print(sample)
    result = ik_model.predict(sample)

    return result

##########################################################################

def robot_command(x_current, y_current):

	print("")
	print("Starting robot_command")
	print("next_x_rel", x_current)
	print("next_y_rel", y_current)


	#open pickle append to get list of intervals so far.
	with open('pickle_append.pickle', "rb") as file4:
		intervals = pickle.load(file4)

	# assign the current iteration tuple x,y to the variable "this_interval".
	this_interval = (x_current ,y_current)


	# Append "this_interval" to the list of intervals.
	intervals.append(this_interval)

	# we now have a primed pickle file for later use in each iteration.
	with open("pickle_append.pickle", "wb") as file4:
		pickle.dump(intervals, file4, -1)


	return
#########################################################################

def get_values():


	# file handling. this section removes previous pickle files.
	directory = os.getcwd()
	print(os.getcwd())
	mpc = "/home/ur10pc/Desktop/mpc/mpc3"
	if directory == mpc:
		for file in glob.glob("*.pickle"):
			os.remove(file)
	elif os.path.exists("/home/ur10pc/Desktop/mpc/mpc3"):
		os.chdir("/home/ur10pc/Desktop/mpc/mpc3")
	else:
		f = open("/home/ur10pc/Desktop/mpc/mpc3")
	os.chdir("/home/ur10pc/Desktop/mpc/mpc3")


	print("")
	print("Starting get_values")

	# find force by invoking force_cal
	force_prediction = forcex.force_calc()
	print("Force prediction =", force_prediction, "N")
	max_force = float(input("Enter Max Force (Default = 2N) : ") or "2")

	with open('pickel_next_move.pickle', "rb") as file6:
		next_x_rel, next_y_rel = pickle.load(file6)


	# Get x,y of goal_pos.
	with open('pickle_goal.pickle', "rb") as file5:
		x_goal,y_goal = pickle.load(file5)

	print("x_goal", x_goal)
	print("y_goal", y_goal)

	# on first iteration, pickle file won't yet exist.
	if not os.path.isfile("pickle_append.pickle"):
		intervals = []
		with open("pickle_append.pickle", "wb") as file4:
			pickle.dump(intervals, file4, -1)

	# on first iteration, pickle file won't yet exist.
	if not os.path.isfile("pickle_xy.pickle"):
		xy_intervals = []
		with open("pickle_xy.pickle", "wb") as file8:
			pickle.dump(xy_intervals, file8, -1)


	x_error = np.abs(x_goal - next_x_rel)
	y_error = np.abs(y_goal - next_y_rel)

	with open('pickle_send.pickle', "rb") as file1:
		polar_rad, polar_angle = pickle.load(file1)


	i = 1

	# while the robot is not at the goal, loop throght finding the next iterative step.
	while x_error > 0.05 or y_error > 0.05:

		if x_error <= 0:
			break

		if i ==100:
			break

		#while i < 5:
		print("restart while loop")
		print(" polar_angle", polar_angle, "polar_rad", polar_rad)

		force_prediction, x,y = forcex.force_calc(polar_rad, polar_angle)

		print("force_prediction")
		print(force_prediction)
		print("")

		# if force is low enough, send invoke robot_command to save current (x,y).
		if force_prediction < max_force:
			robot_command(next_x_rel, next_y_rel)
		else:
			# if force is too large invoke beam_adjust to find new beam length and lower force.
			if (np.abs(next_x_rel) < np.abs(x_goal)) and next_y_rel>-1.0:

				print("##############force prediction############", force_prediction)
				print("##############max force############", max_force)

				while force_prediction > max_force:
					print("")
					print("Starting Beam Adjust!!!!!!!!!!!!!!!!!!")
					print("")
					force, x, y = forcex.beam_adjust()
					print("force step = ", force)
					force_prediction = force
					print(x,y)
					if np.abs(x) >2 or np.abs(y) >2:
						break

			# Open pickle where new angle and distance are saved by beam_adjust.
			with open('pickle_send.pickle', "rb") as file2:
				pickle_out = pickle.load(file2)

			# Assign variables to pickled objects.
			L_1, pull_angle = pickle_out

			# Using new angle and distance; get new x,y for next iterative move.
			next_x_rel, next_y_rel = goal.goal_pos_calc(pull_angle, L_1)

			# invoke robot_command to save append latest x,y step.
			robot_command(next_x_rel, next_y_rel)

		# Now with the current low force x,y saved, start over to find the next xy.
		e = 1 # Used to swith offset function on/off in next_state
		# We input the current x,y into state_calc and get a new iterative step x,y out.

		print(" next_x_rel", next_x_rel)
		print("next_y_rel", next_y_rel)
		polar_rad, polar_angle, x_current,y_current, next_x_rel, next_y_rel= state.state_calc(e, \
			next_x_rel, \
			next_y_rel, \
			x_goal, \
			y_goal\
			)
		print("\033[1;34;40m Bright Green  \n")
		print("next_x_rel", next_x_rel)
		print("next_y_rel", next_y_rel)
		print("\033[1;32;40m Bright Green  \n")
		x_error = np.abs(x_goal - next_x_rel)
		y_error = np.abs(y_goal - next_y_rel)

		i += 1
		print("i =", i)
		print("")

		print("x_error", x_error)
		print("y_error", y_error)

	# Append the goal position as the last iterative move to make sure the robot reaches the target.
	robot_command(x_goal, y_goal)

	with open("pickle_append.pickle",  "rb") as file4:
			intervals = pickle.load(file4)

	return intervals

def robotmove_intervals():
	intervals = get_values()

	robot_moves = [list(i) for i in intervals]

	del robot_moves[0]

	last_move = []
	last_move = robot_moves[-1]

	robot_moves = robot_moves[0::11]

	print("last_move", last_move)
	robot_moves.append(last_move)

	print("'intervals'")
	pprint(robot_moves)


	robot_moves = [tuple(i) for i in robot_moves]

	print("robot_moves")
	pprint(robot_moves)

	robot_moves_offset =[]
	for i in robot_moves:
		(x,y)  = ur.task_to_base(i)
		robot_moves_offset.append((x,y))


	robot_movesx = [list(i) for i in robot_moves_offset]

	del robot_movesx[0]

	print("offset moves")
	pprint(robot_movesx)


	plt.ion()
	fig = plt.figure()
	data = np.array(robot_moves)
	#plt.figure(num='Task Frame Moves')
	plt.title('Task Frame Moves')
	plt.xlabel('x')
	plt.ylabel('y')
	axes = plt.gca()
	axes.set_xlim([-0.2,0.7])
	axes.set_ylim([-1.4,0])
	x, y = data.T
	plt.scatter(x,y,)
	plt.show()
	plt.waitforbuttonpress(0)


	plt.ion()
	fig = plt.figure()
	data = np.array(robot_movesx)
	plt.title('Base Frame Moves')
	plt.xlabel('x')
	plt.ylabel('y')
	axes = plt.gca()
	axes.set_xlim([-0.2,0.7])
	axes.set_ylim([-1.4,0])
	x, y = data.T
	plt.scatter(x,y)
	#plt.show()
	plt.waitforbuttonpress(0)

	plt.close("all")


	zeros = [0.05, 3.142, 0, 0]

	for i in range(len(robot_movesx)):
		robot_movesx[i].extend(zeros)

	robot_moves_offset = [list(i) for i in robot_moves_offset]

	zeros = [0,0,0,0]


	for i in range(len(robot_moves_offset)):
		robot_moves_offset[i].extend(zeros)


	with open('pickle_xy.pickle', "rb") as file8:
		xy_intervals = pickle.load(file8)

	robot_moves_intervals = [list(i) for i in xy_intervals]


	for i in range(len(robot_moves_intervals)):
		robot_moves_intervals[i][1] = - robot_moves_intervals[i][1]

	for i in range(len(robot_moves_intervals)):
		robot_moves_intervals[i].extend(zeros)

	return robot_movesx

if __name__ == "__main__":
	#robotmove_intervals()


	e0 = 5.056
	e1 = -5.338
	e2 = -2.337
	e3 = 14.429
	e4 = 14.067
	e5 = 30.009

	# using the mean values for velocity accros 80k samples
	v0 = 0.006
	v2 = -0.006
	v4 = -0.000
	v5 = -0.011

	joints = ik_predictor(0.909684, -0.218834)

	j0 = joints[0][0]
	j2 = joints[0][1]
	j4 = joints[0][2]
	j5 = joints[0][3]


	force = model(j0, j2, j4, j5, \
	      e0, e1, e2, e3, e4, e5,\
	      v0, v2, v4, v5)
	print(force)
