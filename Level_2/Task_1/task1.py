
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Set project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "dataset" / "Dataset.csv"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# 2. Create results folder
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load dataset
df = pd.read_csv(DATASET_PATH)

# 4. Check required columns
required_columns = ["Aggregate rating", "Votes"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Required column not found: {column}")

# 5. Convert columns to numeric
df["Aggregate rating"] = pd.to_numeric(
    df["Aggregate rating"], errors="coerce"
)

df["Votes"] = pd.to_numeric(
    df["Votes"], errors="coerce"
)

# ==========================================
# PART 1: DISTRIBUTION OF AGGREGATE RATINGS
# ==========================================

ratings_df = df.dropna(subset=["Aggregate rating"]).copy()

# Exclude unrated restaurants (rating = 0)
rated_df = ratings_df[ratings_df["Aggregate rating"] > 0].copy()

# Define rating ranges
bins = [0, 1, 2, 3, 4, 5]
labels = [
    ">0–1.0",
    ">1.0–2.0",
    ">2.0–3.0",
    ">3.0–4.0",
    ">4.0–5.0"
]

rated_df["Rating Range"] = pd.cut(
    rated_df["Aggregate rating"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# Count restaurants in each rating range
rating_counts = rated_df["Rating Range"].value_counts(
    sort=False
)

# Calculate percentages
rating_percentages = (
    rating_counts / rating_counts.sum() * 100
).round(2)

# Create results table
rating_distribution = pd.DataFrame({
    "Rating Range": labels,
    "Restaurant Count": rating_counts.values,
    "Percentage": rating_percentages.values
})

print("\n===== AGGREGATE RATING DISTRIBUTION =====")
print(rating_distribution.to_string(index=False))

# Find the most common rating range
most_common_range = rating_counts.idxmax()

print("\n===== MOST COMMON RATING RANGE =====")
print("Rating range:", most_common_range)
print("Number of restaurants:", rating_counts.max())

# Save rating distribution
rating_distribution.to_csv(
    RESULTS_DIR / "rating_distribution.csv",
    index=False
)

# Create rating distribution chart
plt.figure(figsize=(9, 5))

bars = plt.bar(
    rating_distribution["Rating Range"].astype(str),
    rating_distribution["Restaurant Count"]
)

plt.title("Distribution of Restaurant Ratings")
plt.xlabel("Aggregate Rating Range")
plt.ylabel("Number of Restaurants")
plt.bar_label(bars, padding=3)
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "rating_distribution.png",
    dpi=300
)

plt.close()

# ==========================================
# PART 2: AVERAGE NUMBER OF VOTES
# ==========================================

votes_df = df.dropna(subset=["Votes"]).copy()

average_votes = votes_df["Votes"].mean()

print("\n===== VOTE ANALYSIS =====")
print("Restaurants with valid vote counts:", len(votes_df))
print("Average number of votes:", round(average_votes, 2))

# Save vote analysis
vote_summary = pd.DataFrame({
    "Metric": [
        "Restaurants with valid vote counts",
        "Average number of votes"
    ],
    "Value": [
        len(votes_df),
        round(average_votes, 2)
    ]
})

vote_summary.to_csv(
    RESULTS_DIR / "average_votes.csv",
    index=False
)

# Create votes chart
plt.figure(figsize=(7, 5))

plt.bar(
    ["Average Votes"],
    [average_votes]
)

plt.title("Average Number of Votes per Restaurant")
plt.ylabel("Number of Votes")
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "average_votes.png",
    dpi=300
)

plt.close()

print("\nAll results saved in:", RESULTS_DIR)
print("Task 1 completed successfully!")

