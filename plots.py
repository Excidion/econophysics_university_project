import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# based on company logos
COMPANY_COLORS = {"Apple": "#666666",
                  "IBM": "#1971C2",
                  "Microsoft": "#7FBA00", #"#F25022",
                  "3M": "#EF1429",
                  "General Electric": "#3874BA",
                  "British Petroleum": "#0E8B42",
                  "Procter & Gamble": "#0039B0",
                  "Coca-Cola": "#F40002",
                  "McDonald's": "#FFCD00",
                  "Walt Disney": "#000000",
                  "Siemens": "#00A2B5",
                  "Goldman Sachs": "#64AAF0",
                  "Daimler": "#c0c0c0",
                  "Bayer": "#55D500",
                  "AMD": "#008E56",
                  "Home Depot": "#F6821F",
                  "Texas Instruments": "#BE372F",
                  "UPS": "#2C0D01",
                  "Lockheed Martin": "#000000",
                  "FedEx": "#652c8f",
                  "John Deere": "#237b36",
                  "Nvidia": "#000000",
                  "Praxair": "#00992f",
                  "Pepsi": "#134c9d"}

def get_company_color(name):
    if name in COMPANY_COLORS:
        return COMPANY_COLORS[name]
    else:
        return None

def get_complementary_color(my_hex):
    if my_hex == None:
        return None
    if my_hex[0] == "#":
        my_hex = my_hex[1:]
    rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
    comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
    return "#" + "".join(comp)


def scale(value, scale_method):
    if scale_method == None:
        return value
    else:
        return scale_method(value)


def plot_time_series_by_company(data, key, scale_method=None):
    for company_name in data["Name"].unique():
        if company_name == "S&P500-Index":
            continue

        plot_data = data[data["Name"] == company_name]
        plt.plot(plot_data["Date"], scale(plot_data[key], scale_method),
                 label = company_name,
                 color = get_company_color(company_name))

    plt.xlabel("Date")
    plt.ylabel(key)
    plt.legend()
    return plt


def plot_time_series(data, ylabel):
    for key in data.keys():
        plt.plot(data[key],
                 label = key,
                 color = get_company_color(key))
        plt.xlabel(data.index.name)
        plt.ylabel(ylabel)
        plt.legend()
    return plt


def plot_probability_density(data, bin_num=100, scale_method=None):
    sorted_values = data.dropna().sort_values()
    bins = np.linspace(sorted_values.min(), sorted_values.max(), bin_num)
    histogram, bins = np.histogram(sorted_values, bins=bins, density=True)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    plt.plot(bin_centers, scale(histogram, scale_method),
             label = "Probability Density",
             color = get_company_color(data.name))

    mean, standard_deviation = stats.norm.fit(sorted_values)
    gauss = stats.norm.pdf(bins, mean, standard_deviation)
    plt.plot(bins, scale(gauss, scale_method),
             color = get_complementary_color(get_company_color(data.name)),
             label = "Gaussian Fit")

    plt.ylabel("Probability Density")
    plt.xlabel("Logarithmic Return")
    plt.legend()

    return plt
