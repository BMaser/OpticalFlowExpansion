#!/usr/bin/env python3
"""
Create videos from organized optical flow expansion outputs.

This script reads images from each category subdirectory and creates
video files at specified frame rate.
"""

import cv2
import numpy as np
import sys
from pathlib import Path
from tqdm import tqdm
import argparse


def create_video_from_images(image_dir, output_video, fps=15, codec='mp4v'):
    """
    Create a video from a sequence of images.
    
    Args:
        image_dir: Directory containing image sequence
        output_video: Output video file path
        fps: Frames per second for the output video
        codec: Video codec fourcc code
    """
    image_dir = Path(image_dir)
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    for ext in image_extensions:
        images.extend(sorted(image_dir.glob(f'*{ext}')))
    
    if not images:
        print(f"  No images found in {image_dir}")
        return False
    
    images = sorted(images)
    print(f"  Found {len(images)} images")
    
    # Read first image to get dimensions
    first_img = cv2.imread(str(images[0]))
    if first_img is None:
        print(f"  Error: Could not read first image {images[0]}")
        return False
    
    height, width = first_img.shape[:2]
    print(f"  Video resolution: {width}x{height}")
    print(f"  Frame rate: {fps} fps")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(str(output_video), fourcc, fps, (width, height))
    
    if not out.isOpened():
        print(f"  Error: Could not open video writer for {output_video}")
        return False
    
    # Write images to video
    print(f"  Creating video: {output_video.name}")
    for img_path in tqdm(images, desc="  Processing frames", unit="frame"):
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"  Warning: Could not read {img_path}")
            continue
        
        # Resize if dimensions don't match (shouldn't happen but safety check)
        if img.shape[:2] != (height, width):
            img = cv2.resize(img, (width, height))
        
        out.write(img)
    
    out.release()
    
    # Get video file size
    size_mb = output_video.stat().st_size / (1024 * 1024)
    print(f"  ✓ Created: {output_video.name} ({size_mb:.2f} MB)")
    
    return True


def create_all_videos(organized_dir, output_dir=None, fps=15, codec='mp4v'):
    """
    Create videos from all category subdirectories.
    
    Args:
        organized_dir: Directory containing organized subdirectories
        output_dir: Output directory for videos (default: organized_dir/videos)
        fps: Frames per second for output videos
        codec: Video codec fourcc code
    """
    organized_path = Path(organized_dir)
    
    if not organized_path.exists():
        print(f"Error: Directory '{organized_dir}' does not exist!")
        sys.exit(1)
    
    # Set default output directory
    if output_dir is None:
        output_dir = organized_path / 'videos'
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Source directory: {organized_path}")
    print(f"Output directory: {output_dir}")
    print(f"Frame rate: {fps} fps")
    print(f"Codec: {codec}")
    print("="*60)
    
    # Find all subdirectories
    subdirs = [d for d in organized_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print("Error: No subdirectories found in organized directory!")
        sys.exit(1)
    
    print(f"Found {len(subdirs)} categories to process\n")
    
    # Video extension based on codec
    codec_extensions = {
        'mp4v': '.mp4',
        'avc1': '.mp4',
        'H264': '.mp4',
        'X264': '.mp4',
        'XVID': '.avi',
        'MJPG': '.avi',
        'DIVX': '.avi'
    }
    video_ext = codec_extensions.get(codec, '.mp4')
    
    # Process each category
    results = {}
    for subdir in sorted(subdirs):
        category_name = subdir.name
        print(f"\nProcessing category: {category_name}")
        print("-" * 60)
        
        output_video = output_dir / f"{category_name}{video_ext}"
        success = create_video_from_images(subdir, output_video, fps, codec)
        results[category_name] = success
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    successful = sum(1 for v in results.values() if v)
    print(f"Successfully created: {successful}/{len(results)} videos")
    print(f"\nVideos created:")
    for category, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {category}")
    
    print(f"\nAll videos saved to: {output_dir}")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in output_dir.glob('*') if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    total_size_gb = total_size / (1024 * 1024 * 1024)
    
    if total_size_gb >= 1:
        print(f"Total size: {total_size_gb:.2f} GB")
    else:
        print(f"Total size: {total_size_mb:.2f} MB")
    
    print("="*60)
    
    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create videos from organized optical flow expansion outputs.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create videos with default settings (15 fps, mp4)
  python create_videos.py /mnt/hdd2/Bob/output_expansion/video01/organized
  
  # Specify custom output directory
  python create_videos.py /mnt/hdd2/Bob/output_expansion/video01/organized \\
      --output /mnt/hdd2/Bob/videos/video01
  
  # Change frame rate and codec
  python create_videos.py /mnt/hdd2/Bob/output_expansion/video01/organized \\
      --fps 30 --codec H264
  
Available codecs:
  - mp4v (default): MPEG-4, .mp4 extension
  - H264/avc1/X264: H.264, .mp4 extension
  - XVID/DIVX/MJPG: Various, .avi extension
        """
    )
    
    parser.add_argument(
        'organized_dir',
        help='Directory containing organized subdirectories with images'
    )
    
    parser.add_argument(
        '--output', '-o',
        dest='output_dir',
        default=None,
        help='Output directory for videos (default: <organized_dir>/videos)'
    )
    
    parser.add_argument(
        '--fps', '-f',
        type=int,
        default=15,
        help='Frames per second for output videos (default: 15)'
    )
    
    parser.add_argument(
        '--codec', '-c',
        default='mp4v',
        help='Video codec fourcc code (default: mp4v)'
    )
    
    args = parser.parse_args()
    
    # Create videos
    create_all_videos(args.organized_dir, args.output_dir, args.fps, args.codec)


if __name__ == '__main__':
    main()

