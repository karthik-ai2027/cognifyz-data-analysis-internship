
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. Define paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "Dataset" / "Dataset.csv"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# 2. Create results folder automatically
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load dataset
df = pd.read_csv(DATASET_PATH)

# 4. Check required columns
required_columns = ["Longitude", "Latitude"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column not found: {column}. "
            f"Available columns: {list(df.columns)}"
        )

# 5. Convert coordinates to numeric values
df["Longitude"] = pd.to_numeric(
    df["Longitude"], errors="coerce"
)

df["Latitude"] = pd.to_numeric(
    df["Latitude"], errors="coerce"
)

# 6. Remove missing or invalid coordinates
geo_df = df.dropna(
    subset=["Longitude", "Latitude"]
).copy()

geo_df = geo_df[
    geo_df["Longitude"].between(-180, 180)
    & geo_df["Latitude"].between(-90, 90)
].copy()

print("\n===== GEOGRAPHIC ANALYSIS =====")
print("Total restaurants in dataset:", len(df))
print("Restaurants with valid coordinates:", len(geo_df))
print("Restaurants excluded:", len(df) - len(geo_df))

if geo_df.empty:
    raise ValueError(
        "No valid coordinates found. Check the dataset."
    )

# 7. Save cleaned geographic data
geo_df.to_csv(
    RESULTS_DIR / "restaurants_with_coordinates.csv",
    index=False
)

# ==========================================
# PART 1: RESTAURANT LOCATION SCATTER PLOT
# ==========================================

plt.figure(figsize=(12, 7))

plt.scatter(
    geo_df["Longitude"],
    geo_df["Latitude"],
    alpha=0.4,
    s=10
)

plt.title("Geographic Distribution of Restaurants")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "restaurant_geographic_distribution.png",
    dpi=300
)

plt.close()

# ==========================================
# PART 2: DENSITY / CLUSTER VISUALIZATION
# ==========================================

plt.figure(figsize=(12, 7))

sns.histplot(
    data=geo_df,
    x="Longitude",
    y="Latitude",
    bins=50,
    cbar=True
)

plt.title("Restaurant Location Density")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "restaurant_location_density.png",
    dpi=300
)

plt.close()

# ==========================================
# PART 3: RESTAURANTS BY CITY
# ==========================================

if "City" in geo_df.columns:
    city_counts = (
        geo_df["City"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
        .reset_index()
    )

    city_counts.columns = [
        "City",
        "Restaurant Count"
    ]

    print("\n===== TOP 10 CITIES BY RESTAURANT COUNT =====")
    print(city_counts.to_string(index=False))

    city_counts.to_csv(
        RESULTS_DIR / "top_10_cities_by_restaurants.csv",
        index=False
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        city_counts["City"][::-1],
        city_counts["Restaurant Count"][::-1]
    )

    plt.title("Top 10 Cities by Number of Restaurants")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("City")
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "top_10_cities_by_restaurants.png",
        dpi=300
    )

    plt.close()

# ==========================================
# PART 4: SUMMARY
# ==========================================

print("\n===== GEOGRAPHIC ANALYSIS SUMMARY =====")
print(
    "Longitude range:",
    round(geo_df["Longitude"].min(), 4),
    "to",
    round(geo_df["Longitude"].max(), 4)
)

print(
    "Latitude range:",
    round(geo_df["Latitude"].min(), 4),
    "to",
    round(geo_df["Latitude"].max(), 4)
)

print("\nResults saved in:", RESULTS_DIR)
print("Task 3 completed successfully!")

