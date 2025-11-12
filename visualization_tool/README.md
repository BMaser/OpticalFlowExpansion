# Optical Flow Expansion - Visualization Tools

This directory contains visualization and organization tools for processing optical flow expansion outputs.

## Tools

### 1. visualize_output.py
Organizes mixed output files into categorized subdirectories by type.

**Features:**
- Automatically detects and categorizes 6 output types
- Handles double extensions (.jpg.jpg) and cleans filenames
- Supports copy, move, or symlink operations
- Calculates and displays directory sizes

**Usage:**
```bash
# Basic usage (copies files)
python visualize_output.py /path/to/sequence/seq

# Use symbolic links to save disk space
python visualize_output.py /path/to/sequence/seq --mode symlink

# Custom output location
python visualize_output.py /path/to/sequence/seq --output /custom/output/path

# Move files instead of copying
python visualize_output.py /path/to/sequence/seq --mode move
```

**Output Structure:**
```
organized/
├── flow/               # Optical flow fields (flo-*.png)
├── expansion/          # Optical expansion maps (exp-*.png)
├── motion_in_depth/    # Motion-in-depth τ (mid-*.png)
├── occlusion/          # Occlusion maps (occ-*.png)
├── flow_viz/           # Flow visualizations (visflo-*.jpg)
└── warped/             # Warped images (warp-*.jpg)
```

---

### 2. create_videos.py
Creates videos from organized image sequences at specified frame rate.

**Features:**
- Processes all category subdirectories automatically
- Configurable frame rate and codec
- Progress bar with frame-by-frame feedback
- Automatic size reporting

**Usage:**
```bash
# Basic usage (15 fps, mp4v codec)
python create_videos.py /path/to/organized

# Change frame rate
python create_videos.py /path/to/organized --fps 30

# Use H.264 codec for better compression
python create_videos.py /path/to/organized --codec H264

# Custom output directory
python create_videos.py /path/to/organized --output /path/to/videos
```

**Supported Codecs:**
- `mp4v` (default): MPEG-4, .mp4 extension
- `H264`/`avc1`/`X264`: H.264, .mp4 extension
- `XVID`/`DIVX`/`MJPG`: Various, .avi extension

---

## Complete Workflow Example

Process a single video sequence from start to finish:

```bash
# 1. Run inference on input frames (from project root)
cd /home/bobmaser/github/OpticalFlowExpansion
CUDA_VISIBLE_DEVICES=0 python submission.py \
    --dataset seq \
    --datapath "/path/to/input/frames" \
    --outdir "/mnt/hdd2/Bob/output_expansion/video01" \
    --loadmodel ./weights/robust/robust.pth \
    --testres 1 --fac 1 --maxdisp 256

# 2. Organize outputs by category
cd visualization_tool
python visualize_output.py \
    /mnt/hdd2/Bob/output_expansion/video01/seq \
    --mode copy

# 3. Create videos from organized outputs
python create_videos.py \
    /mnt/hdd2/Bob/output_expansion/video01/organized \
    --fps 15
```

---

## Output Types Explained

### Flow (flo-*.png)
**16-bit PNG** containing 2D motion vectors (u, v) for each pixel. Represents horizontal and vertical displacement between consecutive frames.

### Expansion (exp-*.png)
**16-bit PNG** showing optical expansion (divergence of flow field). Indicates regions where the scene is expanding (moving toward camera) or contracting (moving away).

### Motion-in-Depth (mid-*.png)
**16-bit PNG** representing τ = d₂/d₁ (ratio of depths between frames). Shows relative depth change for each pixel.

### Occlusion (occ-*.png)
**8-bit PNG** showing probability of pixel occlusion. Helps identify regions where objects become hidden or revealed.

### Flow Visualization (visflo-*.jpg)
**JPEG** with color-coded flow visualization for human interpretation. Uses color wheel encoding for direction and magnitude.

### Warped (warp-*.jpg)
**JPEG** showing frame 2 warped using predicted flow from frame 1. Useful for assessing flow accuracy.

---

## Requirements

### Python Dependencies
```bash
conda activate opt-flow  # or your environment name
pip install opencv-python numpy tqdm pathlib
```

### System Requirements
- Python 3.6+
- OpenCV with video codec support
- Sufficient disk space for organized outputs and videos

---

## Tips

### Disk Space Management
- Use `--mode symlink` to avoid duplicating large datasets
- Videos are significantly compressed compared to PNG sequences
- Consider processing categories separately if storage is limited

### Performance
- Video creation is I/O bound - faster storage = faster processing
- 16-bit PNGs maintain maximum precision but are larger
- JPEG visualizations provide good quality at smaller sizes

### Batch Processing
For multiple sequences, create a simple bash script:
```bash
#!/bin/bash
for i in {01..20}; do
    echo "Processing video$i..."
    python visualize_output.py "/path/to/video${i}/seq"
    python create_videos.py "/path/to/video${i}/organized" --fps 15
done
```

---

## Troubleshooting

### "No images found" error
- Check that the path points to a directory with image files
- Verify image extensions match expected patterns (*.png, *.jpg)

### Video codec errors
- Install additional codecs: `sudo apt-get install ffmpeg`
- Try alternative codec: `--codec XVID` or `--codec MJPG`

### Out of memory during video creation
- Process smaller batches
- Reduce frame rate or image resolution
- Use more efficient codec (H264)

---

## Contact

For questions or issues, contact Bob Maser.

