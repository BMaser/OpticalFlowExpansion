#!/bin/bash
# Quick Progress Checker for Batch Processing
# Usage: ./scripts/check_progress.sh

OUTPUT_BASE="/mnt/hdd2/Bob/robust_outputs"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          BATCH PROCESSING PROGRESS CHECK                           ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if process is running
if pgrep -f "batch_process_all_sequences.sh" > /dev/null || pgrep -f "submission.py.*robust" > /dev/null; then
    echo -e "${GREEN}✓ Status: RUNNING${NC}"
else
    echo -e "${RED}✗ Status: NOT RUNNING${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "COMPLETED SEQUENCES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

COMPLETED=0
TOTAL=26

for seq_dir in "$OUTPUT_BASE"/*/; do
    if [ -d "$seq_dir" ]; then
        SEQ_NAME=$(basename "$seq_dir")
        VIDEO_DIR="$seq_dir/videos"
        
        if [ -d "$VIDEO_DIR" ] && [ "$(ls -A $VIDEO_DIR/*.mp4 2>/dev/null | wc -l)" -gt 0 ]; then
            VIDEO_COUNT=$(ls -1 "$VIDEO_DIR"/*.mp4 2>/dev/null | wc -l)
            echo -e "${GREEN}✓${NC} $SEQ_NAME (${VIDEO_COUNT} videos)"
            ((COMPLETED++))
        else
            OUTPUT_COUNT=$(ls -1 "$seq_dir/seq" 2>/dev/null | wc -l)
            if [ "$OUTPUT_COUNT" -gt 0 ]; then
                FRAMES=$((OUTPUT_COUNT / 6))
                echo -e "${YELLOW}⚡${NC} $SEQ_NAME (${FRAMES} frames processed, organizing...)"
            fi
        fi
    fi
done

if [ $COMPLETED -eq 0 ]; then
    echo "  (None yet)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CURRENTLY PROCESSING:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CURRENT_SEQ=$(ps aux | grep "submission.py.*robust" | grep -v grep | sed 's/.*--outdir //; s/ .*//' | xargs -I {} basename {})

if [ -n "$CURRENT_SEQ" ]; then
    CURRENT_DIR="$OUTPUT_BASE/$CURRENT_SEQ"
    if [ -d "$CURRENT_DIR/seq" ]; then
        OUTPUT_COUNT=$(ls -1 "$CURRENT_DIR/seq" 2>/dev/null | wc -l)
        FRAMES=$((OUTPUT_COUNT / 6))
        
        # Try to estimate total frames (rough estimate)
        echo -e "${YELLOW}⚡ Processing:${NC} $CURRENT_SEQ"
        echo "   Frames processed: $FRAMES"
        echo "   Files generated: $OUTPUT_COUNT"
        
        # Show recent processing speed
        RECENT_FILES=$(find "$CURRENT_DIR/seq" -type f -mmin -5 | wc -l)
        if [ "$RECENT_FILES" -gt 0 ]; then
            RATE=$((RECENT_FILES / 5 / 6))  # frames per minute
            echo "   Processing rate: ~$RATE frames/min"
        fi
    fi
else
    echo "  No active inference process"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Completed: $COMPLETED / $TOTAL sequences"
echo "  Output location: $OUTPUT_BASE"
echo ""

# Show disk usage
DISK_USAGE=$(du -sh "$OUTPUT_BASE" 2>/dev/null | cut -f1)
echo "  Disk usage: $DISK_USAGE"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RECENT LOG ENTRIES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -5 /home/bobmaser/github/OpticalFlowExpansion/logs/batch_process_*.log 2>/dev/null | tail -5

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 To monitor continuously: watch -n 30 ./scripts/check_progress.sh"
echo "📊 To see full logs: tail -f logs/batch_process_*.log"
echo ""

