import pandas as pd
import numpy as np
import csv


def pull_window(df, window_size):
    """
    Input: 
    df -- dataframe of cleaned input data, likely from a csv
    window_size -- number of rows of data to convert to 1 row for AcceleRater
    Output:
    windows -- list of lists of accel data (EX:[x,y,z,...,x,y,z,class_label])
    """
    if window_size > df.shape[0]:
        raise ValueError('Window larger than data given')
    windows = []
    number_of_rows_minus_window = df.shape[0] - window_size + 1
    for i in range(0, number_of_rows_minus_window, window_size):
#        numberofrowsminuswindow = df.shape[0] - window_length+1
        window = df[i:i+window_size]
        if len(set(window.behavior)) != 1:
            continue
        if len(set(np.ediff1d(window.input_index))) != 1:
             continue
        windows.append(window)
    return windows


def construct_train_test(windows):
    """
    Input:
        windows -- list of dataframes of all one class 
    Output:
        total_data -- list of lists of flattened accel datawith class label a the end
    """
    positions = ['acc_x', 'acc_y', 'acc_z']
    total_data = [] 
    for window in windows:
        windowdata = window[positions].to_numpy()
        xlist = windowdata.tolist()
        flat_list = [item for sublist in xlist for item in sublist]
        flat_list.append(window['behavior'].iloc[0])
        total_data.append(flat_list)
        
    return total_data


def main():
    #WILL need to altered to initially accept a df
    df = pd.read_csv("~/CNNworkspace/testdataDEC/nomil_cleanstitch.csv")
    windows = pull_window(df, 25)
    all_data = construct_train_test(windows)
    with open("flattened_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)




if __name__ == "__main__":
    main()