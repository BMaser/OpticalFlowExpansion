#!/bin/bash
# Complete workflow: Wait for inference → Organize → Create videos → Cleanup
# For Anti-UAV video01 with ROBUST model
#
# Location: /home/bobmaser/github/OpticalFlowExpansion/scripts/
# Log file: /home/bobmaser/github/OpticalFlowExpansion/logs/
# Author: Bob Maser
# Date: November 11, 2024

set -e  # Exit on error

# Project paths (Rule 2: Never use /tmp/)
PROJECT_ROOT="/home/bobmaser/github/OpticalFlowExpansion"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/video01_workflow_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

echo "======================================================================"
echo "  Complete Processing Workflow for video01 (ROBUST model)"
echo "======================================================================"
echo ""

# Paths
OUTPUT_DIR="/mnt/hdd2/Bob/output_expansion_robust"
SEQ_DIR="$OUTPUT_DIR/seq"
ORGANIZED_DIR="$OUTPUT_DIR/organized"
VIDEOS_DIR="$OUTPUT_DIR/videos"
OLD_OUTPUT="/mnt/hdd2/Bob/output_expansion"

# Expected number of files (6 types × 1,049 frame pairs)
EXPECTED_FILES=6294

echo "Step 1: Waiting for inference to complete..."
echo "-------------------------------------------------------------------"
echo "Expected files: $EXPECTED_FILES"
echo ""

# Wait for inference to complete
while true; do
    if [ -d "$SEQ_DIR" ]; then
        FILE_COUNT=$(ls "$SEQ_DIR" 2>/dev/null | wc -l)
        FRAMES=$((FILE_COUNT / 6))
        PROGRESS=$(echo "scale=1; $FRAMES * 100 / 1049" | bc)
        
        echo -ne "\rProgress: $FILE_COUNT files ($FRAMES frames, ${PROGRESS}%)   "
        
        # Check if complete (allow some margin)
        if [ "$FILE_COUNT" -ge 6288 ]; then
            echo ""
            echo "✓ Inference complete! Generated $FILE_COUNT files"
            break
        fi
        
        # Check if process is still running
        if ! pgrep -f "submission.py.*robust.pth" > /dev/null; then
            echo ""
            echo "⚠ Warning: Inference process not running. Current files: $FILE_COUNT"
            if [ "$FILE_COUNT" -lt 100 ]; then
                echo "❌ Error: Too few files generated. Something went wrong."
                exit 1
            fi
            echo "Proceeding with available files..."
            break
        fi
    else
        echo "Waiting for output directory to be created..."
    fi
    
    sleep 10
done

echo ""
echo "======================================================================"
echo "Step 2: Organizing outputs into 6 categories"
echo "======================================================================"
echo ""

cd /home/bobmaser/github/OpticalFlowExpansion/visualization_tool

# Run organize script
conda run -n opt-flow python visualize_output.py "$SEQ_DIR" --mode copy

echo ""
echo "✓ Organized outputs into:"
ls -d "$ORGANIZED_DIR"/*/ | while read dir; do
    category=$(basename "$dir")
    count=$(ls "$dir" 2>/dev/null | wc -l)
    echo "  - $category: $count files"
done

echo ""
echo "======================================================================"
echo "Step 3: Creating video clips for each category"
echo "======================================================================"
echo ""

# Create videos at 15 fps
conda run -n opt-flow python create_videos.py "$ORGANIZED_DIR" --output "$VIDEOS_DIR" --fps 15

echo ""
echo "✓ Videos created:"
ls -lh "$VIDEOS_DIR"/*.mp4 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}'

echo ""
echo "======================================================================"
echo "Step 4: Removing old output data"
echo "======================================================================"
echo ""

if [ -d "$OLD_OUTPUT" ]; then
    echo "Removing old output directory: $OLD_OUTPUT"
    OLD_SIZE=$(du -sh "$OLD_OUTPUT" 2>/dev/null | cut -f1)
    echo "Size to be freed: $OLD_SIZE"
    
    read -p "Confirm deletion? (yes/no): " CONFIRM
    if [ "$CONFIRM" = "yes" ]; then
        rm -rf "$OLD_OUTPUT"
        echo "✓ Old data removed successfully"
    else
        echo "⚠ Skipped deletion. Old data preserved at: $OLD_OUTPUT"
    fi
else
    echo "No old output directory found at: $OLD_OUTPUT"
fi

echo ""
echo "======================================================================"
echo "  WORKFLOW COMPLETE!"
echo "======================================================================"
echo ""
echo "Summary:"
echo "  Input:  1,050 frames from Anti-UAV video01"
echo "  Model:  ROBUST (optimized for aerial footage)"
echo "  Output: $OUTPUT_DIR"
echo ""
echo "Generated content:"
echo "  - Raw outputs:  $SEQ_DIR/ ($FILE_COUNT files)"
echo "  - Organized:    $ORGANIZED_DIR/ (6 categories)"
echo "  - Videos:       $VIDEOS_DIR/ (6 video clips)"
echo ""
echo "Categories:"
echo "  1. flow/           - Optical flow (flo-*.png)"
echo "  2. expansion/      - Optical expansion (exp-*.png)"
echo "  3. motion_in_depth/- Motion-in-depth (mid-*.png)"
echo "  4. occlusion/      - Occlusion masks (occ-*.png)"
echo "  5. flow_viz/       - Flow visualizations (visflo-*.jpg)"
echo "  6. warped/         - Warped frames (warp-*.jpg)"
echo ""
echo "Video clips (15 fps):"
ls "$VIDEOS_DIR"/*.mp4 2>/dev/null | xargs -n1 basename | sed 's/^/  - /'
echo ""
echo "✓ All done!"
echo "======================================================================"

