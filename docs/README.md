# OpticalFlowExpansion Documentation

Comprehensive documentation for understanding and using the OpticalFlowExpansion project outputs.

**Author:** Bob Maser  
**Project:** OpticalFlowExpansion  
**Location:** `/home/bobmaser/github/OpticalFlowExpansion/docs/`

---

## Overview

This project generates **6 types of outputs** from video sequences:

| Output Type | Description | File Pattern | Documentation |
|-------------|-------------|--------------|---------------|
| **Optical Flow** | 2D motion vectors (u, v) | `flo-*.png` | [Flow Viz →](flow_viz/) |
| **Expansion** | Divergence of flow field | `exp-*.png` | [Expansion →](expansion/) ✓ |
| **Motion-in-Depth** | Depth ratio (τ = d₂/d₁) | `mid-*.png` | [MID →](motion_in_depth/) ✓ |
| **Occlusion** | Occluded/disoccluded pixels | `occ-*.png` | [Occlusion →](occlusion/) ✓ |
| **Flow Visualization** | Color-coded flow display | `visflo-*.jpg` | [Flow Viz →](flow_viz/) ✓ |
| **Warped Frames** | Frame 2 warped to Frame 1 | `warp-*.jpg` | [Warping →](wrapper/) ✓ |

**Legend:** ✓ = Complete documentation

---

## Documentation by Topic

### 1. Flow Visualization 📊 ✓

**Location:** [`flow_viz/`](flow_viz/)

Learn how optical flow is visualized using the Middlebury color wheel and how to extract optical flow.

**Topics covered:**
- What is optical flow?
- Middlebury color wheel algorithm
- Flow extraction methods (VCN, RAFT, OpenCV)
- Step-by-step visualization algorithm
- Color interpretation guide

**Key files:**
- [FlowVisualization_Explained.md](flow_viz/FlowVisualization_Explained.md) - Main documentation
- [README.md](flow_viz/README.md) - Quick reference
- `color_wheel.png` - Color wheel diagram
- `examples/` - Various flow pattern examples

---

### 2. Optical Expansion 📈 ✓

**Location:** [`expansion/`](expansion/)

**NEW!** Understand optical expansion (divergence) and its applications in collision detection, depth estimation, and motion analysis.

**Topics covered:**
- What is optical expansion (divergence)?
- Mathematical foundation: ∂u/∂x + ∂v/∂y
- Physical interpretation (approaching vs receding)
- Applications: collision detection, time-to-contact, depth estimation
- Common expansion patterns
- Code examples for UAV/robotics applications

**Key files:**
- [ExpansionExplained.md](expansion/ExpansionExplained.md) - Complete guide
- [README.md](expansion/README.md) - Quick reference
- `divergence_concept.png` - Positive vs negative divergence
- `camera_forward_expansion.png` - Forward motion pattern
- `uav_flight_expansion.png` - Aerial footage example
- `interpretation_guide.png` - Color interpretation

**Quick example:**
```python
# Detect collision risk from expansion
expansion = cv2.imread('exp-0001.png', cv2.IMREAD_UNCHANGED)
risk_zones = (expansion / 65535.0) > 0.7  # High positive = approaching
if risk_zones.any():
    print("COLLISION WARNING!")
```

---

### 3. Motion-in-Depth (MID) 📏 ✓

**Location:** [`motion_in_depth/`](motion_in_depth/)

**NEW!** Understand motion-in-depth (τ = d₂/d₁) and its role in 3D reconstruction and scene understanding.

**Topics covered:**
- What is motion-in-depth (depth ratio)?
- Mathematical foundation: τ = Z₂/Z₁
- Physical interpretation (approaching vs receding)
- Applications: monocular 3D reconstruction, scene flow, collision time
- Relationship to expansion
- Depth segmentation and ordering
- Code examples for UAV/robotics applications

**Key files:**
- [MotionInDepthExplained.md](motion_in_depth/MotionInDepthExplained.md) - Complete guide
- [README.md](motion_in_depth/README.md) - Quick reference
- `tau_concept.png` - Visual explanation of τ
- `camera_forward_mid.png` - Forward motion pattern
- `uav_descending_mid.png` - Aerial descent example
- `depth_layers.png` - Depth segmentation
- `interpretation_guide.png` - Color interpretation

