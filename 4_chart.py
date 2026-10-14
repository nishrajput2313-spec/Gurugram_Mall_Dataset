import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("final_dataset.csv").dropna(subset=["distance_km"])
if df.empty:
    raise SystemExit("No valid distances found. Run 3_geocode_distance.py first.")


labels = ["0-2 km", "2-5 km", "5-10 km", "10-40 km"]
bands = pd.cut(df["distance_km"], [0, 2, 5, 10, 40], labels=labels, include_lowest=True)
counts = bands.value_counts().reindex(labels).fillna(0).astype(int)


ax = counts.plot(kind="bar", color="#0F766E", figsize=(8, 5), rot=0)
ax.bar_label(ax.containers[0])  # show the number on top of each bar
ax.set_title("Malls and shopping centres by distance from Sohna Road, Gurugram")
ax.set_xlabel("Distance from reference point")
ax.set_ylabel("Number of malls")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("chart.png", dpi=150)


counts.rename("number_of_malls").to_csv("distance_summary.csv", header=True)

print(counts)
print("Saved chart.png and distance_summary.csv")