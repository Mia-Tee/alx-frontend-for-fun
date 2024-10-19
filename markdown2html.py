#!/usr/bin/env python3
"""
This script converts a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re
import hashlib

def md5_hash(text):
    """Return the MD5 hash of the input text."""
    return hashlib.md5(text.encode()).hexdigest()

def parse_line(line):
    """Process a single line of Markdown for headings, lists, and special syntax."""
    # Handle [[text]] for MD5 hash
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: md5_hash(m.group(1)), line)
    # Handle ((text)) to remove 'c' (case insensitive)
    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)
    return line

def convert_md_to_html(input_file, output_file):
    """Convert Markdown to HTML."""
    with open(input_file, encoding='utf-8') as f:
        md_lines = f.readlines()

    html_lines = []
    in_list = False

    for line in md_lines:
        line = parse_line(line).strip()
        
        # Check for headings
        if line.startswith("#"):
            level = line.count('#')
            html_lines.append(f'<h{level}>{line[level:].strip()}</h{level}>')
        # Check for unordered lists
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f'    <li>{line[2:].strip()}</li>')
        # Check for ordered lists
        elif re.match(r'^\d+\.\s', line):
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
            html_lines.append(f'    <li>{line[line.index(".") + 1:].strip()}</li>')
        # Handle paragraphs
        elif line:
            if in_list:
                html_lines.append("</ul>" if line.startswith("- ") else "</ol>")
                in_list = False
            html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>" if line.startswith("- ") else "</ol>")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html_lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML')
    parser.add_argument('input_file', help='Path to input markdown file')
    parser.add_argument('output_file', help='Path to output HTML file')
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        exit(1)

    convert_md_to_html(args.input_file, args.output_file)
