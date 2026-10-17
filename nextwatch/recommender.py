"""Genre baseline and TF-IDF hybrid; no user data leaves this process."""
import json
import math
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_catalog(path):
    shows = json.loads(Path(path).read_text())
    if not isinstance(shows, list):
        raise ValueError('Catalog must be a list.')
    seen = set()
    for show in shows:
        if not isinstance(show, dict):
            raise ValueError('Each catalog entry must be an object.')
        for key in ('show_id', 'title', 'description'):
            if not isinstance(show.get(key), str) or not show[key].strip():
                raise ValueError(f'Each show needs a nonempty {key}.')
        genres = show.get('genres')
        if not isinstance(genres, list) or not genres or any(
            not isinstance(g, str) or not g.strip() for g in genres
        ):
            raise ValueError('Each show needs a nonempty list of genres.')
        if show['show_id'] in seen:
            raise ValueError('Duplicate show ID: ' + show['show_id'])
        seen.add(show['show_id'])
    return shows


def validate_preferences(preferences, shows):
    if not isinstance(preferences, dict):
        raise ValueError('Preferences must be an object.')
    fields = ('favorite_genres', 'liked_show_ids', 'disliked_show_ids', 'watched_show_ids')
    unknown = set(preferences) - set(fields)
    if unknown:
        raise ValueError('Unsupported preference fields: ' + ', '.join(sorted(unknown)))
    p = {}
    for key in fields:
        values = preferences.get(key, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(key + ' must be a list of nonempty strings.')
        p[key] = sorted(set(values))
    ids = {s['show_id'] for s in shows}
    for key in fields[1:]:
        if set(p[key]) - ids:
            raise ValueError('Unknown show IDs in ' + key)
    if set(p['liked_show_ids']) & set(p['disliked_show_ids']):
        raise ValueError('A show cannot be both liked and disliked.')
    genres = {g for s in shows for g in s['genres']}
    if set(p['favorite_genres']) - genres:
        raise ValueError('Unknown favorite genre. Use a genre from the catalog.')
    return p


def recommend(shows, preferences, method='hybrid', top_k=5, genre_weight=0.5):
    if method not in ('genre', 'hybrid'):
        raise ValueError('Method must be genre or hybrid.')
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
        raise ValueError('top_k must be a positive integer.')
    if not isinstance(genre_weight, (float, int)) or not math.isfinite(genre_weight) or not 0 <= genre_weight <= 1:
        raise ValueError('genre_weight must be between 0 and 1.')
    if not shows:
        return {'status': 'empty_catalog', 'message': 'The catalog is empty.', 'results': []}
    p = validate_preferences(preferences, shows)
    liked = set(p['liked_show_ids'])
    positive_genres = set(p['favorite_genres'])
    for show in shows:
        if show['show_id'] in liked:
            positive_genres.update(show['genres'])
    if not positive_genres and not liked:
        return {'status': 'needs_preferences', 'message': 'Choose a genre or a liked show first.', 'results': []}

    excluded = liked | set(p['watched_show_ids']) | set(p['disliked_show_ids'])
    similarities = np.zeros(len(shows))
    shared_terms = [[] for _ in shows]
    has_text_profile = False
    if method == 'hybrid' and liked:
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            matrix = vectorizer.fit_transform([s['description'] for s in shows])
        except ValueError as error:
            if 'empty vocabulary' not in str(error):
                raise
        else:
            indices = [i for i, s in enumerate(shows) if s['show_id'] in liked]
            profile = np.asarray(matrix[indices].mean(axis=0))
            has_text_profile = bool(np.linalg.norm(profile))
            if has_text_profile:
                similarities = cosine_similarity(matrix, profile).ravel()
                terms = vectorizer.get_feature_names_out()
                for i in range(len(shows)):
                    contributions = matrix[i].toarray().ravel() * profile.ravel()
                    order = sorted(np.flatnonzero(contributions > 0), key=lambda j: (-contributions[j], terms[j]))
                    shared_terms[i] = [str(terms[j]) for j in order[:3]]

    results = []
    effective_weight = genre_weight if has_text_profile else 1.0
    for i, show in enumerate(shows):
        if show['show_id'] in excluded:
            continue
        candidate_genres = set(show['genres'])
        overlap = sorted(candidate_genres & positive_genres)
        genre_score = len(overlap) / len(candidate_genres | positive_genres)
        text_score = float(similarities[i])
        score = effective_weight * genre_score + (1 - effective_weight) * text_score
        if score <= 0:
            continue
        reasons = []
        if overlap and effective_weight > 0:
            reasons.append('Shared preferred/liked-show genres: ' + ', '.join(overlap))
        if shared_terms[i] and effective_weight < 1:
            reasons.append('Shared description terms with liked shows: ' + ', '.join(shared_terms[i]))
        results.append({
            'show_id': show['show_id'], 'title': show['title'], 'score': score,
            'genre_score': genre_score, 'text_score': text_score,
            'reasons': reasons,
        })
    results.sort(key=lambda row: (-row['score'], row['show_id']))
    return {
        'status': 'ok' if results else 'no_matches',
        'message': ('Scores are ranking signals, not liking probabilities.' if results else 'No eligible positive-score matches. Try different preferences.'),
        'method': method, 'effective_genre_weight': effective_weight,
        'results': results[:top_k],
    }
