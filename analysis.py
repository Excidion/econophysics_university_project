import pandas as pd
import numpy as np


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


def generate_fake_close_data(data):
    close_data = extract_per_company(data, "Close")
    log_returns = compute_log_returns(close_data, 1)

    fake_close_data = pd.DataFrame()
    for company_name in data["Name"].unique():
        company_data = data[data["Name"] == company_name]
        starting_value = company_data[company_data["Date"] == company_data["Date"].min()]["Close"][0]

        shuffled_log_returns = log_returns[company_name].sample(frac=1).reset_index(drop=True)
        time_series = np.cumsum(shuffled_log_returns).shift(1).fillna(0)
        time_series += np.log(starting_value)
        time_series.index = log_returns[company_name].index

        fake_close_data["Generated from " + company_name] = time_series

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
