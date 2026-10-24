import os
import time

from matplotlib.figure import Figure
from matplotlib.patches import Circle

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
CHARTS_DIR = os.path.join(ASSETS_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

_counter = 0


def render_donut_chart(labels, sizes, title, colors=None):
    """Renders a donut chart to assets/charts/ and returns the src path (relative to assets_dir) for ft.Image."""
    global _counter
    _counter += 1

    fig = Figure(figsize=(6, 6), dpi=130)
    ax = fig.add_subplot(111)
    wedges, _, autotexts = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        autopct=lambda pct: str(int(round(pct * sum(sizes) / 100))),
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.4, edgecolor="w"),
    )
    for autotext in autotexts:
        autotext.set_color("black")
        autotext.set_fontsize(11)

    centre = Circle((0, 0), 0.60, fc="white", edgecolor="w")
    ax.add_artist(centre)
    ax.set_title(title, pad=20, fontsize=14)
    ax.axis("equal")

    legend_labels = [f"{label} ({size})" for label, size in zip(labels, sizes)]
    ax.legend(
        wedges,
        legend_labels,
        title="Legend",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=9,
    )
    fig.tight_layout(pad=3)

    filename = f"chart_{_counter}_{int(time.time() * 1000)}.png"
    path = os.path.join(CHARTS_DIR, filename)
    fig.savefig(path, bbox_inches="tight")

    return f"charts/{filename}"


def count_by(records, index, default="Unknown"):
    counts = {}
    for rec in records:
        key = (rec[index] or default)
        key = key.strip() if isinstance(key, str) else key
        if not key:
            key = default
        counts[key] = counts.get(key, 0) + 1
    return list(counts.keys()), list(counts.values())
