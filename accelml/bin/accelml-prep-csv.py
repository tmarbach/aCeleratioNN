#1. take the csv, lowercase and underscore the column names, separate columns for the index#, label source_file
 #   1a. ignore any data without a time signature
#2. convert the na to 0 and pull out all the annotated data (behavior)
#3. output a csv of all annotated data
#4. create csvs of each class of annotated data
#future prep
#1. cluster data into input chunks for the cnn
#2. experiment with different size clusters
import os
import pandas as pd
import argparse

def arguments():
    parser = argparse.ArgumentParser(prog='accelml_prep_csv', 
            description="Clean and prepare accelerometer csv data for CNN input by rounding to\
                         3 decimal places and removing blank timestamps",
            epilog="Columns of accelerometer data must be arranged:'tag_id', 'date', 'time', 'camera_date', 'camera_time', \
                  'behavior', 'acc_x', 'acc_y', 'acc_z', 'temp_c', 'battery_voltage', 'metadata'")
    parser.add_argument(
            "csv_file",
            type=str,
            help = "input the path to the csv file of accelerometer data that requires cleaning")
    parser.add_argument("-o", "--output", help="Directs the output to a name of your choice")
    return parser.parse_args()



def accel_data_csv_cleaner(accel_data_csv, output_location):
    rawacceldf = pd.read_csv(accel_data_csv,low_memory=False)
    rawacceldf.columns = ['tag_id', 'date', 'time', 'camera_date', 'camera_time', \
                  'behavior', 'acc_x', 'acc_y', 'acc_z', 'temp_c', 'battery_voltage', 'metadata']
    roundacceldf = rawacceldf.round({'acc_x': 3, 'acc_y': 3, 'acc_z': 3})
    roundacceldf = roundacceldf.fillna(0)
    allannoted_acceldf = roundacceldf.loc[roundacceldf['behavior'] != 0]
    allanno_withtimeacceldf = allannoted_acceldf.loc[allannoted_acceldf['time'] != 0]
    allclasses_acceldf = allanno_withtimeacceldf.loc[allanno_withtimeacceldf['behavior'] != 'n']
    allclasses_acceldf.to_csv(output_location, index=False)

# def make_output_dir():
#     """Makes an output/ directory if it does not already exist."""
#     try:
#         os.mkdir('output')
#     except FileExistsError:
#         pass


def main():
    args = arguments()
    accel_data_csv_cleaner(args.csv_file, args.output)

if __name__ == "__main__":
    main()
