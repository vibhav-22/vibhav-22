"""Render the most recent 31 days from GitHub's contribution calendar."""
import json
import sys
from pathlib import Path

weeks = json.load(sys.stdin)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
days = [day for week in weeks for day in week["contributionDays"]][-31:]
counts = [day["contributionCount"] for day in days]
peak = max(1, max(counts))
points = []
for index, count in enumerate(counts):
    x = 48 + 704 * index / max(1, len(days) - 1)
    y = 155 - 92 * count / peak
    points.append(f"{x:.1f},{y:.1f}")

chart = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 205">',
    '<rect width="800" height="205" rx="12" fill="#251B16"/>',
    '<g font-family="sans-serif" fill="#FFE0C6">',
    '<text x="28" y="32" font-size="20">Contributions over the last month</text>',
    f'<text x="752" y="32" text-anchor="end">{sum(counts)} contributions</text>',
    f'<text x="32" y="67" text-anchor="end">{peak}</text>',
    '<text x="32" y="160" text-anchor="end">0</text>',
    f'<text x="48" y="185">{days[0]["date"]}</text>',
    f'<text x="752" y="185" text-anchor="end">{days[-1]["date"]}</text></g>',
    '<path d="M48 63h704M48 155h704" stroke="#614737"/>',
    f'<polygon points="48,155 {" ".join(points)} 752,155" fill="#A94F25" opacity=".45"/>',
    f'<polyline points="{" ".join(points)}" fill="none" stroke="#FF994F" stroke-width="3"/>',
]
for day, point in zip(days, points):
    x, y = point.split(",")
    chart.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#FFD3A1"><title>{day["date"]}: {day["contributionCount"]}</title></circle>')
Path("dist/activity.svg").write_text("".join(chart) + "</svg>")
