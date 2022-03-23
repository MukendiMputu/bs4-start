import pandas as pd


# Read the billets of interest out the Excel/CSV file and return a dictionary
def get_billets_infos(file):
    data = {}
    # with open(file) as xlsFile:
    data_frames = pd.read_csv(file)
    for row in data_frames.values:
        data[row[0]] = row[1]
    return data
