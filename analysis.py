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
