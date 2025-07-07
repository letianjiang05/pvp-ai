#!/usr/bin/env python3
"""
Demo script to download an image from URL and analyze it
"""

from download_image_info import download_image, get_image_info, display_image_info

def demo_download_and_analyze():
    """Demo downloading and analyzing an image from URL"""
    
    # Use a sample image URL (a small test image)
    sample_url = "https://httpbin.org/image/png"
    
    print("🖼️  Demo: Download and Analyze Image from URL")
    print("="*60)
    print(f"URL: {sample_url}")
    
    # Download the image
    image_path = download_image(sample_url, "demo_downloads")
    
    if image_path:
        print(f"\n📥 Download completed!")
        
        # Get and display image information
        info = get_image_info(image_path)
        display_image_info(info)
        
        print(f"\n✅ Demo completed successfully!")
        print(f"📁 Image saved to: {image_path}")
    else:
        print("❌ Failed to download image")

if __name__ == "__main__":
    demo_download_and_analyze() 