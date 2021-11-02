from os import error
import pandas as pd


# I want this script to read a csv of one behavior
    # pull unique times from it
    # determine the chunks of time (consecutive)
    # average the length of time of the behavior (sum(time between start & end)/# of chunks)
    # that number * 25 should be the window size for the CNN

def average_generator(single_behavior_csv):
    #when taking in the correct csvs, header will exist already
    rdf = pd.read_csv(single_behavior_csv,low_memory=False, names=['origin_file',
                                                                    'other_origin',
                                                                    'date',
                                                                    'time',
                                                                    'cam-date',
                                                                    'cam-time',
                                                                    'behavior',
                                                                    'acc_x',
                                                                    'acc_y',
                                                                    'acc_z',
                                                                    'temp_c',
                                                                    'battery_voltage',
                                                                    'metadata'])    
    
    df = rdf[rdf.date != '0']

# Just gonna combine the 'date' and 'time' columns = datetime (this is easier to parse)
    df['date']= df['date'].str.replace('/','-')

    df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'],
                                     format = '%d-%m-%Y %H:%M:%S')
    uniquedf = df.date_time.unique()
# once coverted to datetime, take unique times (nparray)
# then make new df with just the unique times and use below code to determine chunks
# eventually, output data to a file. Not perfect, but can get us started. 
#DOESNT WORK IF DATA ISNT CLEAN aka time or date is bad. 
#Now in date_time format, code below can chunk it into groups
    dt = pd.DataFrame(uniquedf, columns = ['date_time'])


    sec = pd.Timedelta('1sec')
    breaks = dt.date_time.diff() != sec
    groups = breaks.cumsum()
    for group in dt.groupby(groups):
        count = group[1]
        print(len(count.index)) # outputs a int of the # of seconds
        


if __name__ == "__main__":
    average_generator('../../../MLSnakes/test_data/combined-training/allinvestcarc.csv')
