"""Render assets/whoami.svg: an animated terminal session that types out who I am.

Edit SESSION below, then run:  python scripts/whoami.py
"""
from html import escape
from pathlib import Path

# (command, [output lines]). Output segments are (text, css class).
SESSION = [
    ("whoami", [[("Kyle Crone", "hi"), (". Founder & builder. Colorado.", "out")]]),
    ("ls ~/building", [[("plexality/   clawality/   skillplum/   atomic-finch/   atomiscan/", "dir")]]),
    ("cat consulting.txt", [[("Sling Automation", "hi"), (" -> equipping ambitious businesses to fight giants, and win.", "out")]]),
    ("echo $WORKFLOW", [[("1 human", "acc"), (" + a fleet of AI agents that ship, test, review, and open PRs before I wake up.", "out")]]),
    ("cat principles.txt", [
        [("✓ ", "ok"), ("Ship fast, iterate faster      ", "out"), ("✓ ", "ok"), ("Systems over slog", "out")],
        [("✓ ", "ok"), ("Truth > comfort                ", "out"), ("✓ ", "ok"), ("Long-term thinking", "out")],
    ]),
]

W, PAD, LINE, TOP = 840, 28, 22, 70
CHAR = 8.4          # approx advance of 14px monospace
TYPE_CPS = 22       # typing speed, chars/sec
PROMPT = "kyle@colorado ~ $ "


def main():
    body, t, y = [], 0.4, TOP
    for cmd, outputs in SESSION:
        type_dur = max(len(cmd) / TYPE_CPS, 0.25)
        px = PAD + len(PROMPT) * CHAR
        body.append(
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="{PAD}" y="{y}"><tspan class="usr">kyle@colorado</tspan> <tspan class="path">~</tspan> <tspan class="pr">$</tspan></text></g>'
        )
        clip = f"c{len(body)}"
        body.append(
            f'<clipPath id="{clip}"><rect x="{px}" y="{y - 16}" height="22" width="0">'
            f'<animate attributeName="width" from="0" to="{len(cmd) * CHAR + 4:.1f}" begin="{t + 0.15:.2f}s" dur="{type_dur:.2f}s" fill="freeze"/></rect></clipPath>'
            f'<text x="{px}" y="{y}" class="cmd" clip-path="url(#{clip})">{escape(cmd)}</text>'
        )
        t += 0.15 + type_dur + 0.25
        y += LINE
        for line in outputs:
            spans = "".join(f'<tspan class="{c}">{escape(s)}</tspan>' for s, c in line)
            body.append(
                f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.3s" fill="freeze"/>'
                f'<text x="{PAD}" y="{y}" xml:space="preserve">{spans}</text></g>'
            )
            t += 0.12
            y += LINE
        t += 0.35
        y += 8

    px = PAD + len(PROMPT) * CHAR
    body.append(
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="{PAD}" y="{y}"><tspan class="usr">kyle@colorado</tspan> <tspan class="path">~</tspan> <tspan class="pr">$</tspan></text>'
        f'<rect x="{px}" y="{y - 14}" width="9" height="17" fill="#ff6b35">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect></g>'
    )
    h = y + 26

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="'JetBrains Mono', 'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace" font-size="14">
<style>
  .usr {{ fill: #a855f7; font-weight: 700; }}
  .path {{ fill: #58a6ff; font-weight: 700; }}
  .pr {{ fill: #8b949e; }}
  .cmd {{ fill: #e6edf3; font-weight: 600; }}
  .out {{ fill: #c9d1d9; }}
  .hi {{ fill: #ff6b35; font-weight: 700; }}
  .acc {{ fill: #ffd23f; font-weight: 700; }}
  .dir {{ fill: #58a6ff; font-weight: 600; }}
  .ok {{ fill: #3fb950; font-weight: 700; }}
  .title {{ fill: #8b949e; font-size: 12px; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#161230"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#302b63"/><stop offset="1" stop-color="#ff6b35"/></linearGradient>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="12" fill="url(#bg)" stroke="url(#edge)" stroke-width="1.5"/>
<rect x="1" y="1" width="{W - 2}" height="36" rx="12" fill="#161b22"/>
<rect x="1" y="25" width="{W - 2}" height="12" fill="#161b22"/>
<circle cx="24" cy="19" r="6" fill="#ff5f57"/><circle cx="44" cy="19" r="6" fill="#febc2e"/><circle cx="64" cy="19" r="6" fill="#28c840"/>
<text x="{W / 2}" y="23" text-anchor="middle" class="title">kyle@colorado: ~ (zsh)</text>
{chr(10).join(body)}
</svg>
'''
    out = Path(__file__).resolve().parent.parent / "assets" / "whoami.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
