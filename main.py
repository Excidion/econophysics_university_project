import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from io import BytesIO
import imageio

# local modules
from utils import get_data, prepare_working_directory, get_part_1_path, get_part_2_path
from plots import save_plot
from plots import plot_time_series_by_company, plot_time_series, plot_probability_density # part 1
from plots import plot_correlation_matrix, plot_correlation_time_series # part 2
from analysis import * # wildcard imports are bad practice, but here it does no harm

# options & parameters
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

                "SPX": "S&P500-Index"}


CHOSEN_COMPANIES = ["FedEx", "Coca-Cola"]




if __name__ == "__main__":

    """ SETUP """
    prepare_working_directory()
    raw_data = get_data(COMPANY_DICT, START_DATE, END_DATE)
    close_data = extract_per_company(raw_data, "Close", group_by="Sector")

    # overview plot
    plt = plot_time_series_by_company(raw_data, "Close")
    save_plot(plt, "TimeSeries_Close")




    """ PART 1 """
    path = get_part_1_path()

    """ TASK 1 """
    # computation
    log_returns = {"daily": compute_log_returns(close_data, 1),
                   "monthly":  compute_log_returns(close_data, 21),
                   "biannual": compute_log_returns(close_data, 126)}

    chosen_company_data = raw_data[raw_data["Name"].isin(CHOSEN_COMPANIES)]

    # price
    plt = plot_time_series_by_company(chosen_company_data, "Close")
    save_plot(plt, path + "timeseries_price_" + "-".join(CHOSEN_COMPANIES))

    # log price
    plt = plot_time_series_by_company(chosen_company_data, "Close", "log")
    save_plot(plt, path + "timeseries_log-price_" + "-".join(CHOSEN_COMPANIES))

    # log returns
    plt = plot_time_series(log_returns["daily"][CHOSEN_COMPANIES], "Logarithmic Daily Returns")
    save_plot(plt, path + "timeseries_daily-log-returns_" + "-".join(CHOSEN_COMPANIES))




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

            save_plot(plt, "{}log-return-densities_{}_{}".format(path, company_name, "X".join(scale_method)))




    """ TASK 3 """
    for dataset in log_returns:
        for company_name in CHOSEN_COMPANIES:
            plt = plot_probability_density(data = log_returns[dataset][company_name],
                                           scale_method = ["linear", "log"],
                                           fit_gauss = True)
            save_plot(plt, "{}{}_{}-log-return-density".format(path, company_name, dataset))




    """ TASK 4 """
    fake_close_data = generate_fake_close_data(chosen_company_data)
    fake_log_returns = {"monthly":  compute_log_returns(fake_close_data, 21),
                        "biannual": compute_log_returns(fake_close_data, 126)}

    for dataset in fake_log_returns:
        for company_name in fake_log_returns[dataset].keys():
            plt = plot_probability_density(data = fake_log_returns[dataset][company_name],
                                           scale_method = ["linear", "log"],
                                           fit_gauss = True)
            save_plot(plt, "{}{}_{}-log-return-density".format(path, company_name, dataset))




    """ TASK 5 """
    volatility = compute_volatility(close_data, range(1,253))
    plt = plot_time_series(volatility, "Volatility", ["log", "log"])
    x = np.linspace(1, 253, 253)
    plt.plot(x, x, label="WTF", color="pink") # reference line TODO find useful slope
    plt.legend()
    save_plot(plt, path + "volatility")




    """ PART 2 """
    """ TASK 1 """
    path = get_part_2_path()
    correlation_matrices = compute_correlation_matrices(close_data.drop("S&P500-Index",axis=1))


    """ TASK 2 """
    # to find interesting matrices plot all single matrices and generate animation
    video = imageio.get_writer(path + "animated_correlation-matrices.gif", mode='I', fps=4)

    for date in correlation_matrices.index.levels[0]:

        correlation_matrix = correlation_matrices.loc[date]
        plt = plot_correlation_matrix(correlation_matrix, "{} Q{}".format(date.year, date.quarter))

        virtual_file = BytesIO()
        plt.savefig(virtual_file) # convert to byte string
        virtual_file.seek(0) # go to start of byte string
        video.append_data(imageio.imread(virtual_file)) # read bytestring and add as frame

        save_plot(plt, "{}correlation-matrix_{}Q{}".format(path, date.year, date.quarter))

    video.close()


    # total correlation matrix
    absolute_correlation_matrix = close_data.drop("S&P500-Index", axis=1).corr()
    plt = plot_correlation_matrix(absolute_correlation_matrix)
    save_plot(plt, path + "absolute_correlation-matrix")


    # time series of mean correlation
    mean_correlation = compute_mean_correlation(correlation_matrices)
    plt = plot_time_series(mean_correlation, "Mean Correlation")
    save_plot(plt, path + "mean_correlation")


    # find strongly (un-)correlated companies
    most_correlated, least_correlated = find_correlation_extrema(absolute_correlation_matrix)
    plt = plot_correlation_time_series(correlation_matrices, [most_correlated, least_correlated])
    save_plot(plt, path + "correlation_time-series")
