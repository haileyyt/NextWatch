# Cycle 2 progress report

Prepared October 17, 2026, for the October 12-18 check-in window.

## Delivered in this update

- A local Python command-line prototype using 12 original fictional catalog records.
- Catalog and preference validation, stable IDs, explicit error messages.
- A genre baseline using Jaccard overlap.
- A hybrid ranker combining genre overlap and TF-IDF description cosine similarity.
- Exclusion of liked seed titles, watched titles, and explicit dislikes.
- Actual shared genres and up to three contributing description terms in explanations.
- Deterministic tie-breaking by show ID; positive-score candidates only.
- Explicit empty-catalog, empty-preference, and no-match responses.
- Genre-only fallback when there is no usable liked-show text profile.
- 16 automated tests, all passing in the authoring environment.
- Reproducible sample output and a comparison report.

## Scoring definition

The positive genre set is the union of selected genres and genres attached to liked shows. Genre score is intersection size divided by union size between that set and the candidate's genres.

TF-IDF is fitted on the catalog descriptions using English stopwords. The user text profile is the mean of the liked-show vectors. Text score is cosine similarity between that mean and each candidate. Default hybrid score is 0.5 * genre score + 0.5 * text score when a usable text profile exists; otherwise it is genre score alone. The coefficients are chosen heuristics, not learned parameters. Scores are not calibrated probabilities.

Liked seed titles are excluded even if they were not separately marked watched, to prevent simply recommending the user's input back to them. Dislikes only exclude exact titles in this version. No broader negative-preference penalty or rewatch weighting is implemented.

## Observed result

With the supplied synthetic profile, Harbor Frequency ranks first under both approaches. Letters from the Coast moves ahead of Quiet Evidence in the hybrid because of overlapping description terms. These descriptions were authored as test fixtures with deliberate overlap, so this is a behavior check, not independent evidence of model quality. See reports/cycle-2-comparison.md.

## Verification

Tested with Python 3.12, NumPy 2.3.5, and scikit-learn 1.8.0. Run `python -m unittest discover -s tests -v` from the repository root. The demo and comparison scripts were also executed successfully. A fresh installation on the user's Mac has not been tested.

## Not complete

The original Cycle 2 target included selecting a real catalog. That remains open: no real title dataset, licensed metadata source, or region-specific Netflix availability feed has been selected. The working prototype uses fictional data to exercise ranking behavior. There is no UI, user study, trained collaborative-filtering model, YouTube integration, or viewing-history importer.

## Development provenance

This implementation and its tests were prepared with ChatGPT/Codex during the October 17 session. No Cline execution or review is asserted. The ambassador should run and review the update, then complete and record an actual Cline task before describing Cline-specific observations in public content. This report is not evidence that the remote GitHub repository has been updated.

## Cycle 3 priorities

1. Select a reusable real-show data source and document its terms.
2. Add a simple preference form and recommendation cards.
3. Collect explicit relevance feedback before making quality claims.
4. Evaluate whether text similarity adds useful information on realistic descriptions.
