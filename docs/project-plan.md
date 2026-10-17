# Project plan

Cycle 2 implementation status: see [cycle-2-progress.md](cycle-2-progress.md). The CLI baseline and hybrid now exist; a real catalog and UI remain pending. The file paths below were the initial proposal; current executable modules are listed in README.md.

## Product goal

Help someone identify a few shows they want to try using preferences they explicitly choose to share. Success means a useful, understandable shortlist, not a claim to outperform Netflix.

## MVP scope

1. A small catalog with documented source and reuse terms.
2. Manual genre, like, dislike, and watched-title inputs.
3. Five ranked suggestions, or fewer when fewer eligible candidates exist.
4. Explanations tied to real genre or text-feature overlap.
5. A simple local interface and optional feedback.

No account system, cloud database, automatic history tracking, or YouTube import is required for the MVP. Use fictional sample data until a suitable catalog source is selected. Label the UI as a demo until real show data is available. Do not label a title as currently on Netflix without region-specific, dated availability evidence.

## Proposed implementation files, to add when needed

| Future file | Responsibility |
| --- | --- |
| `app.py` | Streamlit preference form and result cards |
| `src/nextwatch/catalog.py` | Load and validate catalog records |
| `src/nextwatch/features.py` | Text and genre representations |
| `src/nextwatch/recommender.py` | Rank eligible candidate shows |
| `src/nextwatch/evaluation.py` | Baseline comparisons and ranking metrics |
| `tests/test_recommender.py` | Ranking edge cases and exclusion behavior |
| `requirements.txt` | Dependencies verified with the actual prototype |

The initial proposed layout above has been simplified: the current ranking implementation is in `nextwatch/recommender.py`, with `demo.py` and `compare.py` at the root. UI and user-quality evaluation remain planned.

## Modeling plan

Begin with a transparent genre-overlap baseline. Next fit TF-IDF on catalog descriptions and compare show vectors using cosine similarity. Build a user profile from liked titles and selected genres. Explore a subtractive dislike signal for similar candidates, but also filter explicitly disliked titles out of results. Treat unreviewed titles as unknown, not disliked.

Rewatch influence is a later experiment. Ask users whether a repeat watch reflects an enduring favorite before giving it extra weight. Cap any bonus. A repeated series name in a viewing export may represent different episodes, not a rewatch.

For a cold-start user, ask for at least a genre or a liked title. If there is no input, invite the user to provide preferences instead of pretending the results are personalized. Handle empty catalogs, unknown IDs, conflicting like/dislike inputs, and fewer than five eligible titles explicitly.

This first model is content-based recommendation. A weighted scoring formula is a heuristic, and TF-IDF similarity is not a supervised model trained on Netflix users. Learned preference weights or collaborative filtering would require suitable data and evaluation and are outside the initial scope.

## Evaluation

First validate input handling and exclusion rules. Next compare the genre baseline with text similarity using the same catalog and withheld explicit ratings. Do not use a held-out like as an input preference. Treat unlabelled recommendations as unknown; collect explicit relevance judgments on top-five lists before calculating precision@5. With incomplete judgments, report the coverage and avoid treating missing labels as negative.

Report the number of users, rated items, and limitations alongside any metric. With synthetic profiles, report software behavior only, not real-world recommendation accuracy. Small volunteer feedback sessions can assess whether explanations make sense and whether users find a show they would try; ask permission before collecting or retaining feedback.

## Semester milestones

| Cycle | Dates from onboarding packet | Proposed engineering outcome |
| --- | --- | --- |
| 1 | Sep 21-Oct 4 | Publish project scope and documentation scaffold; submit posts by Oct 3 at 11:59 p.m. per coordinator email |
| 2 | Oct 5-18 | Choose usable catalog data, implement genre baseline and TF-IDF comparison |
| 3 | Oct 19-Nov 1 | Connect a basic interface, likes/dislikes, exclusions, and explanations |
| 4 | Nov 2-15 | Try rewatch weighting, evaluate baseline comparisons, improve usability |
| 5 | Nov 16-29 | Fix issues, document setup and limitations, record a final demo; YouTube experiment only if core work is stable |
| Wrap-up | Nov 30-Dec 6 | Prepare final report and summarize actual outcomes |

Each cycle also requires five Reddit posts, five matching X posts, and one Medium article. Future exact due dates should be confirmed from coordinator messages; the packet gives check-in weeks, not specific submission times.

## Definition of a finished semester MVP

A new user can follow setup instructions, enter preferences, receive eligible recommendations with grounded explanations, and understand data sources and limitations. The repository has a license, a reproducible example, and meaningful checks for recommendation behavior. A YouTube integration is not necessary to meet this definition.
