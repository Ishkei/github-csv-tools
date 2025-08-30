#!/usr/bin/env python3
import csv
import re
import html

def clean_text(text, max_length=200):
    """Clean and truncate text content"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def clean_csv(input_file, output_file):
    """Clean and organize the CSV file"""
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Define cleaner column names
        fieldnames = [
            'issue_number',
            'issue_title', 
            'issue_state',
            'issue_labels',
            'issue_milestone',
            'issue_user',
            'issue_assignee',
            'issue_assignees',
            'issue_created_at',
            'issue_updated_at',
            'issue_closed_at',
            'issue_body',
            'comment_user',
            'comment_created_at',
            'comment_updated_at',
            'comment_body',
            'row_type'
        ]
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        row_count = 0
        for row in reader:
            row_count += 1
            
            # Clean and organize the data
            cleaned_row = {
                'issue_number': row.get('issue.number', ''),
                'issue_title': clean_text(row.get('issue.title', ''), 100),
                'issue_state': row.get('issue.state', ''),
                'issue_labels': row.get('issue.labels', ''),
                'issue_milestone': row.get('issue.milestone', ''),
                'issue_user': row.get('issue.user', ''),
                'issue_assignee': row.get('issue.assignee', ''),
                'issue_assignees': row.get('issue.assignees', ''),
                'issue_created_at': row.get('issue.created_at', ''),
                'issue_updated_at': row.get('issue.updated_at', ''),
                'issue_closed_at': row.get('issue.closed_at', ''),
                'issue_body': clean_text(row.get('issue.body', ''), 150),
                'comment_user': row.get('comment.user', ''),
                'comment_created_at': row.get('comment.created_at', ''),
                'comment_updated_at': row.get('comment.updated_at', ''),
                'comment_body': clean_text(row.get('comment.body', ''), 150),
                'row_type': 'comment' if row.get('comment.user') else 'issue'
            }
            
            writer.writerow(cleaned_row)
            
            # Progress indicator
            if row_count % 10000 == 0:
                print(f"Processed {row_count} rows...")
    
    print(f"Cleaning complete! Processed {row_count} rows.")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    input_file = "cookie-autodelete-issues-with-comments.csv"
    output_file = "cookie-autodelete-clean.csv"
    
    print("Starting CSV cleanup...")
    clean_csv(input_file, output_file)
