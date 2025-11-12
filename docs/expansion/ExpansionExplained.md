# Optical Expansion Explained

A comprehensive guide to understanding optical expansion (divergence) in optical flow analysis.

**Author:** Bob Maser  
**Date:** November 12, 2024  
**Project:** OpticalFlowExpansion

---

## Table of Contents
1. [What is Optical Expansion?](#what-is-optical-expansion)
2. [Why Do We Need Expansion?](#why-do-we-need-expansion)
3. [The Mathematics Behind Expansion](#the-mathematics-behind-expansion)
4. [How It's Computed](#how-its-computed)
5. [Visual Examples](#visual-examples)
6. [Practical Applications](#practical-applications)
7. [Interpreting Expansion Maps](#interpreting-expansion-maps)
8. [Summary](#summary)

---

## What is Optical Expansion?

**Optical expansion** (also called **divergence**) measures how much the optical flow field is "spreading out" or "contracting" at each point in the image.

### Simple Analogy

Imagine you're watching water flow:
- **Positive expansion** (divergence): Water flowing away from a source, spreading out (like a fountain)
- **Negative expansion** (convergence): Water flowing toward a drain, coming together
- **Zero expansion**: Water flowing parallel, no spreading or contracting

In computer vision:
- **Positive expansion**: Objects getting larger (moving closer to camera)
- **Negative expansion**: Objects getting smaller (moving away from camera)
- **Zero expansion**: Objects moving parallel to image plane (no depth change)

### Mathematical Definition

Expansion is the **divergence** of the optical flow field:

```
div(u, v) = ∂u/∂x + ∂v/∂y
```

Where:
- `u(x, y)` = horizontal flow component
- `v(x, y)` = vertical flow component
- `∂u/∂x` = rate of change of horizontal flow in horizontal direction
- `∂v/∂y` = rate of change of vertical flow in vertical direction

---

## Why Do We Need Expansion?

### 1. **Depth Information**

Expansion is directly related to how fast objects are approaching or receding:

```
Expansion ∝ Velocity_toward_camera / Depth
```

**Key insight:** If you know the expansion and the object's speed, you can estimate its depth!

### 2. **Collision Detection**

For autonomous vehicles or drones:
- **Large positive expansion** in center of view = "Something is coming toward me fast!"
- **Uniform positive expansion** = "I'm moving forward into the scene"
- **Negative expansion** = "Objects are receding, safe"

### 3. **Scene Understanding**

Expansion helps distinguish:
- **Camera motion** (entire scene expands/contracts uniformly)
- **Object motion** (local regions have different expansion)
- **Rigid vs deformable objects** (rigid objects maintain consistent expansion patterns)

### 4. **Time-to-Contact (TTC)**

For a moving camera approaching a stationary object:

```
TTC = -1 / expansion
```

This tells autonomous systems: "How long until I hit that obstacle?"

---

## The Mathematics Behind Expansion

### Divergence Intuition

The divergence operator measures the "outflow" from a point:

![Divergence Concept](divergence_concept.png)

```
     ↗  ↑  ↖         Positive divergence
    →  •  ←          (flow spreading out)
     ↘  ↓  ↙

     ↖  ↑  ↗         Negative divergence
    ←  •  →          (flow converging)
     ↙  ↓  ↘
```

### Computation from Flow Field

Given optical flow `(u, v)` at each pixel, compute derivatives:

```python
# Horizontal derivative of horizontal flow
∂u/∂x ≈ (u[x+1, y] - u[x-1, y]) / 2

# Vertical derivative of vertical flow
∂v/∂y ≈ (v[x, y+1] - v[x, y-1]) / 2

# Expansion (divergence)
expansion = ∂u/∂x + ∂v/∂y
```

### Physical Interpretation

For a point moving in 3D space:

```
X = (X, Y, Z)  →  Image point (x, y)
```

The image coordinates change as:

```
x = f·X/Z
y = f·Y/Z
```

Taking time derivatives:

```
u = dx/dt = f·(Ẋ·Z - X·Ż)/Z²
v = dy/dt = f·(Ẏ·Z - Y·Ż)/Z²
```

The divergence becomes:

```
div(u, v) = -2f·Ż/Z² + (higher order terms)
```

**Key insight:** Expansion is proportional to `-Ż/Z²`:
- If `Ż < 0` (approaching), expansion is **positive**
- If `Ż > 0` (receding), expansion is **negative**

---

## How It's Computed

### Step 1: Compute Optical Flow

Use VCN, RAFT, or other methods to get flow field `(u, v)`.

### Step 2: Compute Spatial Derivatives

Use finite differences, Sobel operators, or Scharr filters:

```python
import cv2
import numpy as np

def compute_expansion(flow):
    """
    Compute expansion (divergence) from optical flow.
    
    Args:
        flow: Optical flow array (H, W, 2) where [:,:,0] is u, [:,:,1] is v
        
    Returns:
        expansion: Divergence map (H, W)
    """
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    
    # Compute derivatives using Sobel operator
    du_dx = cv2.Sobel(u, cv2.CV_64F, 1, 0, ksize=3) / 8.0
    dv_dy = cv2.Sobel(v, cv2.CV_64F, 0, 1, ksize=3) / 8.0
    
    # Expansion = divergence
    expansion = du_dx + dv_dy
    
    return expansion
```

### Step 3: Log Transform for Visualization

Since expansion can have large range, we typically use log transform:

```python
# Avoid log(0) by adding small epsilon
epsilon = 1e-8
log_expansion = np.sign(expansion) * np.log(np.abs(expansion) + epsilon)

# Normalize to [0, 255] for visualization
exp_norm = (log_expansion - log_expansion.min()) / (log_expansion.max() - log_expansion.min())
exp_vis = (exp_norm * 255).astype(np.uint8)
```

### What the Code Does

```python
# In submission.py (OpticalFlowExpansion project)

# 1. Extract flow components
flowx = flow[:,:,0:1]  # u component
flowy = flow[:,:,1:2]  # v component

# 2. Compute gradients
dx, dy = gradient_xy(flow)
# dx[:,:,0] = ∂u/∂x
# dx[:,:,1] = ∂v/∂x
# dy[:,:,0] = ∂u/∂y
# dy[:,:,1] = ∂v/∂y

# 3. Compute divergence
div = dx[:,:,0:1] + dy[:,:,1:2]  # ∂u/∂x + ∂v/∂y

# 4. Log transform
logexp = torch.sign(div)*torch.log(torch.abs(div)+1e-8)
```

---

## Visual Examples

### Example 1: Camera Moving Forward

When a camera moves forward, the entire scene expands radially:

![Camera Forward](camera_forward_expansion.png)

```
Scene view:         Expansion map:
   |  ↑  |             [+ + + +]
   ← • →   Camera      [+ + + +]  Positive everywhere
   |  ↓  |             [+ + + +]  (approaching all objects)
```

**Characteristics:**
- Positive expansion everywhere
- Stronger near image center (focus of expansion)
- Uniform if all objects at similar depth

### Example 2: Camera Moving Backward

When a camera moves backward, the scene contracts:

![Camera Backward](camera_backward_expansion.png)

```
Scene view:         Expansion map:
   →  ↓  ←             [- - - -]
   →  •  ←  Camera     [- - - -]  Negative everywhere
   →  ↑  ←             [- - - -]  (receding from all objects)
```

**Characteristics:**
- Negative expansion everywhere
- All objects receding
- Focus of contraction at image center

### Example 3: Object Approaching

Single object moving toward camera while others are stationary:

![Object Approaching](object_approaching.png)

```
Scene:              Expansion map:
Background          [0 0 0 0 0]
  Car→You           [0 + + + 0]  Positive only on moving object
Background          [0 + + + 0]
                    [0 0 0 0 0]
```

**Characteristics:**
- Positive expansion localized to moving object
- Background has zero/near-zero expansion
- Can segment moving objects

### Example 4: Complex Scene (UAV Flight)

Drone flying forward over varied terrain:

![UAV Flight](uav_flight_expansion.png)

```
Distant mountains:   Low positive expansion (far away)
Mid-range trees:     Medium positive expansion
Close ground:        High positive expansion (close objects)
```

**Color mapping (typical):**
- **Blue/Dark**: Negative expansion (receding)
- **Black/Gray**: Zero expansion (parallel motion)
- **Yellow/Red**: Positive expansion (approaching)

---

## Practical Applications

### 1. Obstacle Avoidance (Drones/Robots)

```python
def detect_collision_risk(expansion_map, threshold=0.5):
    """
    Detect potential collisions from expansion map.
    """
    # High positive expansion = approaching obstacles
    risk_zones = expansion_map > threshold
    
    # Compute risk score
    risk_score = np.mean(expansion_map[expansion_map > 0])
    
    if risk_score > threshold:
        return "COLLISION WARNING", risk_zones
    else:
        return "SAFE", risk_zones
```

### 2. Depth Estimation

```python
def estimate_relative_depth(expansion_map, velocity):
    """
    Estimate relative depth from expansion.
    
    Formula: depth ∝ velocity / expansion
    """
    epsilon = 1e-8
    relative_depth = velocity / (np.abs(expansion_map) + epsilon)
    
    return relative_depth
```

### 3. Motion Segmentation

```python
def segment_moving_objects(expansion_map, threshold=0.1):
    """
    Segment objects based on expansion anomalies.
    """
    # Compute global median expansion (camera motion)
    global_expansion = np.median(expansion_map)
    
    # Find regions with significantly different expansion
    anomaly = np.abs(expansion_map - global_expansion)
    moving_objects = anomaly > threshold
    
    return moving_objects
```

### 4. Time-to-Contact

```python
def compute_time_to_contact(expansion_map, min_ttc=0.1):
    """
    Compute time-to-contact for each pixel.
    
    TTC = -1 / expansion (for positive expansion)
    """
    ttc = np.zeros_like(expansion_map)
    
    # Only compute for positive expansion (approaching)
    mask = expansion_map > 0
    ttc[mask] = -1.0 / expansion_map[mask]
    
    # Clip unrealistic values
    ttc = np.clip(ttc, 0, 100)  # Max 100 seconds
    
    return ttc
```

---

## Interpreting Expansion Maps

### Color Coding (Typical Visualization)

Our project saves expansion as 16-bit PNG with normalized values:

```python
# In submission.py
exp_norm = (logexp - logexp.min()) / (logexp.max() - logexp.min() + 1e-8)
exp_16bit = (exp_norm * 65535).astype(np.uint16)
cv2.imwrite('exp-XXXX.png', exp_16bit)
```

When visualized with color map:

| Color | Value Range | Interpretation |
|-------|-------------|----------------|
| **Dark Blue** | 0 - 0.3 | Strong negative expansion (fast receding) |
| **Light Blue** | 0.3 - 0.45 | Moderate negative expansion |
| **Gray** | 0.45 - 0.55 | Near-zero expansion (parallel motion) |
| **Yellow** | 0.55 - 0.7 | Moderate positive expansion |
| **Red/White** | 0.7 - 1.0 | Strong positive expansion (fast approaching) |

### Reading Expansion Maps

**For UAV/Drone footage:**

1. **Uniform positive expansion** → Flying forward, check for obstacles
2. **Negative expansion at top, positive at bottom** → Descending
3. **Positive at top, negative at bottom** → Ascending  
4. **Left side positive, right side negative** → Rotating right
5. **Localized high expansion** → Object in motion or very close

**For Driving footage:**

1. **Strong positive in center** → Road ahead, moving forward
2. **Positive on sides** → Passing close objects (trees, buildings)
3. **Localized anomalies** → Other vehicles or pedestrians
4. **Negative expansion** → Braking or object moving away

### Common Patterns

```
Pattern 1: Forward Motion
╔════════════════╗
║ + + + + + + + +║  Uniform positive
║ + + +++ + + + +║  expansion, stronger
║ + ++++++++ + + ║  toward center
║ + + +++ + + + +║  (Focus of Expansion)
║ + + + + + + + +║
╚════════════════╝

Pattern 2: Rotating Camera
╔════════════════╗
║ + + + 0 - - - -║  Positive on one side,
║ + + + 0 - - - -║  negative on other
║ + + + 0 - - - -║  (Rotation axis)
║ + + + 0 - - - -║
╚════════════════╝

Pattern 3: Moving Object
╔════════════════╗
║ 0 0 0 0 0 0 0 0║  Localized expansion
║ 0 0 +++ 0 0 0 0║  on moving object
║ 0 0 +++ 0 0 0 0║  background is zero
║ 0 0 0 0 0 0 0 0║
╚════════════════╝
```

---

## Implementation Details (VCN Model)

The OpticalFlowExpansion project uses a volumetric cost network to compute expansion:

### Architecture

```
Input: Frame pair (I₁, I₂)
   ↓
Feature Extraction (CNN)
   ↓
Cost Volume Construction
   ↓
Cost Aggregation
   ↓
Optical Flow (u, v)
   ↓
Gradient Computation (∂u/∂x, ∂v/∂y)
   ↓
Expansion = ∂u/∂x + ∂v/∂y
```

### Advantages of Learning-Based Approach

**Traditional methods** (finite differences on estimated flow):
- Noisy flow → Very noisy expansion
- Errors amplified by derivative computation

**VCN approach** (joint estimation):
- Smoother flow field
- Regularized expansion
- End-to-end learned from data
- Better handles occlusions and discontinuities

### Code Snippet from Project

```python
# From submission.py

# Compute flow
pred_flow = model(imgL, imgR)  # VCN model

# Extract components
flowx = flow[:,:,0:1]
flowy = flow[:,:,1:2]

# Compute spatial gradients
dx, dy = gradient_xy(flow)

# Divergence (expansion)
div = dx[:,:,0:1] + dy[:,:,1:2]

# Log transform for numerical stability
logexp = torch.sign(div)*torch.log(torch.abs(div)+1e-8)

# Save as 16-bit PNG
exp_norm = (logexp - logexp.min()) / (logexp.max() - logexp.min() + 1e-8)
exp_16bit = (exp_norm * 65535).astype(np.uint16)
cv2.imwrite('exp-%s.png' % filename, exp_16bit)
```

---

## Summary

### Key Takeaways

1. **Definition**: Expansion = divergence of optical flow = `∂u/∂x + ∂v/∂y`

2. **Physical Meaning**: 
   - Positive expansion → Objects approaching camera
   - Negative expansion → Objects receding
   - Zero expansion → Parallel motion

3. **Applications**:
   - Collision detection and avoidance
   - Depth estimation
   - Time-to-contact computation
   - Motion segmentation
   - Camera ego-motion analysis

4. **Computation**:
   - Compute optical flow
   - Calculate spatial derivatives
   - Sum horizontal and vertical divergence
   - Apply log transform for visualization

5. **Interpretation**:
   - Look for uniform patterns (camera motion)
   - Look for anomalies (moving objects)
   - High values near center = forward motion
   - Localized high values = approaching objects

### Related Concepts

- **Optical Flow**: The 2D velocity field → Expansion is derived from this
- **Motion-in-Depth**: Ratio of depths (τ = d₂/d₁) → Related but different
- **Curl**: Rotation component of flow (∂v/∂x - ∂u/∂y)
- **Deformation**: Full Jacobian of flow field

### Further Reading

- **Mathematics**: Vector Calculus, Divergence Theorem
- **Computer Vision**: Structure from Motion, Visual Odometry
- **Robotics**: Visual Servoing, Obstacle Avoidance
- **Papers**: 
  - Horn & Schunck (1981) - Optical Flow fundamentals
  - Longuet-Higgins & Prazdny (1980) - Interpretation of optical flow
  - VCN paper - Modern deep learning approach

---

## Quick Reference

### Python Code Template

```python
import cv2
import numpy as np

# 1. Load expansion map
exp_map = cv2.imread('exp-0001.png', cv2.IMREAD_UNCHANGED)
exp_normalized = exp_map.astype(np.float32) / 65535.0

# 2. Reverse log transform (if needed)
exp_linear = np.sign(exp_normalized - 0.5) * np.exp(np.abs(exp_normalized - 0.5))

# 3. Visualize with color map
exp_vis = cv2.applyColorMap((exp_normalized * 255).astype(np.uint8), cv2.COLORMAP_JET)
cv2.imshow('Expansion', exp_vis)

# 4. Detect high expansion regions
threshold = 0.7  # Adjust based on your data
approaching = exp_normalized > threshold
cv2.imshow('Approaching Objects', approaching.astype(np.uint8) * 255)
```

### Matlab Code Template

```matlab
% 1. Load expansion map
exp_map = imread('exp-0001.png');
exp_normalized = double(exp_map) / 65535.0;

% 2. Visualize
figure;
imagesc(exp_normalized);
colormap(jet);
colorbar;
title('Optical Expansion');

% 3. Detect approaching regions
threshold = 0.7;
approaching = exp_normalized > threshold;
figure;
imshow(approaching);
title('Approaching Objects');
```

---

**Document Version:** 1.0  
**Last Updated:** November 12, 2024  
**Author:** Bob Maser  
**Project:** OpticalFlowExpansion  
**Location:** `/home/bobmaser/github/OpticalFlowExpansion/docs/expansion/`

