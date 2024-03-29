import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import close as close_figures
from scipy import stats
import seaborn as sns

# based on dominant company logo color
COMPANY_COLORS = {"S&P500-Index": "#000000",
                  "Apple": "#666666",
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
    try:
        return COMPANY_COLORS[name]
    except KeyError:
        return None

def get_complementary_color(my_hex):
    if my_hex == None or my_hex == "#000000": # dont return white for black
        return None
    if my_hex[0] == "#":
        my_hex = my_hex[1:]
    rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
    comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
    return "#" + "".join(comp)


def save_plot(figure, path, extension="pdf"):
    figure.savefig("{}.{}".format(path, extension))
    close_figures("all")



def plot_time_series_by_company(data, key, scale_method="linear"):
    for company_name in data["Name"].unique():
        if "Index" in company_name:
            continue # do not plot stock indices

        plot_data = data[data["Name"] == company_name]
        plt.plot(plot_data["Date"], plot_data[key],
                 label = company_name,
                 color = get_company_color(company_name))

    plt.yscale(scale_method)
    plt.xlabel("Date")
    plt.ylabel(key)
    plt.legend()
    plt.tight_layout()
    return plt


def plot_time_series(data, ylabel="", scale_method=["linear","linear"]):
    for key in data.keys():
        plt.plot(data[key],
                 label = key,
                 color = get_company_color(key))
    plt.xlabel(data.index.name)
    plt.ylabel(ylabel)

    plt.yscale(scale_method[1])
    if not scale_method[0] == "linear":
        plt.xscale(scale_method[0])

    if len(data.keys()) > 1: # no legend for single plot
        plt.legend()
    plt.tight_layout()
    return plt


def plot_probability_density(data, bin_num=100, scale_method=["linear","linear"], fit_gauss=False):
    values = data.dropna()
    if scale_method[0] == "log":
        values = values.abs()

    bins = np.linspace(values.min(), values.max(), bin_num)
    histogram, bins = np.histogram(values, bins=bins, density=True)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    plt.plot(bin_centers, histogram,
             color = get_company_color(data.name),
             label = "Histogram")

    if fit_gauss:
        mean, standard_deviation = stats.norm.fit(values)
        gauss = stats.norm.pdf(bins, mean, standard_deviation)
        plt.plot(bins, gauss,
                 color = get_complementary_color(get_company_color(data.name)),
                 label = "Gaussian Fit")
        plt.legend()

    plt.xscale(scale_method[0])
    plt.yscale(scale_method[1])
    plt.ylabel("Probability Density")
    plt.xlabel("Logarithmic Return")
    plt.tight_layout()
    return plt


def plot_correlation_matrix(correlation_matrix, title=""):
    fig = plt.figure()
    ax = fig.add_subplot()
    colorspace = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(correlation_matrix, ax=ax,
                cmap=colorspace, vmax=1, vmin=-1, center=0,
                square=True, linewidths=.5)
    plt.xticks(rotation=45, rotation_mode="anchor", horizontalalignment="right")
    plt.title(title)
    plt.tight_layout()
    return fig


def plot_correlation_time_series(correlation_matrices, list_of_pairs):
    for pair in list_of_pairs:
        subset = correlation_matrices[correlation_matrices.index.get_level_values(None) == pair[0]][pair[1]]
        plt.plot(subset.index.levels[0], subset.values, label=" & ".join(pair))

    if len(list_of_pairs) > 1:
        plt.legend()
    plt.xlabel(subset.index.names[0])
    plt.ylabel("Correlation")
    plt.tight_layout()
    return plt
