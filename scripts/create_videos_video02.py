#!/usr/bin/env python3
"""Create videos from organized optical flow outputs"""

import cv2
import glob
import numpy as np
from pathlib import Path

BASE_DIR = "/mnt/hdd2/Bob/video02_output"
VIDEO_DIR = f"{BASE_DIR}/videos"
FPS = 15

Path(VIDEO_DIR).mkdir(parents=True, exist_ok=True)

def create_video_from_jpgs(pattern, output_name):
    """Create video from JPEG files"""
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"  ⚠ No files found for {output_name}")
        return
    
    print(f"🎬 Creating {output_name}...")
    img = cv2.imread(files[0])
    height, width = img.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"{VIDEO_DIR}/{output_name}", fourcc, FPS, (width, height))
    
    for i, f in enumerate(files):
        img = cv2.imread(f)
        if img is not None:
            out.write(img)
        if (i+1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(files)} frames...", end='\r')
    
    out.release()
    size_mb = Path(f"{VIDEO_DIR}/{output_name}").stat().st_size / (1024*1024)
    print(f"  ✓ {output_name}: {len(files)} frames, {size_mb:.1f} MB")

def create_video_from_pngs_normalized(pattern, output_name, colormap=cv2.COLORMAP_JET):
    """Create video from 16-bit PNG files with normalization and color mapping"""
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"  ⚠ No files found for {output_name}")
        return
    
    print(f"🎬 Creating {output_name}...")
    img = cv2.imread(files[0], cv2.IMREAD_UNCHANGED)
    height, width = img.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"{VIDEO_DIR}/{output_name}", fourcc, FPS, (width, height))
    
    for i, f in enumerate(files):
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is not None:
            # Normalize 16-bit to 8-bit
            img_norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            # Apply colormap for better visualization
            img_color = cv2.applyColorMap(img_norm, colormap)
            out.write(img_color)
        if (i+1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(files)} frames...", end='\r')
    
    out.release()
    size_mb = Path(f"{VIDEO_DIR}/{output_name}").stat().st_size / (1024*1024)
    print(f"  ✓ {output_name}: {len(files)} frames, {size_mb:.1f} MB")

def create_video_from_pngs_grayscale(pattern, output_name):
    """Create video from 8-bit PNG files (occlusion masks)"""
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"  ⚠ No files found for {output_name}")
        return
    
    print(f"🎬 Creating {output_name}...")
    img = cv2.imread(files[0])
    height, width = img.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"{VIDEO_DIR}/{output_name}", fourcc, FPS, (width, height))
    
    for i, f in enumerate(files):
        img = cv2.imread(f)
        if img is not None:
            out.write(img)
        if (i+1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(files)} frames...", end='\r')
    
    out.release()
    size_mb = Path(f"{VIDEO_DIR}/{output_name}").stat().st_size / (1024*1024)
    print(f"  ✓ {output_name}: {len(files)} frames, {size_mb:.1f} MB")

print("=" * 70)
print("  Creating Videos @ 15 FPS")
print("=" * 70)
print()

# Create videos for each category
create_video_from_jpgs(f"{BASE_DIR}/flow_viz/*.jpg", "flow_visualization.mp4")
create_video_from_jpgs(f"{BASE_DIR}/warp/*.jpg", "warped_frames.mp4")
create_video_from_pngs_normalized(f"{BASE_DIR}/expansion/*.png", "expansion.mp4", cv2.COLORMAP_JET)
create_video_from_pngs_normalized(f"{BASE_DIR}/motion_in_depth/*.png", "motion_in_depth.mp4", cv2.COLORMAP_VIRIDIS)
create_video_from_pngs_normalized(f"{BASE_DIR}/flow/*.png", "optical_flow.mp4", cv2.COLORMAP_JET)
create_video_from_pngs_grayscale(f"{BASE_DIR}/occlusion/*.png", "occlusion.mp4")

print()
print("=" * 70)
print("  ✓ All Videos Created!")
print("=" * 70)
print()
print(f"📁 Output: {VIDEO_DIR}/")
print()

# List created videos
videos = sorted(Path(VIDEO_DIR).glob("*.mp4"))
if videos:
    print("🎬 Generated Videos:")
    for v in videos:
        size_mb = v.stat().st_size / (1024*1024)
        print(f"   - {v.name:30s} {size_mb:6.1f} MB")
    print()
    total_size = sum(v.stat().st_size for v in videos) / (1024*1024)
    print(f"   Total: {len(videos)} videos, {total_size:.1f} MB")

