#!/bin/bash
# Batch Process All Sequences with ROBUST Model
# Author: Bob Maser
# Date: November 11, 2024
#
# This script processes all available sequences with the ROBUST model,
# organizes outputs, and creates videos automatically.

set -e  # Exit on error

echo "======================================================================"
echo "  BATCH PROCESSING ALL SEQUENCES WITH ROBUST MODEL"
echo "======================================================================"
echo ""

# Configuration
PROJECT_ROOT="/home/bobmaser/github/OpticalFlowExpansion"
INPUT_BASE="/mnt/hdd2/ura1/database/RGB Frames"
OUTPUT_BASE="/mnt/hdd2/Bob/robust_outputs"
MODEL_PATH="$PROJECT_ROOT/weights/robust/robust.pth"
LOG_DIR="$PROJECT_ROOT/logs"
CUDA_DEVICE=0

# Model parameters
TESTRES=1
FAC=1
MAXDISP=256

# Create necessary directories
mkdir -p "$OUTPUT_BASE"
mkdir -p "$LOG_DIR"

# Get current timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
MASTER_LOG="$LOG_DIR/batch_process_${TIMESTAMP}.log"

echo "Configuration:" | tee -a "$MASTER_LOG"
echo "  - Model: ROBUST (mixed datasets)" | tee -a "$MASTER_LOG"
echo "  - Input base: $INPUT_BASE" | tee -a "$MASTER_LOG"
echo "  - Output base: $OUTPUT_BASE" | tee -a "$MASTER_LOG"
echo "  - GPU: $CUDA_DEVICE" | tee -a "$MASTER_LOG"
echo "  - Log: $MASTER_LOG" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Array to track processing results
declare -a SUCCESSFUL=()
declare -a FAILED=()

