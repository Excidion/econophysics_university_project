import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from scipy import stats

# local modules
from utils import get_data, prepare_working_directory, get_part_1_path, get_part_2_path
from plots import plot_time_series_by_company, plot_time_series, plot_probability_density, plot_correlation_matrix
from analysis import *

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
                #"DIS": "Walt Disney", # already enough companies
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
    close_data = extract_per_company(raw_data, "Close", group_by="Sector")

    # overview plot
    plt = plot_time_series_by_company(raw_data, "Close")
    plt.savefig("TimeSeries_Close.pdf")
    plt.close()




    """ PART 1 """
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
    for scale_method in [["linear","linear"], ["linear","log"], ["log","log"]]:
        for company_name in COMPANY_DICT.values():
            for dataset in log_returns:
                plt = plot_probability_density(data = log_returns[dataset][company_name],
                                               scale_method = scale_method)
                plt.gca().get_lines()[-1].set_label(dataset) # re-label based on dataset

            # edit existing colors and replace with fixed order
            colors = ["red", "indigo", "blue"]
            for i, line in enumerate(plt.gca().get_lines()):
                line.set_color(colors[i])

            plt.legend()
            plt.savefig("{}{}_log-return-densities_{}.pdf".format(path, company_name, "X".join(scale_method)))
            plt.close()




    """ TASK 3 """
    for dataset in log_returns:
        for company_name in CHOSEN_COMPANIES:
            plt = plot_probability_density(data = log_returns[dataset][company_name],
                                           scale_method = ["linear", "log"],
                                           fit_gauss = True)
            plt.savefig("{}{}_{}-log-return-density.pdf".format(path, company_name, dataset))
            plt.close()




    """ TASK 4 """
    fake_close_data = generate_fake_close_data(chosen_company_data)
    fake_log_returns = {"monthly":  compute_log_returns(fake_close_data, 21),
                        "biannual": compute_log_returns(fake_close_data, 126)}

    for dataset in fake_log_returns:
        for company_name in fake_log_returns[dataset].keys():
            plt = plot_probability_density(data = fake_log_returns[dataset][company_name],
                                           scale_method = ["linear", "log"],
                                           fit_gauss = True)
            plt.savefig("{}{}_{}-log-return-density.pdf".format(path, company_name, dataset))
            plt.close()




    """ TASK 5 """
    volatility = compute_volatility(close_data, range(1,253))
    plt = plot_time_series(volatility, "Volatility", ["log", "log"])
    x = np.linspace(1, 253, 253)
    plt.plot(x, x, label="WTF", color="pink") # reference line TODO find useful slope
    plt.legend()
    plt.savefig(path + "volatility.pdf")
    plt.close()




    """ PART 2 """
    """ TASK 1 """
    path = get_part_2_path()
    correlation_matrices = compute_correlation_matrices(close_data)
