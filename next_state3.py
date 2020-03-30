import numpy as np
import ur_data_plus_joints as ur
import goal_calc2 as goal
import pickle as pickle
import data_driven_force_calculator3 as f



def state_calc(e = 0, x_current = 0, y_current = 0, x_goal = 0, y_goal = 0):

	print("")
	print("    Starting state_calc")


	if e == 0:

		j0, j2, j4, j5,e0, e1, e2, e3, e4, e5,v0, v2, v4, v5, x, y  = ur.where_now()#

		current_pos_x = x
		current_pos_y = y

	else:
		current_pos_x = x_current
		current_pos_y = y_current

	if e == 0:
		# import user defined goal position.
		x_goal,y_goal = goal.goal_pos_calc()


	if e == 0:
		'''Translate the robot into the task space by offsetting the current robot position.
		'''
		current_pos_x, current_pos_y = ur.base_to_task(current_pos_x, current_pos_y)

	print("    current_pos_x", current_pos_x)
	print("    current_pos_y", current_pos_y)

	opposite = x_goal - current_pos_x # opposite
	adjacent = y_goal - current_pos_y # adjacent

	print("    opposite", opposite)
	adjacent = np.abs(adjacent)
	print("    adjacent", adjacent)

	# square the opposite and adjacent sides.
	x_sq = (opposite)**2 #adj^2
	y_sq = (adjacent)**2 #oppo^2

	# calculate hypotenuse between current and goal pos.
	#this is needed in order to build a new triangle to feed back into the goal calc.
	polar_rad = np.sqrt(x_sq + y_sq)

	print("    polar rad", polar_rad)
	x = opposite
	y = adjacent

	'''find the new angle in degrees to feed back into goal calc.
	'''
	polar_angle = np.arctan(x/y) # in radians.
	polar_angle = polar_angle *(180/np.pi) # convert rad to deg.
	print("    polar angle", polar_angle)
	polar_angle = np.abs(polar_angle)

	# using  < symbol cus y values are positive due to tan()
	# opperation in goal_calc.
	if y_goal > current_pos_y and x_goal < current_pos_x:
		polar_angle = 180 + polar_angle
		print("    adjust 1")


	elif current_pos_y < y_goal and x_goal > current_pos_x:
		polar_angle = 180 - polar_angle
		print("    adjust 2")


	elif x_goal < current_pos_x and y_goal < current_pos_y:
		polar_angle = 360 - polar_angle
		print("    adjust 3")

	else:
		polar_angle =  polar_angle
		print("    Not adjusted")


	print("    adusted polar angle", polar_angle)


	# segment the hypotenuse into 10mm intervals.
	interval =  0.01 #10mm interval  #polar_rad


	x,y = goal.goal_pos_calc(polar_angle, interval)

	x = x
	y = y#*(-1) #sign needs inverting to make it relative to robot space. but srews up trig functions.
	#better to leave sign untill value gets posed to robot.


	# x_rel = next_x_relative_to_orifice
	print("    current_pos_x", current_pos_x)
	print("    current_pos_y", current_pos_y)


	x = np.abs(x)
	if np.abs(x_goal) > np.abs(current_pos_x) :
		next_x_rel = current_pos_x + x
		print("    x+x")
	else:
		next_x_rel = current_pos_x - x
		print("   x-x")


	if y_goal > current_pos_y:
		next_y_rel = current_pos_y - y # Remember it's (- - = +!)
		print("    y-y")
	else:
		next_y_rel = current_pos_y + y
		print("    y+y")

	#next_y_rel = np.abs(next_y_rel)
	print("    next_x_reletive to orifice", next_x_rel)
	print("    next_y_reletive to orifice", next_y_rel)
	'''find the angle and distance between iterative step and the orifice by
	squaring the opposite and adjacent sides.
	no need for subtracting orifice from next position as
	orifice is 0,0.
	'''
	next_x_sq = next_x_rel**2 #adj^2
	next_y_sq = next_y_rel**2 #oppo^2

	# calculate hypotenuse between iterative step and orifice.
	#this is needed in order to build a new triangle to feed
	#length back into the goal calc.
	polar_rad = np.sqrt(next_x_sq + next_y_sq) #distance from orifice to iterative step.


	polar_angle = np.arctan(next_x_rel/next_y_rel) # in radians.between orifice and iterative step.
	polar_angle = polar_angle *(180/np.pi) # convert rad to deg.



	polar_angle = np.abs(polar_angle)

	print("    x_goal y_goal", x_goal, y_goal)
	print("    angle ", polar_angle)


	# Pickle everything to avoid circular feferences.
	pickel_goal = x_goal, y_goal #persistant goal values
	with open('pickle_goal.pickle', "wb") as file5:
		pickle.dump(pickel_goal, file5, -1)


	pickel_file = x,y #of iterative step.
	with open('pickle_file.pickle', "wb") as file1:
		pickle.dump(pickel_file, file1, -1)

	pickel_send = polar_rad, polar_angle # remember, this is between step and orifice!
	with open('pickle_send.pickle', "wb") as file2:
		pickle.dump(pickel_send, file2, -1)


	pickel_next_move = next_x_rel, next_y_rel # remember, this is between step and orifice!
	with open('pickel_next_move.pickle', "wb") as file6:
		pickle.dump(pickel_next_move, file6, -1)

	print("    Return: polar_rad", polar_rad) # between next step and orifice
	print("    Return polar_angle", polar_angle) # between next step and orifice.
	print("    Return x, y", x,y)
	print("    Return next steps relative to orifice", next_x_rel, next_y_rel)
	return  polar_rad, polar_angle, x, y, next_x_rel, next_y_rel

if __name__ == '__main__':
	state_calc()
