#!/bin/bash
# Process 3 Anti-UAV videos and create videos directly (no intermediate image files)
# Author: Bob Maser
# Date: November 11, 2024

set -e

PROJECT_ROOT="/home/bobmaser/github/OpticalFlowExpansion"
INPUT_BASE="/mnt/hdd2/Bob/new_drone_db/RGB Frames/Anti-UAV/Anti-UAV-Tracking-V0"
OUTPUT_BASE="/mnt/hdd2/Bob/output_expansion_robust/videos20_18_19"
MODEL_PATH="$PROJECT_ROOT/weights/robust/robust.pth"

# Videos to process
VIDEOS=("video18" "video19" "video20")

# Model parameters (ROBUST - best for drone)
TESTRES=1
FAC=1
MAXDISP=256

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     Processing 3 Anti-UAV Videos with ROBUST Model                ║"
echo "║     Direct to Video - No Intermediate Image Files                 ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📂 Input: $INPUT_BASE"
echo "💾 Output: $OUTPUT_BASE"
echo "🤖 Model: ROBUST (optimized for UAV/drone motion)"
echo ""

# Create output directory
mkdir -p "$OUTPUT_BASE"

# Count total frames
TOTAL_FRAMES=0
for VIDEO in "${VIDEOS[@]}"; do
    FRAME_COUNT=$(ls -1 "$INPUT_BASE/$VIDEO"/*.jpg 2>/dev/null | wc -l)
    TOTAL_FRAMES=$((TOTAL_FRAMES + FRAME_COUNT))
    echo "📊 $VIDEO: $FRAME_COUNT frames"
done
echo ""
echo "📊 Total: $TOTAL_FRAMES frames across 3 videos"
echo "⚡ Estimated time: ~${TOTAL_FRAMES} seconds (~$((TOTAL_FRAMES / 60)) minutes)"
echo ""

# Process each video
VIDEO_NUM=1
for VIDEO in "${VIDEOS[@]}"; do
    echo "══════════════════════════════════════════════════════════════════════"
    echo "  Processing Video $VIDEO_NUM/3: $VIDEO"
    echo "══════════════════════════════════════════════════════════════════════"
    echo ""
    
    INPUT_DIR="$INPUT_BASE/$VIDEO"
    TEMP_OUTPUT="$OUTPUT_BASE/temp_$VIDEO"
    
    # Check if input exists
    if [ ! -d "$INPUT_DIR" ]; then
        echo "❌ Error: Input directory not found: $INPUT_DIR"
        continue
    fi
    
    FRAME_COUNT=$(ls -1 "$INPUT_DIR"/*.jpg 2>/dev/null | wc -l)
    echo "📊 Frames: $FRAME_COUNT"
    echo ""
    
    # Create temp directory
    mkdir -p "$TEMP_OUTPUT/seq"
    
    echo "⚡ Running inference with live progress..."
    echo ""
    
    # Run inference in background
    cd "$PROJECT_ROOT"
    CUDA_VISIBLE_DEVICES=0 python submission.py \
        --dataset seq \
        --datapath "$INPUT_DIR" \
        --outdir "$TEMP_OUTPUT" \
        --loadmodel "$MODEL_PATH" \
        --testres $TESTRES \
        --fac $FAC \
        --maxdisp $MAXDISP 2>&1 | grep -E "time =|jpg" | while read line; do
        if [[ "$line" == *".jpg"* ]]; then
            echo -ne "."
        fi
    done &
    
    INFERENCE_PID=$!
    
    # Monitor progress
    while kill -0 $INFERENCE_PID 2>/dev/null; do
        if [ -d "$TEMP_OUTPUT/seq" ]; then
            FILE_COUNT=$(ls -1 "$TEMP_OUTPUT/seq" 2>/dev/null | wc -l)
            FRAMES_DONE=$((FILE_COUNT / 6))
            PERCENT=$((FRAMES_DONE * 100 / FRAME_COUNT))
            
            # Progress bar
            FILLED=$((PERCENT / 2))
            BAR=$(printf "%${FILLED}s" | tr ' ' '█')
            EMPTY=$(printf "%$((50 - FILLED))s" | tr ' ' '░')
            
            echo -ne "\r  [$BAR$EMPTY] $PERCENT% ($FRAMES_DONE/$FRAME_COUNT frames)   "
        fi
        sleep 2
    done
    
    wait $INFERENCE_PID
    
    echo ""
    echo ""
    OUTPUT_COUNT=$(ls -1 "$TEMP_OUTPUT/seq" 2>/dev/null | wc -l)
    echo "✓ Inference complete: $OUTPUT_COUNT files generated"
    echo ""
    
    # Create videos directly from temp files
    echo "🎬 Creating videos @ 15 FPS..."
    echo ""
    
    cd "$PROJECT_ROOT"
    python -c "
import cv2
import glob
import numpy as np
from pathlib import Path

temp_dir = '$TEMP_OUTPUT/seq'
output_dir = '$OUTPUT_BASE'
video_name = '$VIDEO'

# Prepare file lists
flow_viz_files = sorted(glob.glob(f'{temp_dir}/visflo-*.jpg'))
warp_files = sorted(glob.glob(f'{temp_dir}/warp-*.jpg'))
exp_files = sorted(glob.glob(f'{temp_dir}/exp-*.png'))
mid_files = sorted(glob.glob(f'{temp_dir}/mid-*.png'))
flow_files = sorted(glob.glob(f'{temp_dir}/flo-*.png'))
occ_files = sorted(glob.glob(f'{temp_dir}/occ-*.png'))

def create_video_jpg(files, output_name):
    if not files:
        return
    print(f'  🎬 {output_name}...', end='', flush=True)
    img = cv2.imread(files[0])
    h, w = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{output_dir}/{video_name}_{output_name}', fourcc, 15.0, (w, h))
    for f in files:
        img = cv2.imread(f)
        if img is not None:
            out.write(img)
    out.release()
    size = Path(f'{output_dir}/{video_name}_{output_name}').stat().st_size / (1024*1024)
    print(f' ✓ {len(files)} frames, {size:.1f} MB')

def create_video_png_colormap(files, output_name, colormap):
    if not files:
        return
    print(f'  🎬 {output_name}...', end='', flush=True)
    img = cv2.imread(files[0], cv2.IMREAD_UNCHANGED)
    h, w = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{output_dir}/{video_name}_{output_name}', fourcc, 15.0, (w, h))
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is not None:
            img_norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            img_color = cv2.applyColorMap(img_norm, colormap)
            out.write(img_color)
    out.release()
    size = Path(f'{output_dir}/{video_name}_{output_name}').stat().st_size / (1024*1024)
    print(f' ✓ {len(files)} frames, {size:.1f} MB')

def create_video_png_gray(files, output_name):
    if not files:
        return
    print(f'  🎬 {output_name}...', end='', flush=True)
    img = cv2.imread(files[0])
    h, w = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{output_dir}/{video_name}_{output_name}', fourcc, 15.0, (w, h))
    for f in files:
        img = cv2.imread(f)
        if img is not None:
            out.write(img)
    out.release()
    size = Path(f'{output_dir}/{video_name}_{output_name}').stat().st_size / (1024*1024)
    print(f' ✓ {len(files)} frames, {size:.1f} MB')

# Create all 6 videos
create_video_jpg(flow_viz_files, 'flow_visualization.mp4')
create_video_jpg(warp_files, 'warped_frames.mp4')
create_video_png_colormap(exp_files, 'expansion.mp4', cv2.COLORMAP_JET)
create_video_png_colormap(mid_files, 'motion_in_depth.mp4', cv2.COLORMAP_VIRIDIS)
create_video_png_colormap(flow_files, 'optical_flow.mp4', cv2.COLORMAP_JET)
create_video_png_gray(occ_files, 'occlusion.mp4')
" 2>&1
    
    echo ""
    echo "🗑️  Cleaning up temporary files..."
    rm -rf "$TEMP_OUTPUT"
    echo "✓ Temporary files deleted"
    echo ""
    
    ((VIDEO_NUM++))
done

echo "══════════════════════════════════════════════════════════════════════"
echo "  ✓ ALL VIDEOS PROCESSED!"
echo "══════════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Output directory: $OUTPUT_BASE"
echo ""

# List all created videos
VIDEO_COUNT=$(ls -1 "$OUTPUT_BASE"/*.mp4 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$OUTPUT_BASE" 2>/dev/null | cut -f1)

echo "🎬 Generated Videos: $VIDEO_COUNT files"
echo ""
ls -lh "$OUTPUT_BASE"/*.mp4 2>/dev/null | awk '{printf "   %-40s %6s\n", $9, $5}' | sed "s|$OUTPUT_BASE/|  |"

echo ""
echo "💾 Total size: $TOTAL_SIZE"
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                  PROCESSING COMPLETE! ✓                            ║"
echo "╚════════════════════════════════════════════════════════════════════╝"


