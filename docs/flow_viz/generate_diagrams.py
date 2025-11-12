#!/usr/bin/env python3
"""
Generate visual diagrams for flow visualization documentation.
Creates color wheel and example flow visualizations.
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import sys
import os

# Add parent directory to path to import flowlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.flowlib import make_color_wheel, compute_color


def create_color_wheel_diagram(output_path='color_wheel.png', size=512):
    """
    Create a visual representation of the Middlebury color wheel.
    """
    # Create coordinate grid
    center = size // 2
    y, x = np.ogrid[-center:center, -center:center]
    
    # Calculate angle and radius for each pixel
    angle = np.arctan2(-y, -x)  # -π to +π
    radius = np.sqrt(x**2 + y**2)
    max_radius = center
    
    # Normalize radius
    radius_norm = np.clip(radius / max_radius, 0, 1)
    
    # Convert angle to u, v components
    u = np.cos(angle) * radius_norm
    v = np.sin(angle) * radius_norm
    
    # Create dummy flow with z-component
    flow = np.zeros((size, size, 3))
    flow[:, :, 0] = u
    flow[:, :, 1] = v
    flow[:, :, 2] = 1  # valid everywhere
    
    # Convert to color using the same algorithm
    img = compute_color(u, v).astype(np.uint8)
    
    # Mask out pixels outside the circle
    mask = radius > max_radius * 0.95
    img[mask] = 255
    
    # Add direction labels
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img)
    ax.axis('off')
    
    # Add directional arrows and labels
    arrow_length = center * 0.7
    arrow_props = dict(arrowstyle='->', lw=3, color='black')
    
    directions = [
        (0, '0° Right', arrow_length, 0, 'red'),
        (45, '45° Up-Right', arrow_length*0.7, arrow_length*0.7, 'orange'),
        (90, '90° Up', 0, arrow_length, 'yellow'),
        (135, '135° Up-Left', -arrow_length*0.7, arrow_length*0.7, 'green'),
        (180, '180° Left', -arrow_length, 0, 'cyan'),
        (225, '225° Down-Left', -arrow_length*0.7, -arrow_length*0.7, 'blue'),
        (270, '270° Down', 0, -arrow_length, 'blue'),
        (315, '315° Down-Right', arrow_length*0.7, -arrow_length*0.7, 'magenta'),
    ]
    
    for angle, label, dx, dy, color in directions:
        # Draw arrow
        ax.annotate('', xy=(center + dx, center + dy), 
                   xytext=(center, center),
                   arrowprops=dict(arrowstyle='->', lw=2, color='white', 
                                 edgecolor='black', linewidth=0.5))
        
        # Add label
        label_x = center + dx * 1.3
        label_y = center + dy * 1.3
        ax.text(label_x, label_y, label, 
               fontsize=10, fontweight='bold',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.title('Middlebury Color Wheel\n(Direction → Color)', 
             fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Created: {output_path}")


def create_example_flows(output_dir='examples'):
    """
    Create example flow visualizations for common scenarios.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    size = 256
    
    examples = [
        {
            'name': 'right_movement',
            'title': 'Moving Right',
            'u': lambda: np.ones((size, size)) * 0.5,
            'v': lambda: np.zeros((size, size)),
            'description': 'u=+0.5, v=0 → Red color'
        },
        {
            'name': 'left_movement',
            'title': 'Moving Left',
            'u': lambda: np.ones((size, size)) * -0.5,
            'v': lambda: np.zeros((size, size)),
            'description': 'u=-0.5, v=0 → Cyan color'
        },
        {
            'name': 'upward_movement',
            'title': 'Moving Up',
            'u': lambda: np.zeros((size, size)),
            'v': lambda: np.ones((size, size)) * -0.5,
            'description': 'u=0, v=-0.5 → Yellow color'
        },
        {
            'name': 'downward_movement',
            'title': 'Moving Down',
            'u': lambda: np.zeros((size, size)),
            'v': lambda: np.ones((size, size)) * 0.5,
            'description': 'u=0, v=+0.5 → Blue color'
        },
        {
            'name': 'expansion',
            'title': 'Expansion (Camera Forward)',
            'u': lambda: np.tile(np.arange(size)[None, :] - size/2, (size, 1)) / size,
            'v': lambda: np.tile((np.arange(size)[:, None] - size/2), (1, size)) / size,
            'description': 'Radial outward → Rainbow pattern'
        },
        {
            'name': 'rotation',
            'title': 'Rotation (Clockwise)',
            'u': lambda: -np.tile((np.arange(size)[:, None] - size/2), (1, size)) / size,
            'v': lambda: np.tile(np.arange(size)[None, :] - size/2, (size, 1)) / size,
            'description': 'Circular motion → Circular color pattern'
        }
    ]
    
    for example in examples:
        u = example['u']()
        v = example['v']()
        
        # Generate color visualization
        img = compute_color(u, v).astype(np.uint8)
        
        # Create figure with flow and visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot flow vectors
        skip = 16
        y, x = np.mgrid[0:size:skip, 0:size:skip]
        ax1.quiver(x, y, u[::skip, ::skip], v[::skip, ::skip], 
                  color='blue', angles='xy', scale_units='xy', scale=0.05)
        ax1.set_xlim(0, size)
        ax1.set_ylim(size, 0)
        ax1.set_aspect('equal')
        ax1.set_title('Flow Vectors', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Plot color visualization
        ax2.imshow(img)
        ax2.axis('off')
        ax2.set_title('Color Visualization', fontsize=12, fontweight='bold')
        
        fig.suptitle(f"{example['title']}\n{example['description']}", 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        output_path = os.path.join(output_dir, f"{example['name']}.png")
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Created: {output_path}")


def create_magnitude_brightness_example(output_path='magnitude_brightness.png'):
    """
    Show how magnitude affects brightness.
    """
    size = 256
    magnitudes = [0.2, 0.5, 0.8, 1.0, 1.5]
    
    fig, axes = plt.subplots(1, len(magnitudes), figsize=(15, 3))
    
    for idx, mag in enumerate(magnitudes):
        # Create flow with constant direction but varying magnitude
        u = np.ones((size, size)) * mag
        v = np.zeros((size, size))
        
        img = compute_color(u, v).astype(np.uint8)
        
        axes[idx].imshow(img)
        axes[idx].axis('off')
        axes[idx].set_title(f'Magnitude: {mag}\n' + 
                           ('Bright' if mag <= 1 else 'Dark'),
                           fontsize=10, fontweight='bold')
    
    fig.suptitle('How Magnitude Affects Brightness\n(All moving right, different speeds)', 
                fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Created: {output_path}")


def create_color_segments_diagram(output_path='color_segments.png'):
    """
    Show the 6 color wheel segments with their size annotations.
    """
    colorwheel = make_color_wheel()
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Display color wheel as a horizontal bar
    colorwheel_rgb = colorwheel / 255.0
    colorwheel_display = colorwheel_rgb[np.newaxis, :, :]
    
    ax.imshow(colorwheel_display, aspect='auto', interpolation='nearest')
    ax.set_xlim(0, len(colorwheel))
    ax.set_ylim(-0.5, 0.5)
    
    # Add segment labels
    segments = [
        ('RY', 0, 15, 'Red→Yellow'),
        ('YG', 15, 21, 'Yellow→Green'),
        ('GC', 21, 25, 'Green→Cyan'),
        ('CB', 25, 36, 'Cyan→Blue'),
        ('BM', 36, 49, 'Blue→Magenta'),
        ('MR', 49, 55, 'Magenta→Red'),
    ]
    
    for name, start, end, desc in segments:
        mid = (start + end) / 2
        ax.text(mid, 0, name, ha='center', va='center', 
               fontsize=12, fontweight='bold', color='white',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        ax.text(mid, -0.7, f'{end-start} colors\n{desc}', 
               ha='center', va='top', fontsize=9)
        
        # Draw segment boundaries
        if end < 55:
            ax.axvline(end, color='black', linewidth=2, linestyle='--')
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.title('Color Wheel Segments (55 total colors)', 
             fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Created: {output_path}")


def main():
    """Generate all diagrams."""
    print("Generating flow visualization diagrams...")
    print("=" * 60)
    
    # Create main color wheel
    create_color_wheel_diagram('docs/color_wheel.png')
    
    # Create color segments diagram
    create_color_segments_diagram('docs/color_segments.png')
    
    # Create magnitude-brightness example
    create_magnitude_brightness_example('docs/magnitude_brightness.png')
    
    # Create example flows
    create_example_flows('docs/examples')
    
    print("=" * 60)
    print("✓ All diagrams generated successfully!")
    print("\nGenerated files:")
    print("  - docs/color_wheel.png")
    print("  - docs/color_segments.png")
    print("  - docs/magnitude_brightness.png")
    print("  - docs/examples/*.png")


if __name__ == '__main__':
    main()

