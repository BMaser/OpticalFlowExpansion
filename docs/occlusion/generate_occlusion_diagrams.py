"""
Generate visual diagrams for Occlusion documentation.

This script creates various diagrams to illustrate occlusion concepts:
1. Occlusion vs disocclusion concept
2. Forward-backward consistency
3. Car motion occlusion
4. Camera motion occlusion
5. Person disocclusion
6. UAV occlusion patterns
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
OUTPUT_DIR = '/home/bobmaser/github/OpticalFlowExpansion/docs/occlusion'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_occlusion_concept():
    """Create diagram explaining occlusion vs disocclusion."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Occlusion (hiding)
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('OCCLUSION\n(Visible → Hidden)', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    # Frame 1: Tree visible
    ax.text(2, 9, 'Frame 1:', fontsize=13, fontweight='bold')
    tree1 = Rectangle((1.5, 5), 1.5, 3, fill=True, facecolor='green',
                     edgecolor='darkgreen', linewidth=2, alpha=0.7)
    ax.add_patch(tree1)
    ax.text(2.25, 6.5, '🌳', fontsize=40, ha='center', va='center')
    ax.text(2.25, 4.5, 'Tree\n(Visible)', ha='center', fontsize=11,
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Frame 2: Car occludes tree
    ax.text(6.5, 9, 'Frame 2:', fontsize=13, fontweight='bold')
    # Car in front
    car = Rectangle((5, 5.5), 2.5, 1.8, fill=True, facecolor='red',
                   edgecolor='darkred', linewidth=3, alpha=0.8)
    ax.add_patch(car)
    ax.text(6.25, 6.4, '🚗', fontsize=30, ha='center', va='center')
    # Tree partially visible behind
    tree2_partial = Rectangle((5.8, 5), 0.4, 1.5, fill=True, facecolor='green',
                             edgecolor='darkgreen', linewidth=2, alpha=0.4)
    ax.add_patch(tree2_partial)
    ax.text(6, 6, '🌳', fontsize=20, ha='center', va='center', alpha=0.3)
    
    ax.text(6.25, 4, 'Tree\n(OCCLUDED)', ha='center', fontsize=11,
           bbox=dict(boxstyle='round', facecolor='red', alpha=0.8), color='white')
    
    # Arrow showing motion
    ax.annotate('', xy=(5, 6.5), xytext=(3, 6.5),
                arrowprops=dict(arrowstyle='->', lw=4, color='blue'))
    ax.text(4, 7.2, 'Car moves', ha='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    # Result
    ax.text(5, 2, 'Result: Tree is OCCLUDED\n(hidden behind car)', ha='center', fontsize=12,
           bbox=dict(boxstyle='round', facecolor='orange', alpha=0.8))
    
    # Disocclusion (revealing)
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('DISOCCLUSION\n(Hidden → Visible)', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    # Frame 1: Wall hidden behind car
    ax.text(2, 9, 'Frame 1:', fontsize=13, fontweight='bold')
    # Car
    car1 = Rectangle((1, 5.5), 2.5, 1.8, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=3, alpha=0.8)
    ax.add_patch(car1)
    ax.text(2.25, 6.4, '🚗', fontsize=30, ha='center', va='center')
    # Wall partially hidden
    wall1_partial = Rectangle((2.7, 5), 0.4, 3, fill=True, facecolor='gray',
                              edgecolor='black', linewidth=2, alpha=0.4)
    ax.add_patch(wall1_partial)
    
    ax.text(2.25, 4, 'Wall\n(Hidden)', ha='center', fontsize=11,
           bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Frame 2: Wall revealed
    ax.text(6.5, 9, 'Frame 2:', fontsize=13, fontweight='bold')
    # Wall now visible
    wall2 = Rectangle((5, 5), 1.5, 3, fill=True, facecolor='gray',
                     edgecolor='black', linewidth=2, alpha=0.7)
    ax.add_patch(wall2)
    ax.text(5.75, 6.5, '🧱', fontsize=35, ha='center', va='center')
    # Car moved away
    car2 = Rectangle((7, 5.5), 2.5, 1.8, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=3, alpha=0.8)
    ax.add_patch(car2)
    ax.text(8.25, 6.4, '🚗', fontsize=30, ha='center', va='center')
    
    ax.text(5.75, 4, 'Wall\n(DISOCCLUDED)', ha='center', fontsize=11,
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Arrow showing motion
    ax.annotate('', xy=(7, 6.5), xytext=(3.5, 6.5),
                arrowprops=dict(arrowstyle='->', lw=4, color='green'))
    ax.text(5.25, 7.5, 'Car moves', ha='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    # Result
    ax.text(6.5, 2, 'Result: Wall is DISOCCLUDED\n(revealed)', ha='center', fontsize=12,
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/occlusion_concept.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created occlusion_concept.png")
    plt.close()


def create_forward_backward_consistency():
    """Create diagram showing forward-backward consistency check."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Top left: Forward flow
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Step 1: Forward Flow\n(Frame 1 → Frame 2)', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Frame 1 pixels
    for i in range(3):
        for j in range(3):
            x, y = 2 + i*2, 3 + j*2
            ax.plot(x, y, 'bo', markersize=15)
            ax.text(x, y, f'({i},{j})', ha='center', va='center', 
                   fontsize=8, color='white', fontweight='bold')
    
    # Forward flow arrows (most consistent)
    ax.arrow(2, 3, 2, 0.5, head_width=0.25, head_length=0.3,
            fc='green', ec='green', linewidth=2)
    ax.arrow(4, 5, 2, 0.5, head_width=0.25, head_length=0.3,
            fc='green', ec='green', linewidth=2)
    ax.arrow(2, 7, 2, 0.5, head_width=0.25, head_length=0.3,
            fc='green', ec='green', linewidth=2)
    
    # One occluded (different direction)
    ax.arrow(6, 7, 1.5, 1.5, head_width=0.25, head_length=0.3,
            fc='red', ec='red', linewidth=2, linestyle='--')
    ax.text(7, 8.5, 'Occluded?', fontsize=9, color='red', fontweight='bold')
    
    ax.text(5, 1, 'Compute flow from Frame 1 to Frame 2', ha='center', fontsize=10)
    
    # Top right: Backward flow
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Step 2: Backward Flow\n(Frame 2 → Frame 1)', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Frame 2 pixels (shifted)
    for i in range(3):
        for j in range(3):
            x, y = 4 + i*2, 3.5 + j*2
            ax.plot(x, y, 'ro', markersize=15)
            ax.text(x, y, f"({i},{j})'", ha='center', va='center',
                   fontsize=8, color='white', fontweight='bold')
    
    # Backward flow arrows (should go back)
    ax.arrow(4, 3.5, -2, -0.5, head_width=0.25, head_length=0.3,
            fc='green', ec='green', linewidth=2)
    ax.arrow(6, 5.5, -2, -0.5, head_width=0.25, head_length=0.3,
            fc='green', ec='green', linewidth=2)
    ax.arrow(4, 7.5, -2, -0.5, head_width=0.25, head_length=0.3,
            fc='green', ec='green', linewidth=2)
    
    # Occluded pixel doesn't go back correctly
    ax.arrow(7.5, 8.5, -0.5, -2, head_width=0.25, head_length=0.3,
            fc='red', ec='red', linewidth=2, linestyle='--')
    ax.text(7, 6, 'Wrong!', fontsize=9, color='red', fontweight='bold')
    
    ax.text(5, 1, 'Compute flow from Frame 2 back to Frame 1', ha='center', fontsize=10)
    
    # Bottom left: Consistency check
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Step 3: Consistency Check\nForward + Backward', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Original pixels
    consistent_pixels = [(2, 3), (4, 5), (2, 7)]
    occluded_pixel = (6, 7)
    
    for x, y in consistent_pixels:
        # Start
        ax.plot(x, y, 'bo', markersize=15, label='Start' if x==2 and y==3 else '')
        # Forward
        ax.plot(x+2, y+0.5, 'ro', markersize=12, alpha=0.5)
        # Backward (returns to start)
        ax.plot(x, y, 'go', markersize=20, alpha=0.3)
        
        # Draw round trip
        ax.annotate('', xy=(x+2, y+0.5), xytext=(x, y),
                   arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
        ax.annotate('', xy=(x+0.1, y+0.1), xytext=(x+2, y+0.5),
                   arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
        
        ax.text(x, y-0.7, '✓', ha='center', fontsize=20, color='green',
               fontweight='bold')
    
    # Occluded pixel
    x, y = occluded_pixel
    ax.plot(x, y, 'bo', markersize=15)
    ax.plot(x+1.5, y+1.5, 'ro', markersize=12, alpha=0.5)
    ax.plot(x+1, y-0.5, 'mx', markersize=15, markeredgewidth=3)
    
    ax.annotate('', xy=(x+1.5, y+1.5), xytext=(x, y),
               arrowprops=dict(arrowstyle='->', color='red', lw=1.5, linestyle='--'))
    ax.annotate('', xy=(x+1, y-0.5), xytext=(x+1.5, y+1.5),
               arrowprops=dict(arrowstyle='->', color='red', lw=1.5, linestyle='--'))
    
    ax.text(x+1, y-1.2, '✗', ha='center', fontsize=20, color='red',
           fontweight='bold')
    ax.text(x+1, y-2, 'OCCLUDED', ha='center', fontsize=10, color='red',
           fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    ax.legend(loc='upper left')
    ax.text(5, 1, 'Check if round-trip returns to start', ha='center', fontsize=10)
    
    # Bottom right: Result (occlusion map)
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_title('Result: Occlusion Map', fontsize=13, fontweight='bold')
    
    # Create occlusion map visualization
    occ_map = np.zeros((50, 50))
    # Most pixels are not occluded
    occ_map[:, :] = 0.1
    # One region is occluded
    occ_map[35:42, 30:37] = 0.9
    
    im = ax.imshow(occ_map, cmap='gray_r', origin='lower', extent=[0, 10, 0, 10])
    ax.set_xlabel('Image X', fontsize=11)
    ax.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Occlusion Probability', fontsize=10)
    
    # Mark the occluded region
    ax.text(6.7, 7.7, 'Occluded\nRegion', ha='center', fontsize=11,
           bbox=dict(boxstyle='round', facecolor='red', alpha=0.8), color='white',
           fontweight='bold')
    
    ax.text(3, 3, 'Visible\nRegions', ha='center', fontsize=11,
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
           fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/forward_backward_consistency.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created forward_backward_consistency.png")
    plt.close()


def create_car_motion_occlusion():
    """Create diagram for car moving and occluding background."""
    fig = plt.figure(figsize=(16, 6))
    
    # Left: Frame 1
    ax1 = plt.subplot(1, 3, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Frame 1\n(Before)', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Background (road + trees)
    ax1.fill_between([0, 10], [0, 0], [10, 10], alpha=0.3, color='lightblue', label='Sky')
    ax1.fill_between([0, 10], [0, 0], [4, 4], alpha=0.4, color='gray', label='Road')
    
    # Trees in background
    for x in [2, 4, 6, 8]:
        ax1.text(x, 6, '🌳', fontsize=25, ha='center')
    
    # Car on right side
    car1 = Rectangle((7, 3), 2, 1.5, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=3, alpha=0.8)
    ax1.add_patch(car1)
    ax1.text(8, 3.75, '🚗', fontsize=25, ha='center', va='center')
    
    ax1.text(5, 1, 'All trees visible', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Middle: Frame 2
    ax2 = plt.subplot(1, 3, 2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.set_title('Frame 2\n(After car moves left)', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    # Background
    ax2.fill_between([0, 10], [0, 0], [10, 10], alpha=0.3, color='lightblue')
    ax2.fill_between([0, 10], [0, 0], [4, 4], alpha=0.4, color='gray')
    
    # Trees
    for x in [2, 8]:
        ax2.text(x, 6, '🌳', fontsize=25, ha='center')
    
    # Car moved left, occludes middle trees
    car2 = Rectangle((3, 3), 2, 1.5, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=3, alpha=0.8)
    ax2.add_patch(car2)
    ax2.text(4, 3.75, '🚗', fontsize=25, ha='center', va='center')
    
    # Partially visible trees behind car
    ax2.text(4, 6, '🌳', fontsize=15, ha='center', alpha=0.3)
    ax2.text(6, 6, '🌳', fontsize=15, ha='center', alpha=0.3)
    
    # Motion arrow
    ax2.annotate('', xy=(4, 5), xytext=(7, 5),
                arrowprops=dict(arrowstyle='->', lw=4, color='red'))
    ax2.text(5.5, 5.5, 'Motion', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    ax2.text(5, 1, 'Middle trees OCCLUDED', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.8), color='white')
    
    # Right: Occlusion map
    ax3 = plt.subplot(1, 3, 3)
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.set_aspect('equal')
    ax3.set_title('Occlusion Map', fontsize=14, fontweight='bold')
    
    # Create occlusion map
    occ_map = np.zeros((100, 100))
    # Low occlusion everywhere
    occ_map[:, :] = 0.1
    # High occlusion where car leading edge is
    occ_map[30:55, 25:35] = 0.9  # Left edge of car
    
    # Add some gradient
    for i in range(10):
        occ_map[30:55, 35+i] = 0.9 - i*0.08
    
    im = ax3.imshow(occ_map, cmap='hot', origin='lower', extent=[0, 10, 0, 10])
    ax3.set_xlabel('Image X', fontsize=11)
    ax3.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    cbar.set_label('Occlusion Probability', fontsize=10)
    
    # Annotations
    ax3.text(3, 4, 'High\nOcclusion', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), fontweight='bold')
    ax3.arrow(3, 3.5, -0.5, 0, head_width=0.3, head_length=0.2,
             fc='white', ec='white', linewidth=2)
    
    ax3.text(7, 6, 'Low\nOcclusion', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7), 
            fontweight='bold', color='white')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/car_motion_occlusion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created car_motion_occlusion.png")
    plt.close()


def create_camera_motion_occlusion():
    """Create diagram for camera motion creating occlusions."""
    fig = plt.figure(figsize=(16, 6))
    
    # Scene setup: Tree (close) and Wall (far)
    
    # Left: Frame 1
    ax1 = plt.subplot(1, 3, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Frame 1\n(Camera position 1)', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Wall (far, background)
    wall1 = Rectangle((3, 4), 5, 4, fill=True, facecolor='gray',
                     edgecolor='black', linewidth=2, alpha=0.5)
    ax1.add_patch(wall1)
    ax1.text(5.5, 6, '🧱 Wall (Far)', ha='center', fontsize=12)
    
    # Tree (close, foreground)
    tree1 = Rectangle((2, 4.5), 1.5, 3, fill=True, facecolor='green',
                     edgecolor='darkgreen', linewidth=2, alpha=0.8)
    ax1.add_patch(tree1)
    ax1.text(2.75, 6, '🌳', fontsize=30, ha='center')
    ax1.text(2.75, 4, 'Tree\n(Close)', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))
    
    # Camera
    ax1.plot(1, 2, 'r*', markersize=25)
    ax1.text(1, 1, 'Camera', ha='center', fontsize=10, fontweight='bold')
    
    # Middle: Frame 2
    ax2 = plt.subplot(1, 3, 2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.set_title('Frame 2\n(Camera moved right)', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    # Wall (shifted less, farther away)
    wall2 = Rectangle((2.5, 4), 5, 4, fill=True, facecolor='gray',
                     edgecolor='black', linewidth=2, alpha=0.5)
    ax2.add_patch(wall2)
    ax2.text(5, 6, '🧱', ha='center', fontsize=20)
    
    # Tree (shifted more, closer)
    tree2 = Rectangle((0.5, 4.5), 1.5, 3, fill=True, facecolor='green',
                     edgecolor='darkgreen', linewidth=2, alpha=0.8)
    ax2.add_patch(tree2)
    ax2.text(1.25, 6, '🌳', fontsize=30, ha='center')
    
    # Wall partially hidden behind tree
    ax2.fill_between([1.25, 2], [4, 4], [8, 8], color='black', alpha=0.3)
    ax2.text(1.6, 6, '❌', fontsize=20, ha='center', color='red')
    
    # Camera
    ax2.plot(3, 2, 'r*', markersize=25)
    ax2.text(3, 1, 'Camera', ha='center', fontsize=10, fontweight='bold')
    
    # Motion arrow
    ax2.annotate('', xy=(3, 2), xytext=(1, 2),
                arrowprops=dict(arrowstyle='->', lw=4, color='red'))
    ax2.text(2, 2.5, 'Right', ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    ax2.text(5, 3, 'Wall OCCLUDED\nby tree', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.8), color='white')
    
    # Right: Occlusion map
    ax3 = plt.subplot(1, 3, 3)
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.set_aspect('equal')
    ax3.set_title('Occlusion Map\n(from Frame 2)', fontsize=14, fontweight='bold')
    
    # Create occlusion map
    occ_map = np.zeros((100, 100))
    # Low everywhere
    occ_map[:, :] = 0.15
    # High where wall is behind tree
    occ_map[45:75, 10:25] = 0.85
    
    im = ax3.imshow(occ_map, cmap='gray_r', origin='lower', extent=[0, 10, 0, 10])
    ax3.set_xlabel('Image X', fontsize=11)
    ax3.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    cbar.set_label('Occlusion Probability', fontsize=10)
    
    # Annotations
    ax3.text(1.75, 6, 'Occluded\nRegion', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9), fontweight='bold')
    
    ax3.text(6, 6, 'Visible\nRegion', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
            fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/camera_motion_occlusion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created camera_motion_occlusion.png")
    plt.close()


def create_person_disocclusion():
    """Create diagram for person walking revealing background."""
    fig = plt.figure(figsize=(16, 6))
    
    # Left: Frame 1
    ax1 = plt.subplot(1, 3, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Frame 1\n(Person on left)', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Wall background
    ax1.fill_between([0, 10], [3, 3], [8, 8], alpha=0.4, color='tan')
    ax1.text(5, 5.5, '🧱 Wall', ha='center', fontsize=15)
    
    # Person on left
    person1 = Circle((2.5, 5), 1, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax1.add_patch(person1)
    ax1.text(2.5, 5, '🚶', fontsize=35, ha='center', va='center')
    ax1.text(2.5, 2.5, 'Person', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    
    # Middle: Frame 2
    ax2 = plt.subplot(1, 3, 2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.set_title('Frame 2\n(Person moved right)', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    # Wall background (now more visible)
    ax2.fill_between([0, 10], [3, 3], [8, 8], alpha=0.4, color='tan')
    ax2.text(5, 5.5, '🧱 Wall', ha='center', fontsize=15)
    
    # Revealed region highlighted
    revealed = Rectangle((1, 3), 2.5, 5, fill=False, edgecolor='green',
                         linewidth=4, linestyle='--')
    ax2.add_patch(revealed)
    ax2.text(2.25, 5.5, '✓', fontsize=40, ha='center', color='green', fontweight='bold')
    
    # Person on right
    person2 = Circle((7, 5), 1, fill=True, facecolor='blue',
                    edgecolor='darkblue', linewidth=2, alpha=0.7)
    ax2.add_patch(person2)
    ax2.text(7, 5, '🚶', fontsize=35, ha='center', va='center')
    
    # Motion arrow
    ax2.annotate('', xy=(6, 5), xytext=(3.5, 5),
                arrowprops=dict(arrowstyle='->', lw=4, color='green'))
    ax2.text(4.75, 5.7, 'Motion', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    ax2.text(2.25, 2, 'Wall REVEALED\n(Disoccluded)', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9), fontweight='bold')
    
    # Right: Occlusion/Disocclusion map
    ax3 = plt.subplot(1, 3, 3)
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.set_aspect('equal')
    ax3.set_title('Disocclusion Map\n(Revealed regions)', fontsize=14, fontweight='bold')
    
    # Create disocclusion map
    disc_map = np.zeros((100, 100))
    # Low everywhere
    disc_map[:, :] = 0.1
    # High where person was (revealed background)
    disc_map[30:80, 10:35] = 0.85
    
    # Use inverted colormap for disocclusion
    im = ax3.imshow(disc_map, cmap='RdYlGn', origin='lower', extent=[0, 10, 0, 10])
    ax3.set_xlabel('Image X', fontsize=11)
    ax3.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    cbar.set_label('Disocclusion Probability', fontsize=10)
    
    # Annotations
    ax3.text(2.25, 5.5, 'Disoccluded\n(Revealed)', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), fontweight='bold')
    
    ax3.text(7, 5.5, 'Normal\n(Always visible)', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/person_disocclusion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created person_disocclusion.png")
    plt.close()


def create_uav_occlusion():
    """Create diagram for UAV flight with occlusions."""
    fig = plt.figure(figsize=(16, 7))
    
    # Left: Side view
    ax1 = plt.subplot(1, 3, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.set_title('Side View\n(UAV Flying Forward)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distance', fontsize=11)
    ax1.set_ylabel('Altitude', fontsize=11)
    
    # Terrain with obstacles
    ax1.fill_between([0, 3], [0, 0], [2, 2], alpha=0.5, color='brown', label='Ground')
    ax1.fill_between([3, 5], [0, 0], [4, 4], alpha=0.6, color='green', label='Hill')
    ax1.fill_between([5, 7], [0, 0], [3, 3], alpha=0.5, color='brown')
    ax1.fill_between([7, 10], [0, 0], [1.5, 1.5], alpha=0.5, color='brown')
    
    # Tree on hill
    ax1.text(4, 5, '🌳', fontsize=30, ha='center')
    
    # UAV trajectory
    ax1.plot([1, 8], [7, 6], 'r--', linewidth=2, label='UAV path')
    ax1.plot(1, 7, 'r*', markersize=20)
    ax1.text(1, 7.5, '🚁', fontsize=20, ha='center')
    ax1.arrow(1, 7, 3, -0.4, head_width=0.3, head_length=0.3,
             fc='red', ec='red', linewidth=2)
    
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Middle: Camera view
    ax2 = plt.subplot(1, 3, 2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.set_title('Camera View\n(Downward facing)', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    # Ground
    ax2.fill_between([0, 10], [7, 7], [10, 10], alpha=0.4, color='brown')
    ax2.text(5, 8.5, 'Ground', ha='center', fontsize=12)
    
    # Hill (appears as elevation)
    hill_patch = patches.Ellipse((4, 5), 3, 4, fill=True, facecolor='darkgreen',
                                edgecolor='green', linewidth=2, alpha=0.7)
    ax2.add_patch(hill_patch)
    ax2.text(4, 5, 'Hill', ha='center', fontsize=11, fontweight='bold', color='white')
    
    # Tree occludes part of hill
    tree_shadow = Circle((4, 5.5), 0.8, fill=True, facecolor='darkgreen',
                        edgecolor='black', linewidth=2, alpha=0.9)
    ax2.add_patch(tree_shadow)
    ax2.text(4, 5.5, '🌳', fontsize=25, ha='center')
    
    # Occlusion region
    ax2.text(4, 4, '❌', fontsize=30, ha='center', color='red', alpha=0.5)
    ax2.text(4, 3.5, 'Occluded\n(behind tree)', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.7), color='white')
    
    # Right: Occlusion map
    ax3 = plt.subplot(1, 3, 3)
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.set_aspect('equal')
    ax3.set_title('Occlusion Map', fontsize=14, fontweight='bold')
    
    # Create occlusion map with terrain
    occ_map = np.zeros((100, 100))
    # Low occlusion for ground
    occ_map[:, :] = 0.1
    
    # Hill region
    y, x = np.ogrid[:100, :100]
    hill_mask = ((x - 40)**2 / 400 + (y - 50)**2 / 900) < 1
    occ_map[hill_mask] = 0.3
    
    # Tree creates high occlusion
    tree_mask = ((x - 40)**2 + (y - 55)**2) < 100
    occ_map[tree_mask] = 0.9
    
    # Occluded region behind tree
    occluded_region = ((x - 40)**2 / 100 + (y - 40)**2 / 200) < 1
    occ_map[occluded_region] = 0.7
    
    im = ax3.imshow(occ_map, cmap='hot', origin='lower', extent=[0, 10, 0, 10])
    ax3.set_xlabel('Image X', fontsize=11)
    ax3.set_ylabel('Image Y', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    cbar.set_label('Occlusion Probability', fontsize=10)
    
    # Annotations
    ax3.text(4, 5.5, 'Tree\n(High)', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), fontweight='bold')
    ax3.text(4, 4, 'Occluded\n(Med)', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='orange', alpha=0.8), fontweight='bold')
    ax3.text(7, 8, 'Ground\n(Low)', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.8),
            fontweight='bold', color='white')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/uav_occlusion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created uav_occlusion.png")
    plt.close()


def create_interpretation_guide():
    """Create interpretation guide for occlusion maps."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create occlusion gradient
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.repeat(gradient, 50, axis=0)
    
    ax.imshow(gradient, aspect='auto', cmap='gray_r', extent=[0, 1, 0, 1])
    ax.set_yticks([])
    ax.set_xticks([0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0])
    ax.set_xticklabels(['0.0\nVisible\n(No occlusion)', '0.2\nLow', '0.4', 
                       '0.5\nUncertain', '0.6', '0.8\nHigh',
                       '1.0\nOccluded\n(Definitely)'], fontsize=10)
    ax.set_xlabel('Occlusion Probability', fontsize=13, fontweight='bold')
    ax.set_title('Occlusion Map Interpretation Guide', fontsize=16, fontweight='bold', pad=20)
    
    # Add interpretation boxes
    interpretations = [
        (0.1, 'Black\nVisible Pixels\n(Valid flow)', 'green', 0.15),
        (0.3, 'Dark Gray\nLow Occlusion\n(Mostly reliable)', 'lightgreen', 0.15),
        (0.5, 'Medium Gray\nUncertain\n(Use with caution)', 'yellow', 0.15),
        (0.7, 'Light Gray\nLikely Occluded\n(Unreliable flow)', 'orange', 0.15),
        (0.9, 'White\nDefinitely Occluded\n(Invalid flow)', 'red', 0.15)
    ]
    
    for prob, text, color, y_pos in interpretations:
        ax.text(prob, y_pos, text, ha='center', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=color, alpha=0.8, edgecolor='black', linewidth=2),
               color='white' if color in ['red', 'orange'] else 'black')
    
    # Add use cases
    ax.text(0.5, 0.85, 'Common Use Cases:', ha='center', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.75,
           '• Object Segmentation: High occlusion at object boundaries\n'
           '• Flow Refinement: Discard flow where occlusion > 0.5\n'
           '• Video Inpainting: Fill occluded regions with plausible content\n'
           '• Depth Ordering: Occluding objects are closer than occluded\n'
           '• Motion Analysis: Occlusion patterns reveal object/camera motion',
           ha='center', va='top', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Add critical thresholds
    ax.axvline(x=0.5, color='blue', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(0.5, 0.95, 'Typical\nThreshold', ha='center', fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='blue', alpha=0.8), color='white')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/interpretation_guide.png', dpi=150, bbox_inches='tight')
    print(f"✓ Created interpretation_guide.png")
    plt.close()


def main():
    """Generate all occlusion diagrams."""
    print("Generating Occlusion Documentation Diagrams...")
    print("=" * 60)
    
    create_occlusion_concept()
    create_forward_backward_consistency()
    create_car_motion_occlusion()
    create_camera_motion_occlusion()
    create_person_disocclusion()
    create_uav_occlusion()
    create_interpretation_guide()
    
    print("=" * 60)
    print(f"✓ All diagrams saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()

