#!/usr/bin/env python3
"""
WE.ED.IT - Intelligent AI Director for Music Videos
Main Application Entry Point

"Musik dirigiert. KI schneidet. Du kreierst."
"""

import argparse
import sys
from pathlib import Path

# Version
__version__ = "0.1.0"

def main():
    parser = argparse.ArgumentParser(
        description="WE.ED.IT - AI-powered music video creator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --analyze-song track.mp3
  %(prog)s --scan-clips ./clips/
  %(prog)s --generate track.mp3 --output ./done/
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--analyze-song",
        type=str,
        help="Analyze music file (MP3 tags, structure, emotion)"
    )
    
    parser.add_argument(
        "--scan-clips",
        type=str,
        help="Scan and index clip pool directory"
    )
    
    parser.add_argument(
        "--generate",
        type=str,
        metavar="SONG",
        help="Generate music video from song and clips"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./done/",
        help="Output directory for generated videos (default: ./done/)"
    )
    
    parser.add_argument(
        "--clips-dir",
        type=str,
        default="./clips/",
        help="Clip pool directory (default: ./clips/)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Route commands
    if args.analyze_song:
        from modules.audio_intelligence import analyze_song
        analyze_song(args.analyze_song, verbose=args.verbose)
    
    elif args.scan_clips:
        from modules.video_vault import scan_clips
        scan_clips(args.scan_clips, verbose=args.verbose)
    
    elif args.generate:
        from modules.director_cutter import generate_video
        generate_video(args.generate, args.clips_dir, args.output, verbose=args.verbose)
    
    else:
        parser.print_help()
        sys.exit(1)

def print_banner():
    """Print WE.ED.IT ASCII banner"""
    banner = """
    ██████╗ ███████╗ █████╗ ████████╗    ███████╗██╗   ██╗███╗   ██╗ ██████╗
    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝    ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
    ██████╔╝█████╗  ███████║   ██║       ███████╗ ╚████╔╝ ██╔██╗ ██║██║
    ██╔══██╗██╔══╝  ██╔══██║   ██║       ╚════██║  ╚██╔╝  ██║╚██╗██║██║
    ██████╔╝███████╗██║  ██║   ██║       ███████║   ██║   ██║ ╚████║╚██████╗
    ╚══════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
    
    Intelligent AI Director for Music Videos
    "Musik dirigiert. KI schneidet. Du kreierst."
    v{}
    """.format(__version__)
    print(banner)

if __name__ == "__main__":
    main()
