import pickle
import pandas as pd
import numpy as np


def ik_predictor(x, y):

    print("Starting ik model")
    # Import the inverse kinematics model.
    with open('/home/ur10pc/Desktop/robot_data/pickle/ik_model.pkl','rb') as ik:
        ik_model = pickle.load(ik)


    #ik_model = joblib.load('/home/ur10pc/Desktop/mpc/mpc3/ik_model.pkl')

    x = x
    y = y
    z = 0.0436 # This doesn't change as the task space is a plane.

    sample = pd.DataFrame([[x, y, z]], columns=['x', 'y', 'z'])
    #print(sample)
    result = ik_model.predict(sample)
    # Trim off the unwanted features. i.e. joint positions 1 and 3 etc.
    #trimmed_results = np.delete(result, [1,3],1)
    #print(result)
    #result = [[ 1.40477544, -1.17178001,  2.48303769 ,-2.86277758 ,-1.56695952 , 2.19049311]]
    return result


if __name__=='__main__':
    results = ik_predictor(0.079684, -0.518834)
    print(results)
    print(trimmed_results)
