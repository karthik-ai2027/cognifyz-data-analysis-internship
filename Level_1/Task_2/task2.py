
import pandas as pd
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
print("Dataset columns:", df.columns.tolist())

# Remove rows with missing city names
df = df.dropna(subset=["City"]).copy()

# Convert rating to numeric values
df["Aggregate rating"] = pd.to_numeric(
    df["Aggregate rating"], errors="coerce"
)

# 1. Find the city with the most restaurants
restaurant_counts = df["City"].value_counts()

top_city = restaurant_counts.idxmax()
top_city_count = restaurant_counts.max()

print("\n========== CITY WITH MOST RESTAURANTS ==========")
print(f"City: {top_city}")
print(f"Number of restaurants: {top_city_count}")

# Save restaurant counts for all cities
city_counts_df = restaurant_counts.rename_axis(
    "City"
).reset_index(name="Restaurant Count")

city_counts_df.to_csv(
    RESULTS_DIR / "city_restaurant_counts.csv",
    index=False
)

# 2. Calculate average rating for each city
city_ratings = (
    df.dropna(subset=["Aggregate rating"])
    .groupby("City")["Aggregate rating"]
    .mean()
    .sort_values(ascending=False)
)

city_ratings_df = city_ratings.rename_axis(
    "City"
).reset_index(name="Average Rating")

city_ratings_df["Average Rating"] = (
    city_ratings_df["Average Rating"].round(2)
)

print("\n========== TOP 10 CITIES BY AVERAGE RATING ==========")
print(city_ratings_df.head(10).to_string(index=False))

# 3. Find the city with the highest average rating
if not city_ratings.empty:
    highest_rated_city = city_ratings.index[0]
    highest_average_rating = city_ratings.iloc[0]

    print("\n========== CITY WITH HIGHEST AVERAGE RATING ==========")
    print(f"City: {highest_rated_city}")
    print(f"Average rating: {highest_average_rating:.2f}")

# Save average ratings for all cities


city_ratings_df.to_csv(
    RESULTS_DIR / "city_average_ratings.csv",
    index=False
)

# Save the highest-rated city separately
if not city_ratings_df.empty:
    highest_city_df = city_ratings_df.head(1)

    highest_city_df.to_csv(
        RESULTS_DIR / "highest_average_rating_city.csv",
        index=False
    )

    print("\nHighest-rated city saved successfully!")
    print(highest_city_df.to_string(index=False))

print("\nResults saved in:", RESULTS_DIR)


