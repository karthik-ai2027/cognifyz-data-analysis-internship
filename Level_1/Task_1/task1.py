import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "dataset" / "Dataset.csv"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# Create results folder if it doesn't exist
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Calculate total number of restaurants
total_restaurants = len(df)

# Extract and count individual cuisines
cuisine_counts = (
    df["Cuisines"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .loc[lambda x: x.ne("")]
    .value_counts()
)

# Select the top three cuisines
top_cuisines = cuisine_counts.head(3)

# Calculate percentages
results = pd.DataFrame({
    "Cuisine": top_cuisines.index,
    "Restaurant Count": top_cuisines.values,
    "Percentage (%)": (
        top_cuisines.values / total_restaurants * 100
    ).round(2)
})

# Display results
print("\n========== TOP 3 CUISINES ==========")
print(results.to_string(index=False))

# Save results to CSV
output_path = RESULTS_DIR / "top_cuisines.csv"
results.to_csv(output_path, index=False)

print(f"\nTotal restaurants: {total_restaurants}")
print(f"Results saved to: {output_path}")