import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity


def extract_per_company(data, key):
    key_data = pd.DataFrame(index=data["Date"].sort_values().unique())
    for company_name in data["Name"].unique():
        company_data = data[data["Name"] == company_name]
        company_key = pd.DataFrame(company_data[["Date", key]]).set_index("Date")
        company_key = company_key.rename(columns={key: company_name})
        key_data = pd.concat([key_data, company_key], axis=1)

    return key_data


def compute_log_returns(close_data, delta_t):
    log_returns = pd.DataFrame()
    for company_name in close_data.keys():
        l_r = np.log(close_data[company_name].shift(-delta_t) / close_data[company_name])
        log_returns = pd.concat([log_returns, l_r], axis=1)

    return log_returns






# unused
def compute_probability_density_function(data, density_function):
    kernel_density_estimation =  KernelDensity(kernel=density_function)
    data = np.array(data.dropna()).reshape(-1,1)
    kernel_density_estimation.fit(data)
    return kernel_density_estimation


def compute_boundaries(kde, data, inv_stepsize=100, thresh=10**-3):
    max = data.max()
    min = data.min()
    mean = data.mean()

    # upper border
    stepwidth = abs(max - mean)/inv_stepsize
    upper = mean
    while np.exp(kde.score_samples(upper)) > thresh:
        upper += stepwidth

    # lower border
    stepwidth = abs(min - mean)/inv_stepsize
    lower = mean
    while np.exp(kde.score_samples(lower)) > thresh:
        lower -= stepwidth

    return lower, upper



# unused in main, useful for data exploration
def get_data_dimensions(data):
    data_dims = {}
    for company_name in data["Name"].unique():
        dim = data[data["Name"] == company_name].shape
        data_dims[company_name] = dim

    return data_dims


def get_missing_dates(data):
    all_dates = data["Date"].sort_values().unique()
    missing_dates_dict = {}

    for company_name in data["Name"].unique():
        company_dates = data[data["Name"] == company_name]["Date"].unique()
        missing_dates_index = np.logical_not(np.isin(all_dates, company_dates))
        missing_dates = all_dates[missing_dates_index]

        missing_dates_dict[company_name] = missing_dates

    return missing_dates_dict
