#!/bin/bash
# Process Anti-UAV video02 with organized outputs and progress display
# Author: Bob Maser
# Date: November 11, 2024

set -e

PROJECT_ROOT="/home/bobmaser/github/OpticalFlowExpansion"
INPUT_DIR="/mnt/hdd2/ura1/database/RGB Frames/Anti-UAV/Anti-UAV-Tracking-V0/video02"
BASE_OUTPUT_DIR="/mnt/hdd2/Bob/video02_output"
MODEL_PATH="$PROJECT_ROOT/weights/robust/robust.pth"
TEMP_OUTPUT="$BASE_OUTPUT_DIR/temp_output"

# Model parameters (ROBUST - best for drone/UAV motion)
TESTRES=1
FAC=1
MAXDISP=256

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         Processing Anti-UAV video02 with ROBUST Model             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📂 Source: $INPUT_DIR"
echo "💾 Output: $BASE_OUTPUT_DIR"
echo "🤖 Model: ROBUST (optimized for UAV/drone motion)"
echo ""

# Count frames
FRAME_COUNT=$(ls -1 "$INPUT_DIR"/*.jpg 2>/dev/null | wc -l)
echo "📊 Total frames: $FRAME_COUNT"
echo "⚡ Expected processing time: ~2-3 minutes"
echo ""

# Create temporary output directory
mkdir -p "$TEMP_OUTPUT/seq"

echo "══════════════════════════════════════════════════════════════════════"
echo "  STEP 1/3: Running Optical Flow Inference"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

# Run inference with progress monitoring in background
cd "$PROJECT_ROOT"
CUDA_VISIBLE_DEVICES=0 python submission.py \
    --dataset seq \
    --datapath "$INPUT_DIR" \
    --outdir "$TEMP_OUTPUT" \
    --loadmodel "$MODEL_PATH" \
    --testres $TESTRES \
    --fac $FAC \
    --maxdisp $MAXDISP &

INFERENCE_PID=$!

# Monitor progress while inference runs
echo "⚡ Processing frames... (showing live progress)"
echo ""

while kill -0 $INFERENCE_PID 2>/dev/null; do
    if [ -d "$TEMP_OUTPUT/seq" ]; then
        FILE_COUNT=$(ls -1 "$TEMP_OUTPUT/seq" 2>/dev/null | wc -l)
        FRAMES_DONE=$((FILE_COUNT / 6))
        PERCENT=$((FRAMES_DONE * 100 / FRAME_COUNT))
        
        # Progress bar
        FILLED=$((PERCENT / 2))
        BAR=$(printf "%${FILLED}s" | tr ' ' '█')
        EMPTY=$(printf "%$((50 - FILLED))s" | tr ' ' '░')
        
        echo -ne "\r  [${BAR}${EMPTY}] ${PERCENT}% ($FRAMES_DONE/$FRAME_COUNT frames)   "
    fi
    sleep 1
done

# Wait for process to complete
wait $INFERENCE_PID

echo ""
echo ""
echo "✓ Inference completed!"
echo ""

# Verify output
OUTPUT_COUNT=$(ls -1 "$TEMP_OUTPUT/seq" 2>/dev/null | wc -l)
echo "📦 Generated $OUTPUT_COUNT files"
echo ""

echo "══════════════════════════════════════════════════════════════════════"
echo "  STEP 2/3: Organizing Outputs by Category"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

# Create organized directories
mkdir -p "$BASE_OUTPUT_DIR/flow"
mkdir -p "$BASE_OUTPUT_DIR/expansion"
mkdir -p "$BASE_OUTPUT_DIR/motion_in_depth"
mkdir -p "$BASE_OUTPUT_DIR/occlusion"
mkdir -p "$BASE_OUTPUT_DIR/flow_viz"
mkdir -p "$BASE_OUTPUT_DIR/warp"

echo "📁 Organizing files..."

# Move files to respective directories
mv "$TEMP_OUTPUT/seq"/flo-*.png "$BASE_OUTPUT_DIR/flow/" 2>/dev/null || true
mv "$TEMP_OUTPUT/seq"/exp-*.png "$BASE_OUTPUT_DIR/expansion/" 2>/dev/null || true
mv "$TEMP_OUTPUT/seq"/mid-*.png "$BASE_OUTPUT_DIR/motion_in_depth/" 2>/dev/null || true
mv "$TEMP_OUTPUT/seq"/occ-*.png "$BASE_OUTPUT_DIR/occlusion/" 2>/dev/null || true
mv "$TEMP_OUTPUT/seq"/visflo-*.jpg "$BASE_OUTPUT_DIR/flow_viz/" 2>/dev/null || true
mv "$TEMP_OUTPUT/seq"/warp-*.jpg "$BASE_OUTPUT_DIR/warp/" 2>/dev/null || true

# Count files in each category
FLOW_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/flow" 2>/dev/null | wc -l)
EXP_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/expansion" 2>/dev/null | wc -l)
MID_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/motion_in_depth" 2>/dev/null | wc -l)
OCC_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/occlusion" 2>/dev/null | wc -l)
VIZ_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/flow_viz" 2>/dev/null | wc -l)
WARP_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/warp" 2>/dev/null | wc -l)

echo "✓ Files organized:"
echo "  ├─ flow/             $FLOW_COUNT files"
echo "  ├─ expansion/        $EXP_COUNT files"
echo "  ├─ motion_in_depth/  $MID_COUNT files"
echo "  ├─ occlusion/        $OCC_COUNT files"
echo "  ├─ flow_viz/         $VIZ_COUNT files"
echo "  └─ warp/             $WARP_COUNT files"
echo ""

# Clean up temp directory
rm -rf "$TEMP_OUTPUT"

echo "══════════════════════════════════════════════════════════════════════"
echo "  STEP 3/3: Creating Videos (FPS=15)"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

# Create videos directory
mkdir -p "$BASE_OUTPUT_DIR/videos"

# Function to create video from images
create_video() {
    local INPUT_PATTERN="$1"
    local OUTPUT_VIDEO="$2"
    local CATEGORY="$3"
    
    echo "🎬 Creating video: $CATEGORY..."
    
    cd "$PROJECT_ROOT"
    python -c "
import cv2
import glob
import numpy as np
from pathlib import Path

pattern = '$INPUT_PATTERN'
output = '$OUTPUT_VIDEO'

files = sorted(glob.glob(pattern))
if not files:
    print('  ⚠ No files found')
    exit(1)

# Read first image to get dimensions
img = cv2.imread(files[0])
if img is None:
    print('  ⚠ Could not read first image')
    exit(1)

height, width = img.shape[:2]

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output, fourcc, 15.0, (width, height))

for i, f in enumerate(files):
    img = cv2.imread(f)
    if img is not None:
        out.write(img)
    if (i+1) % 10 == 0:
        print(f'  Processing frame {i+1}/{len(files)}...', end='\r')

out.release()
print(f'  ✓ Created: {Path(output).name} ({len(files)} frames)          ')
" || echo "  ✗ Failed to create video"
}

# Create videos for each category
create_video "$BASE_OUTPUT_DIR/flow_viz/*.jpg" "$BASE_OUTPUT_DIR/videos/flow_visualization.mp4" "Flow Visualization"
create_video "$BASE_OUTPUT_DIR/warp/*.jpg" "$BASE_OUTPUT_DIR/videos/warped_frames.mp4" "Warped Frames"

# For PNG files, need to convert or use different approach
echo "🎬 Creating video: Expansion..."
python -c "
import cv2
import glob
import numpy as np

files = sorted(glob.glob('$BASE_OUTPUT_DIR/expansion/*.png'))
if files:
    img = cv2.imread(files[0], cv2.IMREAD_UNCHANGED)
    height, width = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('$BASE_OUTPUT_DIR/videos/expansion.mp4', fourcc, 15.0, (width, height))
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is not None:
            # Normalize 16-bit to 8-bit for video
            img_norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            img_color = cv2.applyColorMap(img_norm, cv2.COLORMAP_JET)
            out.write(img_color)
    out.release()
    print(f'  ✓ Created: expansion.mp4 ({len(files)} frames)')
" || echo "  ⚠ Could not create expansion video"

echo "🎬 Creating video: Motion-in-Depth..."
python -c "
import cv2
import glob
import numpy as np

files = sorted(glob.glob('$BASE_OUTPUT_DIR/motion_in_depth/*.png'))
if files:
    img = cv2.imread(files[0], cv2.IMREAD_UNCHANGED)
    height, width = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('$BASE_OUTPUT_DIR/videos/motion_in_depth.mp4', fourcc, 15.0, (width, height))
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is not None:
            img_norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            img_color = cv2.applyColorMap(img_norm, cv2.COLORMAP_VIRIDIS)
            out.write(img_color)
    out.release()
    print(f'  ✓ Created: motion_in_depth.mp4 ({len(files)} frames)')
" || echo "  ⚠ Could not create motion_in_depth video"

echo "🎬 Creating video: Occlusion..."
python -c "
import cv2
import glob

files = sorted(glob.glob('$BASE_OUTPUT_DIR/occlusion/*.png'))
if files:
    img = cv2.imread(files[0])
    height, width = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('$BASE_OUTPUT_DIR/videos/occlusion.mp4', fourcc, 15.0, (width, height))
    for f in files:
        img = cv2.imread(f)
        if img is not None:
            out.write(img)
    out.release()
    print(f'  ✓ Created: occlusion.mp4 ({len(files)} frames)')
" || echo "  ⚠ Could not create occlusion video"

echo ""
VIDEO_COUNT=$(ls -1 "$BASE_OUTPUT_DIR/videos"/*.mp4 2>/dev/null | wc -l)
echo "✓ Created $VIDEO_COUNT videos in: $BASE_OUTPUT_DIR/videos/"
echo ""

echo "══════════════════════════════════════════════════════════════════════"
echo "  ✓ PROCESSING COMPLETE!"
echo "══════════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Output Structure:"
echo "   $BASE_OUTPUT_DIR/"
echo "   ├── flow/              ($FLOW_COUNT files)"
echo "   ├── expansion/         ($EXP_COUNT files)"
echo "   ├── motion_in_depth/   ($MID_COUNT files)"
echo "   ├── occlusion/         ($OCC_COUNT files)"
echo "   ├── flow_viz/          ($VIZ_COUNT files)"
echo "   ├── warp/              ($WARP_COUNT files)"
echo "   └── videos/            ($VIDEO_COUNT videos @ 15 FPS)"
echo ""

if [ -d "$BASE_OUTPUT_DIR/videos" ]; then
    echo "🎬 Generated Videos:"
    ls -lh "$BASE_OUTPUT_DIR/videos"/*.mp4 | awk '{print "   " $9 " (" $5 ")"}'
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                     ALL DONE! ✓                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"

