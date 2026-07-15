#!/usr/bin/env python3
"""
JPQ Construction Media Manifest Generator v3
Scans media folder, filters project images/videos, creates proper JSON format
Excludes: logos, contact info
Only includes: project photos, van photos, videos
"""

import os
import json
import sys
from pathlib import Path

# Configuration
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), 'media')
MANIFEST_FILE = os.path.join(os.path.dirname(__file__), 'media-manifest.json')

# Supported formats (only widely-supported, cross-browser compatible)
# Images: Formats with excellent browser support
IMAGE_FORMATS = {
    '.jpg', '.jpeg',  # Universal JPEG support
    '.png',           # Universal PNG support
    '.gif',           # Universal GIF support
    '.webp',          # Modern browsers (Chrome, Firefox, Safari, Edge)
    '.svg'            # Universal vector format
}

# Videos: Formats with reliable cross-browser support
VIDEO_FORMATS = {
    '.mp4',   # Universal video format (H.264 codec)
    '.webm'   # Good support (Chrome, Firefox, Edge)
}

# Files to EXCLUDE (logos, contact info, etc)
EXCLUDE_KEYWORDS = ['logo', 'contact_info']

def should_exclude(filename):
    """Check if file should be excluded from carousel"""
    filename_lower = filename.lower()
    return any(keyword in filename_lower for keyword in EXCLUDE_KEYWORDS)

def get_file_size(filepath):
    """Get human-readable file size"""
    size_bytes = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def scan_media_folder(debug=False):
    """Scan media folder and return list of project files"""
    media_items = []
    
    if not os.path.exists(MEDIA_FOLDER):
        if debug:
            print(f"❌ Media folder not found: {MEDIA_FOLDER}")
        return media_items
    
    if debug:
        print(f"📁 Scanning folder: {MEDIA_FOLDER}\n")
    
    try:
        files = sorted(os.listdir(MEDIA_FOLDER))
        
        for filename in files:
            filepath = os.path.join(MEDIA_FOLDER, filename)
            
            # Skip folders
            if os.path.isdir(filepath):
                continue
            
            # Skip excluded files (logos, contact info)
            if should_exclude(filename):
                if debug:
                    print(f"   ⏭️  SKIP (excluded): {filename}")
                continue
            
            # Get file extension
            ext = os.path.splitext(filename)[1].lower()
            
            # Check if supported format
            if ext in IMAGE_FORMATS:
                file_size = get_file_size(filepath)
                # Remove file extension for display name
                name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
                media_items.append({
                    'type': 'image',
                    'src': f'media/{filename}',
                    'name': name
                })
                if debug:
                    print(f"   ✅ IMAGE: {filename} ({file_size})")

            elif ext in VIDEO_FORMATS:
                file_size = get_file_size(filepath)
                # Remove file extension for display name
                name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
                media_items.append({
                    'type': 'video',
                    'src': f'media/{filename}',
                    'name': name
                })
                if debug:
                    print(f"   ✅ VIDEO: {filename} ({file_size})")
            
            elif debug:
                print(f"   ⏭️  SKIP (unsupported): {filename}")
    
    except Exception as e:
        print(f"❌ Error scanning folder: {e}")
        return []
    
    return media_items

def create_manifest(media_items):
    """Create media-manifest.json"""
    manifest = media_items
    
    try:
        with open(MANIFEST_FILE, 'w') as f:
            json.dump(manifest, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error creating manifest: {e}")
        return False

def main():
    """Main execution"""
    debug = '--debug' in sys.argv
    
    print("🎬 Generating media manifest (project files only)...\n")
    
    # Scan media folder
    media_items = scan_media_folder(debug=debug)
    
    if not media_items:
        print("❌ No project media files found in /media folder")
        print(f"   Supported images: {', '.join(IMAGE_FORMATS)}")
        print(f"   Supported videos: {', '.join(VIDEO_FORMATS)}")
        print(f"   Excluded: {', '.join(EXCLUDE_KEYWORDS)}")
        return
    
    # Create manifest
    if create_manifest(media_items):
        print(f"\n✅ SUCCESS: Manifest created")
        print(f"📍 Location: {MANIFEST_FILE}")
        print(f"📊 Found {len(media_items)} project media files:\n")
        
        for item in media_items:
            icon = "🖼️ " if item['type'] == 'image' else "🎬"
            print(f"   {icon} {item['name']}")
        
        print("\n✅ Your carousel is ready! Open the website in your browser.")
    else:
        print("❌ Failed to create manifest")

if __name__ == '__main__':
    main()
