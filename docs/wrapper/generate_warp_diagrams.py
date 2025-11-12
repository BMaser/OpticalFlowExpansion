#!/usr/bin/env python3
"""
Generate Visual Diagrams for Image Warping Documentation

This script creates visual examples showing how optical flow warping works.

Author: Bob Maser
Date: November 2024
Project: OpticalFlowExpansion
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
import os

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_grid_visualization():
    """
    Create a visualization showing coordinate grid transformation
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Image Warping: Grid Transformation Process', fontsize=16, fontweight='bold')
    
    # Original grid
    ax = axes[0, 0]
    ax.set_title('Step 1: Original Pixel Grid', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    # Draw grid
    for i in range(5):
        for j in range(5):
            circle = Circle((i, j), 0.15, color='blue', fill=True)
            ax.add_patch(circle)
            if i < 4 and j < 4:
                ax.text(i, j-0.4, f'({i},{j})', ha='center', fontsize=8)
    
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (width)', fontsize=10)
    ax.set_ylabel('Y (height)', fontsize=10)
    ax.text(2, -1.2, 'Each dot = one pixel', ha='center', fontsize=9, style='italic')
    
    # Flow vectors
    ax = axes[0, 1]
    ax.set_title('Step 2: Optical Flow Vectors (U, V)', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    # Create example flow field (moving right and up)
    u = 1.5  # Move right
    v = -0.8  # Move up
    
    for i in range(5):
        for j in range(5):
            circle = Circle((i, j), 0.15, color='blue', fill=True)
            ax.add_patch(circle)
            # Draw arrow
            if i < 4 and j < 4:
                arrow = FancyArrowPatch((i, j), (i+u, j+v),
                                       arrowstyle='->', mutation_scale=15,
                                       color='red', linewidth=2)
                ax.add_patch(arrow)
    
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (width)', fontsize=10)
    ax.set_ylabel('Y (height)', fontsize=10)
    ax.text(2, -1.2, f'Flow: U=+{u:.1f} (right), V={v:.1f} (up)', 
            ha='center', fontsize=9, style='italic', color='red')
    
    # Warped grid
    ax = axes[1, 0]
    ax.set_title('Step 3: Warped Sampling Positions', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 6)
    ax.set_ylim(-2, 4.5)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    # Draw original grid (light)
    for i in range(5):
        for j in range(5):
            circle = Circle((i, j), 0.12, color='lightgray', fill=True, alpha=0.5)
            ax.add_patch(circle)
    
    # Draw warped grid
    for i in range(5):
        for j in range(5):
            new_x = i + u
            new_y = j + v
            circle = Circle((new_x, new_y), 0.15, color='green', fill=True)
            ax.add_patch(circle)
            if i < 4 and j < 4:
                ax.text(new_x, new_y-0.4, f'({new_x:.1f},{new_y:.1f})', 
                       ha='center', fontsize=7, color='green')
    
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (width)', fontsize=10)
    ax.set_ylabel('Y (height)', fontsize=10)
    ax.text(2.5, -1.5, 'Gray = original, Green = new positions', 
            ha='center', fontsize=9, style='italic')
    
    # Bilinear interpolation example
    ax = axes[1, 1]
    ax.set_title('Step 4: Bilinear Interpolation', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    # Sample at position (1.3, 1.7)
    sample_x, sample_y = 1.3, 1.7
    
    # Draw 2x2 neighborhood
    for i in [1, 2]:
        for j in [1, 2]:
            rect = patches.Rectangle((i-0.5, j-0.5), 1, 1, 
                                     linewidth=2, edgecolor='blue', 
                                     facecolor='lightblue', alpha=0.3)
            ax.add_patch(rect)
            circle = Circle((i, j), 0.15, color='blue', fill=True)
            ax.add_patch(circle)
            ax.text(i, j-0.35, f'P({i},{j})', ha='center', fontsize=9)
    
    # Draw sample point
    sample_circle = Circle((sample_x, sample_y), 0.15, color='red', fill=True, zorder=10)
    ax.add_patch(sample_circle)
    ax.text(sample_x, sample_y+0.35, f'Sample\n({sample_x},{sample_y})', 
           ha='center', fontsize=9, color='red', fontweight='bold')
    
    # Show weights
    dx = sample_x - 1
    dy = sample_y - 1
    weights = [
        (1-dx)*(1-dy), dx*(1-dy),
        (1-dx)*dy, dx*dy
    ]
    positions = [(1,1), (2,1), (1,2), (2,2)]
    
    for (x, y), w in zip(positions, weights):
        ax.text(x, y+0.7, f'w={w:.2f}', ha='center', fontsize=8, 
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (width)', fontsize=10)
    ax.set_ylabel('Y (height)', fontsize=10)
    ax.text(1.5, 3.2, f'Result = Σ weight × pixel_value', 
            ha='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'grid_transformation.png'), dpi=150, bbox_inches='tight')
    print(f"✓ Created: grid_transformation.png")
    plt.close()


def create_warp_example():
    """
    Create a simple visual example of image warping
    """
    # Create two simple images
    height, width = 200, 300
    
    # Frame 1: Circle on left
    frame1 = np.ones((height, width, 3), dtype=np.uint8) * 240
    cv2.circle(frame1, (80, 100), 30, (255, 0, 0), -1)  # Blue circle
    cv2.putText(frame1, 'Frame 1 (t=0)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (0, 0, 0), 2)
    
    # Frame 2: Circle on right (moved right by 80 pixels)
    frame2 = np.ones((height, width, 3), dtype=np.uint8) * 240
    cv2.circle(frame2, (160, 100), 30, (255, 0, 0), -1)  # Blue circle moved right
    cv2.putText(frame2, 'Frame 2 (t=1)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (0, 0, 0), 2)
    
    # Create optical flow: circle moved right from 80 to 160
    # To warp frame2 back to frame1, we need REVERSE flow
    # For each pixel in warped image, where should we sample from frame2?
    # Pixel at x=80 in warped should come from x=160 in frame2
    # So flow at destination 80 should point to source 160
    
    # Create sampling map (where to read FROM in frame2 for each pixel)
    # IMPORTANT: Don't use identity mapping! We want to show ONLY the warped circle
    # So sample from way outside the image for most pixels (will be gray background)
    map_x = np.full((height, width), -1000, dtype=np.float32)  # Out of bounds
    map_y = np.full((height, width), -1000, dtype=np.float32)  # Out of bounds
    
    # Only for the target circle region at x=80, sample from source at x=160
    y_coords, x_coords = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    mask_center_frame1 = (x_coords - 80)**2 + (y_coords - 100)**2 <= 35**2
    map_x[mask_center_frame1] = x_coords[mask_center_frame1] + 80  # Sample 80 pixels to the right
    map_y[mask_center_frame1] = y_coords[mask_center_frame1]  # Same y coordinate
    
    # For visualization: create flow field showing the motion
    flow = np.zeros((height, width, 2), dtype=np.float32)
    y, x = np.ogrid[:height, :width]
    mask_center_frame2 = (x - 160)**2 + (y - 100)**2 <= 35**2
    flow[mask_center_frame2, 0] = -80  # Motion is leftward
    
    warped = cv2.remap(frame2, map_x, map_y, cv2.INTER_LINEAR, 
                      borderMode=cv2.BORDER_CONSTANT, borderValue=(240, 240, 240))
    cv2.putText(warped, 'Warped Frame 2', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (0, 0, 0), 2)
    
    # Create flow visualization
    flow_vis = np.ones((height, width, 3), dtype=np.uint8) * 240
    # Draw arrows
    step = 20
    for y in range(0, height, step):
        for x in range(0, width, step):
            if mask_center_frame2[y, x]:
                cv2.arrowedLine(flow_vis, (x, y), (x + int(flow[y,x,0]/4), y), 
                              (0, 0, 255), 2, tipLength=0.3)
    cv2.circle(flow_vis, (160, 100), 30, (100, 100, 100), 2)
    cv2.putText(flow_vis, 'Optical Flow', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (0, 0, 0), 2)
    cv2.putText(flow_vis, '(arrows show motion)', (10, 55), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
    
    # Combine all images
    top_row = np.hstack([frame1, frame2])
    bottom_row = np.hstack([flow_vis, warped])
    combined = np.vstack([top_row, bottom_row])
    
    # Add separator lines
    cv2.line(combined, (0, height), (width*2, height), (150, 150, 150), 2)
    cv2.line(combined, (width, 0), (width, height*2), (150, 150, 150), 2)
    
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'warp_example_simple.png'), combined)
    print(f"✓ Created: warp_example_simple.png")


def create_quality_comparison():
    """
    Create visualization showing good vs bad warp quality
    """
    height, width = 150, 200
    
    # Good case: Accurate flow
    frame1_good = np.ones((height, width, 3), dtype=np.uint8) * 230
    cv2.rectangle(frame1_good, (60, 50), (140, 100), (0, 128, 255), -1)
    cv2.putText(frame1_good, 'Frame 1', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 
               0.6, (0, 0, 0), 2)
    
    warped_good = frame1_good.copy()
    cv2.putText(warped_good, 'Warped', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 
               0.6, (0, 0, 0), 2)
    
    # Bad case: Inaccurate flow
    frame1_bad = frame1_good.copy()
    
    warped_bad = np.ones((height, width, 3), dtype=np.uint8) * 230
    # Distorted rectangle
    cv2.rectangle(warped_bad, (50, 45), (150, 95), (0, 128, 255), -1)
    cv2.rectangle(warped_bad, (55, 50), (145, 90), (230, 230, 230), 5)
    cv2.putText(warped_bad, 'Warped', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 
               0.6, (0, 0, 0), 2)
    
    # Create comparison
    good_row = np.hstack([frame1_good, warped_good])
    bad_row = np.hstack([frame1_bad, warped_bad])
    
    # Add labels
    label_height = 40
    good_label = np.ones((label_height, good_row.shape[1], 3), dtype=np.uint8) * 200
    cv2.putText(good_label, 'GOOD FLOW: Frame 1 ~= Warped Frame 2', 
               (10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 0), 2)
    
    bad_label = np.ones((label_height, bad_row.shape[1], 3), dtype=np.uint8) * 200
    cv2.putText(bad_label, 'BAD FLOW: Frame 1 != Warped Frame 2', 
               (10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 200), 2)
    
    good_combined = np.vstack([good_label, good_row])
    bad_combined = np.vstack([bad_label, bad_row])
    final = np.vstack([good_combined, np.ones((20, good_combined.shape[1], 3), dtype=np.uint8)*255, bad_combined])
    
    # Add check/cross marks
    cv2.putText(final, 'V', (good_combined.shape[1] - 40, 90), 
               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 200, 0), 4)
    cv2.putText(final, 'X', (good_combined.shape[1] - 40, good_combined.shape[0] + 110), 
               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 200), 4)
    
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'quality_comparison.png'), final)
    print(f"✓ Created: quality_comparison.png")


def create_pipeline_diagram():
    """
    Create a visual pipeline diagram
    """
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(5, 13.5, 'Complete Warping Pipeline', 
           ha='center', fontsize=16, fontweight='bold')
    
    # Steps
    steps = [
        ('Input', 'Frame 1 & Frame 2\nConsecutive video frames', 12.5),
        ('VCN Model', 'Extract CNN features\nMulti-scale pyramid', 11),
        ('Cost Volume', 'Correlate features\nMatch Frame 1 ↔ Frame 2', 9.5),
        ('Internal Warp', 'Warp features for refinement\n(Coarse → Fine)', 8),
        ('Predict Flow', 'Output: (U, V) per pixel\nDense optical flow field', 6.5),
        ('Final Warp', 'Warp Frame 2 RGB image\nUsing predicted flow', 5),
        ('Output', 'Save: warp-*.jpg\nVisual quality check', 3.5),
    ]
    
    # Draw boxes and arrows
    for i, (title, desc, y) in enumerate(steps):
        # Box
        rect = patches.FancyBboxPatch((1, y-0.6), 8, 1.2, 
                                     boxstyle="round,pad=0.1",
                                     linewidth=2, 
                                     edgecolor='steelblue' if i != 5 else 'red',
                                     facecolor='lightblue' if i != 5 else 'lightcoral',
                                     alpha=0.7)
        ax.add_patch(rect)
        
        # Text
        ax.text(5, y+0.15, title, ha='center', fontsize=11, fontweight='bold')
        ax.text(5, y-0.25, desc, ha='center', fontsize=9, style='italic')
        
        # Arrow to next step
        if i < len(steps) - 1:
            arrow = FancyArrowPatch((5, y-0.7), (5, steps[i+1][2]+0.7),
                                   arrowstyle='->', mutation_scale=30,
                                   color='black', linewidth=2)
            ax.add_patch(arrow)
    
    # Annotations
    ax.text(9.5, 8, '← Internal\n(Model)', ha='left', fontsize=8, 
           style='italic', color='steelblue')
    ax.text(9.5, 5, '← External\n(Post-process)', ha='left', fontsize=8, 
           style='italic', color='red')
    
    # Legend
    legend_y = 1.5
    ax.text(5, legend_y, 'Blue boxes: Inside VCN neural network', 
           ha='center', fontsize=9, color='steelblue', fontweight='bold')
    ax.text(5, legend_y-0.4, 'Red box: Post-processing for visualization', 
           ha='center', fontsize=9, color='red', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'pipeline_diagram.png'), dpi=150, bbox_inches='tight')
    print(f"✓ Created: pipeline_diagram.png")
    plt.close()


def main():
    """
    Generate all warping visualization diagrams
    """
    print("=" * 60)
    print("Generating Image Warping Diagrams")
    print("=" * 60)
    print()
    
    print("Creating diagrams...")
    print()
    
    try:
        create_grid_visualization()
        create_warp_example()
        create_quality_comparison()
        create_pipeline_diagram()
        
        print()
        print("=" * 60)
        print("✓ All diagrams generated successfully!")
        print(f"✓ Output directory: {OUTPUT_DIR}")
        print("=" * 60)
        print()
        print("Generated files:")
        print("  - grid_transformation.png    (Grid warping process)")
        print("  - warp_example_simple.png    (Simple warping example)")
        print("  - quality_comparison.png     (Good vs bad flow)")
        print("  - pipeline_diagram.png       (Complete pipeline)")
        print()
        
    except Exception as e:
        print(f"✗ Error generating diagrams: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

