import os
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like # stupid fix for pandas_datareader
from pandas_datareader import data as web

DATA_SOURCE = "morningstar"

DATA_FOLDER = "stock_data"
PART_1_FOLDER = "part_1"


def get_data(company_dictionary, start_date, end_date):
    all_data = pd.DataFrame()
    print("Interval is set from {} to {}.".format(start_date, end_date))
    print("Companies include: " + ", ".join(list(company_dictionary.values())))

    for company_ticker in company_dictionary:

        savepoint_path = get_savepoint_path(company_ticker, start_date, end_date)

        if os.path.exists(savepoint_path):
            data = pd.read_pickle(savepoint_path)
            print("Loaded data from " + savepoint_path)
        else:
            data = download_data(company_ticker, start_date, end_date, company_dictionary)
            data.to_pickle(savepoint_path)
            print("Saved data to " + savepoint_path)

        all_data = pd.concat([all_data, data])

    return all_data


def download_data(company_ticker, start_date, end_date, company_dictionary):
    print("Downloading data for {}...".format(company_dictionary[company_ticker]))
    data = web.DataReader(company_ticker, DATA_SOURCE, start_date, end_date)
    data = data.reset_index()
    data["Name"] = data["Symbol"].apply(lambda x: company_dictionary[x])
    return data


def get_savepoint_path(company_ticker, start_date, end_date):
    return "{}{}/{}_{}_{}.pickle".format(get_working_directory_path(),
                                         DATA_FOLDER,
                                         company_ticker,
                                         start_date,
                                         end_date)


def prepare_working_directory():
    for folder in [DATA_FOLDER, PART_1_FOLDER]:
        if not os.path.exists(get_working_directory_path() + folder):
            os.makedirs(get_working_directory_path() + folder)

def get_part_1_path():
    return get_working_directory_path() + PART_1_FOLDER + "/"

def get_working_directory_path():
    return os.getcwd().replace("\\","/") + "/"
