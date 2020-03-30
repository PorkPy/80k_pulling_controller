import pickle
import pandas as pd
import numpy as np


def ik_predictor(x, y):

    print("Starting ik model")
    # Import the inverse kinematics model.
    with open('/home/ur10pc/Desktop/robot_data/pickle/ik_model.pkl','rb') as ik:
        ik_model = pickle.load(ik)

    x = x
    y = y
    z = 0.0436 # This doesn't change as the task space is a plane.

    sample = pd.DataFrame([[x, y, z]], columns=['x', 'y', 'z'])
    #print(sample)
    result = ik_model.predict(sample)
    # Trim off the unwanted features. i.e. joint positions 1 and 3 etc.
    trimmed_results = np.delete(result, [1,3],1)
    return(trimmed_results)


if __name__=='__main__':
    results = ik_predictor(0.079684, -0.518834)
    print(result)
    print(trimmed_results)