**Quick example:**
```python
# Estimate collision time from motion-in-depth
mid = cv2.imread('mid-0001.png', cv2.IMREAD_UNCHANGED) / 65535.0
approaching = mid < 0.45  # τ < 1 (normalized)

# Approximate tau and compute time-to-contact
tau_approx = np.exp((mid - 0.5) * 4)
dt = 0.033  # Frame time (30 fps)
ttc = dt / (1 - tau_approx + 1e-8)
ttc[tau_approx >= 1] = np.inf

print(f"Minimum time to collision: {np.min(ttc[approaching]):.2f}s")
```

---

### 4. Occlusion Detection 🔍 ✓

**Location:** [`occlusion/`](occlusion/)

**NEW!** Understand occlusion and disocclusion detection and their role in video analysis.

**Topics covered:**
- What is occlusion? (Visible → Hidden)
- What is disocclusion? (Hidden → Visible)
- Types: motion, depth, self-occlusion
- Forward-backward consistency detection method
- Relationship to motion-in-depth and expansion
- Applications: segmentation, inpainting, depth ordering
- Code examples for video editing and analysis

**Key files:**
- [OcclusionExplained.md](occlusion/OcclusionExplained.md) - Complete guide
- [README.md](occlusion/README.md) - Quick reference
- `occlusion_concept.png` - Visual explanation of occlusion vs disocclusion
- `forward_backward_consistency.png` - Detection method
- `car_motion_occlusion.png` - Moving object example
- `person_disocclusion.png` - Background revelation
- `uav_occlusion.png` - Aerial flight example
- `interpretation_guide.png` - Color interpretation

**Quick example:**
```python
# Segment objects using occlusion boundaries
occ = cv2.imread('occ-0001.png', cv2.IMREAD_GRAYSCALE) / 255.0
flow_mag = np.sqrt(flow[:,:,0]**2 + flow[:,:,1]**2)

# Objects have high occlusion + high flow
objects = (occ > 0.4) & (flow_mag > 5.0)

# Refine flow (mark occluded as invalid)
flow_clean = flow.copy()
flow_clean[occ > 0.5] = np.nan
```

---

### 5. Frame Warping 🔄 ✓

**Location:** [`wrapper/`](wrapper/)

Learn how frames are warped using optical flow and what it tells you about flow quality.

**Topics covered:**
- Forward vs backward warping
- Bilinear interpolation
- Warping as quality metric
- Handling occlusions and holes

**Key files:**
- [WarpingExplained.md](wrapper/WarpingExplained.md) - Main documentation
- [README.md](wrapper/README.md) - Quick reference
- `grid_transformation.png` - Warping visualization
- `pipeline_diagram.png` - Full pipeline

---


## Quick Start Guides

### Loading and Visualizing Outputs

#### Python

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load expansion (16-bit PNG)
exp = cv2.imread('exp-0001.png', cv2.IMREAD_UNCHANGED)
exp_norm = exp.astype(np.float32) / 65535.0

# Visualize
plt.imshow(exp_norm, cmap='jet')
plt.colorbar(label='Expansion')
plt.title('Optical Expansion')
plt.show()

# Load flow visualization (8-bit JPG)
flow_viz = cv2.imread('visflo-0001.jpg')
flow_viz_rgb = cv2.cvtColor(flow_viz, cv2.COLOR_BGR2RGB)
plt.imshow(flow_viz_rgb)
plt.title('Flow Visualization')
plt.show()

# Load occlusion (8-bit PNG)
occ = cv2.imread('occ-0001.png', cv2.IMREAD_GRAYSCALE)
plt.imshow(occ, cmap='gray')
plt.title('Occlusion Map')
plt.show()
```

#### MATLAB

```matlab
% Load expansion
exp = imread('exp-0001.png');
exp_norm = double(exp) / 65535.0;

% Visualize
figure;
imagesc(exp_norm);
colormap(jet);
colorbar;
title('Optical Expansion');

