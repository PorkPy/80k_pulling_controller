







#!/home/ur10pc/anaconda3/bin/python

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive
import pickle


def model(j0, j2, j4, j5):
          #e0, e1, e2, e3, e4, e5,\
          #v0, v2, v4, v5):

    print("Starting 80k model!!!!!")
    # Construct dummy data frame to house
    dataw = pd.DataFrame([[ j0, j2, j4, j5]], #
                            #e0, e1, e2, e3, e4, e5,\
                            #v0, v2, v4, v5]],
                columns=["joint_0",    "joint_2", "joint_4", "joint_5"])
                #"effot_joint_0",   "effot_joint_1",   "effot_joint_2",   "effot_joint_3",   "effot_joint_4",   "effot_joint_5",
                #"vel_joint_0", "vel_joint_2", "vel_joint_4", "vel_joint_5"])

    # # Data has 'no' added synthetic data- previous controller did.
    # data0 = pd.read_csv('/home/ur10pc/Desktop/robot_data2/80k_data/data_sample.csv', delimiter=',')
    # data0 = pd.DataFrame(data0)

    # print(data0)
    # #data0.drop(data0.tail(1).index,inplace=True) # drop last n rows

    # # Append new data-point to existing data for regularisation
    # data0 = data0.append(dataw, ignore_index = True, sort=False)
    # print(data0)
    # print(dataw)

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



    # # Load Saved Model
    with open('/home/ur10pc/Desktop/robot_data/pickle/80k_model2.pkl','rb') as f:
        pipeline = pickle.load(f)


    # joblib.dump(pipeline, 'bigmodel.pkl')


    #pipeline = joblib.load('/home/ur10pc/Desktop/mpc/mpc3/regressor_model.pkl')

     # Make New Prediction On New datapoint
    sample = dataw#.drop('force', axis=1)#features[-1:]
    #sample = sample[-1:]
    result = pipeline.predict(sample)
    result = result[0]
    print('hello',result)


    #print(result)
    return result


if __name__ == "__main__":

    model(1.607, 2.507,   -1.567,  2.801) #,  -0.105 , -4.655  ,-2.002 , -0.846,  0.608  , -0.038 , -0.000  ,0.000  , 0.000   ,0.000  ) #force = 1.297

# ac -pr
# 42 -34
# 0.1-13



