#!/usr/bin/env python3

"""
# Basic usage (copies files)
python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq

# Use symbolic links to save space
python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq --mode symlink

# Custom output location
python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq \
    --output /mnt/hdd2/Bob/organized_results/video01

"""


"""
Organize optical flow expansion outputs into categorized subdirectories.

This script reads all outputs from a sequence directory and organizes them
into 6 subdirectories based on output type:
- flow/          : Optical flow fields (flo-*.png)
- expansion/     : Optical expansion maps (exp-*.png)
- motion_in_depth/: Motion-in-depth (mid-*.png)
- occlusion/     : Occlusion maps (occ-*.png)
- flow_viz/      : Flow visualizations (visflo-*.jpg)
- warped/        : Warped images (warp-*.jpg)
"""

import os
import sys
import shutil
import glob
from pathlib import Path


def organize_outputs(source_dir, output_base_dir=None, mode='copy'):
    """
    Organize output files into categorized subdirectories.
    
    Args:
        source_dir: Directory containing the mixed output files (e.g., /path/to/video01/seq)
        output_base_dir: Base directory for organized outputs (default: source_dir/../organized)
        mode: 'copy' to copy files, 'move' to move files, 'symlink' to create symbolic links
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist!")
        sys.exit(1)
    
    # Set default output directory if not specified
    if output_base_dir is None:
        output_base_dir = source_path.parent / 'organized'
    else:
        output_base_dir = Path(output_base_dir)
    
    # Define output categories
    categories = {
        'flow': 'flo-*.png',
        'expansion': 'exp-*.png',
        'motion_in_depth': 'mid-*.png',
        'occlusion': 'occ-*.png',
        'flow_viz': ['visflo-*.jpg', 'visflo-*.jpg.jpg'],  # Handle both correct and double-extension
        'warped': ['warp-*.jpg', 'warp-*.jpg.jpg']  # Handle both correct and double-extension
    }
    
    print(f"Source directory: {source_path}")
    print(f"Output directory: {output_base_dir}")
    print(f"Mode: {mode}\n")
    
    # Create output subdirectories
    for category in categories.keys():
        category_dir = output_base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {category_dir}")
    
    print("\nOrganizing files...")
    
    # Process each category
    stats = {}
    for category, pattern in categories.items():
        # Handle both single pattern and list of patterns
        patterns = [pattern] if isinstance(pattern, str) else pattern
        
        # Find all files matching the pattern(s)
        files = []
        for pat in patterns:
            files.extend(source_path.glob(pat))
        
        # Remove duplicates and sort
        files = sorted(set(files))
        stats[category] = len(files)
        
        category_dir = output_base_dir / category
        
        for file_path in files:
            # Clean up filename by removing double extensions
            clean_name = file_path.name.replace('.jpg.jpg', '.jpg').replace('.png.png', '.png')
            dest_path = category_dir / clean_name
            
            if mode == 'copy':
                shutil.copy2(file_path, dest_path)
            elif mode == 'move':
                shutil.move(str(file_path), str(dest_path))
            elif mode == 'symlink':
                if dest_path.exists():
                    dest_path.unlink()
                dest_path.symlink_to(file_path.absolute())
            else:
                print(f"Error: Unknown mode '{mode}'")
                sys.exit(1)
        
        if stats[category] > 0:
            print(f"  {category:20s}: {stats[category]:5d} files")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    total_files = sum(stats.values())
    print(f"Total files organized: {total_files}")
    print(f"\nBreakdown by category:")
    for category, count in stats.items():
        print(f"  - {category:20s}: {count:5d} files")
    
    # Calculate directory sizes
    print(f"\nDirectory sizes:")
    for category in categories.keys():
        category_dir = output_base_dir / category
        size = sum(f.stat().st_size for f in category_dir.glob('*') if f.is_file())
        size_mb = size / (1024 * 1024)
        size_gb = size / (1024 * 1024 * 1024)
        if size_gb >= 1:
            print(f"  - {category:20s}: {size_gb:6.2f} GB")
        else:
            print(f"  - {category:20s}: {size_mb:6.2f} MB")
    
    total_size = sum((output_base_dir / cat).stat().st_size 
                     for cat in categories.keys() if (output_base_dir / cat).exists())
    
    print(f"\nOutput location: {output_base_dir}")
    print("="*60)
    
    return stats


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Organize optical flow expansion outputs into categorized subdirectories.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Copy files to organized structure (default)
  python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq
  
  # Specify custom output directory
  python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq \\
      --output /mnt/hdd2/Bob/organized_output/video01
  
  # Create symbolic links instead of copying (saves disk space)
  python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq \\
      --mode symlink
  
  # Move files instead of copying
  python visualize_output.py /mnt/hdd2/Bob/output_expansion/video01/seq \\
      --mode move
        """
    )
    
    parser.add_argument(
        'source_dir',
        help='Source directory containing mixed output files (e.g., /path/to/video01/seq)'
    )
    
    parser.add_argument(
        '--output', '-o',
        dest='output_dir',
        default=None,
        help='Output base directory (default: <source_dir>/../organized)'
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['copy', 'move', 'symlink'],
        default='copy',
        help='File operation mode (default: copy)'
    )
    
    args = parser.parse_args()
    
    # Run the organization
    organize_outputs(args.source_dir, args.output_dir, args.mode)


if __name__ == '__main__':
    main()

