"""
Video Vault Module
Intelligent clip pool management and indexing

Features:
- Recursive directory scanning with symlink support
- Metadata extraction (NFO files)
- Auto-tagging based on content and filename
- JSON/Node-based database
- Non-destructive workflow (symlinks only)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class VideoVault:
    """Manages and indexes video clips"""
    
    def __init__(self, vault_dir: str, verbose=False):
        self.vault_dir = Path(vault_dir)
        self.verbose = verbose
        self.db_file = self.vault_dir / "vault.db.json"
        self.clips = []
    
    def scan_directory(self) -> List[Dict]:
        """Recursively scan directory for video files"""
        video_extensions = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv"}
        clips = []
        
        if not self.vault_dir.exists():
            if self.verbose:
                print(f"Creating vault directory: {self.vault_dir}")
            self.vault_dir.mkdir(parents=True, exist_ok=True)
            return clips
        
        for file_path in self.vault_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                clip_info = self._analyze_clip(file_path)
                clips.append(clip_info)
                if self.verbose:
                    print(f"  Found: {file_path.name}")
        
        self.clips = clips
        return clips
    
    def _analyze_clip(self, file_path: Path) -> Dict:
        """Analyze individual clip and extract metadata"""
        clip = {
            "id": hash(str(file_path)) % 10**8,
            "filename": file_path.name,
            "path": str(file_path),
            "relative_path": str(file_path.relative_to(self.vault_dir)),
            "size_mb": file_path.stat().st_size / (1024 * 1024),
            "duration": None,
            "resolution": None,
            "fps": None,
            "tags": [],
            "detected_scenes": [],
            "composition": None,
            "lighting": None,
            "emotion": None,
            "energy": None,
            "nfo_data": self._extract_nfo(file_path),
            "last_indexed": datetime.now().isoformat()
        }
        
        # Try to get video metadata
        try:
            import cv2
            cap = cv2.VideoCapture(str(file_path))
            if cap.isOpened():
                clip["fps"] = cap.get(cv2.CAP_PROP_FPS)
                clip["duration"] = cap.get(cv2.CAP_PROP_FRAME_COUNT) / clip["fps"]
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                clip["resolution"] = f"{w}x{h}"
                cap.release()
        except ImportError:
            pass
        
        # Auto-tag based on filename
        clip["tags"] = self._auto_tag(file_path.stem)
        
        return clip
    
    def _extract_nfo(self, file_path: Path) -> Optional[Dict]:
        """Extract NFO metadata file if exists"""
        nfo_path = file_path.with_suffix(".nfo")
        if nfo_path.exists():
            try:
                with open(nfo_path, "r", encoding="utf-8") as f:
                    return {"content": f.read()}
            except:
                pass
        return None
    
    def _auto_tag(self, filename: str) -> List[str]:
        """Generate tags from filename"""
        tags = []
        
        # Common tags to detect
        tag_keywords = {
            "face": ["face", "closeup", "ccu", "ecu", "mouth", "lips", "eyes"],
            "wide": ["wide", "ws", "wide_shot", "establishing"],
            "medium": ["medium", "ms", "med_shot"],
            "action": ["action", "movement", "motion", "dance", "jump", "run"],
            "slow": ["slow", "slowmo", "slo-mo", "120fps", "240fps"],
            "landscape": ["landscape", "nature", "outdoor", "sky", "water"],
            "indoor": ["indoor", "inside", "room", "studio", "home"],
            "night": ["night", "dark", "neon", "party"],
            "day": ["day", "sunlight", "bright", "daylight"],
        }
        
        filename_lower = filename.lower()
        for tag, keywords in tag_keywords.items():
            if any(kw in filename_lower for kw in keywords):
                tags.append(tag)
        
        return tags
    
    def save_database(self):
        """Save vault database to JSON"""
        db = {
            "version": 1,
            "created": datetime.now().isoformat(),
            "vault_dir": str(self.vault_dir),
            "total_clips": len(self.clips),
            "clips": self.clips
        }
        
        with open(self.db_file, "w") as f:
            json.dump(db, f, indent=2)
        
        if self.verbose:
            print(f"\n✅ Database saved: {self.db_file}")
    
    def load_database(self) -> Optional[Dict]:
        """Load vault database from JSON"""
        if self.db_file.exists():
            with open(self.db_file, "r") as f:
                return json.load(f)
        return None
    
    def search_clips(self, query: str) -> List[Dict]:
        """Search clips by tags or filename"""
        results = []
        query_lower = query.lower()
        
        for clip in self.clips:
            if (query_lower in clip["filename"].lower() or
                any(query_lower in tag for tag in clip["tags"])):
                results.append(clip)
        
        return results

def scan_clips(clips_dir: str, verbose=False):
    """Main function to scan and index clip pool"""
    vault = VideoVault(clips_dir, verbose=verbose)
    
    if verbose:
        print(f"\n🎬 Scanning clip pool: {clips_dir}")
    
    clips = vault.scan_directory()
    vault.save_database()
    
    if verbose:
        print(f"\n📊 Scan Summary:")
        print(f"  Total clips found: {len(clips)}")
        if clips:
            total_size = sum(c["size_mb"] for c in clips)
            total_duration = sum(c["duration"] or 0 for c in clips)
            print(f"  Total size: {total_size:.1f} MB")
            print(f"  Total duration: {total_duration/60:.1f} minutes")
    
    return vault
