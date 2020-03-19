# Echo client program
import socket
import time
import struct
import pickle as pickle
import numpy as np
from pprint import pprint
import math

HOST = "123.124.125.11" # The remote host
PORT_30003 = 30003

def where_now():
	print( "")
	print("Starting where_now!")

	count = 0
	home_status = 0
	program_run = 0





	# while (True):
	# 	if program_run == 0:
	# 		try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(10)
	s.connect((HOST, PORT_30003))
	time.sleep(1.00)
	print ("")
	packet_1 = s.recv(4)
	packet_2 = s.recv(8)
	packet_3 = s.recv(48)
	packet_4 = s.recv(48)
	packet_5 = s.recv(48)
	packet_6 = s.recv(48)
	packetx = s.recv(48)

	packet_13 = s.recv(8)
	packet_13 = packet_13#.encode("hex") #convert the data from \x hex notation to plain hex
	j0 = str(packet_13)
	j0 = struct.unpack('!d', packet_13)#.decode('hex'))[0]

	packet_14 = s.recv(8)
	packet_14 = packet_14#.encode("hex") #convert the data from \x hex notation to plain hex
	j1 = str(packet_14)
	j1 = struct.unpack('!d', packet_14)#.decode('hex'))[0]

	packet_15 = s.recv(8)
	packet_15 = packet_15#.encode("hex") #convert the data from \x hex notation to plain hex
	j2 = str(packet_15)
	j2 = struct.unpack('!d', packet_15)#.decode('hex'))[0]

	packet_16 = s.recv(8)
	packet_16 = packet_16#.encode("hex") #convert the data from \x hex notation to plain hex
	j3 = str(packet_16)
	j3 = struct.unpack('!d', packet_16)#.decode('hex'))[0]

	packet_17 = s.recv(8)
	packet_17 = packet_17#.encode("hex") #convert the data from \x hex notation to plain hex
	j4 = str(packet_17)
	j4 = struct.unpack('!d', packet_17)#.decode('hex'))[0]


	packet_18 = s.recv(8)
	packet_18 = packet_18#.encode("hex") #convert the data from \x hex notation to plain hex
	j5 = str(packet_18)
	j5 = struct.unpack('!d', packet_18)#.decode('hex'))[0]

	packet_19 = s.recv(8)
	packet_19 = packet_19#.encode("hex") #convert the data from \x hex notation to plain hex
	v0 = str(packet_19)
	v0 = struct.unpack('!d', packet_19)#.decode('hex'))[0]

	packet_20 = s.recv(8)
	packet_20 = packet_20#.encode("hex") #convert the data from \x hex notation to plain hex
	v1 = str(packet_20)
	v1 = struct.unpack('!d', packet_20)#.decode('hex'))[0]

	packet_21 = s.recv(8)
	packet_21 = packet_21#.encode("hex") #convert the data from \x hex notation to plain hex
	v2 = str(packet_21)
	v2 = struct.unpack('!d', packet_21)#.decode('hex'))[0]

	packet_22 = s.recv(8)
	packet_13 = packet_13#.encode("hex") #convert the data from \x hex notation to plain hex
	v3 = str(packet_13)
	v3 = struct.unpack('!d', packet_13)#.decode('hex'))[0]

	packet_22 = s.recv(8)
	packet_22 = packet_22#.encode("hex") #convert the data from \x hex notation to plain hex
	v4 = str(packet_22)
	v4 = struct.unpack('!d', packet_22)#.decode('hex'))[0]

	packet_23 = s.recv(8)
	packet_23 = packet_23#.encode("hex") #convert the data from \x hex notation to plain hex
	v5 = str(packet_23)
	v5 = struct.unpack('!d', packet_23)#.decode('hex'))[0]

	packet_25 = s.recv(48)

	packet_7 = s.recv(8)
	packet_7 = packet_7#.encode("hex") #convert the data from \x hex notation to plain hex
	e0 = str(packet_7)
	e0 = struct.unpack('!d', packet_7)#.decode('hex'))[0]

	packet_8 = s.recv(8)
	packet_8 = packet_8#.encode("hex") #convert the data from \x hex notation to plain hex
	e1 = str(packet_8)
	e1 = struct.unpack('!d', packet_8)#.decode('hex'))[0]

	packet_9 = s.recv(8)
	packet_9 = packet_9#.encode("hex") #convert the data from \x hex notation to plain hex
	e2 = str(packet_9)
	e2 = struct.unpack('!d', packet_9)#.decode('hex'))[0]

	packet_11 = s.recv(8)
	packet_11 = packet_11#.encode("hex") #convert the data from \x hex notation to plain hex
	e3 = str(packet_11)
	e3 = struct.unpack('!d', packet_11)#.decode('hex'))[0]

	packet_11 = s.recv(8)
	packet_11 = packet_11#.encode("hex") #convert the data from \x hex notation to plain hex
	e4 = str(packet_11)
	e4 = struct.unpack('!d', packet_11)#.decode('hex'))[0]

	packet_12 = s.recv(8)
	packet_12 = packet_12#.encode("hex") #convert the data from \x hex notation to plain hex
	e5 = str(packet_12)
	e5 = struct.unpack('!d', packet_12)#.decode('hex'))[0]




	packet_26 = s.recv(8)
	packet_26 = packet_26#.encode("hex") #convert the data from \x hex notation to plain hex
	x = str(packet_26)
	x = struct.unpack('!d', packet_26)#.decode('hex'))[0]
	#print "X = ", x * 1000

	packet_27 = s.recv(8)
	packet_27 = packet_27#.encode("hex") #convert the data from \x hex notation to plain hex
	y = str(packet_27)
	y = struct.unpack('!d', packet_27)#.decode('hex'))[0]
	#print "Y = ", y * 1000

	packet_28 = s.recv(8)
	packet_28 = packet_28#.encode("hex") #convert the data from \x hex notation to plain hex
	z = str(packet_28)
	z = struct.unpack('!d', packet_28)#.decode('hex'))[0]
	#print "Z = ", z * 1000

	packe_29 = s.recv(8)
	packe_29 = packe_29#.encode("hex") #convert the data from \x hex notation to plain hex
	Rx = str(packe_29)
	Rx = struct.unpack('!d', packe_29)#.decode('hex'))[0]
	#print "Rx = ",_29
	packe_30 = s.recv(8)
	packe_30 = packe_30#.encode("hex") #convert the data from \x hex notation to plain hex
	Ry = str(packe_30)
	Ry = struct.unpack('!d', packe_30)#.decode('hex'))[0]
	#print "Ry = ", Ry

	packet_31 = s.recv(8)
	packet_31 = packet_31#.encode("hex") #convert the data from \x hex notation to plain hex
	Rz = str(packet_31)
	Rz = struct.unpack('!d', packet_31)#.decode('hex'))[0]
	#print "Rz = ", Rz



	#print pose["x"]

	# create a short variable to input into robot command-(move)
	#nextmove =  [goal['x'], goal['y'], goal['z'], goal['Rx'], goal['Ry'], goal['Rz']]

	#return pose

	home_status = 1
	program_run = 0
	s.close()
			# except socket.error as socketerror:
			# 	print("Error: ", socketerror)
	pose = x,y
	with open('ur_data.pickle', "wb") as ur_file:
		pickle.dump(pose, ur_file, -1)

	#y = np.abs(y)
	return j0[0],  j1[0], j2[0], j3[0], j4[0], j5[0], e0[0],e1[0],e2[0],e3[0],e4[0],e5[0],v0[0],v1[0],v2[0],v3[0],v4[0],v5[0]




if __name__ == '__main__':
	j0, j1, j2,j3, j4, j5, e0,e1,e2,e3,e4,e5,v0,v1, v2,v3, v4,v5 = where_now()
	print(j0, j1, j2, j3, j4, j5)
	import pandas as pd
	data = [{"j0":j0, "j1":j1, "j2":j2, "j3":j3, "j4":j4, "j5":j5, "e0":e0,"e1":e1,"e2":e2,"e3":e3,
			"e4":e4,"e5":e5,"v0":v0,"v1":v1,"v2":v2,"v3":v3,"v4":v4,"v5":v5}]

	data2 = pd.DataFrame(data, columns=["j0", "j1", "j2", "j3", "j4", "j5", "e0","e1","e2","e3","e4","e5","v0","v1","v2","v3","v4","v5"])
	print(data2)

