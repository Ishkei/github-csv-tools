#!/usr/bin/env python3
import csv
from collections import Counter
from datetime import datetime

def generate_html_report(filename):
    """Generate an HTML report from the cleaned CSV data"""
    
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
    
    # Calculate statistics
    total_issues = len(issues)
    total_comments = len(comments)
    open_issues = len([i for i in issues if i['issue_state'] == 'open'])
    closed_issues = len([i for i in issues if i['issue_state'] == 'closed'])
    
    # Top labels
    label_counts = Counter(labels)
    top_labels = label_counts.most_common(15)
    
    # Top users
    user_counts = Counter(users)
    top_users = user_counts.most_common(10)
    
    # Top commenters
    commenter_counts = Counter(comment_users)
    top_commenters = commenter_counts.most_common(10)
    
    # Recent issues
    recent_issues = sorted(issues, key=lambda x: x['issue_created_at'], reverse=True)[:10]
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cookie-AutoDelete Repository Analysis</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #3498db; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
        .table-container {{ overflow-x: auto; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #e8f4f8; }}
        .issue-item {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #e74c3c; }}
        .issue-number {{ font-weight: bold; color: #2c3e50; }}
        .issue-title {{ color: #34495e; margin: 5px 0; }}
        .issue-meta {{ color: #7f8c8d; font-size: 0.9em; }}
        .open {{ border-left-color: #e74c3c; }}
        .closed {{ border-left-color: #27ae60; }}
        .timestamp {{ color: #95a5a6; font-size: 0.8em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🍪 Cookie-AutoDelete Repository Analysis</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_issues:,}</div>
                <div class="stat-label">Total Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_comments:,}</div>
                <div class="stat-label">Total Comments</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{open_issues:,}</div>
                <div class="stat-label">Open Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{closed_issues:,}</div>
                <div class="stat-label">Closed Issues</div>
            </div>
        </div>
        
        <h2>🏷️ Top Labels</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr><th>Label</th><th>Count</th></tr>
                </thead>
                <tbody>
"""
    
    for label, count in top_labels:
        html_content += f"                    <tr><td>{label}</td><td>{count}</td></tr>\n"
    
    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <h2>👥 Top Issue Creators</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr><th>User</th><th>Issues Created</th></tr>
                </thead>
                <tbody>
"""
    
    for user, count in top_users:
        html_content += f"                    <tr><td>{user}</td><td>{count}</td></tr>\n"
    
    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <h2>💬 Top Commenters</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr><th>User</th><th>Comments</th></tr>
                </thead>
                <tbody>
"""
    
    for user, count in top_commenters:
        html_content += f"                    <tr><td>{user}</td><td>{count}</td></tr>\n"
    
    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <h2>🆕 Recent Issues</h2>
"""
    
    for issue in recent_issues:
        state_class = issue['issue_state']
        html_content += f"""
        <div class="issue-item {state_class}">
            <div class="issue-number">#{issue['issue_number']}</div>
            <div class="issue-title">{issue['issue_title']}</div>
            <div class="issue-meta">
                State: {issue['issue_state'].capitalize()} | 
                Created by: {issue['issue_user']} | 
                <span class="timestamp">{issue['issue_created_at']}</span>
            </div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open('cookie-autodelete-report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML report generated: cookie-autodelete-report.html")

if __name__ == "__main__":
    generate_html_report("cookie-autodelete-clean.csv")
