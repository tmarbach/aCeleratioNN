#1. take the csv, lowercase and underscore the column names, separate columns for the index#, label source_file
 #   1a. ignore any data without a time signature
#2. convert the na to 0 and pull out all the annotated data (behavior)
#3. output a csv of all annotated data
#4. create csvs of each class of annotated data
#future prep
#1. cluster data into input chunks for the cnn
#2. experiment with different size clusters

import pandas as pd
import argparse

def arguments():
    parser = argparse.ArgumentParser(prog='accelml_prep_csv',
      description="Clean and prepare accelerometer csv data for CNN input by rounding to 3 decimal places\
       and removing blank timestamps",\
        epilog="Columns of accelerometer data must be arranged:'tag_id', 'date', 'time', 'camera_date', 'camera_time', \
                  'behavior', 'acc_x', 'acc_y', 'acc_z', 'temp_c', 'battery_voltage', 'metadata'")
    parser.add_argument("file", type=argparse.FileType('r'), help = "input the path to the csv file of accelerometer data that\
                                       requires cleaning")
    return parser.parse_args()



def accel_csv_cleaner(accel_csv):
    rawacceldf = pd.read_csv(accel_csv)
    rawacceldf.columns = ['tag_id', 'date', 'time', 'camera_date', 'camera_time', \
                  'behavior', 'acc_x', 'acc_y', 'acc_z', 'temp_c', 'battery_voltage', 'metadata']
    roundacceldf = rawacceldf.round({'acc_x': 3, 'acc_y': 3, 'acc_z': 3})
    allannoted_acceldf = roundacceldf.loc[roundacceldf['behavior'] != '']
    allanno_withtimeacceldf = allannoted_acceldf.loc[allannoted_acceldf['time'] != '']
    allclasses_acceldf = allanno_withtimeacceldf.loc[allanno_withtimeacceldf['behavior'] != 'n']
    filetitle = 'cleaned_'+ str(accel_csv)
    allclasses_acceldf.to_csv(filetitle)

def make_output_dir():
    """Makes an output/ directory if it does not already exist."""
    try:
        os.mkdir('output')
    except FileExistsError:
        pass


def main():
    args = arguments()
    accel_csv_cleaner(args.file)

if __name__ == "__main__":
    main()
