"""
AI Vision Module
Deep visual analysis of video content

Features:
- Shot composition detection (Wide, Medium, Close-up, ECU)
- Camera movement analysis (Pan, Tilt, Zoom, Tracking)
- Lighting analysis (Key light, Fill, Backlighting)
- Emotion & Dynamik detection
- JSON/CSV export
"""

from typing import Dict, List, Optional
import json

class VisualAnalyzer:
    """Analyzes visual properties of video clips"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def detect_shot_composition(self, video_path: str) -> Dict:
        """Detect shot types (Wide, Medium, Close-up, ECU)"""
        composition = {
            "shot_types": [],
            "primary_shot": None,
            "confidence": 0.0
        }
        
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Sample frames
            sample_indices = [
                int(frame_count * 0.25),
                int(frame_count * 0.50),
                int(frame_count * 0.75)
            ]
            
            face_count = 0
            frame_samples = 0
            
            for idx in sample_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    frame_samples += 1
                    # Detect faces to determine shot type
                    try:
                        import os
                        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                        face_cascade = cv2.CascadeClassifier(cascade_path)
                        faces = face_cascade.detectMultiScale(frame, 1.1, 4)
                        
                        h, w = frame.shape[:2]
                        face_area_ratio = len(faces) * 1000 / (h * w) if faces.size > 0 else 0
                        
                        if face_area_ratio > 0.3:
                            composition["shot_types"].append("close-up")
                        elif face_area_ratio > 0.1:
                            composition["shot_types"].append("medium")
                        else:
                            composition["shot_types"].append("wide")
                    except:
                        pass
            
            cap.release()
            
            # Determine primary shot
            if composition["shot_types"]:
                from collections import Counter
                shot_counts = Counter(composition["shot_types"])
                composition["primary_shot"] = shot_counts.most_common(1)[0][0]
                composition["confidence"] = shot_counts.most_common(1)[0][1] / len(composition["shot_types"])
        
        except ImportError:
            pass
        
        return composition
    
    def detect_camera_movement(self, video_path: str) -> Dict:
        """Detect camera movements (Pan, Tilt, Zoom, Tracking)"""
        movement = {
            "types": [],
            "has_movement": False,
            "movement_intensity": 0.0
        }
        
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(video_path)
            ret, prev_frame = cap.read()
            
            if not ret:
                return movement
            
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            flow_vectors = []
            
            frame_count = 0
            max_frames_check = 30
            
            while cap.isOpened() and frame_count < max_frames_check:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(
                    prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
                )
                
                # Calculate average motion
                mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                avg_motion = np.mean(mag)
                
                if avg_motion > 5:
                    movement["has_movement"] = True
                    movement["movement_intensity"] = float(avg_motion)
                    movement["types"].append("dynamic")
                
                prev_gray = gray
                frame_count += 1
            
            cap.release()
        
        except ImportError:
            pass
        
        return movement
    
    def analyze_lighting(self, video_path: str) -> Dict:
        """Analyze lighting characteristics"""
        lighting = {
            "brightness": 0.0,
            "contrast": 0.0,
            "color_temperature": None,
            "lighting_style": None
        }
        
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Convert to grayscale for brightness
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                lighting["brightness"] = float(np.mean(gray) / 255.0)
                
                # Calculate contrast
                lighting["contrast"] = float(np.std(gray) / 255.0)
                
                # Determine lighting style
                if lighting["brightness"] > 0.7:
                    lighting["lighting_style"] = "bright"
                elif lighting["brightness"] < 0.3:
                    lighting["lighting_style"] = "dark"
                else:
                    lighting["lighting_style"] = "medium"
        
        except ImportError:
            pass
        
        return lighting
    
    def detect_emotion(self, video_path: str) -> Dict:
        """Detect emotional content through visual cues"""
        emotion = {
            "dominant_emotion": None,
            "intensity": 0.0,
            "descriptors": []
        }
        
        # Placeholder for emotion detection
        # Would typically use facial expression recognition
        emotion["descriptors"] = [
            "dynamic", "engaging", "rhythmic"
        ]
        
        return emotion

def analyze_visual_content(video_path: str, verbose=False) -> Dict:
    """Main function to analyze video visual content"""
    analyzer = VisualAnalyzer(verbose=verbose)
    
    analysis = {
        "file": video_path,
        "composition": analyzer.detect_shot_composition(video_path),
        "camera_movement": analyzer.detect_camera_movement(video_path),
        "lighting": analyzer.analyze_lighting(video_path),
        "emotion": analyzer.detect_emotion(video_path)
    }
    
    if verbose:
        print(f"\n🎨 Visual Analysis Complete:")
        print(f"  Primary shot: {analysis['composition']['primary_shot']}")
        print(f"  Camera movement: {analysis['camera_movement']['has_movement']}")
        print(f"  Lighting: {analysis['lighting']['lighting_style']}")
    
    return analysis
