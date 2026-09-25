import matplotlib.pyplot as plt
import numpy as np

minutes = [10, 20, 30, 40, 50, 60]
pre = [123.64, 367.73, 717.50, 1244.69, 1805.58, 2220.70]
post = [93.41, 288.41, 568.79, 955.36, 1375.65, 1691.31]

x = np.arange(len(minutes))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(x - width/2, pre, width, label="Before flood", color="#1a9850")
ax.bar(x + width/2, post, width, label="After flood", color="#b2182b")

for i, (p, q) in enumerate(zip(pre, post)):
    pct = (q - p) / p * 100
    ax.text(i, max(p, q) + 40, f"{pct:.1f}%", ha="center", fontsize=9)

ax.set_xlabel("Travel time to nearest hospital (minutes)")
ax.set_ylabel("Reachable area (km2)")
ax.set_title("Reachable Area by Travel Time, Before vs After Flood")
ax.set_xticks(x)
ax.set_xticklabels(minutes)
ax.legend()

plt.tight_layout()
plt.savefig("data/osm/accessibility_chart.png", dpi=150)
print("Saved: data/osm/accessibility_chart.png")
