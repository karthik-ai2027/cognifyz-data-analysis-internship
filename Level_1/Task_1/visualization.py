import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Get the results folder
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# Load the results
file_path = RESULTS_DIR / "top_cuisines.csv"
df = pd.read_csv(file_path)

# Create the bar chart
plt.figure(figsize=(9, 5))

bars = plt.bar(df["Cuisine"], df["Restaurant Count"])

plt.title("Top 3 Cuisines by Restaurant Count")
plt.xlabel("Cuisine")
plt.ylabel("Number of Restaurants")

# Show counts above the bars
plt.bar_label(bars, padding=3)

plt.tight_layout()

# Save the chart
output_path = RESULTS_DIR / "top_cuisines_chart.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

# Display the chart
plt.show()

print(f"Chart saved to: {output_path}")