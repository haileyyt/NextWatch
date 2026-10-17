"""Produce a reproducible behavior comparison, not an accuracy benchmark."""
import json
from pathlib import Path
from nextwatch.recommender import load_catalog, recommend

ROOT = Path(__file__).resolve().parent

def main():
    shows = load_catalog(ROOT / 'data/demo_catalog.json')
    prefs = json.loads((ROOT / 'data/demo_preferences.json').read_text())
    outputs = {method: recommend(shows, prefs, method) for method in ('genre', 'hybrid')}
    lines = ['# Cycle 2 reproducible comparison', '',
             'Fictional catalog, synthetic preferences. This demonstrates ranking behavior, not real-user quality.', '',
             'Input: likes Midnight Signal; prefers mystery and science-fiction; dislikes Second Serve.', '']
    for method, output in outputs.items():
        lines += ['## ' + method, '', '| Rank | Title | Genre | Text | Combined |', '| --- | --- | --- | --- | --- |']
        for rank, row in enumerate(output['results'], 1):
            lines.append(f"| {rank} | {row['title']} | {row['genre_score']:.4f} | {row['text_score']:.4f} | {row['score']:.4f} |")
        lines.append('')
    lines += ['Genre mode does not compute text scores. The hybrid uses 0.5 genre + 0.5 text for this profile.', '',
              'Weights are hand-selected, not fitted. No relevance labels or accuracy metrics were collected.', '',
              'Regenerate: `python compare.py`.']
    folder = ROOT / 'reports'
    folder.mkdir(exist_ok=True)
    (folder / 'cycle-2-comparison.md').write_text('\n'.join(lines) + '\n')
    (folder / 'cycle-2-demo.json').write_text(json.dumps(outputs, indent=2) + '\n')
    print('Wrote reports/cycle-2-comparison.md and reports/cycle-2-demo.json')

if __name__ == '__main__':
    main()
