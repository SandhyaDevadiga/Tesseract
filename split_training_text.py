import os
import random
import pathlib
import subprocess

# Set training text
training_text_file = 'langdata/eng/training_text'

# List all fonts you're using (must match names in font_properties and real .ttf/.otf)
font_list = [
    'NotoSans-Bold',
    'NotoSans-ExtraBold',
    'NotoSans-Light',
    'NotoSans-Medium',
    'NotoSans-Regular',
    'NotoSans-SemiBold',
    'NotoSansArabic-Bold',
    'NotoSansArabic-ExtraBold',
    'NotoSansArabic-Light',
    'NotoSansArabic-Medium',
    'NotoSansArabic-Regular',
    'NotoSansArabic-SemiBold',
    'NotoSansCJKsc-Bold',
    'NotoSansCJKsc-Light',
    'NotoSansCJKsc-Medium',
    'NotoSansCJKsc-Regular',
]

# Load lines from training text
lines = []
with open(training_text_file, 'r', encoding='utf-8') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

# Output folder
output_directory = 'tesstrain/data/Noto-ground-truth'
os.makedirs(output_directory, exist_ok=True)

# Shuffle and limit to 100 lines
random.shuffle(lines)
lines = lines[:100]

# Generate training data per font
line_count = 0
for font in font_list:
    for i, line in enumerate(lines):
        # Save line as .gt.txt
        gt_file = os.path.join(output_directory, f'{font}_{i}.gt.txt')
        with open(gt_file, 'w', encoding='utf-8') as output_file:
            output_file.write(line)

        # Generate image + box file using text2image
        subprocess.run([
            'text2image',
            f'--font={font}',
            f'--text={gt_file}',
            f'--outputbase={output_directory}/{font}_{i}',
            '--fonts_dir=./fonts',  # Tells text2image to look in your local fonts folder
            '--fontconfig_tmpdir=./tmp_fontconfig',  # Avoid system-level font caching
            '--max_pages=1',
            '--strip_unrenderable_words',
            '--leading=32',
            '--xsize=3600',
            '--ysize=480',
            '--char_spacing=1.0',
            '--exposure=0',
            '--unicharset_file=langdata/eng.unicharset',
            '--fonts_conf=fonts.conf',  # <- 🔥 VERY IMPORTANT
        ])

    line_count += 1
