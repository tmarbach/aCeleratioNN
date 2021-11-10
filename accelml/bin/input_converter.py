import numpy as np
import pandas as pd


# will eventually also convert the overall behavior to one-hot and 
# add its label to the same spot on another array.
def window_maker(cleancsv):
    df = pd.read_csv(cleancsv)
    groups = df.groupby(['time'])
    print(len(groups))
    arraylist = []
    for group in groups:
        time_df = group[1]
        nparray = time_df[['acc_x',  'acc_y',  'acc_z']].to_numpy()
        truearray = nparray.transpose()
        arraylist.append(truearray)
    stacked = np.stack((arraylist), axis=0)

    print(stacked)


def main():
    window_maker("../../../CNNworkspace/fullsectestdata.csv")

if __name__=="__main__":
    main()