% Load flow visualization
flow_viz = imread('visflo-0001.jpg');
figure;
imshow(flow_viz);
title('Flow Visualization');

% Load occlusion
occ = imread('occ-0001.png');
figure;
imshow(occ);
title('Occlusion Map');
```

---

## File Format Reference

| Output | Extension | Bit Depth | Range | Notes |
|--------|-----------|-----------|-------|-------|
| Flow | `.png` | 16-bit | 0-65535 | `(flow + 512) * 64` encoded |
| Expansion | `.png` | 16-bit | 0-65535 | Log-transformed, normalized |
| Motion-in-Depth | `.png` | 16-bit | 0-65535 | Log-transformed, normalized |
| Occlusion | `.png` | 8-bit | 0-255 | Probability (0=visible, 255=occluded) |
| Flow Viz | `.jpg` | 8-bit RGB | 0-255 | Middlebury color encoding |
| Warped | `.jpg` | 8-bit RGB | 0-255 | Warped frame visualization |

---

## Workflow Documentation

### Processing Pipeline

```
Input: Video Frames (frame_t, frame_{t+1})
   ↓
[VCN Model] Optical Flow Estimation
   ↓
├── Flow (u, v) → flo-*.png
├── Flow Visualization → visflo-*.jpg
├── Warping → warp-*.jpg
├── Occlusion Detection → occ-*.png
├── Expansion (∂u/∂x + ∂v/∂y) → exp-*.png
└── Motion-in-Depth (τ) → mid-*.png
```

### Organization & Video Creation

See [`visualization_tool/README.md`](../visualization_tool/README.md) for:
- Organizing outputs into categories
- Creating video clips from sequences
- Batch processing multiple sequences

---

## Common Use Cases

### 1. Collision Avoidance (UAV/Robotics)

**Use expansion maps** to detect approaching obstacles:

```python
expansion = cv2.imread('exp-0001.png', cv2.IMREAD_UNCHANGED) / 65535.0
high_risk = expansion > 0.75  # Threshold for "fast approaching"

if np.sum(high_risk) > 100:  # Significant area
    print("COLLISION WARNING - Take evasive action!")
```

**Documentation:** [expansion/ExpansionExplained.md](expansion/ExpansionExplained.md)

### 2. Depth Estimation

**Use expansion + known velocity** to estimate relative depth:

```python
# depth ∝ velocity / expansion
relative_depth = velocity / (expansion + epsilon)
```

**Documentation:** [expansion/ExpansionExplained.md](expansion/ExpansionExplained.md) (Section: Depth Estimation)

### 3. Motion Segmentation

**Use expansion anomalies** to detect moving objects:

```python
global_exp = np.median(expansion)
anomaly = np.abs(expansion - global_exp)
moving_objects = anomaly > threshold
```

**Documentation:** [expansion/ExpansionExplained.md](expansion/ExpansionExplained.md) (Section: Motion Segmentation)

### 4. Flow Quality Assessment

**Use warped frames** to evaluate flow accuracy:

```python
frame1 = cv2.imread('frame_0001.jpg')
warped = cv2.imread('warp-0001.jpg')
error = np.mean(np.abs(frame1 - warped))
print(f"Warping error: {error:.2f}")
```

**Documentation:** [wrapper/WarpingExplained.md](wrapper/WarpingExplained.md)

### 5. Time-to-Contact

**Compute TTC** for autonomous navigation:

```python
# TTC = -1 / expansion (for positive expansion)
expansion_linear = ...  # Convert from normalized
ttc = -1.0 / expansion_linear
ttc[ttc < 0] = np.inf  # Ignore receding objects
```

**Documentation:** [expansion/ExpansionExplained.md](expansion/ExpansionExplained.md) (Section: Time-to-Contact)

---

## Regenerating Documentation

All documentation includes Python scripts to regenerate diagrams:

```bash
# Activate environment
conda activate opt-flow

# Flow visualization diagrams
cd docs/flow_viz
python generate_diagrams.py

# Expansion diagrams
cd docs/expansion
python generate_expansion_diagrams.py

