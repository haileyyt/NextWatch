# NextWatch

A local show-recommendation prototype exploring genres and liked-show descriptions.

## Cycle 2 status

The project now has a runnable Python demo, a genre baseline, a TF-IDF hybrid ranker, explanations, and 16 passing tests. The included catalog contains 12 fictional shows, not real Netflix titles. Streaming availability is not implemented.

This is a Cline Campus Ambassador project. This update was prepared with ChatGPT/Codex; Cline-specific work will be documented separately after it occurs.

## Run locally

Use Python 3.11 or newer (tested here with Python 3.12). From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python demo.py --method genre
python demo.py --method hybrid
python -m unittest discover -s tests -v
python compare.py
```

Edit `data/demo_preferences.json` to change your inputs. Choose IDs and genres from `data/demo_catalog.json`.

```bash
python demo.py --preferences data/demo_preferences.json --top-k 3 --genre-weight 0.7
```

`--genre-weight` applies to hybrid mode when liked-show text is available. No liked-show text means genre-only fallback. Scores are ranking signals, not probabilities. Positive-score candidates only are returned, so a list can contain fewer than the requested number.

## What works

- Favorite genres and liked titles form a positive profile.
- Explicit dislikes, watched titles, and liked seed titles are excluded.
- Genre ranking uses Jaccard overlap.
- Hybrid ranking uses an adjustable blend of genre overlap and description cosine similarity.
- Explanations show actual shared genres and contributing words.
- Empty input, invalid IDs, conflicting ratings, and no matches are handled explicitly.

Dislikes do not penalize an entire genre. Rewatch counts and history imports are not supported. Unsupported preference fields are rejected rather than silently ignored.

## Files

| File | Purpose |
| --- | --- |
| `demo.py` | Command-line entry point |
| `compare.py` | Regenerates sample comparison artifacts |
| `nextwatch/recommender.py` | Validation, feature extraction, filtering, ranking |
| `tests/test_recommender.py` | 16 behavior tests |
| `data/demo_catalog.json` | 12 original fictional shows |
| `data/demo_preferences.json` | Synthetic preferences accepted by the demo |
| `reports/cycle-2-comparison.md` | Reproducible ranking comparison |
| `docs/cycle-2-progress.md` | Implemented work, limitations, and provenance |
| `docs/project-plan.md` | Roadmap |

The Cycle 1 `sample_shows.csv` and `sample_preferences.json` are historical schema sketches. Use the new `demo_*.json` files with the executable prototype; rewatch fields from the earlier sketch are not implemented.

## Next

Select a suitable real catalog, add a small UI, and evaluate with explicitly collected relevance judgments. A ranking change on synthetic data is not evidence of improved recommendation quality.

## Data and license

Fictional test records are original project material covered by the MIT license. No real viewing histories or credentials are required. Keep private data out of commits and AI prompts. Third-party datasets will need separately documented permissions. Independent of Netflix and YouTube; no affiliation with either service.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE](LICENSE).

## Technical references

- https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
