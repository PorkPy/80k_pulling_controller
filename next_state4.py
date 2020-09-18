import numpy as np
import ur_data_plus_joints2 as ur
import goal_calc4 as goal
import pickle as pickle
import data_driven_force_calculator4 as f



def state_calc(e = 0, x_current = 0, y_current = 0, x_goal = 0, y_goal = 0):
	#the argument x_current is the next_x_rel which is the next
	#position from which the future positions should be calculated.
	print("")
	print("    Starting state_calc")

	''' this code takes in the robot's current position and user defined goal position, and
	calculates the distance between them.
	it then breaks down that distance into intervals and returns the next interval as an angle
	and distance which then gets imported into force_calculator.
	'''


	if e == 0:
		#import current robot position and add to dictionary current_pos.

		x,y  = ur.where_now()

		#create a dictionary of the current x,y position.
		current_pos_x = x
		current_pos_y = y

	else:
		current_pos_x = x_current
		current_pos_y = y_current



	'''This block gets the goal position in x,y and uses it to work out the angle and distance between
	the current position and the goal.
	'''


	if e == 0:
		# import user defined goal position.
		x_goal,y_goal = goal.goal_pos_calc()


	if e == 0:
		'''Translate the robot into the task space by offsetting the current robot position.
		'''
		current_pos_x, current_pos_y = ur.base_to_task(current_pos_x, current_pos_y)

	#current_pos_y = current_pos_y *(-1)

	print("    current_pos_x", current_pos_x)
	print("    current_pos_y", current_pos_y)

	'''build new dict to find lengths of opposite and adjacent sides of triangle
	formed between current position and goal position. These are then used to
	find the hypotenuse which is the trajectory between the current and goal positions.
	'''

	opposite = x_goal - current_pos_x # opposite
	adjacent = np.abs(y_goal - current_pos_y) # adjacent

	print("    opposite", opposite)
	print("    adjacent", adjacent)

	# calculate hypotenuse between current and goal pos.
	#this is needed in order to build a new triangle to feed back into the goal calc.
	polar_rad = np.sqrt(opposite**2 + adjacent**2)

	x = opposite
	y = adjacent

	'''find the new angle in degrees to feed back into goal calc.
	'''
	polar_angle = np.arctan(x/y) # in radians.
	polar_angle = np.abs(np.degrees(polar_angle))

	# This section is the unit circle adjustment. We only calculate angles
	# between 0 and 90, but we need angle from 0 to 360. therefore, by
	# determining where the goal and current positions are relative to each other,
	# on a unit circle, the actual angle between 0 and 360 can be determined.
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


	print("    adjusted polar angle", polar_angle)



	# Segment the hypotenuse of the above into 10mm intervals.
	# The first interval be the proposal for the next iterative step,
	# as long as the force is low enough.
	interval =  0.01 #10mm interval  #polar_rad


	# The iterative step angle and distance can now be fed back to
	# the goal pos calculator to get the x,y coordinates of the iterative step.
	x,y = goal.goal_pos_calc(polar_angle, interval)



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


	# Find the angle and distance between iterative step and the orifice by
	# squaring the opposite and adjacent sides.
	# No need for subtracting orifice from next position as
	# orifice is 0,0.

	# calculate hypotenuse between iterative step and orifice.
	# This new angle and length will be used to determine the the the force on the hose
	# when pulled by the robot at the iterative step.
	polar_rad = np.sqrt(next_x_rel**2 + next_y_rel**2) #distance from orifice to iterative step.

	polar_angle = np.abs(np.degrees(np.arctan(next_x_rel/next_y_rel)))


	# Pickle everything to avoid circular references.
	pickel_goal = x_goal, y_goal #persistent goal values
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


	return polar_rad, polar_angle, x,y, next_x_rel, next_y_rel


if __name__ == '__main__':
	state_calc()
