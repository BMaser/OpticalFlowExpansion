"""
Generate visual diagrams for Motion-in-Depth documentation.

This script creates various diagrams to illustrate motion-in-depth concepts:
1. Tau concept diagram
2. Camera forward motion
3. Camera backward motion
4. Object approaching
5. UAV descending
6. Depth layers
7. Interpretation guide

Author: Bob Maser
Date: November 12, 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch
import cv2
import os

# Set output directory
OUTPUT_DIR = '/home/bobmaser/github/OpticalFlowExpansion/docs/motion_in_depth'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_tau_concept():
    """Create diagram explaining tau = d2/d1 concept."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Approaching (tau < 1)
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Approaching: τ < 1\n(Depth Decreases)', fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Frame 1
    ax.text(2, 8, 'Frame 1:', fontsize=12, fontweight='bold')
    car1 = Rectangle((1.5, 5), 1.5, 1.2, fill=True, facecolor='blue', 
                     edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax.add_patch(car1)
    ax.text(2.25, 5.6, '🚗', fontsize=25, ha='center', va='center')
    ax.text(2.25, 4.5, 'd₁ = 100m', ha='center', fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Frame 2
    ax.text(6, 8, 'Frame 2:', fontsize=12, fontweight='bold')
    car2 = Rectangle((5, 4.5), 2, 1.6, fill=True, facecolor='red',
                     edgecolor='darkred', linewidth=2, alpha=0.7)
    ax.add_patch(car2)
    ax.text(6, 5.3, '🚗', fontsize=35, ha='center', va='center')
    ax.text(6, 3.5, 'd₂ = 80m', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    # Arrow showing motion
    ax.annotate('', xy=(5, 5.5), xytext=(3, 5.5),
                arrowprops=dict(arrowstyle='->', lw=3, color='green'))
    ax.text(4, 6, 'Getting Closer!', ha='center', fontsize=11, fontweight='bold',
            color='green')
    
    # Result
    ax.text(5, 1.5, 'τ = d₂/d₁ = 80/100 = 0.8', ha='center', fontsize=13,
            fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    ax.text(5, 0.5, '(20% closer)', ha='center', fontsize=11, color='green')
    
    # No depth change (tau = 1)
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('No Depth Change: τ = 1\n(Parallel Motion)', fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Frame 1
    ax.text(2, 8, 'Frame 1:', fontsize=12, fontweight='bold')
    person1 = Circle((2.25, 5.5), 0.6, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax.add_patch(person1)
    ax.text(2.25, 5.5, '🚶', fontsize=25, ha='center', va='center')
    ax.text(2.25, 4.5, 'd₁ = 10m', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Frame 2
    ax.text(6, 8, 'Frame 2:', fontsize=12, fontweight='bold')
    person2 = Circle((7, 5.5), 0.6, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax.add_patch(person2)
    ax.text(7, 5.5, '🚶', fontsize=25, ha='center', va='center')
    ax.text(7, 4.5, 'd₂ = 10m', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Arrow showing lateral motion
    ax.annotate('', xy=(6.5, 5.5), xytext=(3, 5.5),
                arrowprops=dict(arrowstyle='->', lw=3, color='gray'))
    ax.text(4.75, 6, 'Moving Sideways', ha='center', fontsize=11, fontweight='bold',
            color='gray')
    
    # Result
    ax.text(5, 1.5, 'τ = d₂/d₁ = 10/10 = 1.0', ha='center', fontsize=13,
            fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.9))
    ax.text(5, 0.5, '(Same distance)', ha='center', fontsize=11, color='gray')
    
    # Receding (tau > 1)
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Receding: τ > 1\n(Depth Increases)', fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Frame 1
    ax.text(2, 8, 'Frame 1:', fontsize=12, fontweight='bold')
    bike1 = Rectangle((1.25, 4.8), 2, 1.4, fill=True, facecolor='red',
                     edgecolor='darkred', linewidth=2, alpha=0.7)
    ax.add_patch(bike1)
    ax.text(2.25, 5.5, '🚴', fontsize=30, ha='center', va='center')
    ax.text(2.25, 4.2, 'd₁ = 20m', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    # Frame 2
    ax.text(6, 8, 'Frame 2:', fontsize=12, fontweight='bold')
    bike2 = Rectangle((5.5, 5.2), 1.2, 0.9, fill=True, facecolor='blue',
                     edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax.add_patch(bike2)
    ax.text(6.1, 5.65, '🚴', fontsize=20, ha='center', va='center')
    ax.text(6.1, 4.5, 'd₂ = 25m', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Arrow showing motion away
    ax.annotate('', xy=(5.5, 5.5), xytext=(3.5, 5.5),
                arrowprops=dict(arrowstyle='->', lw=3, color='orange'))
    ax.text(4.5, 6.2, 'Moving Away!', ha='center', fontsize=11, fontweight='bold',
            color='orange')
    
    # Result
    ax.text(5, 1.5, 'τ = d₂/d₁ = 25/20 = 1.25', ha='center', fontsize=13,
            fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    ax.text(5, 0.5, '(25% farther)', ha='center', fontsize=11, color='orange')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/tau_concept.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created tau_concept.png")
    plt.close()


def create_camera_forward_mid():
    """Create diagram for camera moving forward with MID map."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: 3D scene view
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Camera Moving Forward\n(All Points Approaching)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distance', fontsize=11)
    ax1.set_ylabel('Height', fontsize=11)
    
    # Depth layers with different tau values
    # Far objects (small depth change)
    ax1.fill_between([0, 10], [7, 7], [10, 10], alpha=0.3, color='gray', label='Far (τ≈0.98)')
    ax1.text(5, 8.5, 'Sky/Mountains', ha='center', fontsize=11, fontweight='bold')
    
    # Medium distance
    ax1.fill_between([0, 10], [4, 4], [7, 7], alpha=0.4, color='green', label='Medium (τ≈0.9)')
    ax1.text(5, 5.5, 'Trees/Buildings', ha='center', fontsize=11, fontweight='bold')
    
    # Close objects (large depth change)
    ax1.fill_between([0, 10], [0, 0], [4, 4], alpha=0.5, color='brown', label='Close (τ≈0.7)')
    ax1.text(5, 2, 'Road/Ground', ha='center', fontsize=11, fontweight='bold', color='white')
    
    # Camera with forward arrow
    ax1.plot(5, 9.5, 'r*', markersize=20)
    ax1.arrow(5, 9.3, 0, -0.5, head_width=0.3, head_length=0.2,
             fc='red', ec='red', linewidth=3)
    ax1.text(5, 9.7, 'Camera', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Right: MID (tau) map
    ax2 = plt.subplot(1, 2, 2)
    
    # Create MID map
    mid_map = np.zeros((100, 100))
    
    # Far: tau close to 1 (small change)
    mid_map[0:30, :] = 0.98
    
    # Medium: tau = 0.9
    mid_map[30:60, :] = 0.90
    
    # Close: tau = 0.7
    mid_map[60:100, :] = 0.70
    
    # Add some variation
    noise = np.random.rand(100, 100) * 0.02
    mid_map += noise
    
    # Log transform
    log_mid = np.log(mid_map)
    
    # Normalize for visualization
    log_mid_norm = (log_mid - log_mid.min()) / (log_mid.max() - log_mid.min())
    
    im = ax2.imshow(log_mid_norm, cmap='RdBu_r', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Motion-in-Depth Map (τ)\nBlue = Approaching', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y', fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('log(τ) normalized', fontsize=11)
    
    # Add annotations
    ax2.text(5, 8.5, 'τ ≈ 0.98', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.text(5, 5.5, 'τ ≈ 0.90', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    ax2.text(5, 2, 'τ ≈ 0.70', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='blue', alpha=0.8), color='white')
    
    # Add depth annotations
    ax2.text(9.5, 8.5, '~100m', ha='right', fontsize=9, fontweight='bold')
    ax2.text(9.5, 5.5, '~20m', ha='right', fontsize=9, fontweight='bold')
    ax2.text(9.5, 2, '~5m', ha='right', fontsize=9, fontweight='bold', color='white')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/camera_forward_mid.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created camera_forward_mid.png")
    plt.close()


def create_camera_backward_mid():
    """Create diagram for camera moving backward with MID map."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: Scene view
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Camera Moving Backward\n(All Points Receding)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distance', fontsize=11)
    ax1.set_ylabel('Height', fontsize=11)
    
    # Depth layers
    ax1.fill_between([0, 10], [7, 7], [10, 10], alpha=0.3, color='gray')
    ax1.text(5, 8.5, 'Sky (τ≈1.02)', ha='center', fontsize=11, fontweight='bold')
    
    ax1.fill_between([0, 10], [4, 4], [7, 7], alpha=0.4, color='green')
    ax1.text(5, 5.5, 'Trees (τ≈1.1)', ha='center', fontsize=11, fontweight='bold')
    
    ax1.fill_between([0, 10], [0, 0], [4, 4], alpha=0.5, color='brown')
    ax1.text(5, 2, 'Ground (τ≈1.3)', ha='center', fontsize=11, fontweight='bold', color='white')
    
    # Camera with backward arrow
    ax1.plot(5, 9.5, 'b*', markersize=20)
    ax1.arrow(5, 9.7, 0, 0.3, head_width=0.3, head_length=0.15,
             fc='blue', ec='blue', linewidth=3)
    ax1.text(5, 10.2, '← Camera', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    
    ax1.grid(True, alpha=0.3)
    
    # Right: MID map
    ax2 = plt.subplot(1, 2, 2)
    
    # Create MID map (tau > 1, receding)
    mid_map = np.zeros((100, 100))
    mid_map[0:30, :] = 1.02  # Far
    mid_map[30:60, :] = 1.10  # Medium
    mid_map[60:100, :] = 1.30  # Close
    
    # Add variation
    noise = np.random.rand(100, 100) * 0.02
    mid_map += noise
    
    # Log transform
    log_mid = np.log(mid_map)
    log_mid_norm = (log_mid - log_mid.min()) / (log_mid.max() - log_mid.min())
    
    im = ax2.imshow(log_mid_norm, cmap='RdBu_r', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Motion-in-Depth Map (τ)\nRed = Receding', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('log(τ) normalized', fontsize=11)
    
    # Annotations
    ax2.text(5, 8.5, 'τ ≈ 1.02', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.text(5, 5.5, 'τ ≈ 1.10', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    ax2.text(5, 2, 'τ ≈ 1.30', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.8), color='white')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/camera_backward_mid.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created camera_backward_mid.png")
    plt.close()


def create_object_approaching_mid():
    """Create diagram for approaching object with static background."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: Scene with moving car
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Approaching Car\n(Static Camera)', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Static background
    ax1.fill_between([0, 10], [0, 0], [10, 10], alpha=0.15, color='green')
    ax1.text(5, 9, 'Static Background (τ = 1.0)', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Moving car
    car_rect = Rectangle((4, 4.5), 2, 1.5, fill=True, facecolor='red',
                         edgecolor='darkred', linewidth=3, alpha=0.7)
    ax1.add_patch(car_rect)
    ax1.text(5, 5.25, '🚗', fontsize=40, ha='center', va='center')
    
    # Motion arrow
    ax1.arrow(5, 7.5, 0, -1.5, head_width=0.4, head_length=0.3,
             fc='blue', ec='blue', linewidth=3)
    ax1.text(5.8, 7, 'Approaching\nτ = 0.75', ha='left', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    # Trees in background
    for x in [1, 3, 7, 9]:
        ax1.text(x, 8.5, '🌲', fontsize=20, ha='center')
        ax1.text(x, 7.8, 'τ=1.0', fontsize=8, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
    
    # Right: MID map
    ax2 = plt.subplot(1, 2, 2)
    
    # Create MID map
    mid_map = np.ones((100, 100))  # Background tau = 1
    
    # Add approaching car (tau < 1)
    y, x = np.ogrid[:100, :100]
    car_mask = ((x - 50)**2 / 400 + (y - 50)**2 / 225) < 1
    mid_map[car_mask] = 0.75
    
    # Smooth the boundary
    mid_map = cv2.GaussianBlur(mid_map, (11, 11), 2)
    
    # Log transform
    log_mid = np.log(mid_map + 1e-8)
    log_mid_norm = (log_mid - log_mid.min()) / (log_mid.max() - log_mid.min() + 1e-8)
    
    im = ax2.imshow(log_mid_norm, cmap='RdBu_r', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Motion-in-Depth Map (τ)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('log(τ) normalized', fontsize=11)
    
    # Annotations
    ax2.text(5, 5, 'Car\nτ = 0.75', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='blue', alpha=0.7), color='white')
    ax2.text(2, 8, 'Background\nτ = 1.0', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Highlight car boundary
    car_outline = plt.Circle((5, 5), 1.5, fill=False, edgecolor='yellow',
                             linewidth=3, linestyle='--')
    ax2.add_patch(car_outline)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/object_approaching_mid.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created object_approaching_mid.png")
    plt.close()


def create_uav_descending_mid():
    """Create diagram for UAV descending over terrain."""
    fig = plt.figure(figsize=(14, 7))
    
    # Left: Side view of UAV and terrain
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('UAV Descending\n(Terrain at Different Heights)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distance', fontsize=11)
    ax1.set_ylabel('Altitude', fontsize=11)
    
    # Sky
    ax1.fill_between([0, 10], [8, 8], [10, 10], alpha=0.2, color='skyblue')
    ax1.text(5, 9, 'Sky (τ ≈ 1.0)', ha='center', fontsize=11, fontweight='bold')
    
    # Distant terrain
    ax1.fill_between([0, 10], [5, 5], [8, 8], alpha=0.3, color='gray')
    ax1.text(5, 6.5, 'Distant Terrain (τ ≈ 0.95)', ha='center', fontsize=10, fontweight='bold')
    
    # Trees
    ax1.fill_between([0, 10], [2.5, 2.5], [5, 5], alpha=0.4, color='green')
    ax1.text(5, 3.75, 'Trees (τ ≈ 0.85)', ha='center', fontsize=10, fontweight='bold')
    
    # Ground
    ax1.fill_between([0, 10], [0, 0], [2.5, 2.5], alpha=0.5, color='brown')
    ax1.text(5, 1.25, 'Ground (τ ≈ 0.70)', ha='center', fontsize=10, 
            fontweight='bold', color='white')
    
    # UAV
    ax1.plot(2, 9.5, 'r*', markersize=25)
    ax1.arrow(2, 9.3, 0, -0.7, head_width=0.3, head_length=0.2,
             fc='red', ec='red', linewidth=3)
    ax1.text(2, 10, '🚁', fontsize=20, ha='center')
    ax1.text(3.5, 9.5, 'Descending', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    ax1.grid(True, alpha=0.3)
    
    # Right: MID map from UAV camera
    ax2 = plt.subplot(1, 2, 2)
    
    # Create MID map with depth gradient
    mid_map = np.zeros((100, 100))
    
    # Sky (top) - far, minimal change
    mid_map[0:20, :] = 1.00
    
    # Distant terrain
    mid_map[20:40, :] = 0.95
    
    # Trees
    mid_map[40:65, :] = 0.85
    
    # Ground (bottom) - close, large change
    mid_map[65:100, :] = 0.70
    
    # Add horizontal variation (terrain features)
    for i in range(100):
        variation = 0.02 * np.sin(i / 10)
        mid_map[:, i] += variation
    
    # Log transform
    log_mid = np.log(mid_map + 1e-8)
    log_mid_norm = (log_mid - log_mid.min()) / (log_mid.max() - log_mid.min() + 1e-8)
    
    im = ax2.imshow(log_mid_norm, cmap='RdBu_r', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Motion-in-Depth Map (τ)\nFrom UAV Camera', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y (Height in frame)', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('log(τ) normalized', fontsize=11)
    
    # Annotations
    ax2.text(5, 9, 'Sky: τ≈1.0', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.text(5, 7, 'Terrain: τ≈0.95', ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    ax2.text(5, 5, 'Trees: τ≈0.85', ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='blue', alpha=0.7), color='white')
    ax2.text(5, 2, 'Ground: τ≈0.70', ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.8), color='white')
    
    # Add distance markers
    ax2.text(9.7, 9, '∞', ha='right', fontsize=12, fontweight='bold')
    ax2.text(9.7, 7, '~200m', ha='right', fontsize=9, fontweight='bold')
    ax2.text(9.7, 5, '~50m', ha='right', fontsize=9, fontweight='bold', color='white')
    ax2.text(9.7, 2, '~10m', ha='right', fontsize=9, fontweight='bold', color='white')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/uav_descending_mid.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created uav_descending_mid.png")
    plt.close()


def create_depth_layers():
    """Create diagram showing depth layer segmentation."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Scene with distinct depth layers
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Scene with 4 Depth Layers', fontsize=14, fontweight='bold')
    ax.set_xlabel('Scene Width', fontsize=11)
    ax.set_ylabel('Vertical Position', fontsize=11)
    
    # Layer 4: Sky (farthest)
    ax.fill_between([0, 10], [8, 8], [10, 10], alpha=0.3, color='skyblue', label='Layer 4: Sky')
    ax.text(5, 9, '∞ distance\nτ = 1.00', ha='center', fontsize=10, fontweight='bold')
    
    # Layer 3: Mountains
    ax.fill_between([0, 10], [6, 6], [8, 8], alpha=0.4, color='gray', label='Layer 3: Mountains')
    ax.text(5, 7, '~500m\nτ = 0.98', ha='center', fontsize=10, fontweight='bold')
    
    # Layer 2: Trees
    ax.fill_between([0, 10], [3.5, 3.5], [6, 6], alpha=0.5, color='green', label='Layer 2: Trees')
    ax.text(5, 4.75, '~50m\nτ = 0.90', ha='center', fontsize=10, fontweight='bold')
    
    # Layer 1: Road (closest)
    ax.fill_between([0, 10], [0, 0], [3.5, 3.5], alpha=0.6, color='darkgray', label='Layer 1: Road')
    ax.text(5, 1.75, '~10m\nτ = 0.70', ha='center', fontsize=10, 
            fontweight='bold', color='white')
    
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Right: MID-based segmentation
    ax = axes[1]
    
    # Create synthetic MID map with clear layers
    mid_map = np.zeros((100, 100))
    mid_map[0:25, :] = 0.70  # Layer 1
    mid_map[25:60, :] = 0.90  # Layer 2
    mid_map[60:80, :] = 0.98  # Layer 3
    mid_map[80:100, :] = 1.00  # Layer 4
    
    # Add boundaries with some roughness
    for i in range(100):
        noise = int(3 * np.sin(i / 5))
        # Shift boundaries slightly
        if 23 + noise < i < 27 + noise:
            mid_map[i, :] = 0.80  # Transition
        if 58 + noise < i < 62 + noise:
            mid_map[i, :] = 0.94  # Transition
        if 78 + noise < i < 82 + noise:
            mid_map[i, :] = 0.99  # Transition
    
    # Create discrete colormap for layers
    from matplotlib.colors import ListedColormap
    colors = ['darkblue', 'blue', 'lightblue', 'white']
    n_bins = 4
    cmap = ListedColormap(colors)
    
    im = ax.imshow(mid_map, cmap=cmap, origin='lower', extent=[0, 10, 0, 10],
                   vmin=0.65, vmax=1.05)
    ax.set_title('Depth Segmentation from τ', fontsize=14, fontweight='bold')
    ax.set_xlabel('Image X', fontsize=11)
    ax.set_ylabel('Image Y', fontsize=11)
    
    # Add layer labels
    ax.text(5, 1.25, 'Layer 1\nτ=0.70', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    ax.text(5, 4.25, 'Layer 2\nτ=0.90', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    ax.text(5, 7, 'Layer 3\nτ=0.98', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), color='white')
    ax.text(5, 9, 'Layer 4\nτ=1.00', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), color='white')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/depth_layers.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created depth_layers.png")
    plt.close()


def create_interpretation_guide():
    """Create color interpretation guide for MID maps."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create tau values from 0.5 to 1.5
    tau_values = np.linspace(0.5, 1.5, 256)
    log_tau = np.log(tau_values)
    
    # Normalize
    log_tau_norm = (log_tau - log_tau.min()) / (log_tau.max() - log_tau.min())
    
    # Create gradient
    gradient = log_tau_norm.reshape(1, -1)
    gradient = np.repeat(gradient, 50, axis=0)
    
    ax.imshow(gradient, aspect='auto', cmap='RdBu_r', extent=[0.5, 1.5, 0, 1])
    ax.set_yticks([])
    ax.set_xlabel('Motion-in-Depth Parameter (τ = d₂/d₁)', fontsize=13, fontweight='bold')
    ax.set_title('Motion-in-Depth (τ) Color Interpretation Guide', fontsize=16, fontweight='bold', pad=20)
    
    # Add major tick marks
    ax.set_xticks([0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5])
    ax.set_xticklabels(['0.5\nFast\nApproaching', '0.7', '0.8', '0.9', 
                       '1.0\nNo Depth\nChange', '1.1', '1.2', '1.3', 
                       '1.5\nFast\nReceding'], fontsize=10)
    
    # Add interpretation boxes
    interpretations = [
        (0.6, 'Dark Blue\nRapid Approach\n(50% closer)', 'darkblue', 0.15),
        (0.8, 'Light Blue\nSlow Approach\n(20% closer)', 'lightblue', 0.15),
        (1.0, 'White/Gray\nParallel Motion\n(Same distance)', 'gray', 0.15),
        (1.2, 'Light Red\nSlow Recession\n(20% farther)', 'lightcoral', 0.15),
        (1.4, 'Dark Red\nRapid Recession\n(40% farther)', 'darkred', 0.15)
    ]
    
    for tau, text, color, y_pos in interpretations:
        ax.text(tau, y_pos, text, ha='center', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=color, alpha=0.8, edgecolor='black', linewidth=2),
               color='white' if color in ['darkblue', 'darkred'] else 'black')
    
    # Add application examples
    ax.text(1.0, 0.85, 'Application Examples:', ha='center', fontsize=12, fontweight='bold')
    ax.text(1.0, 0.75, 
           '• UAV Navigation: Blue values = descending/approaching terrain\n'
           '• Collision Detection: Dark blue = immediate danger\n'
           '• 3D Reconstruction: τ variations reveal depth structure\n'
           '• Object Tracking: Different τ = independent motion',
           ha='center', va='top', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Add critical thresholds
    ax.axvline(x=0.7, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(0.7, 0.95, 'Collision\nWarning', ha='center', fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='red', alpha=0.8), color='white')
    
    ax.axvline(x=1.0, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(1.0, 0.95, 'Neutral\nDepth', ha='center', fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='green', alpha=0.8), color='white')
    
    ax.set_xlim(0.5, 1.5)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/interpretation_guide.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created interpretation_guide.png")
    plt.close()


def main():
    """Generate all motion-in-depth diagrams."""
    print("Generating Motion-in-Depth Documentation Diagrams...")
    print("=" * 60)
    
    create_tau_concept()
    create_camera_forward_mid()
    create_camera_backward_mid()
    create_object_approaching_mid()
    create_uav_descending_mid()
    create_depth_layers()
    create_interpretation_guide()
    
    print("=" * 60)
    print(f"✓ All diagrams saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()