# Function to process a single sequence
process_sequence() {
    local SEQ_NAME="$1"
    local INPUT_DIR="$2"
    local OUTPUT_NAME="$3"
    
    echo "======================================================================"
    echo "  Processing: $SEQ_NAME"
    echo "======================================================================"
    
    local SEQ_OUTPUT="$OUTPUT_BASE/$OUTPUT_NAME"
    local SEQ_DIR="$SEQ_OUTPUT/seq"
    local ORGANIZED_DIR="$SEQ_OUTPUT/organized"
    local VIDEOS_DIR="$SEQ_OUTPUT/videos"
    
    # Count frames
    local FRAME_COUNT=$(ls -1 "$INPUT_DIR"/*.jpg 2>/dev/null | wc -l)
    echo "Frames: $FRAME_COUNT"
    
    if [ "$FRAME_COUNT" -lt 2 ]; then
        echo "❌ Error: Not enough frames (need at least 2)"
        FAILED+=("$SEQ_NAME")
        return 1
    fi
    
    # Step 1: Run inference
    echo ""
    echo "Step 1/4: Running optical flow inference..."
    echo "-------------------------------------------------------------------"
    
    local START_TIME=$(date +%s)
    
    cd "$PROJECT_ROOT"
    CUDA_VISIBLE_DEVICES=$CUDA_DEVICE python submission.py \
        --dataset seq \
        --datapath "$INPUT_DIR" \
        --outdir "$SEQ_OUTPUT" \
        --loadmodel "$MODEL_PATH" \
        --testres $TESTRES \
        --fac $FAC \
        --maxdisp $MAXDISP \
        2>&1 | tee -a "$LOG_DIR/${OUTPUT_NAME}_inference.log"
    
    if [ $? -ne 0 ]; then
        echo "❌ Error: Inference failed for $SEQ_NAME"
        FAILED+=("$SEQ_NAME")
        return 1
    fi
    
    local END_TIME=$(date +%s)
    local DURATION=$((END_TIME - START_TIME))
    echo "✓ Inference completed in ${DURATION}s"
    
    # Verify output files
    local OUTPUT_COUNT=$(ls -1 "$SEQ_DIR" 2>/dev/null | wc -l)
    local EXPECTED_COUNT=$((FRAME_COUNT * 6))  # 6 output types per frame pair
    
    echo "Generated: $OUTPUT_COUNT files (expected ~$EXPECTED_COUNT)"
    
    if [ "$OUTPUT_COUNT" -lt $((EXPECTED_COUNT / 2)) ]; then
        echo "⚠ Warning: Fewer files than expected"
    fi
    
    # Step 2: Organize outputs
    echo ""
    echo "Step 2/4: Organizing outputs by type..."
    echo "-------------------------------------------------------------------"
    
    cd "$PROJECT_ROOT/visualization_tool"
    python visualize_output.py "$SEQ_DIR" --mode copy \
        2>&1 | tee -a "$LOG_DIR/${OUTPUT_NAME}_organize.log"
    
    if [ $? -ne 0 ]; then
        echo "⚠ Warning: Organization failed, but continuing..."
    else
        echo "✓ Outputs organized"
    fi
    
    # Step 3: Create videos
    echo ""
    echo "Step 3/4: Creating videos..."
    echo "-------------------------------------------------------------------"
    
    python create_videos.py "$ORGANIZED_DIR" --fps 15 --output-dir "$VIDEOS_DIR" \
        2>&1 | tee -a "$LOG_DIR/${OUTPUT_NAME}_videos.log"
    
    if [ $? -ne 0 ]; then
        echo "⚠ Warning: Video creation failed"
    else
        echo "✓ Videos created"
    fi
    
    # Step 4: Summary
    echo ""
    echo "Step 4/4: Summary for $SEQ_NAME"
    echo "-------------------------------------------------------------------"
    echo "Output directory: $SEQ_OUTPUT"
    echo "  ├── seq/         (raw outputs: $OUTPUT_COUNT files)"
    echo "  ├── organized/   (categorized)"
    echo "  └── videos/      (MP4 videos)"
    
    if [ -d "$VIDEOS_DIR" ]; then
        local VIDEO_COUNT=$(ls -1 "$VIDEOS_DIR"/*.mp4 2>/dev/null | wc -l)
        echo ""
        echo "Generated $VIDEO_COUNT videos:"
        ls -1 "$VIDEOS_DIR"/*.mp4 2>/dev/null | sed 's/^/    - /'
    fi
    
    echo ""
    echo "✓ Processing completed for $SEQ_NAME in ${DURATION}s"
    SUCCESSFUL+=("$SEQ_NAME")
    
    return 0
}

# Main processing loop
echo "======================================================================"
echo "  STARTING BATCH PROCESSING"
echo "======================================================================"
echo ""

TOTAL_START=$(date +%s)

# Process numbered sequences (10, 29, 121, 186, 208, 217)
NUMBERED_SEQUENCES=("10 - RGB" "29 - RGB" "121 - RGB" "186 - RGB" "208 - RGB" "217 - RGB")

for SEQ in "${NUMBERED_SEQUENCES[@]}"; do
    INPUT_DIR="$INPUT_BASE/$SEQ"
    OUTPUT_NAME=$(echo "$SEQ" | sed 's/ - RGB//')
    
    echo ""
    echo "======================================================================"
    echo "  Sequence: $SEQ"
    echo "======================================================================"
    
    if [ ! -d "$INPUT_DIR" ]; then
        echo "❌ Error: Directory not found: $INPUT_DIR"
        FAILED+=("$SEQ")
        continue
    fi
    
    process_sequence "$SEQ" "$INPUT_DIR" "seq_${OUTPUT_NAME}" || true
    
    echo ""
    echo "Waiting 5 seconds before next sequence..."
    sleep 5
done

# Process Anti-UAV videos
echo ""
echo "======================================================================"
echo "  Processing Anti-UAV Videos (20 sequences)"
echo "======================================================================"
echo ""

for i in $(seq -f "%02g" 1 20); do
    VIDEO_NAME="video${i}"
    INPUT_DIR="$INPUT_BASE/Anti-UAV/Anti-UAV-Tracking-V0/$VIDEO_NAME"
    
    echo ""
    echo "======================================================================"
    echo "  Anti-UAV: $VIDEO_NAME"
    echo "======================================================================"
    
    if [ ! -d "$INPUT_DIR" ]; then
        echo "❌ Error: Directory not found: $INPUT_DIR"
        FAILED+=("Anti-UAV/$VIDEO_NAME")
        continue
    fi
    
    process_sequence "Anti-UAV/$VIDEO_NAME" "$INPUT_DIR" "AntiUAV_${VIDEO_NAME}" || true
    
    echo ""
    echo "Waiting 5 seconds before next sequence..."
    sleep 5
done

# Final summary
TOTAL_END=$(date +%s)
TOTAL_DURATION=$((TOTAL_END - TOTAL_START))
TOTAL_HOURS=$((TOTAL_DURATION / 3600))
TOTAL_MINUTES=$(((TOTAL_DURATION % 3600) / 60))
TOTAL_SECONDS=$((TOTAL_DURATION % 60))

echo ""
echo "======================================================================"
echo "  BATCH PROCESSING COMPLETE"
echo "======================================================================"
echo ""
echo "Total time: ${TOTAL_HOURS}h ${TOTAL_MINUTES}m ${TOTAL_SECONDS}s"
echo ""
echo "Successful: ${#SUCCESSFUL[@]}"
for seq in "${SUCCESSFUL[@]}"; do
    echo "  ✓ $seq"
done
echo ""
echo "Failed: ${#FAILED[@]}"
for seq in "${FAILED[@]}"; do
    echo "  ✗ $seq"
done
echo ""
echo "Output directory: $OUTPUT_BASE"
echo "Logs directory: $LOG_DIR"
echo "Master log: $MASTER_LOG"
echo ""
echo "======================================================================"

# Create summary file
SUMMARY_FILE="$OUTPUT_BASE/processing_summary_${TIMESTAMP}.txt"
cat > "$SUMMARY_FILE" << EOF
BATCH PROCESSING SUMMARY
========================

Date: $(date)
Model: ROBUST
Total Duration: ${TOTAL_HOURS}h ${TOTAL_MINUTES}m ${TOTAL_SECONDS}s

Successful (${#SUCCESSFUL[@]}):
$(printf "  ✓ %s\n" "${SUCCESSFUL[@]}")

Failed (${#FAILED[@]}):
$(printf "  ✗ %s\n" "${FAILED[@]}")

Output Location: $OUTPUT_BASE
Logs Location: $LOG_DIR
EOF

echo "Summary saved to: $SUMMARY_FILE"
echo ""
echo "Done!"


