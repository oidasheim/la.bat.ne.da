# 🎬 WE.ED.IT – Intelligent AI Director for Music Videos

**"Musik dirigiert. KI schneidet. Du kreierst."** (Music directs. AI cuts. You create.)

WE.ED.IT ist der erste intelligente KI-Regisseur für Musikvideos. Die Song ist der Director. Die Clips sind die Darsteller. Die KI ist der Cutter mit jahrelanger Musikvideo-Erfahrung.

---

## 🎯 Core Philosophy

**"Die Song gibt den Takt vor – die Clips tanzen danach."** *(The song sets the rhythm – the clips dance to it.)*

- 🎵 Music-driven editing: Every cut, transition, and effect is orchestrated by the song's structure and emotion
- 🎬 Intelligent clip matching: AI understands visual content at a semantic level
- ⚡ Professional results: Mimics seasoned music video directors' techniques
- 🖥️ Fully local & hardware-optimized: Privacy-first, works on any hardware

---

## ✨ Key Features

### 1. 🎵 Audio Intelligence
- **MP3-Tag Extraction**: Artist, Genre, BPM, Lyrics, Custom Tags
- **Song Structure Analysis**: Verse, Chorus, Bridge, Drop, Breakdown detection
- **Semantic Emotion Recognition**: Energy, Mood, Intensity curves
- **Beat, Breath & Drop Detection**: Precise timing for cuts
- **Dynamic Timeline**: Intelligent cut markers based on musical structure

### 2. 🎬 Video Vault (Clip Pool)
- **Recursive Reading** with Symlink Support – no source files are moved or changed
- **Internal JSON/Node-based Database** – organized, searchable clip library
- **NFO Metadata Extraction** – reads existing metadata and subtitle information
- **Auto-Tagging** – based on filename and content analysis
- **Non-destructive Workflow** – original files remain untouched

### 3. 🧠 Deep AI Visual Analysis
- **Shot Composition**: Wide, Medium, Close-up, Extreme Close-up (ECU) detection
- **Camera Movement**: Static, Pan, Tilt, Zoom, Tracking analysis
- **Lighting Analysis**: Key light, fill, backlighting, gels, color grading
- **Emotion & Dynamik Detection**: Visual intensity and emotional resonance
- **Export to JSON/CSV**: Structured data for further processing

### 4. 🎯 Creative Vector Logic
- **Gender Vector**: Match performer gender to artist (e.g., female rappers for female rap)
- **Style Vector**: Genre-matching and visual style alignment
- **Energy Vector**: Intensity matching between song and clips
- **Story Vector**: Narrative flow and visual continuity
- **Bidirectional Matching**: "Do you have? – Do you need?" intelligent pairing

### 5. ⚡ Professional Director's Cutter
- **Automatic Beat-Sync Cuts**: Perfectly timed to musical beats
- **Intelligent Transition Effects**: Smart blends, wipes, and creative transitions
- **Dynamic Pacing & Rhythm-Based Cuts**: Follows song's breathing and intensity
- **Face-Cut Optimization**: Maximizes viral potential with strategic close-ups

### 6. 📊 Viral Scoring & Analytics
- **Realistic Viral Scoring** (0-100 scale)
- **Concrete Improvement Tips**:
  - "More face-cuts in drop → +15% viral potential"
  - "Faster cuts in verse → +8% engagement"
  - "Better color balance → +12% watchtime"

### 7. 🖥️ Hardware & Performance
- **Hardware Detection**: CPU, GPU, RAM analysis
- **Automatic Optimization**: Scales to weak or powerful hardware
- **GPU Support**: CUDA, OpenCL, Metal acceleration
- **Memory-Efficient Processing**: Handles large video projects smoothly

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- FFmpeg
- GPU (optional but recommended)

### Installation
```bash
git clone https://github.com/oidasheim/la.bat.ne.da.git
cd la.bat.ne.da
pip install -r requirements.txt
```

### Quick Start
```bash
# Analyze your music
python weedit.py --analyze-song path/to/track.mp3

# Scan your clip pool
python weedit.py --scan-clips ./clips/

# Generate music video
python weedit.py --generate path/to/track.mp3 --output ./done/
```

---

## 📁 Directory Structure

```
la.bat.ne.da/
├── README.md
├── requirements.txt
├── weedit.py                 # Main application
├── clips/                    # Symlinked video clips
├── snd/                      # Audio/MP3 files
├── done/                     # Generated videos
└── modules/
    ├── audio_intelligence/   # Music analysis
    ├── video_vault/          # Clip pool management
    ├── ai_vision/            # Visual analysis
    ├── vector_logic/         # Semantic matching
    ├── director_cutter/      # Video editing engine
    ├── viral_scoring/        # Analytics
    └── hardware_optimizer/   # Performance tuning
```

---

## 🎓 How It Works

1. **Music Analysis**: Deep dive into song structure, BPM, emotions, and lyrical content
2. **Clip Scanning**: Index your entire video library with intelligent tagging
3. **Semantic Matching**: AI matches clips to song moments using creative vectors
4. **Intelligent Cutting**: Automatic beat-sync cuts with professional transitions
5. **Viral Optimization**: Real-time suggestions to maximize engagement
6. **Export**: 16:9 final video with versioning (no overwrites)

---

## 🔗 Related Projects

- [BeatSync-Engine](https://github.com/Merserk/BeatSync-Engine.git) – Beat detection and synchronization
- [CutClaw](https://github.com/GVCLab/CutClaw) – Intelligent video cutting patterns

---

## 📝 License

[Add your license here]

---

## 🤝 Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

---

## 💬 Feedback & Support

Have ideas? Found a bug? [Open an issue](https://github.com/oidasheim/la.bat.ne.da/issues) or start a discussion.

---

**Made with ❤️ for music video creators who dream bigger.**
