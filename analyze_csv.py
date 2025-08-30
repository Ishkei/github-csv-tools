#!/usr/bin/env python3
import csv
from collections import Counter
from datetime import datetime

def analyze_csv(filename):
    """Analyze the cleaned CSV file and provide insights"""
    
    issues = []
    comments = []
    labels = []
    users = []
    comment_users = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['row_type'] == 'issue':
                issues.append(row)
                if row['issue_labels']:
                    labels.extend([label.strip() for label in row['issue_labels'].split(',')])
                if row['issue_user']:
                    users.append(row['issue_user'])
            else:
                comments.append(row)
                if row['comment_user']:
                    comment_users.append(row['comment_user'])
    
    print("=" * 60)
    print("COOKIE-AUTODELETE REPOSITORY ANALYSIS")
    print("=" * 60)
    
    print(f"\n📊 OVERVIEW:")
    print(f"   Total Issues: {len(issues)}")
    print(f"   Total Comments: {len(comments)}")
    print(f"   Total Rows: {len(issues) + len(comments)}")
    
    # Issue states
    states = Counter([issue['issue_state'] for issue in issues])
    print(f"\n🔍 ISSUE STATUS:")
    for state, count in states.items():
        print(f"   {state.capitalize()}: {count}")
    
    # Top labels
    if labels:
        label_counts = Counter(labels)
        print(f"\n🏷️  TOP LABELS:")
        for label, count in label_counts.most_common(10):
            print(f"   {label}: {count}")
    
    # Top issue creators
    if users:
        user_counts = Counter(users)
        print(f"\n👥 TOP ISSUE CREATORS:")
        for user, count in user_counts.most_common(10):
            print(f"   {user}: {count}")
    
    # Top commenters
    if comment_users:
        commenter_counts = Counter(comment_users)
        print(f"\n💬 TOP COMMENTERS:")
        for user, count in commenter_counts.most_common(10):
            print(f"   {user}: {count}")
    
    # Date range
    if issues:
        dates = [issue['issue_created_at'] for issue in issues if issue['issue_created_at']]
        if dates:
            try:
                earliest = min(dates)
                latest = max(dates)
                print(f"\n📅 DATE RANGE:")
                print(f"   Earliest Issue: {earliest}")
                print(f"   Latest Issue: {latest}")
            except:
                pass
    
    # Recent activity
    print(f"\n🆕 RECENT ISSUES:")
    recent_issues = sorted(issues, key=lambda x: x['issue_created_at'], reverse=True)[:5]
    for issue in recent_issues:
        title = issue['issue_title'][:60] + "..." if len(issue['issue_title']) > 60 else issue['issue_title']
        print(f"   #{issue['issue_number']}: {title}")
        print(f"      State: {issue['issue_state']}, Created: {issue['issue_created_at']}")
    
    print(f"\n" + "=" * 60)

if __name__ == "__main__":
    analyze_csv("cookie-autodelete-clean.csv")
