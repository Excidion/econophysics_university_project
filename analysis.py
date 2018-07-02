import pandas as pd
import numpy as np


def extract_per_company(data, key, group_by=None):
    key_data = pd.DataFrame(index=data["Date"].sort_values().unique())
    for company_name in data["Name"].unique():
        company_data = data[data["Name"] == company_name]
        company_key = pd.DataFrame(company_data[["Date", key]]).set_index("Date")
        company_key = company_key.rename(columns={key: company_name})
        key_data = pd.concat([key_data, company_key], axis=1)

    if group_by == None:
        return key_data

    groups = data[group_by].unique()
    names_by_group = []
    for group in groups: # loop over groups
        names_in_group = data[data[group_by] == group]["Name"].unique()
        for name in names_in_group:
            names_by_group.append(name) # add to list ordered by group

    key_data = key_data[names_by_group] # reorder names by list
    return key_data


def compute_log_returns(close_data, delta_t):
    log_returns = pd.DataFrame()
    for company_name in close_data.keys():
        l_r = np.log(close_data[company_name].shift(-delta_t) / close_data[company_name])
        log_returns = pd.concat([log_returns, l_r], axis=1)

    return log_returns


def generate_fake_close_data(data):
    close_data = extract_per_company(data, "Close")
    log_returns = compute_log_returns(close_data, 1)

    fake_close_data = pd.DataFrame()
    for company_name in data["Name"].unique():
        company_data = data[data["Name"] == company_name]
        starting_value = company_data.loc[company_data["Date"].idxmin(),"Close"]

        shuffled_log_returns = log_returns[company_name].sample(frac=1).reset_index(drop=True)
        time_series = np.cumsum(shuffled_log_returns).shift(1).fillna(0)
        time_series += np.log(starting_value)
        time_series.index = log_returns[company_name].index

        fake_close_data["Generated-from-" + company_name] = time_series

    return fake_close_data


def compute_volatility(close_data, timesteps):
    volatility = pd.DataFrame(columns=close_data.keys(), index=timesteps)
    volatility.index.name = r"$\Delta t$"
    for deltaT in timesteps:
        l_r = compute_log_returns(close_data, deltaT)
        for company_name in l_r.keys():
            volatility.loc[deltaT, company_name] = l_r[company_name].var()

    return volatility


def compute_correlation_matrices(close_data):
    quarter_ends = close_data[close_data.index.is_quarter_end].index

    list_of_CM = []
    for i in range(len(quarter_ends)-1):
        quarter_close_data = close_data[(close_data.index <= quarter_ends[i+1]) &
                                        (close_data.index > quarter_ends[i])]
        correlation_matrix = quarter_close_data.corr()
        list_of_CM.append(correlation_matrix)

    return pd.concat(list_of_CM, keys=quarter_ends[1:], axis=0)


def compute_mean_correlation(correlation_matrices):
    mean_correlation = pd.DataFrame(index = correlation_matrices.index.levels[0],
                                    columns = ["Mean Correlation"])

    for date in correlation_matrices.index.levels[0]:
        correlation_matrix = np.array(correlation_matrices.loc[date])
        np.fill_diagonal(correlation_matrix, np.NAN) # no diagonal elements
        mean_correlation.loc[date] = np.nanmean(correlation_matrix)

    return mean_correlation


def find_correlation_extrema(correlation_matrix):
    nan_diagonal = np.zeros_like(correlation_matrix)
    np.fill_diagonal(nan_diagonal, np.NAN) # create diagonal NAN matrix
    cleaned_matrix = correlation_matrix - nan_diagonal # substraction with NAN returns NAN
    correlation_order = cleaned_matrix.abs().unstack().sort_values().dropna()

    most_correlated = list(correlation_order.index[-1])
    least_correlated = list(correlation_order.index[0])
    return most_correlated, least_correlated
