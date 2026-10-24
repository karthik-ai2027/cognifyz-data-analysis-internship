
import pandas as pd
import matplotlib.pyplot as plt
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
required_columns = ["Cuisines", "Aggregate rating"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Required column not found: {column}")

# 5. Clean required columns
df["Cuisines"] = df["Cuisines"].fillna("").astype(str).str.strip()

df["Aggregate rating"] = pd.to_numeric(
    df["Aggregate rating"], errors="coerce"
)

# Exclude rows without cuisine information
df = df[df["Cuisines"] != ""].copy()

# 6. Standardize cuisine combinations
# Sort cuisine names so combinations are counted consistently
def standardize_cuisines(cuisine_text):
    cuisines = [
        cuisine.strip().lower()
        for cuisine in cuisine_text.split(",")
        if cuisine.strip()
    ]

    cuisines = sorted(set(cuisines))

    return ", ".join(cuisines)


df["Cuisine Combination"] = df["Cuisines"].apply(
    standardize_cuisines
)

# Remove any combinations that became empty
df = df[df["Cuisine Combination"] != ""].copy()

# ==========================================
# PART 1: MOST COMMON CUISINE COMBINATIONS
# ==========================================

combination_counts = (
    df["Cuisine Combination"]
    .value_counts()
    .head(10)
)

common_combinations = pd.DataFrame({
    "Cuisine Combination": combination_counts.index,
    "Restaurant Count": combination_counts.values
})

print("\n===== TOP 10 CUISINE COMBINATIONS =====")
print(common_combinations.to_string(index=False))

# Save common combinations
common_combinations.to_csv(
    RESULTS_DIR / "common_cuisine_combinations.csv",
    index=False
)

# Plot top cuisine combinations
plt.figure(figsize=(12, 7))

plt.barh(
    common_combinations["Cuisine Combination"][::-1],
    common_combinations["Restaurant Count"][::-1]
)

plt.title("Top 10 Most Common Cuisine Combinations")
plt.xlabel("Number of Restaurants")
plt.ylabel("Cuisine Combination")
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "common_cuisine_combinations.png",
    dpi=300
)

plt.close()

# ==========================================
# PART 2: RATINGS BY CUISINE COMBINATION
# ==========================================

rated_df = df[
    df["Aggregate rating"].notna()
    & (df["Aggregate rating"] > 0)
].copy()

rating_analysis = (
    rated_df.groupby("Cuisine Combination")
    .agg(
        Restaurant_Count=("Aggregate rating", "size"),
        Average_Rating=("Aggregate rating", "mean")
    )
    .reset_index()
)

rating_analysis["Average_Rating"] = (
    rating_analysis["Average_Rating"].round(2)
)

# Include only combinations with at least 10 restaurants
# This reduces the influence of combinations appearing very rarely
reliable_combinations = rating_analysis[
    rating_analysis["Restaurant_Count"] >= 10
].copy()

# Sort by average rating
highest_rated = reliable_combinations.sort_values(
    by="Average_Rating",
    ascending=False
).head(10)

print("\n===== TOP 10 HIGHEST-RATED CUISINE COMBINATIONS =====")
print(highest_rated.to_string(index=False))

# Save all combinations' rating analysis
rating_analysis.sort_values(
    by="Average_Rating",
    ascending=False
).to_csv(
    RESULTS_DIR / "cuisine_combination_ratings.csv",
    index=False
)

# Save the highest-rated combinations with at least 10 restaurants
highest_rated.to_csv(
    RESULTS_DIR / "highest_rated_cuisine_combinations.csv",
    index=False
)

# Plot highest-rated combinations
if not highest_rated.empty:
    plot_df = highest_rated.sort_values(
        by="Average_Rating",
        ascending=True
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        plot_df["Cuisine Combination"],
        plot_df["Average_Rating"]
    )

    plt.title(
        "Highest-Rated Cuisine Combinations "
        "(At Least 10 Restaurants)"
    )
    plt.xlabel("Average Aggregate Rating")
    plt.ylabel("Cuisine Combination")
    plt.xlim(0, 5)
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "highest_rated_cuisine_combinations.png",
        dpi=300
    )

    plt.close()

# ==========================================
# FINAL SUMMARY
# ==========================================

if not common_combinations.empty:
    most_common = common_combinations.iloc[0]

    print("\n===== MOST COMMON COMBINATION =====")
    print("Cuisine combination:", most_common["Cuisine Combination"])
    print("Restaurant count:", most_common["Restaurant Count"])

if not highest_rated.empty:
    highest = highest_rated.sort_values(
        by="Average_Rating",
        ascending=False
    ).iloc[0]

    print("\n===== HIGHEST-RATED COMMON COMBINATION =====")
    print("Cuisine combination:", highest["Cuisine Combination"])
    print("Number of restaurants:", highest["Restaurant_Count"])
    print("Average rating:", highest["Average_Rating"])

print("\nAll results saved in:", RESULTS_DIR)
print("Task 2 completed successfully!")

