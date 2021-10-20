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
    #df.rename() for renaming dictionary. 
    #df.rename(columns={"A": "a", "B": "b", "C": "c"}, errors="raise")
        # above line raises erro if the key in the name dic does not exist.
       # check for correct number of columns, then check for correct column titles
       #original titles = TagID,Date,Time,Camera date,Camera time,Behavior,accX,accY,
       # accZ,Temp. (?C),Battery Voltage (V),Metadata
    df.columns = ['tag_id', 'date', 'time', 'camera_date', 'camera_time', \
                  'behavior', 'acc_x', 'acc_y', 'acc_z', 'temp_c', 'battery_voltage', 'metadata']
    df= df.dropna(subset=['time', 'behavior'])
    #package into a separate func
    #allannoted_acceldf = roundacceldf.loc[roundacceldf['behavior'] != 0]
    #allanno_withtimeacceldf = allannoted_acceldf.loc[allannoted_acceldf['time'] != 0]
    cleaned_df = df.loc[df['behavior'] != 'n']
    return cleaned_df
    #cleaned_df.to_csv(output_location, index=False)


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
    size -- the number of rows of data to include in each "image"
    
    Returns:
    packaged_cnn_data -- clustered data points representing a window of time and movement
                        The "images" the CNN will label.  
    """
    # Window is starting with 1/5 of a second (5 lines)
    #  This should take x rows of the df, convert to np.array (.to_numpy()) 
    #   store and repeat the process until whole df is converted to "images"
    # this will plug into the CNN
    return (cleaned_csv_df[pos:pos + size] for pos in xrange(0, len(cleaned_csv_df), size))



def main():
    args = arguments()
    clean_data = accel_data_csv_cleaner(args.csv_file)
    output_data(args.csv_file, clean_data, args.output)

if __name__ == "__main__":
    main()
