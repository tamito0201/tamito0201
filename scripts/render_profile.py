"""保存した実績データからGitHubプロフィール用SVGを再生成する。"""

from collections import defaultdict
from datetime import date
from html import escape
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
DATA = json.loads((ROOT / 'data/activity.json').read_text())
WIDTH = 1100
BG = '#0b1220'
PANEL = '#111e30'
LINE = '#24364c'
WHITE = '#f2f6fc'
MUTED = '#a7b8ce'
GREEN = '#83f2c4'
BLUE = '#82b8ff'
GOLD = '#ffd59a'


def text(x, y, value, size=20, color=WHITE, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def rect(x, y, width, height, fill, radius=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" {extra}/>'


def line(x1, y1, x2, y2, color=LINE, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" {extra}/>'


def save(name, height, title, description, parts):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
        '<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Arial, sans-serif">'
        + rect(0, 0, WIDTH, height, BG, 20)
        + ''.join(parts) + '</g></svg>\n'
    )
    (ASSETS / name).write_text(svg)


days = [day for week in DATA['weeks'] for day in week['contributionDays']]
assert sum(day['contributionCount'] for day in days) == DATA['total']
active = sum(day['contributionCount'] > 0 for day in days)
streak = longest = 0
for day in days:
    streak = streak + 1 if day['contributionCount'] else 0
    longest = max(longest, streak)
total = DATA['total']

hero = [
    '<defs><radialGradient id="glow"><stop stop-color="#15454a" stop-opacity=".8"/>'
    '<stop offset="1" stop-color="#0b1220" stop-opacity="0"/></radialGradient></defs>',
    '<ellipse cx="936" cy="225" rx="290" ry="280" fill="url(#glow)"/>',
    text(50, 49, 'TAKAOMI MURASAKI / @tamito0201', 19, GREEN, 650, 'letter-spacing="2"'),
    text(48, 144, 'Build systems.', 78, WHITE, 750),
    text(48, 239, 'Ship intelligence.', 78, GREEN, 750),
    text(52, 302, 'SOFTWARE ENGINEER  /  BACKEND & CLOUD ARCHITECT', 19, MUTED, 600),
    line(52, 331, 1048, 331),
    text(52, 369, 'Go  ·  Java  ·  Rails  ·  TypeScript  ·  Applied AI', 20, WHITE, 450),
    text(1048, 369, 'PROMARI ↗', 18, GREEN, 700, 'text-anchor="end"'),
]
for x1, y1, x2, y2 in [(842, 95, 1000, 128), (1000, 128, 935, 225), (935, 225, 1030, 280), (842, 95, 935, 225)]:
    hero.append(line(x1, y1, x2, y2, '#356270', 'stroke-width="1.4"'))
for x, y, label in [(842, 95, 'API'), (1000, 128, 'DATA'), (935, 225, 'CLOUD'), (1030, 280, 'AI')]:
    hero += [f'<circle cx="{x}" cy="{y}" r="7" fill="{GREEN}"/>', text(x, y-20, label, 14, MUTED, 600, 'text-anchor="middle"')]
save('hero.svg', 404, 'Takaomi Murasaki — Build systems. Ship intelligence.', 'Software engineer and backend/cloud architect. Go, Java, Rails, TypeScript, applied AI.', hero)

impact = [text(36, 44, 'PROVEN WORK. REAL SCALE.', 20, MUTED, 700, 'letter-spacing="2"')]
cards = [
    (28, 68, '20+', 'YEARS BUILDING SOFTWARE', 'Engineering career started in 2004', GREEN),
    (562, 68, '100Ks', 'RECORD HISTORIES', 'MySQL versioning · hundreds of thousands', BLUE),
    (28, 262, '0 → 1', 'SAAS PRODUCT LAUNCH', 'Go backend + Rails BFF · July 2024', GOLD),
    (562, 262, f'{total:,}', 'GITHUB CONTRIBUTIONS', '12 months ending Sep 29, 2026', GREEN),
]
for x, y, number, label, note, accent in cards:
    impact += [rect(x, y, 510, 176, PANEL, 12), rect(x+20, y+22, 4, 130, accent, 2),
               text(x+42, y+77, number, 62, accent, 750), text(x+43, y+115, label, 18, WHITE, 650),
               text(x+43, y+145, note, 16, MUTED)]
save('impact.svg', 464, 'Engineering impact at a glance', '20+ years building software; hundreds of thousands of record histories; a SaaS launch from zero in July 2024; 13,623 GitHub contributions in the dated 12-month snapshot.', impact)

experience = [text(42, 54, 'Technical depth, built over years.', 33, WHITE, 700),
              text(43, 87, 'Reported hands-on experience · December 22, 2025', 18, MUTED)]
skills = [('Java', 16), ('Linux', 12), ('MySQL', 8), ('AWS', 7), ('Amazon RDS', 5), ('Go', 3), ('Ruby on Rails', 3), ('TypeScript', 2)]
for year in range(0, 17, 4):
    x = 236 + year*46
    experience += [line(x, 118, x, 478), text(x, 509, year, 15, MUTED, extra='text-anchor="middle"')]
for index, (label, years) in enumerate(skills):
    y = 145 + index*44
    accent = GREEN if label in ('Java', 'Go', 'Ruby on Rails') else BLUE
    experience += [text(43, y+7, label, 20, WHITE, 550), rect(236, y-13, years*46, 24, accent, 4),
                   text(250+years*46, y+6, f'{years} yr', 17, WHITE, 650)]
experience += [text(44, 548, 'Experience overlaps across technologies; bars share a zero-based years axis.', 17, MUTED)]
save('experience.svg', 576, 'Reported technology experience', '; '.join(f'{name}: {years} years' for name, years in skills)+'. Source: professional experience record, December 22, 2025.', experience)

activity = [text(42, 52, 'A year of building.', 35, WHITE, 700),
            text(44, 84, 'GITHUB ACTIVITY / SEP 29, 2025 — SEP 29, 2026', 18, MUTED, 550)]
for x, value, label in [(44, f'{total:,}', 'CONTRIBUTIONS'), (414, str(active), 'ACTIVE DAYS'), (784, str(longest), 'LONGEST STREAK / DAYS')]:
    activity += [text(x, 160, value, 54, GREEN, 750), text(x+1, 191, label, 17, MUTED, 600)]
months = defaultdict(int)
for day in days:
    months[day['date'][:7]] += day['contributionCount']
activity += [text(44, 240, 'MONTHLY CONTRIBUTIONS', 17, WHITE, 650)]
chart_bottom = 453
chart_height = 158
scale = 3000
for count in (0, 1000, 2000, 3000):
    y = chart_bottom - count/scale*chart_height
    activity += [line(79, y, 1054, y), text(65, y+5, '0' if count == 0 else f'{count//1000}k', 13, MUTED, extra='text-anchor="end"')]
for index, (month, count) in enumerate(months.items()):
    x = 92 + index*74
    height = count/scale*chart_height
    label = date.fromisoformat(month+'-01').strftime('%b')
    partial = index in (0, len(months)-1)
    activity += [rect(x, round(chart_bottom-height, 2), 46, round(height, 2), BLUE if partial else GREEN, 4),
                 text(x+23, round(chart_bottom-height-9, 2), f'{count:,}', 14, WHITE, 550, 'text-anchor="middle"'),
                 text(x+23, 480, label+('*' if partial else ''), 14, MUTED, extra='text-anchor="middle"'),
                 text(x+23, 499, month[:4], 12, MUTED, extra='text-anchor="middle"')]
activity += [text(44, 547, 'DAILY CONTRIBUTIONS', 17, WHITE, 650)]
calendar_y = 569
colors = ['#1b2b3d', '#194e44', '#277a61', '#44b38a', GREEN]
for week_index, week in enumerate(DATA['weeks']):
    for day in week['contributionDays']:
        count = day['contributionCount']
        level = 0 if count == 0 else 1 if count < 10 else 2 if count < 30 else 3 if count < 70 else 4
        row = (date.fromisoformat(day['date']).weekday()+1)%7
        activity.append(f'<g><title>{day["date"]}: {count} contributions</title>'+rect(81+week_index*18, calendar_y+row*16, 14, 12, colors[level], 2)+'</g>')
for row, name in [(1,'Mon'), (3,'Wed'), (5,'Fri')]:
    activity.append(text(44, calendar_y+row*16+10, name, 12, MUTED))
activity.append(text(44, 716, 'Contributions / day', 15, MUTED))
for index, label in enumerate(['0', '1–9', '10–29', '30–69', '70+']):
    x = 560 + index*100
    activity += [rect(x, 702, 14, 12, colors[index], 2), text(x+22, 714, label, 14, MUTED)]
activity += [text(44, 751, '* Partial months. Counts include private contributions. Snapshot: Sep 29, 2026.', 16, MUTED),
             text(44, 780, 'Activity is one signal; engineering outcomes are documented in the case studies.', 15, MUTED)]
save('activity.svg', 808, 'GitHub contribution activity', f'{total:,} contributions across {active} active days, longest streak {longest} days. Includes private contributions. Dates {DATA["from"]} to {DATA["to"]}. Monthly and daily counts from GitHub GraphQL API.', activity)
print(f'Generated 4 SVG assets; {total:,} contributions, {active} active days, {longest}-day streak.')
