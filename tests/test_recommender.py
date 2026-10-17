import json
import tempfile
import unittest
from pathlib import Path
from nextwatch.recommender import load_catalog, recommend

ROOT = Path(__file__).resolve().parents[1]

class RecommendationTests(unittest.TestCase):
    def setUp(self):
        self.shows = load_catalog(ROOT / 'data/demo_catalog.json')
        self.p = json.loads((ROOT / 'data/demo_preferences.json').read_text())

    def test_exclusions_both_methods(self):
        self.p['disliked_show_ids'] = ['demo_004']
        self.p['watched_show_ids'] = ['demo_006']
        for method in ('genre', 'hybrid'):
            ids = {r['show_id'] for r in recommend(self.shows, self.p, method)['results']}
            self.assertFalse(ids & {'demo_001', 'demo_004', 'demo_006'})

    def test_empty_preferences(self):
        self.assertEqual(recommend(self.shows, {})['status'], 'needs_preferences')

    def test_dislikes_only_not_positive(self):
        self.assertEqual(recommend(self.shows, {'disliked_show_ids': ['demo_001']})['status'], 'needs_preferences')

    def test_conflicting_inputs(self):
        with self.assertRaises(ValueError):
            recommend(self.shows, {'liked_show_ids': ['demo_001'], 'disliked_show_ids': ['demo_001']})

    def test_unknown_ids(self):
        with self.assertRaises(ValueError):
            recommend(self.shows, {'liked_show_ids': ['missing']})

    def test_malformed_preferences(self):
        for p in ([], {'favorite_genres': 'mystery'}, {'favorite_genres': ['not-a-genre']}, {'rewatch_counts': {}}):
            with self.assertRaises(ValueError):
                recommend(self.shows, p)

    def test_empty_catalog(self):
        self.assertEqual(recommend([], {})['status'], 'empty_catalog')

    def test_all_excluded(self):
        p = {'favorite_genres': ['mystery'], 'watched_show_ids': [s['show_id'] for s in self.shows]}
        self.assertEqual(recommend(self.shows, p)['status'], 'no_matches')

    def test_genre_fallback(self):
        p = {'favorite_genres': ['mystery']}
        self.assertEqual(recommend(self.shows, p, 'genre')['results'], recommend(self.shows, p, 'hybrid')['results'])

    def test_known_jaccard_score(self):
        rows = recommend(self.shows, {'favorite_genres': ['mystery']}, 'genre', top_k=30)['results']
        row = next(r for r in rows if r['show_id'] == 'demo_001')
        self.assertAlmostEqual(row['score'], 0.5)

    def test_ties_and_short_lists(self):
        rows = recommend(self.shows, {'favorite_genres': ['comedy']}, 'genre', top_k=30)['results']
        self.assertEqual([r['show_id'] for r in rows], ['demo_002', 'demo_008'])

    def test_hybrid_uses_text(self):
        a = recommend(self.shows, self.p, 'genre')['results']
        b = recommend(self.shows, self.p, 'hybrid')['results']
        self.assertTrue(any(r['text_score'] > 0 for r in b))
        self.assertNotEqual([r['show_id'] for r in a], [r['show_id'] for r in b])

    def test_text_explanation_is_grounded(self):
        shows = [dict(show_id='a', title='A', genres=['drama'], description='orchard lantern'),
                 dict(show_id='b', title='B', genres=['drama'], description='orchard meadow')]
        row = recommend(shows, {'liked_show_ids': ['a']}, genre_weight=0)['results'][0]
        self.assertEqual(row['reasons'], ['Shared description terms with liked shows: orchard'])

    def test_stopwords_only_fallback(self):
        shows = [dict(s, description='the and or') for s in self.shows]
        self.assertEqual(recommend(shows, self.p)['effective_genre_weight'], 1)

    def test_bad_parameters(self):
        for kwargs in ({'top_k': 0}, {'method': 'unknown'}, {'genre_weight': float('nan')}, {'genre_weight': 2}):
            with self.assertRaises(ValueError):
                recommend(self.shows, self.p, **kwargs)

    def test_catalog_validation(self):
        for data in ([self.shows[0], self.shows[0]], [{'show_id': 'x'}], {'oops': []}):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'bad.json'
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_catalog(path)

if __name__ == '__main__':
    unittest.main()
