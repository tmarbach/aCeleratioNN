import os
import pandas as pd
import argparse


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
    df.rename(columns={'TagID':'tag_id',
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
    df= df.dropna(subset=['time', 'behavior','date'])
    df = df.loc[df['behavior'] != 'n']
    df['date']= df['date'].str.replace('/','-')
    df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'],
                                     format = '%d-%m-%Y %H:%M:%S')
                                     
    return df


def output_data(original_data, clean_csv_df, output_location):
    filename = os.path.basename(original_data)
    if output_location == False:
        clean_csv_df.to_csv('clean_'+filename, index=False)
    else:
        clean_csv_df.to_csv(output_location, index=False)

# def make_output_dir():
#     """Makes an output/ directory if it does not already exist."""
#     try:
#         os.mkdir('output')
#     except FileExistsError:
#         pass


def data_packaging(cleaned_csv_df, size):
    """
    Args:
    cleaned_csv_df -- output of accel_data_csv_cleaner, a dataframe that contains 
                        annotated and timestamped accelerometer data. 
    size -- the number of rows of data to include in each "image",
            (EX: 25 = 1 second, 5 = 1/5 second, 500 = 20 seconds)
    
    Returns:
    packaged_cnn_data -- generator class that packages the data according to the size integer,
                        the data must be accessed using a for loop.   
    """
    # Window is starting with 1/5 of a second (5 lines)
    #  This should take x rows of the df, convert to np.array (.to_numpy()) 
    #   store and repeat the process until whole df is converted to "images"
    # this will plug into the CNN

    return (cleaned_csv_df[pos:pos + size] for pos in range(0, len(cleaned_csv_df), size))


def convert_2_ndarray(packaged_data):
    for image in packaged_data:


def main():
    args = arguments()
    clean_data = accel_data_csv_cleaner(args.csv_file)
    output_data(args.csv_file, clean_data, args.output)
    # return output_data which will be an LIST of ndarrays

if __name__ == "__main__":
    main()
