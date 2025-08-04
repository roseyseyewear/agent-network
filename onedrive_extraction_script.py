#!/usr/bin/env python3
"""
OneDrive Roseys Business Document Extraction Script
Enhanced with duplicate detection and version prioritization
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import csv
import json
import re
from datetime import datetime
from pathlib import Path
import traceback
from collections import defaultdict

def extract_docx_content(filepath):
    """Extract text content from DOCX files using zipfile method"""
    try:
        with zipfile.ZipFile(filepath, 'r') as docx:
            try:
                xml_content = docx.read('word/document.xml')
                root = ET.fromstring(xml_content)
                
                # Extract all text elements
                text_elements = []
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        text_elements.append(elem.text.strip())
                
                return ' '.join(text_elements)
            except:
                try:
                    for file_info in docx.infolist():
                        if 'document' in file_info.filename.lower():
                            content = docx.read(file_info.filename).decode('utf-8', errors='ignore')
                            return content
                except:
                    pass
                return f"Error extracting content from {filepath}"
    except Exception as e:
        return f"Error extracting {filepath}: {str(e)}"

def extract_txt_content(filepath):
    """Extract content from TXT files"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {filepath}: {str(e)}"

def extract_csv_content(filepath):
    """Extract content from CSV files"""
    try:
        content = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    content.append(f"Headers: {', '.join(row)}")
                elif row_num < 50:  # Limit to first 50 rows for large CSVs
                    content.append(' | '.join(row))
                elif row_num == 50:
                    content.append("... (truncated for length)")
                    break
        return '\n'.join(content)
    except Exception as e:
        return f"Error reading CSV {filepath}: {str(e)}"

