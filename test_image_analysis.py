#!/usr/bin/env python3
"""
Test script to demonstrate image analysis functionality
"""

import os
from download_image_info import get_image_info, display_image_info

def test_existing_image():
    """Test the image analysis with an existing image from the project"""
    
    # Use an existing image from the heroimg directory
    test_image_path = "crawler/heroimg/151.jpg"
    
    if os.path.exists(test_image_path):
        print("🖼️  Testing Image Analysis with Existing Image")
        print("="*50)
        print(f"Analyzing: {test_image_path}")
        
        # Get and display image information
        info = get_image_info(test_image_path)
        display_image_info(info)
        
        print(f"\n✅ Image analysis completed successfully!")
    else:
        print(f"❌ Test image not found: {test_image_path}")
        print("Available images in crawler/heroimg/ directory:")
        
        # List some available images
        heroimg_dir = "crawler/heroimg"
        if os.path.exists(heroimg_dir):
            files = os.listdir(heroimg_dir)[:10]  # Show first 10
            for file in files:
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    print(f"  - {file}")

if __name__ == "__main__":
    test_existing_image() 