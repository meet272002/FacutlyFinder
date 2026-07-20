import numpy as np
from typing import Any, List, Dict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class FacultyComparator:
    """Compare multiple faculty profiles across research, teaching, and education dimensions."""
    FIELD_ALIASES = {
        'specialization': ['Specializations', 'specializations', 'specialization'],
        'research':       ['Researches', 'researches', 'research'],
        'teaching':       ['Teachings', 'teachings', 'teaching'],
        'education':      ['Education', 'education', 'education_field'],
        'name':           ['Name', 'name'],
        'id':             ['Faculty_id', 'id'],
    }
    def __init__(self):
        """Initialize with database cursor to fetch faculty data."""
        self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2', device="cpu")

    # ── helpers ──────────────────────────────────────────────
    def _get(self, fac: Dict, field: str, default=None):
        for key in self.FIELD_ALIASES.get(field, [field]):
            if key in fac and fac[key] is not None:
                return fac[key]
        return default

    def _get_list(self, fac: Dict, field: str) -> List[str]:
        val = self._get(fac, field, [])
        if isinstance(val, str):
            return [val] if val.strip() else []
        return [str(v).strip() for v in val if v and str(v).strip()]

    def _compare_list_field(self, faculties: List[Dict], field: str,threshold: float = 0.6) -> Dict[str, Any]:
        """Cosine-similarity comparison for a list-valued field."""
        entries = []
        for fac in faculties:
            entries.append({
                'id': self._get(fac, 'id'),
                'name': self._get(fac, 'name', 'Unknown'),
                'items': self._get_list(fac, field),
            })

        per_faculty = {e['name']: e['items'] for e in entries}

        # embed everything in one batch
        flat = [item for e in entries for item in e['items']]
        if not flat:
            return {'by_faculty': per_faculty, 'pairwise': {}}

        vectors = self.model.encode(flat, normalize_embeddings=True)
        offset, emb_map = 0, {}
        for e in entries:
            n = len(e['items'])
            emb_map[e['name']] = vectors[offset:offset + n]
            offset += n

        pairwise = {}
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                a, b = entries[i], entries[j]
                key = f"{a['name']} <-> {b['name']}"

                if not a['items'] or not b['items']:
                    pairwise[key] = {'score': 0.0, 'exact_matches': [], 'similar_pairs': []}
                    continue

                sim = cosine_similarity(emb_map[a['name']], emb_map[b['name']])

                exact = sorted(
                    {x.lower() for x in a['items']} & {y.lower() for y in b['items']}
                )

                similar = []
                for ai, a_item in enumerate(a['items']):
                    bj = int(np.argmax(sim[ai]))
                    best = float(sim[ai][bj])
                    if best >= threshold and a_item.lower() != b['items'][bj].lower():
                        similar.append({
                            'from': a_item,
                            'to': b['items'][bj],
                            'similarity': round(best, 3),
                        })
                similar.sort(key=lambda d: d['similarity'], reverse=True)

                # score = mean of each item's best match, both directions
                score = float((sim.max(axis=1).mean() + sim.max(axis=0).mean()) / 2)

                pairwise[key] = {
                    'score': round(score, 3),
                    'exact_matches': exact,
                    'similar_pairs': similar[:5],
                }

        return {'by_faculty': per_faculty, 'pairwise': pairwise}    

    def compare_specializations(self, faculties: List[Dict]) -> Dict:
        return self._compare_list_field(faculties, 'specialization', threshold=0.65)
    
    def compare_research_interests(self, faculties: List[Dict]) -> Dict:
        return self._compare_list_field(faculties, 'research', threshold=0.60)
    
    def compare_teaching_areas(self, faculties: List[Dict]) -> Dict:
        return self._compare_list_field(faculties, 'teaching', threshold=0.65)

    def generate_comparison_report(self, data: List) -> List[Dict]:
        """Fetch faculty profiles from database."""
        WEIGHTS = {'specialization': 0.45, 'research': 0.35, 'teaching': 0.20}
        faculty_data = data
        
        if len(faculty_data) < 2:
            return {
                'faculty_count': len(faculty_data),
                'error': 'At least 2 faculty required for comparison',
            }

        specialization = self.compare_specializations(faculty_data)
        research = self.compare_research_interests(faculty_data)
        teaching = self.compare_teaching_areas(faculty_data)

        overall = {}
        for pair in specialization['pairwise']:
            parts = {
                'specialization': specialization['pairwise'][pair]['score'],
                'research':       research['pairwise'].get(pair, {}).get('score', 0.0),
                'teaching':       teaching['pairwise'].get(pair, {}).get('score', 0.0),
            }
            total = sum(parts[k] * w for k, w in WEIGHTS.items())
            overall[pair] = {
                'overall_score': round(total * 100, 2),   # 0–100
                'breakdown': {k: round(v * 100, 2) for k, v in parts.items()},
            }

        return {
            'faculty_count': len(faculty_data),
            'faculty': [{
                'id': self._get(f, 'id'),
                'name': self._get(f, 'name', 'Unknown'),
            } for f in faculty_data],
            'specialization_comparison': specialization,
            'research_comparison': research,
            'teaching_comparison': teaching,
            'overall_similarity': overall,
        }
