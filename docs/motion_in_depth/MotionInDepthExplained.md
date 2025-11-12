# Motion-in-Depth Explained

A comprehensive guide to understanding motion-in-depth (τ = d₂/d₁) in optical flow analysis.

**Author:** Bob Maser  
**Date:** November 12, 2024  
**Project:** OpticalFlowExpansion

---

## Table of Contents
1. [What is Motion-in-Depth?](#what-is-motion-in-depth)
2. [Why Do We Need Motion-in-Depth?](#why-do-we-need-motion-in-depth)
3. [The Mathematics Behind MID](#the-mathematics-behind-mid)
4. [Relationship to Optical Expansion](#relationship-to-optical-expansion)
5. [How It's Computed](#how-its-computed)
6. [Visual Examples](#visual-examples)
7. [Practical Applications](#practical-applications)
8. [Interpreting MID Maps](#interpreting-mid-maps)
9. [Summary](#summary)

---

## What is Motion-in-Depth?

**Motion-in-Depth (MID)**, denoted as **τ (tau)**, is the ratio of depths between two consecutive frames:

```
τ = d₂/d₁ = Z(t+1) / Z(t)
```

Where:
- `d₁` or `Z(t)` = depth at time t (first frame)
- `d₂` or `Z(t+1)` = depth at time t+1 (second frame)
- `τ` = depth ratio (motion-in-depth parameter)

### Simple Analogy

Imagine watching a car approach you:
- **Frame 1:** Car is 100 meters away (d₁ = 100m)
- **Frame 2:** Car is 90 meters away (d₂ = 90m)
- **τ = 90/100 = 0.9** (The car got closer, depth decreased by 10%)

Or imagine a person walking away:
- **Frame 1:** Person is 5 meters away (d₁ = 5m)
- **Frame 2:** Person is 6 meters away (d₂ = 6m)
- **τ = 6/5 = 1.2** (The person moved farther, depth increased by 20%)

### Key Interpretation

```
τ < 1  →  Object APPROACHING (depth decreased)
τ = 1  →  No motion in depth (parallel motion only)
τ > 1  →  Object RECEDING (depth increased)
```

### Real-World Meaning

Motion-in-depth tells us **how much closer or farther** an object is between frames:
- **τ = 0.5**: Object is now at **half** the original distance (very fast approach!)
- **τ = 0.9**: Object is at **90%** of original distance (slow approach)
- **τ = 1.0**: Object maintains **same** distance (parallel motion)
- **τ = 1.1**: Object is at **110%** of original distance (slow recession)
- **τ = 2.0**: Object is now **twice** as far (fast recession)

---

## Why Do We Need Motion-in-Depth?

### 1. **3D Structure Recovery**

MID provides depth information without stereo:
- Single moving camera can estimate depth changes
- Essential for monocular 3D reconstruction
- Complements optical flow (2D motion)

### 2. **Scene Flow Computation**

Optical flow gives 2D motion, MID adds the 3rd dimension:

```
2D Flow (u, v)  +  MID (τ)  =  3D Motion (Scene Flow)
```

Scene flow describes full 3D motion of every point in the scene.

### 3. **Separating Camera vs Object Motion**

MID helps distinguish:
- **Camera motion**: Affects entire scene uniformly
- **Object motion**: Creates local MID variations
- **Static objects**: τ depends only on camera motion

### 4. **Depth Ordering & Segmentation**

Objects at different depths have different τ values:
- Close objects: Larger τ variation
- Far objects: τ ≈ 1 (less depth change)
- Can segment scene by depth layers

### 5. **Physical Interaction Understanding**

For robotics and autonomous systems:
- Approaching obstacles (τ < 1): Take evasive action
- Receding objects (τ > 1): Safe to proceed
- Constant depth (τ = 1): Object moving parallel

---

## The Mathematics Behind MID

### Geometric Foundation

Consider a 3D point **P = (X, Y, Z)** at time t:

```
Frame 1: P₁ = (X₁, Y₁, Z₁)
Frame 2: P₂ = (X₂, Y₂, Z₂)
```

The motion-in-depth parameter is:

```
τ = Z₂/Z₁
```

### Relationship to Image Coordinates

A 3D point projects to image coordinates:

```
x = f·X/Z
y = f·Y/Z
```

Where f is focal length.

### Optical Flow and MID

The optical flow (u, v) relates to 3D motion:

```
u = f·(Ẋ·Z - X·Ż)/Z²
v = f·(Ẏ·Z - Y·Ż)/Z²
```

The motion-in-depth can be expressed as:

```
τ = (Z + Ż·Δt) / Z = 1 + (Ż/Z)·Δt
```

Where:
- `Ż` = velocity in depth direction
- `Δt` = time between frames

### Log Transform

Since τ can range from near 0 to infinity, we use log transform:

```
log(τ) = log(Z₂/Z₁) = log(Z₂) - log(Z₁)
```

**Interpretation of log(τ):**
- `log(τ) < 0`: Approaching (τ < 1)
- `log(τ) = 0`: No depth change (τ = 1)
- `log(τ) > 0`: Receding (τ > 1)

The log transform has nice properties:
- Symmetric around 0
- Additive: log(d₃/d₁) = log(d₃/d₂) + log(d₂/d₁)
- Easier to visualize

---

## Relationship to Optical Expansion

Motion-in-depth and optical expansion are **closely related**:

### Mathematical Connection

Recall expansion (divergence):

```
div = ∂u/∂x + ∂v/∂y
```

For a point moving primarily in depth:

```
div ≈ -2f·Ż/Z² = -2f·(1-τ)/(Z·Δt)
```

### Key Relationship

```
τ ≈ 1 - (div·Z·Δt)/(2f)
```

Or inversely:

```
div ≈ -2f·(1-τ)/(Z·Δt)
```

### Intuitive Connection

- **High negative expansion** (div << 0) → **τ << 1** (approaching)
- **Zero expansion** (div ≈ 0) → **τ ≈ 1** (parallel motion)
- **High positive expansion** (div >> 0) → **τ >> 1** (receding)

**Wait, that seems backwards!** 

Actually, there's a sign convention issue. In the VCN model:
- Large positive expansion → Approaching (τ < 1)
- Large negative expansion → Receding (τ > 1)

The exact relationship depends on the model's convention.

### Complementary Information

| Property | Optical Expansion | Motion-in-Depth |
|----------|------------------|-----------------|
| **Type** | Local differential | Integrated ratio |
| **Units** | 1/time | Dimensionless |
| **Range** | -∞ to +∞ | 0 to +∞ |
| **Interpretation** | Rate of depth change | Total depth change |
| **Use Case** | Immediate collision detection | 3D reconstruction |

They provide complementary views:
- **Expansion**: How **fast** is depth changing?
- **MID**: By what **ratio** did depth change?

---

## How It's Computed

### Method 1: From Optical Flow (Traditional)

Given optical flow and known camera motion:

```python
def compute_mid_from_flow(flow, focal_length, camera_velocity, dt):
    """
    Compute motion-in-depth from optical flow.
    
    Requires known camera motion (egomotion).
    """
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    
    # Assume camera moves forward with velocity V
    # For a point at depth Z:
    # tau = 1 + (V/Z) * dt
    
    # From flow magnitude and direction, estimate Z
    # (This is simplified; actual computation is more complex)
    
    # Example: radial expansion from FOE
    foe_x, foe_y = image_center
    dx = x_coords - foe_x
    dy = y_coords - foe_y
    
    # Depth from expansion
    expansion = compute_divergence(flow)
    Z_estimate = -2 * focal_length * camera_velocity / (expansion + 1e-8)
    
    # Motion-in-depth
    tau = 1 + (camera_velocity / Z_estimate) * dt
    
    return tau
```

### Method 2: Deep Learning (VCN Approach)

The VCN model learns to estimate τ directly from image pairs:

```python
# In VCN model (simplified)

# 1. Extract features from both images
feat1 = feature_extractor(img1)
feat2 = feature_extractor(img2)

# 2. Build cost volume (correlation)
cost_volume = build_cost_volume(feat1, feat2)

# 3. Predict flow and depth changes jointly
flow, expansion, mid = decoder(cost_volume)

# 4. Motion-in-depth (tau)
# Learned directly as part of scene flow estimation
tau = mid  # Output from network
```

### Implementation in Our Project

```python
# From submission.py

# After computing flow and expansion:
logexp = torch.sign(div)*torch.log(torch.abs(div)+1e-8)

# Motion-in-depth is computed from expansion
# Using learned relationship between div and tau
logmid = model.compute_mid(flow, div)  # Simplified

# The actual VCN model has a dedicated head for this:
# mid_logits = mid_decoder(features, flow, expansion)
# tau = torch.exp(mid_logits)

# Save as 16-bit PNG (normalized)
mid_norm = (logmid - logmid.min()) / (logmid.max() - logmid.min() + 1e-8)
mid_16bit = (mid_norm * 65535).astype(np.uint16)
cv2.imwrite('mid-%s.png' % filename, mid_16bit)
```

### Why Deep Learning Works Better

**Traditional methods** require:
- Known camera parameters (focal length)
- Known egomotion (camera velocity)
- Accurate flow estimation
- Solving complex optimization

**VCN approach**:
- Learns from data (stereo + flow datasets)
- No need for explicit camera parameters
- Joint optimization of flow + expansion + MID
- Handles occlusions and textureless regions better

---

## Visual Examples

### Example 1: Camera Moving Forward (Uniform Approach)

When camera moves straight forward, all points approach:

![Camera Forward MID](camera_forward_mid.png)

```
Scene:              MID Map (τ):
  ← •  →              [0.8 0.8 0.8]  
  ← • →   Camera      [0.9 0.9 0.9]  All τ < 1
  ← • →               [0.95 0.95 0.95]  (approaching)
```

**Characteristics:**
- All points have τ < 1 (approaching)
- Closer objects: Smaller τ (larger depth change)
- Far objects: τ closer to 1 (small depth change)
- Radial pattern from focus of expansion

**Depth Interpretation:**
- If you move 1 meter forward:
  - Object at 100m: τ ≈ 0.99 (now at 99m)
  - Object at 10m: τ ≈ 0.9 (now at 9m)
  - Object at 2m: τ ≈ 0.5 (now at 1m)

### Example 2: Camera Moving Backward (Uniform Recession)

When camera moves backward, all points recede:

![Camera Backward MID](camera_backward_mid.png)

```
Scene:              MID Map (τ):
  → • ←               [1.05 1.05 1.05]
  → • ←   Camera      [1.1 1.1 1.1]  All τ > 1
  → • ←               [1.2 1.2 1.2]  (receding)
```

**Characteristics:**
- All points have τ > 1 (receding)
- Closer objects: Larger τ (larger depth change)
- Far objects: τ closer to 1 (small depth change)

### Example 3: Object Approaching (While Camera Static)

Car approaching a stationary camera:

![Object Approaching MID](object_approaching_mid.png)

```
Scene:              MID Map (τ):
Background          [1.0 1.0 1.0 1.0]  Static (τ = 1)
  🚗→You            [1.0 0.7 0.7 1.0]  Car has τ < 1
Background          [1.0 1.0 1.0 1.0]  Static (τ = 1)
```

**Characteristics:**
- Background: τ ≈ 1 (no depth change)
- Moving car: τ < 1 (approaching)
- Sharp boundaries at object edges
- Can segment moving objects

### Example 4: Mixed Scene (UAV Descending)

Drone descending over terrain:

![UAV Descending MID](uav_descending_mid.png)

```
Top (sky):          τ ≈ 1.0 (far background)
Middle (trees):     τ = 0.8 (getting closer)
Bottom (ground):    τ = 0.6 (rapidly approaching)
```

**Characteristics:**
- Gradient from top to bottom
- Sky: τ ≈ 1 (infinite depth, no change)
- Ground: Small τ (close and getting closer)
- Trees: Intermediate τ

### Example 5: Depth Layers

Scene with multiple depth planes:

![Depth Layers MID](depth_layers_mid.png)

```
Layer 1 (close):    τ = 0.5  (2m → 1m)
Layer 2 (medium):   τ = 0.8  (10m → 8m)
Layer 3 (far):      τ = 0.95 (100m → 95m)
Background:         τ = 1.0  (sky, infinite)
```

**Key Insight:** MID reveals depth stratification!

---

## Practical Applications

### 1. Monocular 3D Reconstruction

```python
def reconstruct_3d_from_flow_and_mid(flow, tau, focal_length):
    """
    Reconstruct 3D scene structure from single moving camera.
    
    Args:
        flow: Optical flow (H, W, 2)
        tau: Motion-in-depth (H, W)
        focal_length: Camera focal length
        
    Returns:
        depth_map: Estimated depth for each pixel
    """
    # From tau and flow, estimate absolute depth
    # This is a simplified example
    
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    
    # For known camera translation T:
    # tau = (Z + T) / Z
    # Solving for Z:
    # Z = T / (1 - tau)
    
    # Assume camera moves forward with T = 1 meter
    T = 1.0
    depth_map = T / (1 - tau + 1e-8)
    
    # Clip unrealistic values
    depth_map = np.clip(depth_map, 0.1, 1000)
    
    return depth_map
```

### 2. Scene Flow Estimation

```python
def compute_scene_flow(flow_2d, tau, depth, dt=1.0):
    """
    Compute 3D scene flow from 2D flow and motion-in-depth.
    
    Scene flow = 3D motion vector for each point
    """
    u = flow_2d[:, :, 0]
    v = flow_2d[:, :, 1]
    
    # 3D motion components
    # Assuming calibrated camera
    Z1 = depth
    Z2 = tau * Z1
    
    # 3D velocities
    Vx = u * Z1  # Simplified; needs camera parameters
    Vy = v * Z1
    Vz = (Z2 - Z1) / dt
    
    scene_flow = np.stack([Vx, Vy, Vz], axis=-1)
    
    return scene_flow
```

### 3. Collision Time Estimation

```python
def estimate_collision_time(tau, dt, threshold=0.1):
    """
    Estimate time until collision for approaching objects.
    
    Args:
        tau: Motion-in-depth map
        dt: Time between frames (seconds)
        threshold: Minimum tau to consider
        
    Returns:
        time_to_contact: Map of collision times (seconds)
    """
    # For tau < 1 (approaching), estimate collision time
    approaching = tau < 1.0
    
    # Time to contact: T = d / v
    # From tau: tau = (d - v*dt) / d
    # Solving: v/d = (1 - tau) / dt
    # TTC = d/v = dt / (1 - tau)
    
    ttc = np.full_like(tau, np.inf)
    ttc[approaching] = dt / (1 - tau[approaching] + 1e-8)
    
    # Clip unrealistic values
    ttc = np.clip(ttc, 0, 100)  # Max 100 seconds
    
    return ttc
```

### 4. Object Segmentation by Depth Motion

```python
def segment_by_depth_motion(tau, flow, threshold=0.05):
    """
    Segment objects based on different motion-in-depth.
    
    Useful for separating independently moving objects.
    """
    # Compute global median tau (camera motion)
    global_tau = np.median(tau)
    
    # Find regions with significantly different tau
    tau_anomaly = np.abs(tau - global_tau)
    
    # Also consider flow magnitude
    flow_mag = np.sqrt(flow[:, :, 0]**2 + flow[:, :, 1]**2)
    
    # Segment: different tau + significant motion
    moving_objects = (tau_anomaly > threshold) & (flow_mag > 5.0)
    
    # Clean up with morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    moving_objects = cv2.morphologyEx(
        moving_objects.astype(np.uint8),
        cv2.MORPH_CLOSE,
        kernel
    ).astype(bool)
    
    return moving_objects
```

### 5. Depth Ordering

```python
def estimate_depth_ordering(tau, camera_motion='forward'):
    """
    Estimate relative depth ordering from motion-in-depth.
    
    Objects with smaller tau are generally closer.
    """
    if camera_motion == 'forward':
        # Smaller tau = closer (more relative depth change)
        depth_order = 1.0 / (tau + 1e-8)
    elif camera_motion == 'backward':
        # Larger tau = closer
        depth_order = tau
    else:
        # Unknown camera motion
        depth_order = np.abs(1.0 - tau)
    
    # Normalize to [0, 1]
    depth_order = (depth_order - depth_order.min()) / (depth_order.max() - depth_order.min() + 1e-8)
    
    return depth_order
```

### 6. UAV Terrain Following

```python
def compute_terrain_clearance(tau, camera_height, dt):
    """
    Compute terrain clearance for UAV navigation.
    
    Args:
        tau: Motion-in-depth map
        camera_height: UAV altitude (meters)
        dt: Time between frames
        
    Returns:
        clearance_map: Distance to ground for each pixel
    """
    # Assuming UAV descends vertically
    # Terrain at different heights will have different tau
    
    # From tau, estimate relative depth
    # (This is simplified; real application needs calibration)
    
    descent_rate = ...  # From IMU or GPS
    
    # Ground distance from tau
    ground_distance = camera_height / (1 - tau + 1e-8)
    
    return ground_distance
```

---

## Interpreting MID Maps

### Color Coding (Typical Visualization)

Our project saves MID as 16-bit PNG with log-transformed, normalized values:

```python
# In submission.py
mid_norm = (logmid - logmid.min()) / (logmid.max() - logmid.min() + 1e-8)
mid_16bit = (mid_norm * 65535).astype(np.uint16)
cv2.imwrite('mid-XXXX.png', mid_16bit)
```

When visualized with a color map (e.g., Jet):

| Color | Normalized Value | log(τ) | τ (approx) | Interpretation |
|-------|-----------------|--------|------------|----------------|
| **Dark Blue** | 0.0 - 0.3 | Large negative | << 1 | Fast approaching |
| **Light Blue** | 0.3 - 0.45 | Small negative | 0.8 - 0.95 | Slow approaching |
| **Gray/Green** | 0.45 - 0.55 | Near zero | ≈ 1.0 | No depth change |
| **Yellow** | 0.55 - 0.7 | Small positive | 1.05 - 1.2 | Slow receding |
| **Red/White** | 0.7 - 1.0 | Large positive | >> 1 | Fast receding |

### Reading MID Maps

**For Forward Camera Motion:**

1. **Uniform blue tones** → All objects approaching (consistent with forward motion)
2. **Darker blue near bottom** → Ground closer, larger depth change
3. **Lighter blue at top** → Sky/far objects, minimal depth change
4. **Localized gray/red** → Object moving away from camera

**For Stationary Camera:**

1. **Mostly gray** → Static scene (τ ≈ 1)
2. **Blue regions** → Objects approaching
3. **Red regions** → Objects receding
4. **Sharp boundaries** → Object edges, occlusions

**For UAV/Drone:**

1. **Gradient pattern** → Terrain at different depths
2. **Blue dominant** → Descending or moving forward
3. **Red dominant** → Ascending or moving backward
4. **Horizontal bands** → Depth layers (ground, trees, sky)

### Common Patterns

```
Pattern 1: Forward Motion (Uniform Approach)
╔════════════════╗
║ B B B B B B B B║  B = Blue (approaching)
║ B B BB BB B B B║  Darker near center (FOE)
║ B BBBBBBBB B B║  or near bottom (ground)
║ B B BB BB B B B║
║ B B B B B B B B║
╚════════════════╝

Pattern 2: Backward Motion (Uniform Recession)
╔════════════════╗
║ R R R R R R R R║  R = Red (receding)
║ R R RR RR R R R║  All points moving away
║ R RRRRRRRR R R║
║ R R RR RR R R R║
║ R R R R R R R R║
╚════════════════╝

Pattern 3: Moving Object (Static Background)
╔════════════════╗
║ G G G G G G G G║  G = Gray (static, τ=1)
║ G G BB B G G G║  B = Blue (approaching car)
║ G G BB B G G G║
║ G G G G G G G G║
╚════════════════╝

Pattern 4: Depth Layers
╔════════════════╗
║ G G G G G G G G║  Sky (far, τ≈1)
║ LB LB LB LB LB║  Trees (light blue)
║ B B B B B B B B║  Ground (blue)
║ DB DB DB DB DB║  Close ground (dark blue)
╚════════════════╝
```

---

## Implementation Details (VCN Model)

### Architecture Overview

The VCN model predicts motion-in-depth as part of scene flow:

```
Input: Image pair (I₁, I₂)
   ↓
Feature Extraction (Shared weights)
   ↓
Cost Volume Construction (4D correlation)
   ↓
Cost Aggregation (3D convolutions)
   ↓
Multi-scale Decoder
   ↓
├── Optical Flow (u, v)
├── Expansion (div)
└── Motion-in-Depth (τ)  ← Our focus
```

### Training Strategy

VCN is trained on multiple datasets:
- **Stereo datasets**: KITTI, SceneFlow → Learn depth
- **Flow datasets**: Sintel, FlyingThings → Learn motion
- **Self-supervised**: Photometric loss + smoothness

The network learns to predict τ by:
1. Geometric consistency (flow + depth must be consistent)
2. Photometric consistency (warping with τ should match images)
3. Smoothness regularization (piecewise smooth τ)

### Loss Function

```python
# Simplified training loss for motion-in-depth

# 1. Photometric loss (warp frame 2 to frame 1 using flow and tau)
I1_warped = warp_with_depth(I2, flow, tau)
photo_loss = |I1 - I1_warped|

# 2. Geometric consistency
tau_from_flow = compute_tau_from_flow(flow, expansion)
geo_loss = |tau - tau_from_flow|

# 3. Smoothness
smooth_loss = |∇tau|

# Total loss
loss = photo_loss + λ₁*geo_loss + λ₂*smooth_loss
```

### Advantages of Joint Estimation

VCN estimates flow, expansion, and MID **jointly**:

**Benefits:**
- Shared features improve all predictions
- Geometric constraints enforce consistency
- End-to-end learning from data
- Handles difficult cases (occlusions, textureless regions)

**vs. Sequential estimation:**
- Flow → Expansion → MID (errors accumulate)
- Each stage needs separate optimization
- No feedback between components

---

## Relationship to Other Outputs

### Motion-in-Depth vs Expansion

| Property | Expansion (div) | Motion-in-Depth (τ) |
|----------|----------------|---------------------|
| **Definition** | ∂u/∂x + ∂v/∂y | Z₂ / Z₁ |
| **Type** | Differential | Integral/Ratio |
| **Units** | 1/time | Dimensionless |
| **Range** | -∞ to +∞ | 0 to +∞ |
| **Meaning** | Rate of depth change | Total depth change |
| **Use** | Collision detection | 3D reconstruction |

**Connection:**
```
τ ≈ 1 + (expansion · Z · Δt) / (2f)
```

### Motion-in-Depth vs Optical Flow

| Property | Optical Flow (u, v) | Motion-in-Depth (τ) |
|----------|-------------------|---------------------|
| **Dimensions** | 2D (image plane) | 1D (depth axis) |
| **Information** | Lateral motion | Depth motion |
| **Combined** | Scene Flow (full 3D motion) | |

**Together they form Scene Flow:**
```
Scene Flow = (u, v, τ) = (lateral_x, lateral_y, depth_change)
```

### Motion-in-Depth vs Occlusion

MID and occlusion are related:
- **Approaching objects** (τ < 1) create **occlusions** (hide background)
- **Receding objects** (τ > 1) create **disocclusions** (reveal background)
- **Occlusion boundaries** often have large τ gradients

---

## Summary

### Key Takeaways

1. **Definition**: Motion-in-Depth τ = Z₂/Z₁ = depth ratio between frames

2. **Physical Meaning**:
   - τ < 1 → Approaching (closer in frame 2)
   - τ = 1 → No depth change (parallel motion)
   - τ > 1 → Receding (farther in frame 2)

3. **Applications**:
   - Monocular 3D reconstruction
   - Scene flow estimation
   - Collision time prediction
   - Depth-based segmentation
   - UAV terrain navigation

4. **Computation**:
   - Traditional: From flow + known camera motion
   - VCN: Joint learning with flow and expansion
   - Output: Log-transformed, normalized 16-bit PNG

5. **Interpretation**:
   - Blue colors → Approaching
   - Gray colors → Static depth
   - Red colors → Receding
   - Gradients → Depth layers

### Related Concepts

- **Optical Flow**: 2D motion → MID adds 3rd dimension
- **Expansion**: Rate of depth change → MID is integrated change
- **Scene Flow**: Full 3D motion = (flow, MID)
- **Depth**: τ relates consecutive depth maps: d₂ = τ·d₁

### Further Reading

- **Papers**:
  - VCN (Yang et al., 2019) - Joint flow and depth estimation
  - Scene Flow estimation papers
  - Structure from Motion literature
  
- **Books**:
  - Hartley & Zisserman - "Multiple View Geometry"
  - Szeliski - "Computer Vision: Algorithms and Applications"

---

## Quick Reference

### Python Code Template

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Load motion-in-depth map
mid_map = cv2.imread('mid-0001.png', cv2.IMREAD_UNCHANGED)
mid_normalized = mid_map.astype(np.float32) / 65535.0

# 2. Visualize
plt.imshow(mid_normalized, cmap='jet')
plt.colorbar(label='Normalized log(τ)')
plt.title('Motion-in-Depth')
plt.show()

# 3. Reverse log transform (approximate)
# Note: Exact values lost in normalization
log_tau_centered = (mid_normalized - 0.5) * 4  # Scale factor depends on data
tau_estimate = np.exp(log_tau_centered)

# 4. Find approaching objects
approaching = mid_normalized < 0.45  # Below midpoint
plt.imshow(approaching, cmap='Reds', alpha=0.5)
plt.title('Approaching Regions (τ < 1)')
plt.show()

# 5. Estimate collision time
dt = 0.033  # 30 fps
tau_approaching = tau_estimate[approaching]
ttc = dt / (1 - tau_approaching + 1e-8)
print(f"Min time-to-contact: {np.min(ttc):.2f} seconds")
```

### MATLAB Code Template

```matlab
% 1. Load motion-in-depth map
mid_map = imread('mid-0001.png');
mid_normalized = double(mid_map) / 65535.0;

% 2. Visualize
figure;
imagesc(mid_normalized);
colormap(jet);
colorbar;
title('Motion-in-Depth');

% 3. Find approaching objects
approaching = mid_normalized < 0.45;
figure;
imshow(approaching);
title('Approaching Regions');

% 4. Estimate tau (approximate)
log_tau = (mid_normalized - 0.5) * 4;
tau_estimate = exp(log_tau);

% 5. Depth segmentation
depth_layers = kmeans(mid_normalized(:), 3);
depth_layers = reshape(depth_layers, size(mid_normalized));
figure;
imagesc(depth_layers);
colormap(parula);
title('Depth Layers from MID');
```

---

**Document Version:** 1.0  
**Last Updated:** November 12, 2024  
**Author:** Bob Maser  
**Project:** OpticalFlowExpansion  
**Location:** `/home/bobmaser/github/OpticalFlowExpansion/docs/motion_in_depth/`

