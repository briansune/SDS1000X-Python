import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TKAgg')

data = [1, 2, 3, 4]

text = 'test\nval\n123128739'

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_title("Sample Line Chart", fontsize=18, fontweight='bold')

ax.tick_params(labelsize=14)
ax.annotate(text,
            xy=(1.0, -0.2),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=10)

fig.tight_layout()
plt.show()
