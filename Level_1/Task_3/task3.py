
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Set project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "dataset" / "Dataset.csv"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# Create results folder
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Check whether the required column exists
if "Price range" not in df.columns:
    raise ValueError("The 'Price range' column was not found.")

# Convert price range to numeric
df["Price range"] = pd.to_numeric(
    df["Price range"], errors="coerce"
)

# Remove rows with missing or invalid price ranges
df = df.dropna(subset=["Price range"]).copy()

# Count restaurants in each price range
price_counts = df["Price range"].value_counts().sort_index()

# Calculate percentages
price_percentages = (
    price_counts / price_counts.sum() * 100
).round(2)

# Create results table
price_distribution = pd.DataFrame({
    "Price Range": price_counts.index,
    "Restaurant Count": price_counts.values,
    "Percentage": price_percentages.values
})

# Display results
print("\n===== PRICE RANGE DISTRIBUTION =====")
print(price_distribution.to_string(index=False))

# Save results to CSV
csv_path = RESULTS_DIR / "price_range_distribution.csv"
price_distribution.to_csv(csv_path, index=False)

# Create bar chart
plt.figure(figsize=(8, 5))

bars = plt.bar(
    price_distribution["Price Range"].astype(int).astype(str),
    price_distribution["Restaurant Count"]
)

plt.title("Distribution of Restaurants by Price Range")
plt.xlabel("Price Range")
plt.ylabel("Number of Restaurants")

# Display restaurant counts on top of bars
plt.bar_label(bars, padding=3)

plt.tight_layout()

# Save chart
chart_path = RESULTS_DIR / "price_range_distribution.png"
plt.savefig(chart_path, dpi=300)
plt.show()

print("\nCSV saved to:", csv_path)
print("Chart saved to:", chart_path)

