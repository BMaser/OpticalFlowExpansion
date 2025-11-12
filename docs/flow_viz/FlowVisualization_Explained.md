# How Flow Visualization Works
## A Simple Guide to Understanding Optical Flow Color Coding

---

## Table of Contents
1. [What is Optical Flow?](#what-is-optical-flow)
2. [How to Extract Optical Flow](#how-to-extract-optical-flow)
3. [Why Do We Need Visualization?](#why-do-we-need-visualization)
4. [The Middlebury Color Wheel](#the-middlebury-color-wheel)
5. [Step-by-Step Algorithm](#step-by-step-algorithm)
6. [Examples](#examples)
7. [Summary](#summary)

---

## What is Optical Flow?

**Optical flow** is like tracking how every pixel in an image moves from one frame to the next.

### Simple Example:
Imagine a ball rolling across your screen:
```
Frame 1:              Frame 2:
┌──────────┐          ┌──────────┐
│    ●     │   →      │      ●   │
└──────────┘          └──────────┘
```

For each pixel in the ball, we need to know:
- **u** = how much it moved horizontally (left/right)
- **v** = how much it moved vertically (up/down)

### Flow Vector:
```
        ↑ v (vertical)
        │
        │
        └────→ u (horizontal)
```

Each pixel gets a **flow vector** `(u, v)`:
- `u = +10` means moved 10 pixels to the right
- `u = -10` means moved 10 pixels to the left
- `v = +5` means moved 5 pixels down
- `v = -5` means moved 5 pixels up

---

## How to Extract Optical Flow

Before we can visualize optical flow, we need to **extract** it from video frames. This is the process of analyzing two consecutive images and computing the motion vectors `(u, v)` for every pixel.

### Classic vs. Deep Learning Methods

There are two main approaches to extracting optical flow:

#### 1. **Classical Methods** (Traditional Computer Vision)
These use mathematical optimization and assumptions about brightness constancy.

**Popular Classical Algorithms:**
- **Lucas-Kanade**: Sparse flow, tracks feature points
- **Horn-Schunck**: Dense flow, global optimization
- **Farnebäck**: Dense polynomial expansion method (available in OpenCV)

**Pros:** Fast, no training needed, mathematically interpretable  
**Cons:** Less accurate on complex scenes, struggles with large motions

#### 2. **Deep Learning Methods** (Neural Networks)
Modern approach using trained neural networks to predict flow.

**Popular Deep Learning Algorithms:**

| Algorithm | Year | Key Features | Typical Use |
|-----------|------|--------------|-------------|
| **FlowNet** | 2015 | First end-to-end CNN for flow | Research baseline |
| **FlowNet2** | 2017 | Stacked networks, higher accuracy | General purpose |
| **PWC-Net** | 2018 | Pyramid, warping, cost volume | Efficient & accurate |
| **LiteFlowNet** | 2018 | Lightweight, fast inference | Real-time applications |
| **RAFT** | 2020 | Recurrent refinement, state-of-the-art | High accuracy needed |
| **GMA** | 2021 | Global motion aggregation | Complex scenes |
| **VCN** | 2019 | Volumetric cost volume | **Used in this project!** |

**Pros:** Very accurate, handles complex scenes and occlusions  
**Cons:** Requires GPU, needs training data, slower than classical methods

---

### This Project: VCN (Volumetric Correspondence Network)

**This OpticalFlowExpansion project uses VCN** as its optical flow extraction backbone.

#### What is VCN?

**VCN** (Yang & Ramanan, 2019) uses a **volumetric cost volume** to match pixels between frames.

**Key Innovation:**
```
Traditional methods:  Match in 2D space
VCN:                 Match in 3D volumetric space
                     → Better at handling large displacements
```

#### How VCN Works (Simplified):

```
Step 1: Feature Extraction
┌─────────┐         ┌─────────┐
│ Frame 1 │  CNN    │Features1│
└─────────┘   →     └─────────┘
┌─────────┐         ┌─────────┐
│ Frame 2 │  CNN    │Features2│
└─────────┘   →     └─────────┘

Step 2: Cost Volume Construction
  Build 4D cost volume by comparing
  all possible matches in 3D space
  
Step 3: Flow Prediction
  Use 3D convolutions to aggregate
  cost volume → predict (u, v)
  
Step 4: Refinement
  Iteratively refine flow prediction
```

#### Why VCN for This Project?

1. **Accurate large motion**: VCN's volumetric approach handles large pixel displacements
2. **Occlusion awareness**: Predicts occlusion masks natively
3. **Depth integration**: Can be extended to estimate depth (used for expansion!)
4. **Scene flow capable**: Can predict 3D motion, not just 2D

---

### How to Extract Flow: Practical Examples

#### Option 1: Using This Project (VCN)

```bash
# Already set up in this project!
conda activate opt-flow
python submission.py \
  --dataset video01 \
  --datapath /path/to/frames/ \
  --outdir /path/to/output/ \
  --loadmodel pretrained_models/exp.tar
```

**Outputs:**
- `flo-*.png` → Raw optical flow (u, v)
- `visflo-*.jpg` → Colorized visualization
- `exp-*.png` → Optical expansion
- `mid-*.png` → Motion-in-depth
- `occ-*.png` → Occlusion mask

---

#### Option 2: Using RAFT (State-of-the-Art)

**RAFT** (Recurrent All-Pairs Field Transforms) is currently the most accurate method.

```python
# Install
pip install torch torchvision
git clone https://github.com/princeton-vl/RAFT.git
cd RAFT

# Download pretrained model
./download_models.sh

# Run inference
python demo.py --model=models/raft-things.pth \
               --path=/path/to/frames/
```

**RAFT Features:**
- ✅ State-of-the-art accuracy (best on benchmarks)
- ✅ Handles occlusions well
- ✅ Fast inference with GPU
- ❌ Only predicts flow (no depth/expansion)

---

#### Option 3: Using OpenCV (Farnebäck - Classical)

Simple classical method, no deep learning required.

```python
import cv2
import numpy as np

# Read two consecutive frames
frame1 = cv2.imread('frame_001.jpg')
frame2 = cv2.imread('frame_002.jpg')

# Convert to grayscale
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

# Calculate optical flow using Farnebäck method
flow = cv2.calcOpticalFlowFarneback(
    gray1, gray2, 
    None,           # output flow
    0.5,            # pyramid scale
    3,              # pyramid levels
    15,             # window size
    3,              # iterations
    5,              # poly neighborhood
    1.2,            # poly sigma
    0               # flags
)

# flow shape: (height, width, 2)
# flow[:,:,0] = u (horizontal)
# flow[:,:,1] = v (vertical)

print(f"Flow shape: {flow.shape}")
print(f"Flow range: u=[{flow[:,:,0].min():.2f}, {flow[:,:,0].max():.2f}]")
print(f"            v=[{flow[:,:,1].min():.2f}, {flow[:,:,1].max():.2f}]")
```

**Pros:** 
- ✅ No GPU needed
- ✅ No training/pretrained models
- ✅ Fast for small images
- ✅ Built into OpenCV

**Cons:**
- ❌ Less accurate than deep learning
- ❌ Struggles with large motions
- ❌ No occlusion handling

---

#### Option 4: Using PWC-Net

**PWC-Net** balances speed and accuracy.

```python
# Install
pip install torch torchvision
git clone https://github.com/sniklaus/pytorch-pwc.git
cd pytorch-pwc

# Download model
wget http://content.sniklaus.com/github/pytorch-pwc/network-default.pytorch

# Use in Python
import torch
from run import estimate

# Load images (as torch tensors)
frame1 = torch.FloatTensor(...)  # shape: (3, H, W)
frame2 = torch.FloatTensor(...)

# Predict flow
flow = estimate(frame1, frame2)  # shape: (2, H, W)

# flow[0] = u, flow[1] = v
```

**Best for:** Real-time applications, good accuracy/speed trade-off

---

### Comparison of Methods

```
Accuracy Ranking (high to low):
1. RAFT (2020)          ★★★★★  Best accuracy
2. GMA (2021)           ★★★★★  Best on complex scenes
3. VCN (2019)           ★★★★☆  Good + depth capability
4. PWC-Net (2018)       ★★★★☆  Good balance
5. FlowNet2 (2017)      ★★★☆☆  Older but reliable
6. Farnebäck (OpenCV)   ★★☆☆☆  Classical, fast

Speed Ranking (fast to slow):
1. Farnebäck (OpenCV)   ⚡⚡⚡⚡⚡  Fastest (CPU)
2. LiteFlowNet          ⚡⚡⚡⚡☆  Optimized for speed
3. PWC-Net              ⚡⚡⚡☆☆  Good speed/accuracy
4. VCN                  ⚡⚡☆☆☆  Slower (3D volumes)
5. FlowNet2             ⚡⚡☆☆☆  Multiple networks
6. RAFT                 ⚡⚡☆☆☆  Iterative refinement

Ease of Use:
1. OpenCV (Farnebäck)   ✅✅✅  Just call one function
2. This Project (VCN)   ✅✅✅  Already set up!
3. RAFT                 ✅✅☆  Need to clone & setup
4. PWC-Net              ✅✅☆  Need to clone & setup
```

---

### Which Method Should You Use?

**For this project → Already using VCN** ✅
- Best choice for depth + flow + expansion
- Already configured and working!

**For highest accuracy → RAFT**
- Best benchmark performance
- Industry standard for research

**For speed/embedded → Farnebäck (OpenCV)**
- No GPU needed
- Good for real-time applications
- Lower accuracy acceptable

**For balance → PWC-Net**
- Good accuracy
- Faster than RAFT
- Popular in production

---

### Benchmarks (KITTI Dataset)

Performance on standard optical flow benchmark:

| Method | EPE ↓ | Fl-all ↓ | Runtime (ms) |
|--------|-------|----------|--------------|
| **RAFT** | **1.43** | **5.1%** | 160 |
| GMA | 1.39 | 4.9% | 180 |
| **VCN** | **1.66** | **5.9%** | 180 |
| PWC-Net | 2.16 | 9.8% | 34 |
| FlowNet2 | 2.30 | 11.7% | 121 |
| Farnebäck | ~5.0 | ~30% | 15 (CPU) |

- **EPE** = End-Point Error (lower is better)
- **Fl-all** = Percentage of outliers (lower is better)
- **Runtime** = Milliseconds per frame pair (GPU: RTX 3090)

---

### Summary: Flow Extraction

**Key Takeaways:**

1. **Optical flow extraction** = Computing (u, v) motion vectors from frame pairs
2. **Two approaches**: Classical (fast, less accurate) vs. Deep Learning (slow, very accurate)
3. **This project uses VCN** for flow + expansion + depth
4. **RAFT** is current state-of-the-art for pure flow
5. **OpenCV Farnebäck** is simplest for basic needs

**After extraction**, we have flow data `(u, v)` → then we **visualize** it using colors (explained in the next sections)!

---

## Why Do We Need Visualization?

Raw optical flow data is just two numbers `(u, v)` per pixel. This is hard to understand by looking at numbers!

**Example Flow Data (hard to understand):**
```
Pixel (100, 50): u=5.2, v=-3.1
Pixel (101, 50): u=4.8, v=-2.9
Pixel (102, 50): u=5.1, v=-3.0
...millions more...
```

**Solution:** Convert to colors that humans can understand instantly!

We use **color** to show:
1. **Direction** (which way is it moving?) → Hue (color)
2. **Speed** (how fast is it moving?) → Saturation/Brightness

---

## The Middlebury Color Wheel

The **Middlebury color wheel** is a standard way to map flow directions to colors.

### Color Wheel Diagram:

```
                    ↑ Up
              Yellow (0°)
                    │
     Green          │          Red
    (270°) ←────────●────────→ (90°)
                    │
              Blue (180°)
                    ↓ Down


   Direction Legend:
   ┌──────────────────────────────┐
   │  →  Right     : Red          │
   │  ↗  Up-Right  : Yellow-Red   │
   │  ↑  Up        : Yellow        │
   │  ↖  Up-Left   : Yellow-Green │
   │  ←  Left      : Cyan (Green) │
   │  ↙  Down-Left : Cyan-Blue    │
   │  ↓  Down      : Blue          │
   │  ↘  Down-Right: Magenta-Blue │
   └──────────────────────────────┘
```

### How Colors Are Assigned:

The color wheel has **6 segments** (55 colors total):

```
Segment  | Colors         | Range | Meaning
---------|----------------|-------|------------------
RY       | Red→Yellow     | 15    | Right to Up-Right
YG       | Yellow→Green   | 6     | Up to Up-Left
GC       | Green→Cyan     | 4     | Up-Left to Left
CB       | Cyan→Blue      | 11    | Left to Down-Left
BM       | Blue→Magenta   | 13    | Down-Left to Down
MR       | Magenta→Red    | 6     | Down to Right
```

**Total:** 15 + 6 + 4 + 11 + 13 + 6 = **55 discrete colors**

---

## Step-by-Step Algorithm

### Step 1: Extract Flow Components

For each pixel, we have:
- `u` = horizontal flow
- `v` = vertical flow

```python
u = flow[:, :, 0]  # horizontal movement
v = flow[:, :, 1]  # vertical movement
```

### Step 2: Calculate Angle and Magnitude

**Angle** (which direction?):
```
angle = arctan2(-v, -u)  # in radians (-π to +π)
```

**Why negative?** Image coordinates have Y increasing downward, but we want colors to match intuitive directions.

**Magnitude** (how fast?):
```
magnitude = √(u² + v²)  # speed of movement
```

### Step 3: Normalize the Flow

Find the maximum flow in the entire image:
```python
max_magnitude = max(all magnitudes in image)
u_normalized = u / max_magnitude
v_normalized = v / max_magnitude
```

This ensures all values fit in our color wheel (0 to 1).

### Step 4: Map Angle to Color Wheel Position

Convert angle to color wheel index:
```python
a = arctan2(-v, -u) / π        # range: -1 to +1
fk = (a + 1) / 2 * (55 - 1) + 1  # range: 1 to 55
```

Now `fk` tells us where on the color wheel (which of 55 colors) to use.

### Step 5: Interpolate Between Colors

Since `fk` is a decimal (e.g., 23.7), we blend between two adjacent colors:

```python
k0 = floor(fk)        # e.g., 23 (lower color)
k1 = k0 + 1           # e.g., 24 (upper color)
f = fk - k0           # e.g., 0.7 (blend factor)

# Blend the colors:
final_color = (1 - f) * color[k0] + f * color[k1]
```

**Example:**
- `fk = 23.7`
- 30% of color #23 + 70% of color #24

### Step 6: Adjust Brightness by Magnitude

Pixels with **small flow** (slow movement) → **brighter** colors
Pixels with **large flow** (fast movement) → **darker** colors

```python
if magnitude <= 1:
    color = 1 - magnitude * (1 - color)  # bright for slow
else:
    color = color * 0.75                  # darker for very fast
```

### Step 7: Convert to RGB Image

The final color is converted to RGB (Red, Green, Blue) values from 0-255:

```python
rgb_image[:, :, R] = floor(255 * red_channel)
rgb_image[:, :, G] = floor(255 * green_channel)
rgb_image[:, :, B] = floor(255 * blue_channel)
```

---

## Visual Examples

### Example 1: Simple Right Movement

```
Original Flow Data:
┌─────────────┐
│ ●────→      │  All pixels moving right
└─────────────┘  u = +10, v = 0

Visualization:
┌─────────────┐
│ [RED COLOR] │  Red = moving right
└─────────────┘
```

### Example 2: Camera Moving Forward

```
Original Scene:
┌──────────┐
│    ◉     │  Camera moves forward
└──────────┘  (objects expand outward)

Flow Vectors:
    ↖  ↑  ↗
     ╲ │ ╱
    ← ◉ →      Everything moves outward
     ╱ │ ╲     from center
    ↙  ↓  ↘

Visualization:
┌──────────────────┐
│ Yellow          │  Up → Yellow
│   Green  Red   │  Left → Green, Right → Red
│     Blue       │  Down → Blue
└──────────────────┘
```

### Example 3: Object Moving Diagonally

```
Flow Vector:
     ↗  up-right
    /   u = +5, v = -5
   /    angle ≈ 45°

Visualization Color:
    [YELLOW-RED]  
    (Orange color)
```

---

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Optical Flow (u, v) for each pixel                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Calculate Angle and Magnitude                      │
│  angle = arctan2(-v, -u)                                    │
│  magnitude = sqrt(u² + v²)                                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Normalize by Maximum Flow                          │
│  u_norm = u / max_magnitude                                 │
│  v_norm = v / max_magnitude                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Map Angle to Color Wheel (55 colors)              │
│  color_index = (angle + π) / (2π) * 55                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Interpolate Between Adjacent Colors                │
│  color = blend(color[floor(index)], color[ceil(index)])    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Adjust Brightness by Magnitude                     │
│  if magnitude <= 1:                                         │
│      color = brighten(color, magnitude)                     │
│  else:                                                      │
│      color = darken(color, 0.75)                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT: RGB Image (0-255 per channel)                      │
│  Saved as: visflo-XXXXX.jpg                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Arrow Overlay (point_vec function)

In addition to the color-coded image, arrows are drawn to show flow direction:

### Arrow Drawing Process:

```
1. Original Image:
┌──────────────┐
│     ●        │
│              │
└──────────────┘

2. Add Color-Coded Flow:
┌──────────────┐
│     ● [RED]  │  Red = moving right
│              │
└──────────────┘

3. Add Arrows (every 20 pixels):
┌──────────────┐
│     ●────→   │  Arrow shows direction
│              │  Arrow color = flow color
└──────────────┘
```

### Arrow Parameters:
- **Skip**: Only draw arrows every 20 pixels (to avoid clutter)
- **Extend**: Arrows are 2× longer than actual flow for visibility
- **Color**: Arrow color matches the flow color from color wheel
- **Thickness**: 4 pixels thick with anti-aliasing

---

## Summary

### What Flow Visualization Does:

1. **Takes**: Numeric flow data `(u, v)` that's hard to interpret
2. **Converts**: To colors using the Middlebury color wheel
3. **Shows**: 
   - **Direction** through HUE (Red=right, Blue=down, etc.)
   - **Speed** through BRIGHTNESS (bright=slow, dark=fast)
4. **Outputs**: Beautiful, intuitive visualization as `visflo-*.jpg`

### Key Insights:

✅ **Color = Direction**: Red/Yellow/Green/Blue tell you which way pixels moved
✅ **Brightness = Speed**: Brighter colors = slower motion, darker = faster motion
✅ **Arrows = Clarity**: Overlaid arrows make direction even more obvious
✅ **Standardized**: Middlebury color wheel is an industry standard

### Remember:

```
Right  → Red    │  Up     → Yellow
Left   → Cyan   │  Down   → Blue
```

### Files Generated:

- **flo-*.png**: Raw flow data (2 channels: u, v)
- **visflo-*.jpg**: ✨ Color visualization (what you see!)
- **warped-*.jpg**: Second frame warped using flow

---

## Real-World Analogy

Think of it like **weather maps**:

```
Weather Map:                 Flow Visualization:
─────────────                ────────────────────
Red = Hot                    Red = Moving Right
Blue = Cold                  Blue = Moving Down
Arrows = Wind direction      Arrows = Pixel motion
```

Just as weather maps make temperature and wind visible, flow visualization makes pixel motion visible!

---

## Technical Details (for reference)

### Color Wheel Construction:

```python
# Segment sizes
RY = 15  # Red to Yellow
YG = 6   # Yellow to Green
GC = 4   # Green to Cyan
CB = 11  # Cyan to Blue
BM = 13  # Blue to Magenta
MR = 6   # Magenta to Red

Total = 55 colors
```

### Formula Reference:

```python
# Angle calculation
angle = arctan2(-v, -u) / π

# Color wheel index
index = (angle + 1) / 2 * 54 + 1

# Magnitude
magnitude = sqrt(u² + v²)

# Normalization
u_norm = u / max(all_magnitudes)
v_norm = v / max(all_magnitudes)
```

---

**Created for:** Bob Maser  
**Project:** Optical Flow Expansion  
**Date:** 2024

For more details, see `utils/flowlib.py` functions:
- `flow_to_image()` - Main conversion function
- `compute_color()` - Color mapping
- `make_color_wheel()` - Color wheel generation
- `point_vec()` - Arrow overlay