def extract_json_content(filepath):
    """Extract content from JSON files"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            return json.dumps(data, indent=2)[:5000]  # Limit length
    except Exception as e:
        return f"Error reading JSON {filepath}: {str(e)}"

def extract_file_date(filepath):
    """Extract date from filename or file modification time"""
    try:
        # Try to extract date from filename
        filename = os.path.basename(filepath)
        
        # Look for date patterns in filename
        date_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',     # YYYY-MM-DD
            r'(\d{4})(\d{2})(\d{2})',       # YYYYMMDD
            r'(\d{2})(\d{2})(\d{2})',       # YYMMDD or DDMMYY
            r'_(\d{6})[\._]',               # _YYMMDD_ or _YYMMDD.
            r'_(\d{6})$',                   # _YYMMDD at end
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    if len(match.group(1)) == 4:  # YYYY format
                        return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
                    elif len(match.group(1)) == 6:  # YYMMDD
                        date_str = match.group(1)
                        year = int(date_str[:2])
                        if year > 50:
                            year += 1900
                        else:
                            year += 2000
                        return datetime(year, int(date_str[2:4]), int(date_str[4:6]))
                    else:  # YY format
                        year = int(match.group(1))
                        if year > 50:
                            year += 1900
                        else:
                            year += 2000
                        return datetime(year, int(match.group(2)), int(match.group(3)))
                except:
                    continue
        
        # Fallback to file modification time
        return datetime.fromtimestamp(os.path.getmtime(filepath))
    
    except:
        return datetime(2020, 1, 1)  # Default date

def identify_duplicate_groups(filepaths):
    """Group files that are likely duplicates/versions of the same document"""
    groups = defaultdict(list)
    
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        
        # Remove common version indicators to find base name
        base_name = filename
        
        # Remove date patterns
        base_name = re.sub(r'_\d{6}', '', base_name)  # _YYMMDD
        base_name = re.sub(r'_\d{8}', '', base_name)  # _YYYYMMDD
        base_name = re.sub(r'_\d{4}-\d{2}-\d{2}', '', base_name)  # _YYYY-MM-DD
        
        # Remove version indicators
        base_name = re.sub(r'_\d+$', '', base_name.rsplit('.', 1)[0]) + '.' + base_name.rsplit('.', 1)[1]
        base_name = re.sub(r' \(\d+\)', '', base_name)  # (1), (2), etc.
        base_name = re.sub(r'_v\d+', '', base_name)  # _v1, _v2, etc.
        base_name = base_name.replace('AutoRecovered', '').replace('Backup of ', '').replace('Copy of ', '')
        
        # Clean up extra spaces and underscores
        base_name = re.sub(r'[_\s]+', '_', base_name).strip('_')
        
        groups[base_name].append(filepath)
    
    return groups

def prioritize_versions(file_group):
    """Select the best version from a group of duplicate files"""
    if len(file_group) == 1:
        return file_group[0], []
    
    # Score each file
    scored_files = []
    for filepath in file_group:
        filename = os.path.basename(filepath).lower()
        score = 0
        
        # Penalty for backup/auto-recovered files
        if 'autorecovered' in filename or 'backup' in filename or 'copy of' in filename:
            score -= 10
        
        # Bonus for date in filename (more recent = higher score)
        file_date = extract_file_date(filepath)
        score += (file_date.year - 2020) * 2  # Bonus for more recent years
        score += file_date.month * 0.1
        score += file_date.day * 0.01
        
        # Bonus for longer filenames (usually more descriptive)
        score += len(filename) * 0.001
        
        scored_files.append((score, filepath))
    
    # Sort by score (highest first)
    scored_files.sort(reverse=True)
    
    primary_file = scored_files[0][1]
    alternate_versions = [f[1] for f in scored_files[1:]]
    
    return primary_file, alternate_versions

def categorize_onedrive_content(filepath):
    """Categorize content based on OneDrive folder structure and filename patterns"""
    filepath_lower = filepath.lower()
    
    # Check folder structure first (higher priority)
    if '\\10_sustainability\\' in filepath_lower or '/10_sustainability/' in filepath_lower:
        return 'sustainability'
    
    if '\\marketing\\' in filepath_lower or '/marketing/' in filepath_lower:
        return 'marketing_brand'
    
    if '\\product\\' in filepath_lower or '/product/' in filepath_lower:
        return 'product_dev'
    
    if ('\\planning\\' in filepath_lower or '/planning/' in filepath_lower or 
        '\\business-plan\\' in filepath_lower or '/business-plan/' in filepath_lower or
        'sdsi' in filepath_lower):
        return 'business_planning'
    
    if ('\\documentary\\' in filepath_lower or '/documentary/' in filepath_lower or
        'documentary-2022' in filepath_lower):
        return 'documentary_media'
    
    # Meeting folders and specific meeting patterns
    if ('meeting' in filepath_lower and ('23_meetings' in filepath_lower or 
        'meetings\\' in filepath_lower or 'meetings/' in filepath_lower)) or any(keyword in filepath_lower for keyword in [
        'intern', 'consultant', 'interview', 'team']):
        return 'operations_team'
    
    # Financial file patterns - more comprehensive
    if any(keyword in filepath_lower for keyword in [
        'proforma', 'revenue', 'expense', 'financial', 'custamor', 'costs', 'sdsi'
    ]):
        return 'financial_planning'
    
    # Then check filename patterns
    # Documentary & Media
    if any(keyword in filepath_lower for keyword in [
        'doc_', 'video', 'media', 'film', 'premiere', 'shot', 'documentary'
    ]):
        return 'documentary_media'
    
    # Marketing & Brand Development
    if any(keyword in filepath_lower for keyword in [
        'marketing', 'brand', 'campaign', 'content', 'social', 'persona', 'ig_', 'revolution'
    ]):
        return 'marketing_brand'
    
    # Product Development
    if any(keyword in filepath_lower for keyword in [
        'product', 'lens', 'frame', 'zeiss', 'specification', '3.0', 'iii'
    ]):
        return 'product_dev'
    
    # Operations & Team Management  
    if any(keyword in filepath_lower for keyword in [
        'intern', 'team', 'interview', 'consultant', 'operations'
    ]):
        return 'operations_team'
    
    # Sustainability Initiatives
    if any(keyword in filepath_lower for keyword in [
        'sustainability', 'social', 'good', 'environmental', 'eco', 'green', 'heysocialgood'
    ]):
        return 'sustainability'
    
    # Business Planning Evolution (including meetings, planning docs)
    if any(keyword in filepath_lower for keyword in [
        'planning', 'strategy', 'roadmap', 'plan', 'annual', 'quarterly', 'meeting', 'business'
    ]):
        return 'business_planning'
    
    # Default to business planning if no clear category
    return 'business_planning'

def create_onedrive_knowledge_base(source_dir, output_dir):
    """Create knowledge base from OneDrive data with duplicate handling"""
    
    extracted_content = {
        'business_planning': [],
        'marketing_brand': [],
        'product_dev': [],
        'operations_team': [],
        'financial_planning': [],
        'documentary_media': [],
        'sustainability': []
    }
    
    duplicate_log = []
    file_extensions = ['.docx', '.txt', '.csv', '.json', '.xlsx']
    
    print(f"OneDrive extraction: {source_dir}")
    
    # Collect all relevant files
    all_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            filepath = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            
            if ext.lower() in file_extensions:
                all_files.append(filepath)
    
    print(f"Found {len(all_files)} files to process")
    
    # Group duplicates
    duplicate_groups = identify_duplicate_groups(all_files)
    
    processed_count = 0
    for base_name, file_group in duplicate_groups.items():
        if len(file_group) > 1:
            primary_file, alternates = prioritize_versions(file_group)
            duplicate_log.append({
                'base_name': base_name,
                'primary': primary_file,
                'alternates': alternates
            })
            files_to_process = [primary_file]  # Only process primary version
            print(f"Duplicate group '{base_name}': Using {os.path.basename(primary_file)} (skipping {len(alternates)} alternates)")
        else:
            files_to_process = file_group
        
        # Process selected files
        for filepath in files_to_process:
            processed_count += 1
            if processed_count % 50 == 0:
                print(f"Processed {processed_count} files...")
            
            try:
                # Extract content based on file type
                _, ext = os.path.splitext(filepath)
                
                if ext.lower() == '.docx':
                    content = extract_docx_content(filepath)
                elif ext.lower() == '.txt':
                    content = extract_txt_content(filepath)
                elif ext.lower() in ['.csv']:
                    content = extract_csv_content(filepath)
                elif ext.lower() == '.json':
                    content = extract_json_content(filepath)
                elif ext.lower() in ['.xlsx']:
                    content = f"Excel file: {filepath} (contains data tables and spreadsheets)"
                else:
                    continue
                
                # Get file date and categorize
                file_date = extract_file_date(filepath)
                category = categorize_onedrive_content(filepath)
                
                # Store extracted content
                extracted_content[category].append({
                    'filepath': filepath,
                    'date': file_date,
                    'content': content,
                    'filename': os.path.basename(filepath)
                })
                
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    print(f"Total files processed: {processed_count}")
    print(f"Duplicate groups resolved: {len([g for g in duplicate_groups.values() if len(g) > 1])}")
    
    # Create knowledge base files
    knowledge_base_files = {
        'business_planning': 'Business Planning Evolution.md',
        'marketing_brand': 'Marketing & Brand Development.md',
        'product_dev': 'Product Development.md',
        'operations_team': 'Operations & Team Management.md',
        'financial_planning': 'Financial Planning.md',
        'documentary_media': 'Documentary & Media.md',
        'sustainability': 'Sustainability Initiatives.md'
    }
    
    descriptions = {
        'business_planning': "Strategic business planning evolution 2021-2024 - roadmaps, annual plans, SDSI documentation",
        'marketing_brand': "Marketing campaigns, brand development, content strategy, social media planning",
        'product_dev': "Product development including Collection III/Delta, lens specifications, costs, Zeiss partnership",
        'operations_team': "Team management, meetings, consultants, intern programs, operational processes",
        'financial_planning': "Financial projections, proformas, revenue models, business case development",
        'documentary_media': "2022 documentary project, video content, media planning and production",
        'sustainability': "Environmental initiatives, social good projects, sustainable business practices"
    }
    
    for category, filename in knowledge_base_files.items():
        filepath = os.path.join(output_dir, filename)
        
        # Sort content chronologically
        content_items = sorted(extracted_content[category], key=lambda x: x['date'])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {filename.replace('.md', '')}\n\n")
            f.write("⚠️ **NEEDS REVIEW** - OneDrive content extraction with duplicate resolution\n\n")
            f.write(f"**Total Documents in Category: {len(content_items)}**\n\n")
            f.write(f"**Category Focus:** {descriptions[category]}\n\n")
            f.write("---\n\n")
            
            if not content_items:
                f.write("*No documents found for this category.*\n")
                continue
            
            for item in content_items:
                f.write(f"## 📄 {item['filename']}\n")
                f.write(f"**Source:** `{item['filepath']}`\n")
                f.write(f"**Date:** {item['date'].strftime('%Y-%m-%d')}\n\n")
                f.write("### Content:\n")
                f.write("```\n")
                f.write(item['content'][:15000])  # Limit content length
                if len(item['content']) > 15000:
                    f.write("\n... (content truncated for length)")
                f.write("\n```\n\n")
                f.write("---\n\n")
        
        print(f"Created: {filepath} with {len(content_items)} documents")
    
    # Create duplicate resolution log
    log_filepath = os.path.join(output_dir, "Duplicate_Resolution_Log.md")
    with open(log_filepath, 'w', encoding='utf-8') as f:
        f.write("# OneDrive Duplicate Resolution Log\n\n")
        f.write("This log shows how duplicate files were resolved during extraction.\n\n")
        
        for log_entry in duplicate_log:
            f.write(f"## {log_entry['base_name']}\n")
            f.write(f"**Primary Version:** `{log_entry['primary']}`\n\n")
            f.write("**Alternate Versions (not extracted):**\n")
            for alt in log_entry['alternates']:
                f.write(f"- `{alt}`\n")
            f.write("\n---\n\n")
    
    return extracted_content

def main():
    source_dir = r"C:\claude_home\onedrive_roseys"
    output_dir = r"C:\claude_home\obsidian_ai-vault\ONEDRIVE_ROSEYS"
    
    print("=== ONEDRIVE ROSEYS EXTRACTION ===")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create knowledge base
    extracted_content = create_onedrive_knowledge_base(source_dir, output_dir)
    
    print("\n=== ONEDRIVE EXTRACTION COMPLETE ===")
    total_docs = 0
    for category, items in extracted_content.items():
        count = len(items)
        total_docs += count
        print(f"{category}: {count} documents")
    
    print(f"\nTotal documents processed: {total_docs}")
    print(f"All 7 knowledge base files created in: {output_dir}")
    print("Duplicate resolution log created: Duplicate_Resolution_Log.md")

if __name__ == "__main__":
    main()