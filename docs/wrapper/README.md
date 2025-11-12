# Image Warping Documentation

This directory contains documentation explaining how optical flow warping works in the OpticalFlowExpansion project.

---

## 📄 Main Document

### [WarpingExplained.md](WarpingExplained.md)
**Complete guide to understanding image warping with optical flow**

A comprehensive, plain-English explanation of how Frame 2 is warped to match Frame 1 using predicted optical flow. This document covers:

- What image warping is and why we use it
- Complete pipeline from input frames to warped output
- Two types of warping (internal feature warping vs final image warping)
- Step-by-step process with visual diagrams
- Technical implementation details
- How to interpret warped outputs

**Perfect for:** Anyone wanting to understand what `warp-*.jpg` files are and how they're created!

---

## Quick Overview

### What is Warping?

**Warping** = Moving pixels from Frame 2 to new positions based on optical flow vectors, so it looks like Frame 1.

```
Frame 1 (reference)  +  Frame 2  +  Optical Flow  →  Warped Frame 2 ≈ Frame 1
```

### Why Warp?

1. **Validate flow accuracy:** If flow is good, warped Frame 2 should match Frame 1
2. **Detect occlusions:** Areas that can't be warped properly
3. **Visual quality check:** See prediction errors at a glance

---

## Output Files

When you run `submission.py`, you get these outputs:

```
output/dataset/
├── flo-frame001.png      # Raw optical flow (u, v) data
├── visflo-frame001.jpg   # Colorful flow visualization  
├── warp-frame001.jpg     # ⭐ WARPED FRAME 2 (explained in this doc!)
├── occ-frame001.png      # Occlusion mask
├── exp-frame001.png      # Optical expansion
└── mid-frame001.png      # Motion-in-depth
```

The **`warp-*.jpg`** files show Frame 2 transformed to look like Frame 1 using the predicted optical flow.

---

## How to Use This Documentation

### For Beginners:
1. Read "What is Image Warping?" section
2. Look at visual examples
3. Understand the quality check process

### For Intermediate Users:
1. Study the complete pipeline overview
2. Understand the two types of warping
3. Learn how to interpret warped outputs

### For Advanced Users:
1. Review technical implementation details
2. Study bilinear interpolation formulas
3. Examine code references in VCN model

---

## Visual Overview

```
┌─────────────────────────────────────────────────────────┐
│              WARPING PIPELINE SUMMARY                    │
└─────────────────────────────────────────────────────────┘

Input: Frame 1, Frame 2
   ↓
VCN Model: Predict Optical Flow (u, v)
   ↓
Internal: Warp features during refinement (coarse→fine)
   ↓
Output: Warp Frame 2 RGB image using predicted flow
   ↓
Save: warp-*.jpg

Quality Check:
  Frame 1 ≈ warp-*.jpg  → Good flow! ✓
  Frame 1 ≠ warp-*.jpg  → Poor flow  ✗
```

---

## Related Code Files

### Core Implementation:

**1. WarpModule (Neural Network)**
- **File:** `models/VCN_exp.py`
- **Lines:** 87-119
- **Purpose:** Warp CNN features during model forward pass
- **Method:** PyTorch `grid_sample()` with bilinear interpolation

**2. warp_flow() (Image Processing)**
- **File:** `utils/flowlib.py`
- **Lines:** 384-390
- **Purpose:** Warp RGB images for visualization
- **Method:** OpenCV `cv2.remap()` with bilinear interpolation

**3. Main Pipeline**
- **File:** `submission.py`
- **Line:** 173
- **Usage:** `imwarped = warp_flow(imgR_o, flow[:,:,:2])`

---

## Key Concepts

### Bilinear Interpolation

When optical flow moves a pixel to position (x+u, y+v), the result is usually not at integer coordinates. Bilinear interpolation blends the 4 nearest neighboring pixels to get a smooth result.

```
Original Grid:       After Flow (+1.3, +0.7):
┌───┬───┬───┐       ┌───┬───┬───┐
│ A │ B │ C │       │   │A·B│B·C│  ← Blended values
├───┼───┼───┤  →    ├───┼───┼───┤
│ D │ E │ F │       │   │D·E│E·F│
├───┼───┼───┤       ├───┼───┼───┤
│ G │ H │ I │       │   │G·H│H·I│
└───┴───┴───┘       └───┴───┴───┘
```

### Occlusion Handling

Some pixels in Frame 1 don't exist in Frame 2 (e.g., areas revealed by camera motion). These appear as:
- Black/white regions in warped output
- High values in `occ-*.png` occlusion mask

---

## Example Workflow

### Running Inference:

```bash
# Activate environment
conda activate opt-flow

# Run inference
python submission.py \
  --dataset UAV_sequence \
  --outdir /mnt/hdd2/Bob/results \
  --leftimg input/frames/ \
  --loadmodel weights/robust/checkpoint.tar

# View results
ls /mnt/hdd2/Bob/results/UAV_sequence/
# → flo-*.png, visflo-*.jpg, warp-*.jpg, occ-*.png, exp-*.png, mid-*.png
```

### Quality Assessment:

1. Open Frame 1 (original input)
2. Open `warp-frame001.jpg`
3. Compare visually:
   - **Similar?** Flow is accurate! ✓
   - **Different?** Check occlusion mask, may be prediction error ✗

---

## Common Questions

### Q: Why does warped image look blurry?
**A:** Bilinear interpolation smooths pixels. This is normal and expected.

### Q: Why are some areas black in warped output?
**A:** Those pixels moved outside the image boundary (occlusion or out-of-view).

### Q: How is this different from homography?
**A:** 
- **Homography:** Single 3×3 matrix, global transformation
- **Optical Flow Warping:** Dense per-pixel vectors, handles complex motion

### Q: Can I warp Frame 1 to Frame 2 instead?
**A:** Yes! Just reverse the flow direction: `flow_reversed = -flow`

---

## Technical Specifications

### Coordinate Convention:
- **u (horizontal):** Positive = right, Negative = left
- **v (vertical):** Positive = down, Negative = up
- **Origin:** Top-left corner (0, 0)

### Interpolation Method:
- **Training/Model:** Bilinear (PyTorch `grid_sample`)
- **Visualization:** Bilinear (OpenCV `cv2.remap`)
- **Precision:** Float32 for flow, uint8 for RGB output

### Resolution Handling:
Flow is computed at 1/4 resolution, then upsampled to original size before warping.

---

## Further Reading

- **Flow Visualization:** `../flow_viz/FlowVisualization_Explained.md`
- **VCN Paper:** Yang & Ramanan, "Volumetric Correspondence Networks for Optical Flow" (NeurIPS 2019)
- **PWC-Net Paper:** Sun et al., "PWC-Net: CNNs for Optical Flow Using Pyramid, Warping, and Cost Volume" (CVPR 2018)

---

## Directory Structure

```
docs/wrapper/
├── README.md              # This file
├── WarpingExplained.md    # Detailed warping guide
└── (future: diagrams/)    # Visual diagram images
```

---

**Created by:** Bob Maser  
**Date:** November 2024  
**Project:** [Optical Flow Expansion](https://github.com/BMaser/OpticalFlowExpansion)

For questions or improvements, feel free to update this documentation!

