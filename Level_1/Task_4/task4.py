
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

# Check required columns
required_columns = ["Has Online delivery", "Aggregate rating"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Required column not found: {column}")

# Clean online delivery values
df["Has Online delivery"] = (
    df["Has Online delivery"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Keep valid Yes/No delivery records
delivery_df = df[
    df["Has Online delivery"].isin(["Yes", "No"])
].copy()

# Convert ratings to numeric
delivery_df["Aggregate rating"] = pd.to_numeric(
    delivery_df["Aggregate rating"],
    errors="coerce"
)

# 1. Calculate delivery percentages
delivery_counts = (
    delivery_df["Has Online delivery"]
    .value_counts()
    .reindex(["Yes", "No"], fill_value=0)
)

total_restaurants = delivery_counts.sum()

delivery_percentages = (
    delivery_counts / total_restaurants * 100
).round(2)

print("\n===== ONLINE DELIVERY DISTRIBUTION =====")
print(f"Total restaurants with valid delivery status: {total_restaurants}")

for status in ["Yes", "No"]:
    print(
        f"{status}: {delivery_counts[status]} restaurants "
        f"({delivery_percentages[status]:.2f}%)"
    )

# Save delivery distribution
delivery_distribution = pd.DataFrame({
    "Online Delivery": ["Yes", "No"],
    "Restaurant Count": [
        delivery_counts["Yes"],
        delivery_counts["No"]
    ],
    "Percentage": [
        delivery_percentages["Yes"],
        delivery_percentages["No"]
    ]
})

delivery_distribution.to_csv(
    RESULTS_DIR / "online_delivery_distribution.csv",
    index=False
)

# 2. Compare

# 2. Compare average ratings
# Exclude rating 0 because it means the restaurant has not been rated
rated_df = delivery_df[
    delivery_df["Aggregate rating"] > 0
].copy()

average_ratings = (
    rated_df.groupby("Has Online delivery")["Aggregate rating"]
    .mean()
    .reindex(["Yes", "No"])
    .round(2)
)

print("\n===== AVERAGE RATING COMPARISON =====")

for status in ["Yes", "No"]:
    if pd.notna(average_ratings[status]):
        print(
            f"{status} online delivery: "
            f"{average_ratings[status]:.2f}"
        )
    else:
        print(f"{status} online delivery: No rated restaurants found")

# Save average ratings to CSV
rating_comparison = average_ratings.rename_axis(
    "Online Delivery"
).reset_index(name="Average Rating")

rating_comparison.to_csv(
    RESULTS_DIR / "online_delivery_rating_comparison.csv",
    index=False
)

# 3. Create chart for online delivery percentages
plt.figure(figsize=(7, 5))

bars = plt.bar(
    delivery_distribution["Online Delivery"],
    delivery_distribution["Percentage"]
)

plt.title("Percentage of Restaurants Offering Online Delivery")
plt.xlabel("Online Delivery")
plt.ylabel("Percentage of Restaurants")
plt.bar_label(bars, fmt="%.2f%%", padding=3)
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "online_delivery_percentage.png",
    dpi=300
)

plt.close()

# 4. Create chart comparing average ratings
rating_chart_data = rating_comparison.dropna()

plt.figure(figsize=(7, 5))

bars = plt.bar(
    rating_chart_data["Online Delivery"],
    rating_chart_data["Average Rating"]
)

plt.title("Average Ratings: Online Delivery vs No Online Delivery")
plt.xlabel("Online Delivery")
plt.ylabel("Average Rating")
plt.bar_label(bars, fmt="%.2f", padding=3)
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "online_delivery_rating_comparison.png",
    dpi=300
)

plt.close()

print("\nAll results saved in:", RESULTS_DIR)
print("Task 4 completed successfully!")


