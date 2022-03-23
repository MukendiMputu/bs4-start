import pandas as pd


def save_as_csv(file_name, dictionary):
    data_frame = get_data_frame(dictionary)
    data_frame.to_csv(file_name)


def save_as_json(file_name, dictionary):
    data_frame = get_data_frame(dictionary)
    data_frame.to_json(file_name)


def get_data_frame(dictionary):
    return pd.DataFrame(dictionary)
