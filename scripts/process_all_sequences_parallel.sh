#!/bin/bash
# Parallel Processing of All Sequences with ROBUST Model
# Author: Bob Maser
# Date: November 11, 2024
#
# This script processes sequences in parallel for faster execution
# Use with caution - monitors GPU memory to avoid overload

set -e

PROJECT_ROOT="/home/bobmaser/github/OpticalFlowExpansion"
OUTPUT_BASE="/mnt/hdd2/Bob/robust_outputs"
LOG_DIR="$PROJECT_ROOT/logs"

# Maximum parallel jobs (adjust based on GPU memory)
MAX_PARALLEL=2

echo "======================================================================"
echo "  PARALLEL BATCH PROCESSING (Max $MAX_PARALLEL jobs)"
echo "======================================================================"
echo ""

# Create a list of all sequences to process
SEQUENCE_LIST="$LOG_DIR/sequence_list_$(date +%Y%m%d_%H%M%S).txt"

# Generate sequence list
{
    # Numbered sequences
    for seq in 10 29 121 186 208 217; do
        echo "/mnt/hdd2/ura1/database/RGB Frames/${seq} - RGB|seq_${seq}"
    done
    
    # Anti-UAV videos
    for i in $(seq -f "%02g" 1 20); do
        echo "/mnt/hdd2/ura1/database/RGB Frames/Anti-UAV/Anti-UAV-Tracking-V0/video${i}|AntiUAV_video${i}"
    done
} > "$SEQUENCE_LIST"

echo "Generated sequence list: $SEQUENCE_LIST"
echo "Total sequences: $(wc -l < "$SEQUENCE_LIST")"
echo ""

# Function to process one sequence (called by GNU parallel)
process_one() {
    local LINE="$1"
    local INPUT_DIR=$(echo "$LINE" | cut -d'|' -f1)
    local OUTPUT_NAME=$(echo "$LINE" | cut -d'|' -f2)
    local SEQ_OUTPUT="$OUTPUT_BASE/$OUTPUT_NAME"
    local MODEL_PATH="$PROJECT_ROOT/weights/robust/robust.pth"
    
    echo "[$(date '+%H:%M:%S')] Starting: $OUTPUT_NAME"
    
    # Run inference
    cd "$PROJECT_ROOT"
    CUDA_VISIBLE_DEVICES=0 python submission.py \
        --dataset seq \
        --datapath "$INPUT_DIR" \
        --outdir "$SEQ_OUTPUT" \
        --loadmodel "$MODEL_PATH" \
        --testres 1 --fac 1 --maxdisp 256 \
        > "$LOG_DIR/${OUTPUT_NAME}_inference.log" 2>&1
    
    # Organize outputs
    cd "$PROJECT_ROOT/visualization_tool"
    python visualize_output.py "$SEQ_OUTPUT/seq" --mode copy \
        > "$LOG_DIR/${OUTPUT_NAME}_organize.log" 2>&1
    
    # Create videos
    python create_videos.py "$SEQ_OUTPUT/organized" --fps 15 --output-dir "$SEQ_OUTPUT/videos" \
        > "$LOG_DIR/${OUTPUT_NAME}_videos.log" 2>&1
    
    echo "[$(date '+%H:%M:%S')] Completed: $OUTPUT_NAME"
}

export -f process_one
export PROJECT_ROOT OUTPUT_BASE LOG_DIR

# Check if GNU parallel is available
if command -v parallel &> /dev/null; then
    echo "Using GNU parallel for faster processing..."
    cat "$SEQUENCE_LIST" | parallel -j $MAX_PARALLEL process_one {}
else
    echo "GNU parallel not found. Processing sequentially..."
    while IFS= read -r line; do
        process_one "$line"
    done < "$SEQUENCE_LIST"
fi

echo ""
echo "======================================================================"
echo "  ALL SEQUENCES PROCESSED"
echo "======================================================================"
echo "Output directory: $OUTPUT_BASE"
echo ""


