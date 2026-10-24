
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Define paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "Dataset" / "Dataset.csv"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# 2. Create results folder
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load dataset
df = pd.read_csv(DATASET_PATH)

# 4. Check required columns
required_columns = [
    "Restaurant Name",
    "Aggregate rating",
    "Votes"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column not found: {column}. "
            f"Available columns: {list(df.columns)}"
        )

# 5. Clean the data
df["Restaurant Name"] = (
    df["Restaurant Name"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

df["Aggregate rating"] = pd.to_numeric(
    df["Aggregate rating"], errors="coerce"
)

df["Votes"] = pd.to_numeric(
    df["Votes"], errors="coerce"
)

# Exclude rows without restaurant names
df = df[df["Restaurant Name"] != ""].copy()

# ==========================================
# PART 1: IDENTIFY RESTAURANT CHAINS
# ==========================================

# Count how many times each restaurant name occurs
restaurant_counts = (
    df.groupby("Restaurant Name")
    .agg(
        Outlet_Count=("Restaurant Name", "size"),
        Average_Rating=("Aggregate rating", "mean"),
        Total_Votes=("Votes", "sum"),
        Average_Votes=("Votes", "mean")
    )
    .reset_index()
)

# A restaurant name appearing more than once
# is treated as a potential restaurant chain.
chains = restaurant_counts[
    restaurant_counts["Outlet_Count"] > 1
].copy()

# Sort by outlet count
chains = chains.sort_values(
    by="Outlet_Count",
    ascending=False
)

chains["Average_Rating"] = chains["Average_Rating"].round(2)
chains["Average_Votes"] = chains["Average_Votes"].round(2)

print("\n===== RESTAURANT CHAIN ANALYSIS =====")
print("Total restaurant records:", len(df))
print("Unique restaurant names:", df["Restaurant Name"].nunique())
print("Potential restaurant chains identified:", len(chains))

print("\n===== TOP 10 CHAINS BY NUMBER OF OUTLETS =====")

top_chains = chains.head(10)

print(
    top_chains[
        [
            "Restaurant Name",
            "Outlet_Count",
            "Average_Rating",
            "Total_Votes",
            "Average_Votes"
        ]
    ].to_string(index=False)
)

# Save all identified chains
chains.to_csv(
    RESULTS_DIR / "all_restaurant_chains.csv",
    index=False
)

# Save top 10 chains by outlets
top_chains.to_csv(
    RESULTS_DIR / "top_10_chains_by_outlets.csv",
    index=False
)

# ==========================================
# PART 2: RATINGS OF RESTAURANT CHAINS
# ==========================================

rated_chains = chains[
    chains["Average_Rating"].notna()
    & (chains["Average_Rating"] > 0)
].copy()

# To make rating comparisons more reliable,
# consider chains with at least 3 outlets.
reliable_rated_chains = rated_chains[
    rated_chains["Outlet_Count"] >= 3
].copy()

highest_rated = reliable_rated_chains.sort_values(
    by="Average_Rating",
    ascending=False
).head(10)

print("\n===== TOP 10 CHAINS BY AVERAGE RATING =====")

if not highest_rated.empty:
    print(
        highest_rated[
            [
                "Restaurant Name",
                "Outlet_Count",
                "Average_Rating",
                "Total_Votes"
            ]
        ].to_string(index=False)
    )
else:
    print("No chains with at least 3 outlets and valid ratings.")

highest_rated.to_csv(
    RESULTS_DIR / "top_10_chains_by_rating.csv",
    index=False
)

# ==========================================
# PART 3: POPULARITY BASED ON TOTAL VOTES
# ==========================================

popular_chains = chains.sort_values(
    by="Total_Votes",
    ascending=False
).head(10)

print("\n===== TOP 10 CHAINS BY TOTAL VOTES =====")

print(
    popular_chains[
        [
            "Restaurant Name",
            "Outlet_Count",
            "Total_Votes",
            "Average_Votes",
            "Average_Rating"
        ]
    ].to_string(index=False)
)

popular_chains.to_csv(
    RESULTS_DIR / "top_10_chains_by_votes.csv",
    index=False
)

# ==========================================
# PART 4: VISUALIZE TOP CHAINS BY OUTLETS
# ==========================================

if not top_chains.empty:
    plot_df = top_chains.sort_values(
        by="Outlet_Count",
        ascending=True
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        plot_df["Restaurant Name"],
        plot_df["Outlet_Count"]
    )

    plt.title("Top 10 Restaurant Chains by Number of Outlets")
    plt.xlabel("Number of Outlets")
    plt.ylabel("Restaurant Chain")
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "top_10_chains_by_outlets.png",
        dpi=300
    )

    plt.close()

# ==========================================
# PART 5: VISUALIZE HIGHEST-RATED CHAINS
# ==========================================

if not highest_rated.empty:
    plot_df = highest_rated.sort_values(
        by="Average_Rating",
        ascending=True
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        plot_df["Restaurant Name"],
        plot_df["Average_Rating"]
    )

    plt.title("Highest-Rated Restaurant Chains")
    plt.xlabel("Average Aggregate Rating")
    plt.ylabel("Restaurant Chain")
    plt.xlim(0, 5)
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "top_10_chains_by_rating.png",
        dpi=300
    )

    plt.close()

# ==========================================
# PART 6: VISUALIZE MOST POPULAR CHAINS
# ==========================================

if not popular_chains.empty:
    plot_df = popular_chains.sort_values(
        by="Total_Votes",
        ascending=True
    )

    plt.figure(figsize=(12, 7))

    plt.barh(
        plot_df["Restaurant Name"],
        plot_df["Total_Votes"]
    )

    plt.title("Most Popular Restaurant Chains by Total Votes")
    plt.xlabel("Total Votes")
    plt.ylabel("Restaurant Chain")
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "top_10_chains_by_votes.png",
        dpi=300
    )

    plt.close()

# ==========================================
# PART 7: FINAL SUMMARY
# ==========================================

print("\n===== FINAL SUMMARY =====")

if not chains.empty:
    largest_chain = chains.iloc[0]

    print(
        "Chain with the most outlets:",
        largest_chain["Restaurant Name"]
    )
    print("Number of outlets:", largest_chain["Outlet_Count"])

if not highest_rated.empty:
    best_rated_chain = highest_rated.iloc[0]

    print(
        "Highest-rated chain with at least 3 outlets:",
        best_rated_chain["Restaurant Name"]
    )
    print("Average rating:", best_rated_chain["Average_Rating"])

if not popular_chains.empty:
    most_popular_chain = popular_chains.iloc[0]

    print(
        "Chain with the most total votes:",
        most_popular_chain["Restaurant Name"]
    )
    print("Total votes:", most_popular_chain["Total_Votes"])

print("\nResults saved in:", RESULTS_DIR)
print("Task 4 completed successfully!")

