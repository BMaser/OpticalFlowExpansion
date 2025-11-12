"""
Generate visual diagrams for Expansion documentation.

This script creates various diagrams to illustrate optical expansion concepts:
1. Divergence concept diagram
2. Camera forward motion
3. Camera backward motion
4. Object approaching
5. UAV flight scenario
6. Expansion patterns

Author: Bob Maser
Date: November 12, 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
import cv2
import os

# Set output directory
OUTPUT_DIR = '/home/bobmaser/github/OpticalFlowExpansion/docs/expansion'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_divergence_concept():
    """Create diagram showing positive and negative divergence."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Positive divergence (expansion)
    ax = axes[0]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_title('Positive Divergence\n(Expansion)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Center point
    ax.plot(0, 0, 'ro', markersize=15, label='Source Point')
    
    # Arrows pointing outward
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for angle in angles:
        dx = 0.8 * np.cos(angle)
        dy = 0.8 * np.sin(angle)
        ax.arrow(0, 0, dx, dy, head_width=0.15, head_length=0.15, 
                fc='blue', ec='blue', linewidth=2, alpha=0.7)
    
    ax.text(0, -1.7, 'Flow spreading OUT', ha='center', fontsize=13, 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    ax.text(0, 1.7, 'div > 0', ha='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # Negative divergence (convergence)
    ax = axes[1]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_title('Negative Divergence\n(Convergence)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Center point
    ax.plot(0, 0, 'ro', markersize=15, label='Sink Point')
    
    # Arrows pointing inward
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for angle in angles:
        dx = -0.8 * np.cos(angle)
        dy = -0.8 * np.sin(angle)
        # Start from outside
        start_x = -dx
        start_y = -dy
        ax.arrow(start_x, start_y, dx, dy, head_width=0.15, head_length=0.15,
                fc='red', ec='red', linewidth=2, alpha=0.7)
    
    ax.text(0, -1.7, 'Flow converging IN', ha='center', fontsize=13,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    ax.text(0, 1.7, 'div < 0', ha='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/divergence_concept.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created divergence_concept.png")
    plt.close()


def create_camera_forward_expansion():
    """Create diagram for camera moving forward."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: Scene view with flow
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Camera Moving Forward\n(Flow Field)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Image X', fontsize=11)
    ax1.set_ylabel('Image Y', fontsize=11)
    
    # Camera at center (focus of expansion)
    center_x, center_y = 5, 5
    ax1.plot(center_x, center_y, 'r*', markersize=20, label='FOE (Focus of Expansion)')
    
    # Create radial flow field
    y_coords, x_coords = np.meshgrid(np.linspace(0.5, 9.5, 10), np.linspace(0.5, 9.5, 10))
    
    # Compute radial flow
    dx = x_coords - center_x
    dy = y_coords - center_y
    dist = np.sqrt(dx**2 + dy**2) + 0.1
    
    # Normalize and scale
    u = dx / dist * 0.5
    v = dy / dist * 0.5
    
    # Plot flow field
    ax1.quiver(x_coords, y_coords, u, v, scale=3, width=0.003, color='blue', alpha=0.7)
    
    # Add camera icon
    camera_rect = Rectangle((4.5, 4.5), 1, 1, fill=True, facecolor='red', 
                            edgecolor='darkred', linewidth=2, alpha=0.7)
    ax1.add_patch(camera_rect)
    ax1.text(5, 5, '📷', fontsize=20, ha='center', va='center')
    
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Right: Expansion map
    ax2 = plt.subplot(1, 2, 2)
    
    # Compute expansion (divergence)
    # For radial expansion: div = ∂u/∂x + ∂v/∂y = 2/r (approximately)
    expansion = 2.0 / dist
    
    # Log transform
    log_expansion = np.log(expansion + 1e-8)
    
    im = ax2.imshow(log_expansion, cmap='jet', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Expansion Map\n(Divergence)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y', fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('log(Expansion)', fontsize=11)
    
    # Mark FOE
    ax2.plot(center_x, center_y, 'w*', markersize=15, markeredgecolor='black', 
            markeredgewidth=1.5)
    
    # Add annotations
    ax2.text(5, 1, 'Positive Everywhere', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.text(5, 9, 'Stronger Near Center', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/camera_forward_expansion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created camera_forward_expansion.png")
    plt.close()


def create_camera_backward_expansion():
    """Create diagram for camera moving backward."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: Scene view with flow
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Camera Moving Backward\n(Flow Field)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Image X', fontsize=11)
    ax1.set_ylabel('Image Y', fontsize=11)
    
    # Camera at center (focus of contraction)
    center_x, center_y = 5, 5
    ax1.plot(center_x, center_y, 'b*', markersize=20, label='FOC (Focus of Contraction)')
    
    # Create radial flow field (inward)
    y_coords, x_coords = np.meshgrid(np.linspace(0.5, 9.5, 10), np.linspace(0.5, 9.5, 10))
    
    # Compute radial flow (opposite direction)
    dx = -(x_coords - center_x)
    dy = -(y_coords - center_y)
    dist = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2) + 0.1
    
    # Normalize and scale
    u = dx / dist * 0.5
    v = dy / dist * 0.5
    
    # Plot flow field
    ax1.quiver(x_coords, y_coords, u, v, scale=3, width=0.003, color='red', alpha=0.7)
    
    # Add camera icon
    camera_rect = Rectangle((4.5, 4.5), 1, 1, fill=True, facecolor='blue',
                            edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax1.add_patch(camera_rect)
    ax1.text(5, 5, '📷', fontsize=20, ha='center', va='center')
    
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Right: Expansion map
    ax2 = plt.subplot(1, 2, 2)
    
    # Compute expansion (negative divergence)
    expansion = -2.0 / dist
    
    # Log transform (preserve sign)
    log_expansion = -np.log(np.abs(expansion) + 1e-8)
    
    im = ax2.imshow(log_expansion, cmap='jet', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Expansion Map\n(Divergence)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y', fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('log(Expansion)', fontsize=11)
    
    # Mark FOC
    ax2.plot(center_x, center_y, 'w*', markersize=15, markeredgecolor='black',
            markeredgewidth=1.5)
    
    # Add annotations
    ax2.text(5, 1, 'Negative Everywhere', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.text(5, 9, 'Scene Receding', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/camera_backward_expansion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created camera_backward_expansion.png")
    plt.close()


def create_object_approaching():
    """Create diagram for single object approaching."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: Scene with moving object
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Object Approaching Camera\n(Flow Field)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Image X', fontsize=11)
    ax1.set_ylabel('Image Y', fontsize=11)
    
    # Static background (no flow)
    ax1.fill_between([0, 10], [0, 0], [10, 10], alpha=0.2, color='green', label='Static Background')
    
    # Moving object region
    obj_x, obj_y = 5, 5
    obj_size = 2
    object_rect = Rectangle((obj_x - obj_size/2, obj_y - obj_size/2), 
                           obj_size, obj_size, fill=True, facecolor='red',
                           edgecolor='darkred', linewidth=3, alpha=0.6, label='Moving Object')
    ax1.add_patch(object_rect)
    
    # Add car emoji
    ax1.text(obj_x, obj_y, '🚗', fontsize=40, ha='center', va='center')
    
    # Flow field only on object (radial expansion)
    y_coords, x_coords = np.meshgrid(np.linspace(4, 6, 5), np.linspace(4, 6, 5))
    dx = (x_coords - obj_x) * 0.3
    dy = (y_coords - obj_y) * 0.3
    ax1.quiver(x_coords, y_coords, dx, dy, scale=2, width=0.005, color='blue', alpha=0.8)
    
    # Arrow showing motion
    ax1.arrow(obj_x, obj_y + 3, 0, 1.5, head_width=0.3, head_length=0.3,
             fc='orange', ec='orange', linewidth=3)
    ax1.text(obj_x + 0.5, obj_y + 3.5, 'Approaching', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Right: Expansion map
    ax2 = plt.subplot(1, 2, 2)
    
    # Create expansion map (zero everywhere except on object)
    expansion = np.zeros((100, 100))
    
    # High expansion on object region
    center = 50
    obj_radius = 20
    y_grid, x_grid = np.ogrid[:100, :100]
    dist_from_center = np.sqrt((x_grid - center)**2 + (y_grid - center)**2)
    
    # Gaussian-like expansion on object
    expansion[dist_from_center < obj_radius] = 0.8 * np.exp(-dist_from_center[dist_from_center < obj_radius]**2 / (obj_radius**2 / 2))
    
    im = ax2.imshow(expansion, cmap='jet', origin='lower', extent=[0, 10, 0, 10], vmin=0, vmax=1)
    ax2.set_title('Expansion Map\n(Divergence)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y', fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('Expansion', fontsize=11)
    
    # Highlight object region
    highlight_rect = Rectangle((4, 4), 2, 2, fill=False, edgecolor='white',
                              linewidth=3, linestyle='--')
    ax2.add_patch(highlight_rect)
    
    # Add annotations
    ax2.text(5, 2, 'Zero on Background', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='blue', alpha=0.6, edgecolor='white'))
    ax2.text(5, 8, 'High on Moving Object', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.6, edgecolor='white'))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/object_approaching.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created object_approaching.png")
    plt.close()


def create_uav_flight_expansion():
    """Create diagram for UAV flight over terrain."""
    fig = plt.figure(figsize=(14, 7))
    
    # Left: 3D-like scene view
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('UAV Flying Forward\n(Terrain at Different Depths)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Image X', fontsize=11)
    ax1.set_ylabel('Image Y (Height)', fontsize=11)
    
    # Distant mountains (top)
    ax1.fill_between([0, 10], [7, 7], [10, 10], alpha=0.4, color='gray', label='Distant Mountains')
    ax1.text(5, 8.5, '🗻 Far (~1000m)', ha='center', fontsize=11, fontweight='bold')
    
    # Mid-range trees (middle)
    ax1.fill_between([0, 10], [3.5, 3.5], [7, 7], alpha=0.5, color='green', label='Trees')
    ax1.text(5, 5.2, '🌲 Medium (~50m)', ha='center', fontsize=11, fontweight='bold')
    
    # Close ground (bottom)
    ax1.fill_between([0, 10], [0, 0], [3.5, 3.5], alpha=0.6, color='brown', label='Ground')
    ax1.text(5, 1.7, 'Ground (~10m)', ha='center', fontsize=11, fontweight='bold',
            color='white')
    
    # UAV icon
    ax1.text(5, 9.5, '🚁 UAV', ha='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    ax1.arrow(5, 9.2, 0, -0.5, head_width=0.3, head_length=0.2,
             fc='red', ec='red', linewidth=2)
    ax1.text(6, 9, 'Forward', fontsize=10, fontweight='bold')
    
    ax1.legend(loc='center left')
    ax1.grid(True, alpha=0.3)
    
    # Right: Expansion map
    ax2 = plt.subplot(1, 2, 2)
    
    # Create expansion map with depth layers
    expansion = np.zeros((100, 100))
    
    # Ground (high expansion - close)
    expansion[65:100, :] = 0.9
    
    # Trees (medium expansion)
    expansion[30:65, :] = 0.6
    
    # Mountains (low expansion - far)
    expansion[0:30, :] = 0.3
    
    # Add some texture/variation
    noise = np.random.rand(100, 100) * 0.05
    expansion += noise
    expansion = np.clip(expansion, 0, 1)
    
    im = ax2.imshow(expansion, cmap='hot', origin='lower', extent=[0, 10, 0, 10])
    ax2.set_title('Expansion Map\n(Closer = Higher Expansion)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Image X', fontsize=11)
    ax2.set_ylabel('Image Y (Height)', fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('Expansion Magnitude', fontsize=11)
    
    # Add annotations
    ax2.text(5, 8.5, 'Low (Far)', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.7, edgecolor='white'),
            color='white')
    ax2.text(5, 5.2, 'Medium', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='orange', alpha=0.7, edgecolor='white'))
    ax2.text(5, 1.7, 'High (Close)', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.7, edgecolor='white'),
            color='white')
    
    # Add depth labels
    ax2.text(9.5, 8.5, '~1000m', ha='right', fontsize=9, color='white', fontweight='bold')
    ax2.text(9.5, 5.2, '~50m', ha='right', fontsize=9, color='black', fontweight='bold')
    ax2.text(9.5, 1.7, '~10m', ha='right', fontsize=9, color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/uav_flight_expansion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created uav_flight_expansion.png")
    plt.close()


def create_expansion_patterns():
    """Create reference chart of common expansion patterns."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    patterns = [
        ('Forward Motion', 'forward'),
        ('Backward Motion', 'backward'),
        ('Rotation (Right)', 'rotation'),
        ('Descending', 'descending'),
        ('Ascending', 'ascending'),
        ('Moving Object', 'object')
    ]
    
    for idx, (title, pattern_type) in enumerate(patterns):
        ax = axes[idx // 3, idx % 3]
        
        # Create pattern
        expansion = np.zeros((50, 50))
        
        if pattern_type == 'forward':
            # Radial expansion from center
            y, x = np.ogrid[:50, :50]
            dist = np.sqrt((x - 25)**2 + (y - 25)**2) + 1
            expansion = 1.0 / dist
            
        elif pattern_type == 'backward':
            # Negative radial expansion
            y, x = np.ogrid[:50, :50]
            dist = np.sqrt((x - 25)**2 + (y - 25)**2) + 1
            expansion = -1.0 / dist
            
        elif pattern_type == 'rotation':
            # Left positive, right negative
            expansion[:, :25] = 0.7
            expansion[:, 25:] = -0.7
            
        elif pattern_type == 'descending':
            # Top negative, bottom positive
            expansion[:25, :] = -0.6
            expansion[25:, :] = 0.8
            
        elif pattern_type == 'ascending':
            # Top positive, bottom negative
            expansion[:25, :] = 0.8
            expansion[25:, :] = -0.6
            
        elif pattern_type == 'object':
            # Localized expansion
            y, x = np.ogrid[:50, :50]
            dist = np.sqrt((x - 25)**2 + (y - 15)**2)
            expansion[dist < 10] = 0.9
        
        # Plot
        im = ax.imshow(expansion, cmap='RdBu_r', origin='lower', vmin=-1, vmax=1)
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Expansion', fontsize=9)
    
    plt.suptitle('Common Expansion Patterns', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/expansion_patterns.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created expansion_patterns.png")
    plt.close()


def create_interpretation_guide():
    """Create color interpretation guide."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create color gradient
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.repeat(gradient, 50, axis=0)
    
    ax.imshow(gradient, aspect='auto', cmap='jet')
    ax.set_yticks([])
    ax.set_xticks([0, 64, 128, 192, 255])
    ax.set_xticklabels(['0.0\nStrong\nReceding', '0.25\nModerate\nReceding', 
                       '0.5\nZero\n(Parallel)', '0.75\nModerate\nApproaching',
                       '1.0\nStrong\nApproaching'], fontsize=11)
    ax.set_title('Expansion Map Color Interpretation Guide', fontsize=16, fontweight='bold', pad=20)
    
    # Add color region labels with boxes
    regions = [
        (32, 'Dark Blue', 'Fast Receding', 'darkblue'),
        (96, 'Light Blue', 'Slow Receding', 'cyan'),
        (128, 'Gray/Green', 'No Depth Change', 'gray'),
        (160, 'Yellow', 'Slow Approaching', 'yellow'),
        (224, 'Red/White', 'Fast Approaching', 'red')
    ]
    
    for x_pos, color_name, meaning, box_color in regions:
        ax.text(x_pos, 60, color_name, ha='center', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=box_color, linewidth=2))
        ax.text(x_pos, 75, meaning, ha='center', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Add example scenarios at bottom
    ax.text(128, -20, 'Example Applications:', ha='center', fontsize=12, fontweight='bold')
    ax.text(128, -30, '• UAV Obstacle Avoidance: High red values = collision warning\n'
                     '• Depth Estimation: Expansion ∝ velocity/depth\n'
                     '• Motion Segmentation: Anomalies indicate moving objects',
           ha='center', fontsize=10, va='top',
           bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    ax.set_xlim(0, 255)
    ax.set_ylim(-35, 80)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/interpretation_guide.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created interpretation_guide.png")
    plt.close()


def main():
    """Generate all expansion diagrams."""
    print("Generating Expansion Documentation Diagrams...")
    print("=" * 60)
    
    create_divergence_concept()
    create_camera_forward_expansion()
    create_camera_backward_expansion()
    create_object_approaching()
    create_uav_flight_expansion()
    create_expansion_patterns()
    create_interpretation_guide()
    
    print("=" * 60)
    print(f"✓ All diagrams saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()

