import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import datetime
from statsmodels.tsa.stattools import acf, ccf
from matplotlib.gridspec import GridSpec

# Set the style for all plots
plt.style.use('ggplot')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
                                                    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'])

# Set the start and end dates for the data
start_date = '1996-01-01'  # Starting from 1996 for India GDP data availability
end_date = '2023-12-31'    # Current data goes up to Q3 2023

def get_macro_data(country_code, start_date, end_date):
    """
    Fetch macroeconomic data for a specific country from FRED
    
    Parameters:
    country_code (str): 'IN' for India
    
    Returns:
    dict: Dictionary containing DataFrames for GDP, consumption, and investment
    """
    data = {}
    
    # Dictionary of FRED series IDs for each country and variable
    series_ids = {
        'IN': {
            'gdp': 'NAEXKP01INQ652S',              # Real GDP (Quarterly)
        }
    }
    
    # Fetch data for each variable
    for var, series_id in series_ids[country_code].items():
        try:
            data[var] = web.DataReader(series_id, 'fred', start_date, end_date)
        except Exception as e:
            print(f"Error fetching {var} data for {country_code}: {e}")
            data[var] = None
    
    return data

def process_cycle_data(data):
    """
    Process raw data: take logs and extract cyclical components
    
    Parameters:
    data (dict): Dictionary of DataFrames for each variable
    
    Returns:
    dict: Dictionary containing cyclical components for each variable
    """
    cycles = {}
    trends = {}
    
    for var, df in data.items():
        if df is not None and not df.empty:
            # Take natural log of the data
            log_data = np.log(df)
            
            # Apply HP filter to extract cyclical component (lambda=1600 for quarterly data)
            cycle, trend = sm.tsa.filters.hpfilter(log_data, lamb=1600)
            
            # Store the cycle and trend components
            cycles[var] = cycle
            trends[var] = trend
    
    return cycles, trends

def calculate_statistics(cycles):
    """
    Calculate standard moments and correlations of cyclical components
    
    Parameters:
    cycles (dict): Dictionary of cyclical components for each variable
    
    Returns:
    tuple: (std_dev, autocorr, corr_with_gdp)
    """
    # Convert all cycles to a single DataFrame
    cycle_df = pd.DataFrame({var: cycle for var, cycle in cycles.items()})
    
    # Calculate standard deviations (volatility)
    std_dev = cycle_df.std() * 100  # Multiply by 100 to express as percentage
    
    # Calculate first-order autocorrelation
    autocorr = pd.Series({var: acf(cycle_df[var].dropna(), nlags=1)[1] for var in cycle_df.columns})
    
    # Calculate correlation with GDP
    corr_with_gdp = cycle_df.corr()['gdp']
    
    return std_dev, autocorr, corr_with_gdp


def plot_trends_and_cycles(country, raw_data, cycles, trends):
    """
    Plot the original data, trend, and cycle for each variable
    
    Parameters:
    country (str): Country name for the title
    raw_data (dict): Dictionary of raw data for each variable
    cycles (dict): Dictionary of cyclical components
    trends (dict): Dictionary of trend components
    """
    # variables = ['gdp', 'consumption', 'investment']
    variables = ['gdp']
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig)
    
    for i, var in enumerate(variables):
        if var in raw_data and raw_data[var] is not None:
            # Left column: Original data and trend
            ax1 = fig.add_subplot(gs[i, 0])
            log_data = np.log(raw_data[var])
            log_data.plot(ax=ax1, label=f"Log {var.capitalize()}")
            trends[var].plot(ax=ax1, label="Trend", linewidth=2, color='red')
            ax1.set_title(f"{var.capitalize()} and Trend for {country}")
            ax1.legend()
            
            # Right column: Cyclical component
            ax2 = fig.add_subplot(gs[i, 1])
            cycles[var].plot(ax=ax2, label=f"Cyclical Component", color='green')
            ax2.set_title(f"{var.capitalize()} Cycle for {country}")
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f"{country.lower().replace(' ', '_')}_trends_and_cycles.png", dpi=300, bbox_inches='tight')
    # plt.show()

def main():
    # Fetch macroeconomic data for India
    country_code = 'IN'
    raw_data = get_macro_data(country_code, start_date, end_date)
    
    # Process the data to extract cycles and trends
    cycles, trends = process_cycle_data(raw_data)
    
    # Calculate statistics
    std_dev, autocorr, corr_with_gdp = calculate_statistics(cycles)
    
    # Print statistics
    print("Standard Deviations (Volatility):")
    print(std_dev)
    print("\nFirst-order Autocorrelations:")
    print(autocorr)
    print("\nCorrelation with GDP:")
    print(corr_with_gdp)
    
    # Plot the trends and cycles
    plot_trends_and_cycles("India", raw_data, cycles, trends)

if __name__ == "__main__":
    main()
