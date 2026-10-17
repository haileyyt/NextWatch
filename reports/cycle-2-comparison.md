# Cycle 2 reproducible comparison

Fictional catalog, synthetic preferences. This demonstrates ranking behavior, not real-user quality.

Input: likes Midnight Signal; prefers mystery and science-fiction; dislikes Second Serve.

## genre

| Rank | Title | Genre | Text | Combined |
| --- | --- | --- | --- | --- |
| 1 | Harbor Frequency | 1.0000 | 0.0000 | 1.0000 |
| 2 | Quiet Evidence | 0.3333 | 0.0000 | 0.3333 |
| 3 | Orbit Nine | 0.3333 | 0.0000 | 0.3333 |
| 4 | Letters from the Coast | 0.3333 | 0.0000 | 0.3333 |
| 5 | Far Station | 0.3333 | 0.0000 | 0.3333 |

## hybrid

| Rank | Title | Genre | Text | Combined |
| --- | --- | --- | --- | --- |
| 1 | Harbor Frequency | 1.0000 | 0.3390 | 0.6695 |
| 2 | Letters from the Coast | 0.3333 | 0.2963 | 0.3148 |
| 3 | Far Station | 0.3333 | 0.2049 | 0.2691 |
| 4 | Quiet Evidence | 0.3333 | 0.0000 | 0.1667 |
| 5 | Orbit Nine | 0.3333 | 0.0000 | 0.1667 |

Genre mode does not compute text scores. The hybrid uses 0.5 genre + 0.5 text for this profile.

Weights are hand-selected, not fitted. No relevance labels or accuracy metrics were collected.

Regenerate: `python compare.py`.
