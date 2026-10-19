"""Render assets/languages.svg from language bytes across ALL repos (private included).

Public stats widgets only see public repos, so this is generated locally with an
authenticated `gh` and committed. Regenerate:

    python scripts/languages.py projectkindred11 theatomicfinch
"""
import collections
import json
import subprocess
import sys
from pathlib import Path

COLORS = {
    "TypeScript": "#3178c6", "Astro": "#ff5a03", "JavaScript": "#f1e05a", "CSS": "#663399",
    "HTML": "#e34c26", "PLpgSQL": "#336790", "Python": "#3572A5", "MDX": "#fcb32c",
    "Rust": "#dea584", "Shell": "#89e051", "PowerShell": "#012456",
}
TOP_N = 9


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def repos(owner):
    out = gh("repo", "list", owner, "--limit", "500", "--json", "name", "--jq", ".[].name")
    return [r for r in out.split() if r]


def main(owners):
    totals = collections.Counter()
    count = 0
    for owner in owners:
        for repo in repos(owner):
            totals.update(json.loads(gh("api", f"repos/{owner}/{repo}/languages") or "{}"))
            count += 1
    grand = sum(totals.values())
    top = totals.most_common(TOP_N)
    other = grand - sum(v for _, v in top)
    rows = [(k, v / grand * 100) for k, v in top] + ([("Other", other / grand * 100)] if other else [])

    w, bar_x, bar_w = 840, 30, 780
    segs, x = [], bar_x
    for name, pct in rows:
        seg_w = bar_w * pct / 100
        segs.append(f'<rect x="{x:.2f}" y="70" width="{seg_w:.2f}" height="12" fill="{COLORS.get(name, "#8b949e")}"/>')
        x += seg_w

    legend = []
    for i, (name, pct) in enumerate(rows):
        col, row = i % 5, i // 5
        lx, ly = 30 + col * 160, 118 + row * 30
        legend.append(
            f'<g class="item" style="animation-delay:{0.15 + i * 0.08:.2f}s">'
            f'<circle cx="{lx + 6}" cy="{ly - 4}" r="6" fill="{COLORS.get(name, "#8b949e")}"/>'
            f'<text x="{lx + 18}" y="{ly}" class="lang">{name}</text>'
            f'<text x="{lx + 18}" y="{ly + 14}" class="pct">{pct:.1f}%</text></g>'
        )

    h = 118 + ((len(rows) - 1) // 5) * 30 + 34
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  .title {{ font: 700 18px 'Segoe UI', Ubuntu, sans-serif; fill: #ff6b35; }}
  .sub {{ font: 400 12px 'Segoe UI', Ubuntu, sans-serif; fill: #8b949e; }}
  .lang {{ font: 600 13px 'Segoe UI', Ubuntu, sans-serif; fill: #e6edf3; }}
  .pct {{ font: 400 11px 'Segoe UI', Ubuntu, sans-serif; fill: #8b949e; }}
  .item {{ opacity: 0; animation: fade .5s ease-out forwards; }}
  .bar {{ animation: grow 1.2s cubic-bezier(.2,.8,.2,1) forwards; transform: scaleX(0); transform-origin: {bar_x}px 0; }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  @keyframes grow {{ to {{ transform: scaleX(1); }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f0c29"/><stop offset="1" stop-color="#1a1638"/></linearGradient>
  <clipPath id="round"><rect x="{bar_x}" y="70" width="{bar_w}" height="12" rx="6"/></clipPath>
</defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="url(#bg)" stroke="#302b63"/>
<text x="30" y="38" class="title">Languages I actually ship in</text>
<text x="30" y="56" class="sub">{grand / 1e6:.0f}M+ bytes of code across {count} repos, private ones included</text>
<g clip-path="url(#round)"><g class="bar">{"".join(segs)}</g></g>
{"".join(legend)}
</svg>
'''
    out = Path(__file__).resolve().parent.parent / "assets" / "languages.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out} ({count} repos)")


if __name__ == "__main__":
    main(sys.argv[1:] or ["projectkindred11"])
