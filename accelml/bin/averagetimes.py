from os import error
import pandas as pd


# I want this script to read a csv of cleaned data
    # pull unique times from it
    # determine the chunks of time (consecutive)
    # average the length of time of the behavior (sum(time between start & end)/# of chunks)
    # that number * 25 should be the window size for the CNN

def class_divider(cleancsv):
    """
    Args:
    cleanedcsv -- output of accelml-prep-csv, csv file of clean 
                        annotated and timestamped accelerometer data.     
    Returns:
    stat_dict -- dict of behavior code and the stats of # of instances
                    and length of instances EX: {'t':[4,1], 'i':[3,500]}   
    """
    stat_dict = {}
    df = pd.read_csv(cleancsv)
    behaviors = df.behavior.unique()
    for behavior in behaviors:
        bdf = df.loc[df['behavior'] == behavior]# df with one behavior
        bdf = bdf.columns = df.columns
        stats = average_generator(bdf)
        stat_dict[behavior].append(stats)
         
    return stat_dict


def average_generator(one_class_df):
    uniquedf = df.date_time.unique()
    dt = pd.DataFrame(uniquedf, columns = ['date_time'])
    sec = pd.Timedelta('1sec')
    breaks = dt.date_time.diff() != sec
    groups = breaks.cumsum()
    counts = []
    for group in dt.groupby(groups):
        count = group[1]
        instance = len(count.index) # outputs a int of the # of seconds
        counts.append(instance)
        instances = len(counts)
        average = sum(counts)/instances
    return list(instances,average)
        


if __name__ == "__main__":
    print(average_generator('../../../MLSnakes/test_data/combined-training/allinvestcarc.csv'))
