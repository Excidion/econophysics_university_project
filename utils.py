import os
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like # stupid fix for pandas_datareader
from pandas_datareader import data as web


DATA_SOURCE = "morningstar"
SECTOR_SOURCE = "iex-tops"


DATA_FOLDER = "stock-data"
PART_1_FOLDER = "part_1"
PART_2_FOLDER = "part_2"




def get_data(company_dictionary, start_date, end_date):
    all_data = pd.DataFrame()
    print("Interval is set from {} to {}.".format(start_date, end_date))
    print("Companies include: " + ", ".join(list(company_dictionary.values())))
    print("Time series data is taken from " + DATA_SOURCE + ".")
    print("Sector information is taken from " + SECTOR_SOURCE + ".")

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

    # time series data
    data = web.DataReader(company_ticker, DATA_SOURCE, start_date, end_date)
    data = data.reset_index()
    data["Name"] = data["Symbol"].apply(lambda x: company_dictionary[x])

    try: # sector data
        data["Sector"] = web.DataReader(company_ticker, SECTOR_SOURCE).loc["sector", 0]
    except KeyError: # should only happen for Index (eg. S&P500)
        data["Sector"] = "none"

    return data


def get_savepoint_path(company_ticker, start_date, end_date):
    return "{}{}_{}_{}.pickle".format(get_data_storage_path(),
                                      company_ticker,
                                      start_date,
                                      end_date)


def prepare_working_directory():
    paths = [get_data_storage_path(), get_part_1_path(), get_part_2_path()]

    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    for path in [p for p in paths if DATA_FOLDER not in p]: # don't remove datasets
        for file in os.listdir(path):
            os.remove(path + file)


def get_part_1_path():
    return get_working_directory_path() + PART_1_FOLDER + "/"

def get_part_2_path():
    return get_working_directory_path() + PART_2_FOLDER + "/"

def get_data_storage_path():
    return get_working_directory_path() + DATA_FOLDER +"_"+ DATA_SOURCE + "/"

def get_working_directory_path():
    return os.getcwd().replace("\\","/") + "/"
