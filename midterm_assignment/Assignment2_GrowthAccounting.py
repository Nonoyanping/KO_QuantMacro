import pandas as pd
import numpy as np

# Load Data
pwt_data = pd.read_stata("https://www.rug.nl/ggdc/docs/pwt90.dta")

# OECD countries
oecd_countries = [
    "Australia",
    "Austria",
    "Belgium",
    "Canada",
    "Denmark",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Iceland",
    "Ireland",
    "Italy",
    "Japan",
    "Netherlands",
    "New Zealand",
    "Norway",
    "Portugal",
    "Spain",
    "Sweden",
    "Switzerland",
    "United Kingdom",
    "United States",
]

# Filter data for OECD countries and 1990-2019 period
data = pd.DataFrame(
    pwt_data[
        pwt_data["country"].isin(oecd_countries) & pwt_data["year"].between(1990, 2019)
    ]
)

relevant_cols = ["countrycode", "country", "year", "rgdpna", "rkna", "emp", "labsh"]

data = data[relevant_cols].dropna()


def calculate_growth_rates(country_data):
    country_data = country_data.sort_values("year")
    start_data = country_data.iloc[0]
    end_data = country_data.iloc[-1]

    years = end_data["year"] - start_data["year"]

    # Calculate per-worker variables
    y_per_worker_start = start_data["rgdpna"] / start_data["emp"]
    y_per_worker_end = end_data["rgdpna"] / end_data["emp"]

    k_per_worker_start = start_data["rkna"] / start_data["emp"]
    k_per_worker_end = end_data["rkna"] / end_data["emp"]

    # Growth rates (annualized)
    g_y = ((y_per_worker_end / y_per_worker_start) ** (1 / years) - 1) * 100
    g_k = ((k_per_worker_end / k_per_worker_start) ** (1 / years) - 1) * 100

    # Capital share (average over period)
    alpha = (1 - start_data["labsh"] + 1 - end_data["labsh"]) / 2

    # Capital deepening contribution
    capital_deepening = alpha * g_k

    # TFP Growth as residual (Solow residual)
    # Following the identity: Growth Rate = TFP Growth + Capital Deepening
    tfp_growth = g_y - capital_deepening

    # Calculate shares
    tfp_share = tfp_growth / g_y if g_y != 0 else 0
    capital_share = capital_deepening / g_y if g_y != 0 else 0

    return {
        "Country": start_data["country"],
        "Growth Rate": round(g_y, 2),
        "TFP Growth": round(tfp_growth, 2),
        "Capital Deepening": round(capital_deepening, 2),
        "TFP Share": round(tfp_share, 2),
        "Capital Share": round(capital_share, 2),
    }


# Calculate for each country
results_list = []
for country in data["country"].unique():
    country_data = data[data["country"] == country]
    if len(country_data) >= 2:
        result = calculate_growth_rates(country_data)
        results_list.append(result)

# Create results DataFrame
results_df = pd.DataFrame(results_list)

# Sort by country name
results_df = results_df.sort_values("Country").reset_index(drop=True)

# Add average row
avg_row = {
    "Country": "Average",
    "Growth Rate": round(results_df["Growth Rate"].mean(), 2),
    "TFP Growth": round(results_df["TFP Growth"].mean(), 2),
    "Capital Deepening": round(results_df["Capital Deepening"].mean(), 2),
    "TFP Share": round(results_df["TFP Share"].mean(), 2),
    "Capital Share": round(results_df["Capital Share"].mean(), 2),
}

results_df = pd.concat([results_df, pd.DataFrame([avg_row])], ignore_index=True)

# Print Result
print("Table 5.1")
print("Growth Accounting in OECD Countries: 1990-2019")
print("")
print(
    f"{'Country':<15} {'Growth Rate':<12} {'TFP Growth':<12} {'Capital Deepening':<18} {'TFP Share':<10} {'Capital Share'}"
)

for _, row in results_df.iterrows():
    print(
        f"{row['Country']:<15} {row['Growth Rate']:<12} {row['TFP Growth']:<12} {row['Capital Deepening']:<18} {row['TFP Share']:<10} {row['Capital Share']}"
    )

# Save results as CSV file
results_df.to_csv("./assignment2_result/GrowthAccounting(1990_2019).csv", index=False)
print("Save results to ./assignment2_result/GrowthAccounting(1990_2019).csv")
