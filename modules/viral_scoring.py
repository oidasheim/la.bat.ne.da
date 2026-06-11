"""
Viral Scoring & Analytics Module
Realistic scoring and improvement suggestions

Features:
- Viral scoring (0-100 scale)
- Concrete improvement tips with impact predictions
- Engagement metrics
- Watchtime predictions
"""

from typing import Dict, List

class ViralScorer:
    """Calculates viral potential and engagement metrics"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def calculate_viral_score(self, editing_plan: Dict, song_analysis: Dict, clips: List[Dict]) -> Dict:
        """Calculate realistic viral potential score (0-100)"""
        score_components = {
            "face_cuts": self._score_face_cuts(editing_plan),
            "pacing": self._score_pacing(editing_plan),
            "transitions": self._score_transitions(editing_plan),
            "music_sync": self._score_music_sync(song_analysis),
            "visual_variety": self._score_visual_variety(clips)
        }
        
        # Weighted average
        weights = {
            "face_cuts": 0.25,
            "pacing": 0.20,
            "transitions": 0.15,
            "music_sync": 0.25,
            "visual_variety": 0.15
        }
        
        total_score = sum(
            score_components[key] * weights[key]
            for key in score_components
        )
        
        return {
            "overall_score": min(100, max(0, total_score)),
            "components": score_components,
            "category": self._categorize_score(total_score)
        }
    
    def _score_face_cuts(self, editing_plan: Dict) -> float:
        """Score effectiveness of face-cut placement"""
        face_cuts = editing_plan.get("face_cuts", [])
        total_cuts = len(editing_plan.get("cut_points", []))
        
        face_cut_ratio = len(face_cuts) / total_cuts if total_cuts > 0 else 0
        
        # Optimal range: 20-30%
        if 0.2 <= face_cut_ratio <= 0.3:
            return 85.0
        elif 0.15 <= face_cut_ratio <= 0.4:
            return 70.0
        else:
            return 50.0
    
    def _score_pacing(self, editing_plan: Dict) -> float:
        """Score pacing and rhythm"""
        pacing = editing_plan.get("pacing", {})
        cut_frequency = pacing.get("cut_frequency", 0)
        
        # Optimal: 0.3-0.5 cuts per second
        if 0.3 <= cut_frequency <= 0.5:
            return 85.0
        elif 0.2 <= cut_frequency <= 0.8:
            return 70.0
        else:
            return 50.0
    
    def _score_transitions(self, editing_plan: Dict) -> float:
        """Score transition quality and variety"""
        transitions = editing_plan.get("transitions", [])
        
        if not transitions:
            return 50.0
        
        # Check for variety
        transition_types = [t.get("type") for t in transitions]
        unique_types = len(set(transition_types))
        
        variety_score = min(100, (unique_types / 3) * 100)
        
        return 60 + (variety_score * 0.4)
    
    def _score_music_sync(self, song_analysis: Dict) -> float:
        """Score music synchronization quality"""
        events = song_analysis.get("events", [])
        beat_count = len([e for e in events if e.get("type") == "beat"])
        
        if beat_count > 50:
            return 80.0
        elif beat_count > 20:
            return 70.0
        else:
            return 50.0
    
    def _score_visual_variety(self, clips: List[Dict]) -> float:
        """Score visual diversity in clip pool"""
        if not clips:
            return 0.0
        
        # Collect all tags
        all_tags = []
        for clip in clips:
            all_tags.extend(clip.get("tags", []))
        
        unique_tags = len(set(all_tags))
        total_tag_slots = len(clips) * 2
        
        variety = min(100, (unique_tags / 10) * 100)
        return variety
    
    def _categorize_score(self, score: float) -> str:
        """Categorize viral score"""
        if score >= 80:
            return "Very High Viral Potential"
        elif score >= 65:
            return "High Viral Potential"
        elif score >= 50:
            return "Moderate Viral Potential"
        elif score >= 35:
            return "Low Viral Potential"
        else:
            return "Needs Improvement"
    
    def generate_improvement_tips(self, score_components: Dict) -> List[Dict]:
        """Generate concrete, actionable improvement tips"""
        tips = []
        
        # Face-cuts optimization
        face_cut_score = score_components.get("face_cuts", 0)
        if face_cut_score < 70:
            tips.append({
                "category": "Face-Cuts",
                "suggestion": "Increase face-cut frequency in drop sections",
                "expected_impact": "+15% viral potential",
                "priority": "high"
            })
        
        # Pacing
        pacing_score = score_components.get("pacing", 0)
        if pacing_score < 70:
            tips.append({
                "category": "Pacing",
                "suggestion": "Accelerate cuts during high-energy verses",
                "expected_impact": "+8% engagement",
                "priority": "high"
            })
        
        # Transitions
        transition_score = score_components.get("transitions", 0)
        if transition_score < 70:
            tips.append({
                "category": "Transitions",
                "suggestion": "Use more varied transition effects",
                "expected_impact": "+12% watchtime",
                "priority": "medium"
            })
        
        # Music sync
        music_sync_score = score_components.get("music_sync", 0)
        if music_sync_score < 70:
            tips.append({
                "category": "Music Sync",
                "suggestion": "Strengthen beat-sync cuts at drop points",
                "expected_impact": "+10% emotional impact",
                "priority": "high"
            })
        
        # Visual variety
        variety_score = score_components.get("visual_variety", 0)
        if variety_score < 70:
            tips.append({
                "category": "Visual Variety",
                "suggestion": "Add more diverse shot types and compositions",
                "expected_impact": "+20% viewer retention",
                "priority": "high"
            })
        
        return tips

def score_video_viral_potential(editing_plan: Dict, song_analysis: Dict, clips: List[Dict], verbose=False) -> Dict:
    """Main function for viral scoring"""
    scorer = ViralScorer(verbose=verbose)
    
    viral_analysis = scorer.calculate_viral_score(editing_plan, song_analysis, clips)
    improvement_tips = scorer.generate_improvement_tips(viral_analysis["components"])
    
    if verbose:
        print(f"\n📊 Viral Score Analysis:")
        print(f"  Overall Score: {viral_analysis['overall_score']:.1f}/100")
        print(f"  Category: {viral_analysis['category']}")
        print(f"\n💡 Improvement Tips:")
        for tip in improvement_tips:
            print(f"  [{tip['priority'].upper()}] {tip['category']}")
            print(f"    → {tip['suggestion']}")
            print(f"    Expected: {tip['expected_impact']}")
    
    return {
        "viral_analysis": viral_analysis,
        "improvement_tips": improvement_tips
    }
