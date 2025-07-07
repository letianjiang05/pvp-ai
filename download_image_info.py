#!/usr/bin/env python3
"""
Image Download and Information Display Script
Downloads an image from a URL and displays its information
"""

import os
import sys
import requests
from urllib.parse import urlparse
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import json

def download_image(url, save_dir="downloads"):
    """Download an image from URL and save it to the specified directory"""
    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Extract filename from URL
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    
    # If no filename in URL, generate one
    if not file_name or '.' not in file_name:
        file_name = f"downloaded_image_{hash(url) % 10000}.jpg"
    
    # Build complete file path
    file_path = os.path.join(save_dir, file_name)
    
    try:
        # Send HTTP request to download file
        print(f"Downloading {url}...")
        response = requests.get(url, timeout=30, stream=True)
        
        # Check if request was successful
        if response.status_code == 200:
            # Write file content to local file
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"✓ Successfully downloaded: {file_path}")
            return file_path
        else:
            print(f"✗ Failed to download {url}, status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading {url}: {e}")
        return None

def get_image_info(image_path):
    """Get comprehensive information about an image"""
    info = {}
    
    try:
        # Get file info
        file_stat = os.stat(image_path)
        info['file_size'] = f"{file_stat.st_size:,} bytes ({file_stat.st_size / 1024:.2f} KB)"
        info['file_path'] = os.path.abspath(image_path)
        
        # Open with PIL for format and mode info
        with Image.open(image_path) as img:
            info['format'] = img.format
            info['mode'] = img.mode
            info['size'] = f"{img.width} x {img.height} pixels"
            info['width'] = img.width
            info['height'] = img.height
            
            # Get EXIF data if available
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                info['exif_available'] = True
                info['exif_data'] = exif
            else:
                info['exif_available'] = False
        
        # Open with OpenCV for additional analysis
        img_cv = cv2.imread(image_path)
        if img_cv is not None:
            info['opencv_shape'] = f"{img_cv.shape[1]} x {img_cv.shape[0]} x {img_cv.shape[2]}"
            info['channels'] = img_cv.shape[2] if len(img_cv.shape) > 2 else 1
            info['data_type'] = str(img_cv.dtype)
            
            # Calculate average color
            avg_color = cv2.mean(img_cv)
            info['average_color_bgr'] = [int(c) for c in avg_color[:3]]
            
            # Calculate image statistics
            info['min_value'] = float(img_cv.min())
            info['max_value'] = float(img_cv.max())
            info['mean_value'] = float(img_cv.mean())
            info['std_deviation'] = float(img_cv.std())
        
        return info
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

def display_image_info(info):
    """Display image information in a formatted way"""
    if not info:
        print("No image information available")
        return
    
    print("\n" + "="*60)
    print("IMAGE INFORMATION")
    print("="*60)
    
    # Basic file info
    print(f"📁 File Path: {info['file_path']}")
    print(f"📊 File Size: {info['file_size']}")
    
    # Image properties
    print(f"🖼️  Format: {info.get('format', 'Unknown')}")
    print(f"🎨 Color Mode: {info.get('mode', 'Unknown')}")
    print(f"📏 Dimensions: {info.get('size', 'Unknown')}")
    
    # OpenCV analysis
    if 'opencv_shape' in info:
        print(f"🔍 OpenCV Shape: {info['opencv_shape']}")
        print(f"🎯 Channels: {info['channels']}")
        print(f"📊 Data Type: {info['data_type']}")
        
        # Color information
        avg_color = info.get('average_color_bgr', [])
        if avg_color:
            print(f"🎨 Average Color (BGR): {avg_color}")
            # Convert BGR to RGB for display
            rgb_color = [avg_color[2], avg_color[1], avg_color[0]]
            print(f"🎨 Average Color (RGB): {rgb_color}")
        
        # Statistics
        print(f"📈 Min Value: {info.get('min_value', 'N/A')}")
        print(f"📈 Max Value: {info.get('max_value', 'N/A')}")
        print(f"📈 Mean Value: {info.get('mean_value', 'N/A'):.2f}")
        print(f"📈 Standard Deviation: {info.get('std_deviation', 'N/A'):.2f}")
    
    # EXIF data
    if info.get('exif_available', False):
        print(f"📷 EXIF Data: Available")
        exif_data = info.get('exif_data', {})
        if exif_data:
            print("   EXIF Tags:")
            for tag_id, value in list(exif_data.items())[:5]:  # Show first 5 tags
                print(f"     Tag {tag_id}: {value}")
            if len(exif_data) > 5:
                print(f"     ... and {len(exif_data) - 5} more tags")
    else:
        print(f"📷 EXIF Data: Not available")
    
    print("="*60)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python download_image_info.py <image_url> [save_directory]")
        print("\nExamples:")
        print("  python download_image_info.py https://example.com/image.jpg")
        print("  python download_image_info.py https://example.com/image.jpg my_images")
        return
    
    url = sys.argv[1]
    save_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    
    print("🖼️  Image Download and Information Tool")
    print("="*50)
    
    # Download the image
    image_path = download_image(url, save_dir)
    
    if image_path:
        # Get and display image information
        info = get_image_info(image_path)
        display_image_info(info)
        
        print(f"\n✅ Image downloaded and analyzed successfully!")
        print(f"📁 Saved to: {image_path}")
    else:
        print("❌ Failed to download image")

if __name__ == "__main__":
    main() 