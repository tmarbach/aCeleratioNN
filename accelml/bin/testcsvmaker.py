import pandas as pd

def test_csv_generator(cleancsv):
    df = pd.read_csv(cleancsv)
    emptydf = pd.DataFrame(columns = df.columns)

    behaviors = df.behavior.unique()
    for behavior in behaviors:
        bdf = df.loc[df['behavior'] == behavior]
        emptydf = emptydf.append(bdf.head(15))

    return emptydf


def test_df_writer(testdf, output_location):
    testdf.to_csv(output_location, index=False)


def main():
    testr = test_csv_generator("../../../CNNworkspace/cleanPenn.csv")
    test_df_writer(testr, "../../../CNNworkspace/testdata.csv")

if __name__=="__main__":
    main()


