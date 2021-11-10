import os
import pandas as pd
import argparse
from datetime import datetime
from datetime import timedelta


def arguments():
    parser = argparse.ArgumentParser(
            prog='accelml_prep_csv', 
            description="Clean and prepare accelerometer csv data for CNN input by rounding\
                        to 3 decimal places and removing blank timestamps",\
            epilog="Columns of accelerometer data must be arranged:'tag_id', 'date', 'time',\
                    'camera_date', 'camera_time', 'behavior', 'acc_x', 'acc_y', 'acc_z', 'temp_c',\
                    'battery_voltage', 'metadata'"
                 )
    parser.add_argument(
            "csv_file",
            type=str,
            help = "input the path to the csv file of accelerometer data that requires cleaning")
    parser.add_argument(
            "-o",
            "--output",
            help="Directs the output to a name of your choice",
            default=False)
    return parser.parse_args()



def accel_data_csv_cleaner(accel_data_csv):
    #rename variables
    df = pd.read_csv(accel_data_csv,low_memory=False)
    #check column names if they fit correctly and add an error if they don't
    df = df.rename(columns={'TagID':'tag_id',
                            'Date':'date',
                            'Time':'time',
                            'Camera date':'camera_date',
                            'Camera time':'camera_time',
                            'Behavior':'behavior',
                            'accX':'acc_x',
                            'accY':'acc_y',
                            'accZ':'acc_z',
                            'Temp. (?C)':'temp_c',
                            'Battery Voltage (V)':'battery_voltage',
                            'Metadata':'metadata'},
                            errors="raise")
    cols_at_front = ['behavior',
                     'acc_x', 
                     'acc_y', 
                     'acc_z']
    df = df[[c for c in cols_at_front if c in df]+
            [c for c in df if c not in cols_at_front]]
                   # check for correct number of columns, then check for correct column titles
    # need to check if the first 1 or 2 time signatures (sampling) have 25 entries, if not, kick an error
    df= df.dropna(subset=['behavior','time'])
    df = df.loc[df['behavior'] != 'n']
    df = df.loc[df['behavior'] != 'h']
    #
    #
    df['date']= df['date'].str.replace('/','-')
    df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'],
                                     format = '%d-%m-%Y %H:%M:%S')
    df["annotation_group_step"] = df.groupby("date_time").cumcount()

    df["date_time"] = (
                    df.groupby("date_time")
                    .apply(lambda x: x.date_time
                        + (timedelta(milliseconds=(1000 / x.shape[0])) * x.annotation_group_step)
                        )
                        .reset_index(drop=True)
                    )

    return df


def output_data(original_data, clean_csv_df, output_location):
    filename = os.path.basename(original_data)
    if output_location == False:
        clean_csv_df.to_csv('clean_'+filename, index=False)
    else:
        clean_csv_df.to_csv(output_location, index=False)




def data_packaging(cleaned_csv_df, rejecttimes):
    """
    Args:
    cleaned_csv_df -- output of accel_data_csv_cleaner, a dataframe that contains 
                        annotated and timestamped accelerometer data. 
    rejecttimes -- empty list
    
    Returns:
    polished_csv_df -- dataframe with every timestamp accounting for 25 rows. Ready for CNN. 
    rejecttimes -- list object with timestamps of times with fewer than 25 entries.  
    """
    groups = cleaned_csv_df.groupby(['time'])
    polished_csv_df = pd.DataFrame(columns = cleaned_csv_df.columns)
    if set(groups) > 1:
        for group in groups:
            if group.size != 25:
                pass 
            else:
                polished_csv_df = polished_csv_df.append(group[1])

    else:
        polished_csv_df == cleaned_csv_df 
        rejecttimes.append('No rejected timestamps')

    return polished_csv_df, rejecttimes


# def convert_2_ndarray(packaged_data):
#     for image in packaged_data:


def main():
    bad_times = []
    args = arguments()
    clean_data = accel_data_csv_cleaner(args.csv_file)
    data_packaging(clean_data,bad_times)
    output_data(args.csv_file, clean_data, args.output)
    # return output_data which will be a csv file of the cleaned
    # and reorganized data, other scripts will work with it from there.

if __name__ == "__main__":
    main()
