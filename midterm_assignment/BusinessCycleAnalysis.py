import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# Data period
start_date = "1991-01-01"
end_date = "2025-01-01"


def get_gdp_data(series_id, start_date, end_date):
    """Fetch GDP data from FRED"""
    try:
        data = web.DataReader(series_id, "fred", start_date, end_date)
        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None


def apply_hp_filter(log_gdp, lambda_values=[10, 100, 1600]):
    """Apply HP filter with multiple lambda values"""
    results = {}
    for lamb in lambda_values:
        cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=lamb)
        results[lamb] = {"cycle": cycle, "trend": trend}
    return results


def plot_original_and_trends(log_gdp, hp_results, country_name):
    """Plot original data with trend components"""
    plt.figure(figsize=(16, 12))

    plt.plot(
        log_gdp.index, log_gdp.values, label="Log Real GDP", linewidth=2, color="black"
    )

    colors = ["red", "blue", "green"]
    for i, (lamb, result) in enumerate(hp_results.items()):
        plt.plot(
            result["trend"].index,
            result["trend"].values,
            label=f"Trend (λ={lamb})",
            linewidth=2,
            color=colors[i],
        )

    plt.title(f"{country_name}: Original Data and Trend Components")
    plt.xlabel("Year")
    plt.ylabel("Log Real GDP")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"output/{country_name}_trends_v2.png")


def plot_cyclical_components(hp_results, country_name):
    """Plot cyclical components for different lambda values"""
    plt.figure(figsize=(16, 12))

    colors = ["red", "blue", "green"]
    for i, (lamb, result) in enumerate(hp_results.items()):
        plt.plot(
            result["cycle"].index,
            result["cycle"].values,
            label=f"Cycle (λ={lamb})",
            linewidth=1.5,
            color=colors[i],
        )

    plt.axhline(y=0, color="black", linestyle="-", alpha=0.3)
    plt.title(f"{country_name}: Cyclical Components")
    plt.xlabel("Year")
    plt.ylabel("Cyclical Component")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"output/{country_name}_cyclical_v2.png")


def calculate_statistics(cycle1, cycle2):
    """Calculate standard deviations and correlation"""
    # Standard deviations (multiply by 100 to express as percentage)
    std1 = cycle1.std() * 100
    std2 = cycle2.std() * 100

    # Correlation (using common period)
    common_start = max(cycle1.index.min(), cycle2.index.min())
    common_end = min(cycle1.index.max(), cycle2.index.max())

    cycle1_common = cycle1[common_start:common_end]
    cycle2_common = cycle2[common_start:common_end]

    correlation = cycle1_common.corr(cycle2_common)

    return std1, std2, correlation


def plot_comparison(cycle1, cycle2, country1, country2):
    """Plot both countries' cyclical components"""
    plt.figure(figsize=(16, 12))

    # Use common period
    common_start = max(cycle1.index.min(), cycle2.index.min())
    common_end = min(cycle1.index.max(), cycle2.index.max())

    cycle1_common = cycle1[common_start:common_end]
    cycle2_common = cycle2[common_start:common_end]

    plt.plot(
        cycle1_common.index,
        cycle1_common.values,
        label=f"{country1}",
        linewidth=2,
        color="blue",
    )
    plt.plot(
        cycle2_common.index,
        cycle2_common.values,
        label=f"{country2}",
        linewidth=2,
        color="red",
    )

    plt.axhline(y=0, color="black", linestyle="-", alpha=0.3)
    plt.title(f"Business Cycle Comparison: {country1} vs {country2}")
    plt.xlabel("Year")
    plt.ylabel("Cyclical Component")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"output/{country1} vs {country2}.png")


def main():
    """Main analysis"""
    print("=== HP Filter Business Cycle Analysis ===")

    # 1. Download data
    print("1. Downloading data...")
    germany_gdp = get_gdp_data("CLVMNACSCAB1GQDE", start_date, end_date)  # Germany
    japan_gdp = get_gdp_data("JPNRGDPEXP", start_date, end_date)  # Japan

    if germany_gdp is None or japan_gdp is None:
        print("Failed to download data")
        return

    # 2. Log transformation
    print("2. Log transformation...")
    log_germany = np.log(germany_gdp).dropna()
    log_japan = np.log(japan_gdp).dropna()

    # 3. Apply HP filter
    print("3. Applying HP filter...")
    germany_hp = apply_hp_filter(log_germany.iloc[:, 0])
    japan_hp = apply_hp_filter(log_japan.iloc[:, 0])

    # 4. Visualizations
    print("4. Creating plots...")

    # Germany plots (First)
    print("Creating Germany trends plot...")
    plot_original_and_trends(log_germany.iloc[:, 0], germany_hp, "Germany")

    print("Creating Germany cyclical components plot...")
    plot_cyclical_components(germany_hp, "Germany")

    # Japan plots (Second)
    print("Creating Japan trends plot...")
    plot_original_and_trends(log_japan.iloc[:, 0], japan_hp, "Japan")

    print("Creating Japan cyclical components plot...")
    plot_cyclical_components(japan_hp, "Japan")

    # 5. Statistics and comparison (using λ=1600)
    print("5. Calculating statistics...")

    germany_cycle = germany_hp[1600]["cycle"]
    japan_cycle = japan_hp[1600]["cycle"]

    std_germany, std_japan, correlation = calculate_statistics(
        germany_cycle, japan_cycle
    )

    print("\n=== Results ===")
    print(f"Germany cyclical component std: {std_germany:.2f}%")
    print(f"Japan cyclical component std: {std_japan:.2f}%")
    print(f"Correlation between cycles: {correlation:.4f}")

    # Comparison plot
    plot_comparison(germany_cycle, japan_cycle, "Germany", "Japan")

    print("\nAnalysis completed!")


if __name__ == "__main__":
    main()
