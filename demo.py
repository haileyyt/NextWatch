"""Run from any directory; defaults resolve relative to this file."""
import argparse
import json
from pathlib import Path
from nextwatch.recommender import load_catalog, recommend

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description='NextWatch fictional-catalog demo')
    parser.add_argument('--catalog', type=Path, default=ROOT / 'data/demo_catalog.json')
    parser.add_argument('--preferences', type=Path, default=ROOT / 'data/demo_preferences.json')
    parser.add_argument('--method', choices=['genre', 'hybrid'], default='hybrid')
    parser.add_argument('--top-k', type=int, default=5)
    parser.add_argument('--genre-weight', type=float, default=0.5)
    args = parser.parse_args()
    try:
        result = recommend(load_catalog(args.catalog), json.loads(args.preferences.read_text()), args.method, args.top_k, args.genre_weight)
    except (ValueError, OSError) as error:
        parser.exit(2, f'Input error: {error}\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