# Warping diagrams
cd docs/wrapper
python generate_warp_diagrams.py
```

---

## Directory Structure

```
docs/
├── README.md                    # This file (main index)
│
├── flow_viz/                    # Flow visualization ✓
│   ├── FlowVisualization_Explained.md
│   ├── README.md
│   ├── generate_diagrams.py
│   └── [diagrams and examples]
│
├── expansion/                   # Optical expansion ✓
│   ├── ExpansionExplained.md
│   ├── README.md
│   ├── generate_expansion_diagrams.py
│   └── [diagrams]
│
├── motion_in_depth/            # Motion-in-depth ✓
│   ├── MotionInDepthExplained.md
│   ├── README.md
│   ├── generate_mid_diagrams.py
│   └── [diagrams]
│
├── occlusion/                  # Occlusion detection ✓ NEW!
│   ├── OcclusionExplained.md
│   ├── README.md
│   ├── generate_occlusion_diagrams.py
│   └── [diagrams]
│
└── wrapper/                     # Frame warping ✓
    ├── WarpingExplained.md
    ├── README.md
    ├── generate_warp_diagrams.py
    └── [diagrams]
```

---

## Contributing

When adding new documentation:

1. **Follow the existing structure** (see [flow_viz/](flow_viz/) as template)
2. **Include diagrams** - Create `generate_*_diagrams.py` script
3. **Add code examples** - Python and MATLAB snippets
4. **Write for beginners** - Plain English, pedagogical approach
5. **Update this index** - Add entry to main README.md

---

## References

### Papers
- **VCN:** Yang et al. (2019) - "Volumetric Correspondence Networks for Optical Flow"
- **RAFT:** Teed & Deng (2020) - "RAFT: Recurrent All-Pairs Field Transforms for Optical Flow"
- **Optical Flow:** Horn & Schunck (1981) - "Determining Optical Flow"

### Datasets
- **KITTI:** [http://www.cvlibs.net/datasets/kitti/](http://www.cvlibs.net/datasets/kitti/)
- **Middlebury:** [http://vision.middlebury.edu/flow/](http://vision.middlebury.edu/flow/)
- **Sintel:** [http://sintel.is.tue.mpg.de/](http://sintel.is.tue.mpg.de/)

### External Resources
- Middlebury color wheel standard
- OpenCV optical flow documentation
- PyTorch tutorials on optical flow

---

## Changelog

### November 12, 2024

**Occlusion Detection Documentation** ✨ **LATEST!**
- ✨ **NEW:** Added complete Occlusion Detection documentation
  - `occlusion/OcclusionExplained.md` - Comprehensive guide
  - 7 visual diagrams with generation script
  - Occluded vs disoccluded concepts explained
  - Forward-backward consistency detection method
  - Code examples for segmentation, inpainting, depth ordering
  - Applications for video editing, autonomous vehicles, UAV
  - Progress: 5/6 outputs documented (83%) 🎉

**Motion-in-Depth Documentation** ✨
- Added complete Motion-in-Depth (MID) documentation
  - `motion_in_depth/MotionInDepthExplained.md` - Comprehensive guide
  - 7 visual diagrams with generation script
  - τ = d₂/d₁ concept explained with real-world examples
  - Code examples for monocular 3D reconstruction, collision time, scene flow
  - Applications for UAV terrain following, depth segmentation
  - Relationship between MID and expansion clarified

**Expansion Documentation** ✨
- Added complete Expansion documentation
  - `expansion/ExpansionExplained.md` - Comprehensive guide
  - 7 visual diagrams with generation script
  - Code examples for collision detection, depth estimation
  - Application examples for UAV/robotics

### November 11, 2024
- Added Warping documentation
- Added Flow Visualization documentation
- Created documentation structure

---

## Contact

**Author:** Bob Maser  
**Date:** November 12, 2024  
**Project:** OpticalFlowExpansion  
**Repository:** `/home/bobmaser/github/OpticalFlowExpansion/`

For questions, improvements, or bug reports, please contact the author.

---

**Last Updated:** November 12, 2024  
**Version:** 1.3  
**Status:** 5/6 outputs documented (Flow, Expansion, Motion-in-Depth, Occlusion, Warping) - 83% Complete! 🎉

