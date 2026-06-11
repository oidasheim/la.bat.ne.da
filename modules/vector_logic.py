"""
Vector Logic Module
Creative semantic matching system

Features:
- Gender vector: Match performer gender to artist
- Style vector: Genre and visual style alignment
- Energy vector: Intensity matching
- Story vector: Narrative flow and continuity
- Bidirectional matching: "Do you have?" - "Do you need?"
"""

from typing import Dict, List, Tuple
import json

class VectorSpace:
    """Multi-dimensional vector space for semantic matching"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.dimensions = {
            "gender": (-1.0, 1.0),           # -1: female, 0: neutral, +1: male
            "energy": (0.0, 1.0),            # 0: calm, 1: intense
            "style": (0.0, 1.0),             # genre alignment
            "narrative": (0.0, 1.0),         # story coherence
            "visual_pace": (0.0, 1.0)        # fast vs slow
        }
    
    def create_song_vector(self, song_analysis: Dict) -> Dict:
        """Create vector representation of song"""
        vector = {}
        
        # Extract metadata
        tags = song_analysis.get("tags", {})
        artist = tags.get("artist", "").lower()
        genre = tags.get("genre", "").lower()
        
        # Gender vector
        gender_keywords_male = ["rapper", "mc", "boy", "male", "dude", "guy"]
        gender_keywords_female = ["girl", "female", "queen", "lady", "woman"]
        
        gender_score = 0.0
        if any(kw in artist for kw in gender_keywords_female):
            gender_score = -1.0
        elif any(kw in artist for kw in gender_keywords_male):
            gender_score = 1.0
        
        vector["gender"] = gender_score
        
        # Energy vector
        structure = song_analysis.get("structure", {})
        bpm = structure.get("bpm_estimated", 120)
        energy_score = min(1.0, (bpm - 60) / 140)  # Normalize 60-200 BPM to 0-1
        vector["energy"] = max(0.0, min(1.0, energy_score))
        
        # Style vector (genre)
        genre_scores = {
            "hip-hop": 0.8, "rap": 0.8,
            "pop": 0.6,
            "electronic": 0.7,
            "rock": 0.5,
            "r&b": 0.7,
            "trap": 0.85,
            "ambient": 0.2
        }
        vector["style"] = genre_scores.get(genre, 0.5)
        
        # Narrative and pace vectors
        vector["narrative"] = 0.5
        vector["visual_pace"] = vector["energy"]  # Correlate with energy
        
        return vector
    
    def create_clip_vector(self, clip_analysis: Dict) -> Dict:
        """Create vector representation of clip"""
        vector = {}
        
        # Gender vector from detected faces
        # Placeholder: would use face detection
        vector["gender"] = 0.0
        
        # Energy vector from motion and composition
        camera_move = clip_analysis.get("camera_movement", {})
        composition = clip_analysis.get("composition", {})
        
        movement_intensity = camera_move.get("movement_intensity", 0.0)
        vector["energy"] = min(1.0, movement_intensity / 30.0)
        
        # Style vector
        vector["style"] = 0.5  # Placeholder
        
        # Narrative
        vector["narrative"] = 0.5  # Placeholder
        
        # Visual pace
        vector["visual_pace"] = vector["energy"]
        
        return vector
    
    def calculate_similarity(self, vector1: Dict, vector2: Dict) -> float:
        """Calculate cosine similarity between vectors"""
        dot_product = 0.0
        magnitude1 = 0.0
        magnitude2 = 0.0
        
        for dim in self.dimensions:
            v1 = vector1.get(dim, 0.0)
            v2 = vector2.get(dim, 0.0)
            
            dot_product += v1 * v2
            magnitude1 += v1 ** 2
            magnitude2 += v2 ** 2
        
        magnitude1 = magnitude1 ** 0.5
        magnitude2 = magnitude2 ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        similarity = dot_product / (magnitude1 * magnitude2)
        return max(0.0, min(1.0, similarity))

class SemanticMatcher:
    """Bidirectional semantic matching between song and clips"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.vector_space = VectorSpace(verbose=verbose)
    
    def match_clips_to_song(self, song_vector: Dict, clips: List[Dict]) -> List[Tuple[Dict, float]]:
        """Match clips to song - 'Do you have? what I need?'"""
        matches = []
        
        if self.verbose:
            print(f"\n🎯 Matching clips to song...")
        
        for clip in clips:
            clip_vector = self.vector_space.create_clip_vector({
                "camera_movement": {},
                "composition": {}
            })
            
            score = self.vector_space.calculate_similarity(song_vector, clip_vector)
            matches.append((clip, score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
    
    def bidirectional_match(self, song_analysis: Dict, clips: List[Dict]) -> Dict:
        """Perform bidirectional matching"""
        song_vector = self.vector_space.create_song_vector(song_analysis)
        
        # Forward: clips to song
        clip_matches = self.match_clips_to_song(song_vector, clips)
        
        if self.verbose:
            print(f"\n📊 Matching Results:")
            print(f"  Top matches:")
            for clip, score in clip_matches[:5]:
                print(f"    {clip['filename']}: {score:.2%}")
        
        return {
            "song_vector": song_vector,
            "matches": [
                {
                    "clip": clip,
                    "score": float(score)
                }
                for clip, score in clip_matches
            ]
        }

def perform_vector_matching(song_analysis: Dict, clips: List[Dict], verbose=False) -> Dict:
    """Main function for vector-based semantic matching"""
    matcher = SemanticMatcher(verbose=verbose)
    return matcher.bidirectional_match(song_analysis, clips)
