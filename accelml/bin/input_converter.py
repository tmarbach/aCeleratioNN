import numpy as np
import pandas as pd

def window_maker(cleancsv):
    df = pd.read_csv(cleancsv)
    groups = df.groupby(['time'])
    for group in groups:
        time_df = group[1]
        #minidf = time_df[['behavior', 'acc_x',  'acc_y',  'acc_z', 'date_time']]
        nparray = time_df[['acc_x',  'acc_y',  'acc_z']].to_numpy()

        print(nparray.transpose().shape)

    #group[1] = df -> behavior, xyz -> convert to np.array & one-hot


    #return groups
    #print(groups)


def main():
    window_maker("../../../CNNworkspace/millicleantestdata.csv")

if __name__=="__main__":
    main()
