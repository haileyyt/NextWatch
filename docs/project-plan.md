# NextWatch Project Plan

## Goal

Build a small, understandable recommendation platform that helps users discover shows based on preferences they choose to share.

The first version should demonstrate a complete flow from entering preferences to receiving a useful shortlist of recommendations.

## Initial user flow

1. Select favorite genres.
2. Identify shows the user likes, dislikes, or has already watched.
3. Request recommendations.
4. View up to five eligible suggestions with brief explanations.
5. Optionally provide feedback on the results.

## Minimum viable product

The first working version will include:

- A small show catalog with documented sources and reuse permissions.
- Manual preference inputs.
- A basic recommendation method.
- Filtering for explicitly disliked and already-watched titles.
- Explanations grounded in actual matching features.
- A simple local interface.

Account connections, automatic viewing-history collection, and YouTube integration are outside the initial scope.

## Recommendation approach

### Step 1: Genre baseline

Start with a transparent ranking method based on overlap between user preferences and show genres.

This provides an understandable baseline for comparing later approaches.

### Step 2: Description similarity

Explore TF-IDF features from show descriptions and cosine similarity.

Use descriptions of liked shows to help identify similar candidates. Evaluate whether these suggestions are more useful than the genre baseline.

### Step 3: Additional preference signals

Experiment with the influence of dislikes and self-reported rewatch preferences.

Unseen shows should remain distinct from disliked shows. Rewatch influence should be limited so a single favorite does not dominate every recommendation.

## Important behaviors to handle

- Ask for preferences when a user has not supplied any.
- Resolve conflicting inputs, such as marking a show both liked and disliked.
- Exclude already-watched and explicitly disliked titles.
- Return fewer than five suggestions when too few eligible titles remain.
- Handle unknown titles and missing catalog information.
- Avoid presenting a similarity score as a probability that a user will like a show.

## Data plan

Begin with synthetic examples while selecting a suitable real show catalog.

Before incorporating a dataset, document:

- Source URL.
- Retrieval date.
- License or reuse terms.
- Attribution requirements.
- Whether redistribution is permitted.
- Available metadata fields.

Do not assume historical Netflix catalog membership establishes current availability.

Personal viewing histories must remain outside the public repository.

## Planned implementation files

These files will be added when implementation begins:

| File | Responsibility |
| --- | --- |
| `app.py` | Preference inputs and recommendation interface |
| `src/nextwatch/catalog.py` | Catalog loading and validation |
| `src/nextwatch/features.py` | Genre and description features |
| `src/nextwatch/recommender.py` | Candidate filtering and ranking |
| `tests/test_recommender.py` | Meaningful checks for recommendation behavior |
| `requirements.txt` | Dependencies verified with the prototype |

## Semester roadmap

### Cycle 1: September 21–October 4

- Define the project and initial scope.
- Create the public repository.
- Document the proposed approach.
- Publish introductory content about the planned project.

### Cycle 2: October 5–18

- Select suitable catalog data.
- Implement the genre baseline.
- Explore description similarity.
- Check basic input and filtering behavior.

### Cycle 3: October 19–November 1

- Build a simple interface.
- Connect preference inputs to recommendation results.
- Add explanations for suggested shows.

### Cycle 4: November 2–15

- Compare recommendation approaches.
- Explore rewatch preferences.
- Collect a small amount of voluntary feedback.
- Improve usability and address weak recommendations.

### Cycle 5: November 16–29

- Fix remaining issues.
- Finalize setup instructions and limitations.
- Prepare a demonstration.
- Explore optional YouTube signals only if the core application is stable.

### Wrap-up: November 30–December 6

- Prepare the final project report.
- Summarize actual results and lessons learned.
- Document possible future improvements.

These are proposed development targets. Exact content submission deadlines will follow coordinator instructions.

## Planned use of Cline

Use Cline to discuss and implement focused tasks, including catalog structure, recommendation logic, interface components, and debugging.

For each task:

1. Define the goal and discuss the approach.
2. Implement a small, reviewable change.
3. Review the generated code.
4. Check the relevant behavior.
5. Record actual outcomes and remaining limitations.

Public updates should distinguish planned features from completed work and describe only development experiences that actually occurred.

## Evaluation

First verify that the application handles inputs and exclusions correctly.

Then compare the genre baseline and description-based approach using the same catalog and explicitly collected relevance judgments. Keep evaluation preferences separate from the preferences used to generate recommendations.

Synthetic examples can demonstrate software behavior but cannot establish real-world recommendation quality.

## Definition of a finished first version

A new user can follow the setup instructions, enter preferences, and receive eligible recommendations with understandable explanations.

The repository documents its data sources, technical approach, and limitations. YouTube integration is not required for the first version to be complete.