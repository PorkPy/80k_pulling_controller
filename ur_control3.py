#http://www.zacobria.com/universal-robots-zacobria-forum-hints-tips-how-to/x-y-and-z-position/
#Echo client program
import socket
import command2
import ur_data2 as ur

import time
HOST = "123.124.125.11"   # The remote host
PORT = 30002             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(b"set_analog_inputrange(0, 0)" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_analog_inputrange(1, 0)" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_analog_outputdomain(0, 0)" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_analog_outputdomain(1, 0)" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_tool_voltage(24)" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_runstate_outputs([])" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_payload(0.0)" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"set_gravity([0.0, 0.0, 9.82])" + "\n".encode('ascii'))
data = s.recv(1024)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (b"get_actual_tcp_pose" + "\n".encode('ascii'))
bob = s.recv(1024)
s.close()

print("hello")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


nextmoves = command2.robotmove_intervals()


i = 1
bob = len(nextmoves)
# s.send("set_gravity([0.0, 0.0, 9.82])" + "\n")
# s.send("set_payload(1.8, [0,0,.3])" + "\n")
for i in range(len(nextmoves)):

	[x,y,z,Rx,Ry,Rz] = nextmoves[i]
	nextmove = [x,y,z,Rx,Ry,Rz]
	move =(("def myProg():" + "\n" + \
		"force_mode_set_damping(0.01)" + "\n" + \
		"set_gravity([0.0, 0.0, 9.82])" + "\n" + \
		"set_payload(1.8, [0,0,.3])" + "\n" + \
		"force_mode(tool_pose(), [0, 0, 0, 0, 0, 1], [0.0, 0.0, 0.0, 0.0, 0.0, -0.9], 2, [0.1, 0.1, 0.1, 20.0, 20.0, 60.0])" + "\n" + \
		"movej(p%s,a=0.2,v=0.2)" % nextmove + "\n" + "end" + "\n" ))

		# impedance =-0.9

	s.send(move.encode())
	time.sleep(2.5)


	print(("Remaining Moves: ", bob))
	bob -= 1
	time.sleep(0.2)

s.close()


print("Finished")
import matplotlib.pyplot as plt
plt.close("all")
