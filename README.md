# RTDE data
This controller uses the UR's RTDE api to access the robot's data.
This api used a zero-starting timestamp and so the csv_writer in the api needed ajusting to incert the Unix timestamp so the data could be combined with other Unix timestamped data such as Robotiq's force torque data which was colled via ROS.
