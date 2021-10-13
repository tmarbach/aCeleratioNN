#1. take the csv, lowercase and underscore the column names, separate columns for the index#, label source_file
 #   1a. ignore any data without a time signature
#2. convert the na to 0 and pull out all the annotated data (behavior)
#3. output a csv of all annotated data
#4. create csvs of each class of annotated data
#future prep
#1. cluster data into input chunks for the cnn
#2. experiment with different size clusters

import pandas as pd


parser = argparse.ArgumentParser(
  description="Clean and prepare accelometer csv data for CNN input by rounding to 3 decimal places\
   and removing blank timestamps")

def accel_csv_cleaner(accel_csv):
    rawacceldf = pd.read_csv(accel_csv)
    no_na_acceldf = rawacceldf.fillna(0)
    allannoted_acceldf = no_na_acceldf.loc[no_na_acceldf['Behavior'] != 0]
    allclasses_acceldf = allannoted_acceldf.loc[allannoted_acceldf['Behavior'] != 'n']
    allannoted_acceldf.to_csv('obsPen11FullR1_non.csv')

def make_output_dir():
    """Makes an output/ directory if it does not already exist."""
    try:
        os.mkdir('output')
    except FileExistsError:
        pass
