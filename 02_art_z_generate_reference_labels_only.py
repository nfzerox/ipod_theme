#!/usr/bin/env python3

from ipodhax.silverdb import unpack_silverdb
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
import platform
import re
import shutil

def get_system_font():
    system = platform.system()
    if system == 'Darwin':  # macOS
        font_paths = [
            '/System/Library/Fonts/Helvetica.ttc',
            '/System/Library/Fonts/Arial.ttf',
            '/Library/Fonts/Arial.ttf',
            '/System/Library/Fonts/SFNSMono.ttf',
            '/System/Library/Fonts/AppleSDGothicNeo.ttc'
        ]
    elif system == 'Windows':
        font_paths = [
            'C:\\Windows\\Fonts\\arial.ttf',
            'C:\\Windows\\Fonts\\calibri.ttf'
        ]
    else:  # Linux and others
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/TTF/arial.ttf'
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
            
    return None

def get_sequence_number(filename):
    match = re.search(r'22944(\d+)_', filename)
    return match.group(1) if match else None

def create_text_image(sequence_number, width, height):
    # Create new image in 'L' mode (grayscale) first
    img = Image.new('L', (width, height), 0)  # 0 is black
    draw = ImageDraw.Draw(img)
    
    font_size = min(width, height)
    text = sequence_number
    system_font = get_system_font()
    
    while font_size > 1:
        try:
            try:
                if system_font:
                    font = ImageFont.truetype(system_font, font_size)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Get text size
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            if text_width <= width * 0.9:
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                
                # Draw white text (255)
                draw.text((x, y), text, fill=255, font=font)
                break
            
            font_size = int(font_size * 0.9)
        except:
            font_size = int(font_size * 0.9)
    
    # Convert to binary image (pure black and white)
    # Threshold at 128 (middle of 0-255 range)
    binary_img = img.point(lambda x: 0 if x < 128 else 255, '1')
    
    # Convert back to RGB without alpha channel and ensure pure black/white
    final_img = Image.new('RGBA', (width, height), (0, 0, 0))  # Black background
    final_img.paste((255, 255, 255), mask=binary_img)  # White text
    
    return final_img

def process_images(directory):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist")
        return

    for filename in os.listdir(directory):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(directory, filename)
            
            sequence_number = get_sequence_number(filename)
            if not sequence_number:
                print(f"Skipping {filename}: Could not extract sequence number")
                continue
            
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                
                new_img = create_text_image(sequence_number, width, height)
                
                # Save as PNG without alpha channel
                new_img.save(filepath, 'PNG', optimize=True)
                print(f"Processed {filename}: extracted sequence number {sequence_number}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

script_dir = Path(__file__).parent
input_path = script_dir / "SilverImagesDB.LE.bin"
output_dir = script_dir / "body"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

output_dir.mkdir()

with open(input_path, "rb") as silver_stream:
  unpack_silverdb(silver_stream, output_dir)

script_dir = Path(__file__).parent
process_images(script_dir / "body")
