import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from scipy import stats

# local modules
from utils import get_data, prepare_working_directory, get_part_1_path
from plots import plot_time_series_by_company, plot_time_series, plot_probability_density
from analysis import extract_per_company, compute_log_returns


# setup & options
TODAY = datetime.date(year=2018, month=6, day=4) #datetime.date.today()
START_DATE = TODAY.replace(year = TODAY.year-25)
END_DATE = TODAY

COMPANY_DICT = {"AMD": "AMD",
                "AAPL": "Apple",
                "IBM": "IBM",
                "KO": "Coca-Cola",
                "MCD": "McDonald's",
                "HD": "Home Depot",
                "TXN": "Texas Instruments",
                "FDX": "FedEx",
                "DIS": "Walt Disney",
                "PX": "Praxair",
                "PEP": "Pepsi",

                # excluded because not enough data points
                #"DDAIF": "Daimler",
                #"BP": "British Petroleum",
                #"UPS": "UPS",
                #"LMT": "Lockheed Martin",
                #"GS": "Goldman Sachs",
                #"BAYRY": "Bayer",
                #"SIEGY": "Siemens",
                #"NVDA": "Nvidia",

                # excluded for other reasons
                #"PG": "Procter & Gamble", # blue similar to Pepsi
                #"MSFT": "Microsoft", # 4 colors wtf MS
                #"MMM": "3M", # red similar to coca cola
                #"GE": "General Electric", # blue similar to IBM
                #"DE": "John Deere", # green similar to AMD

                "SPX": "S&P500-Index"}


CHOSEN_COMPANIES = ["FedEx", "Coca-Cola"]




if __name__ == "__main__":

    """ PREPARATION """
    prepare_working_directory()
    path = get_part_1_path()

    raw_data = get_data(COMPANY_DICT, START_DATE, END_DATE)
    close_data = extract_per_company(raw_data, "Close")

    # overview plot
    plt = plot_time_series_by_company(raw_data, "Close")
    plt.savefig("TimeSeries_Close.pdf")
    plt.close()




    """ TASK 1 """
    # computation
    log_returns = {"daily": compute_log_returns(close_data, 1),
                   "monthly":  compute_log_returns(close_data, 21),
                   "biannual": compute_log_returns(close_data, 126)}

    chosen_company_data = raw_data[raw_data["Name"].isin(CHOSEN_COMPANIES)]

    # price
    plt = plot_time_series_by_company(chosen_company_data, "Close")
    plt.savefig(path + "price.pdf")
    plt.close()

    # log price
    plt = plot_time_series_by_company(chosen_company_data, "Close", "log")
    plt.savefig(path + "log_price.pdf")
    plt.close()

    # log returns
    plt = plot_time_series(log_returns["daily"][CHOSEN_COMPANIES], "Logarithmic Returns")
    plt.savefig(path + "daily_log_returns.pdf")
    plt.close()




    """ TASK 2 """
    # TODO




    """ TASK 3 """
    # TODO make log plots
    for dataset in log_returns:
        for company_name in CHOSEN_COMPANIES:
            plt = plot_probability_density(log_returns[dataset][company_name], 100)
            plt.savefig("{}{}_{}-log-return-density.pdf".format(path, company_name, dataset))
            plt.close()




    """ TASK 4 """
    # TODO




    """ TASK 5 """
    # TODO
