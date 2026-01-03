"""
GitHub Actions Workflow Generator
Creates workflow files for auto-analyzing PRs with RepoPilot
"""

from typing import Dict


class GitHubActionsGenerator:
    """Generate GitHub Actions workflow files for CI/CD integration"""
    
    @staticmethod
    def generate_pr_analysis_workflow() -> str:
        """
        Generate GitHub Actions workflow that analyzes PRs with RepoPilot
        Analyzes changed files and comments results on PR
        """
        workflow = """name: RepoPilot PR Analysis

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      with:
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install RepoPilot dependencies
      run: |
        python -m pip install --upgrade pip
        pip install streamlit networkx gitpython requests python-dotenv
    
    - name: Run repository analysis
      run: |
        python -m analysis-engine.main . pr-analysis.json
    
    - name: Comment results on PR
      if: always()
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          let comment = '## 📊 RepoPilot Analysis Results\\n\\n';
          
          try {
            const analysis = JSON.parse(fs.readFileSync('pr-analysis.json', 'utf8'));
            const structure = analysis.structure;
            
            comment += `**Repository Statistics:**\\n`;
            comment += `- Total Files: ${structure.files.length}\\n`;
            comment += `- Total Directories: ${structure.directories.length}\\n`;
            comment += `- Primary Language: ${structure.primary_language || 'Unknown'}\\n\\n`;
            
            if (structure.language_distribution) {
              comment += `**Language Distribution:**\\n`;
              Object.entries(structure.language_distribution).forEach(([lang, count]) => {
                comment += `- ${lang}: ${count} files\\n`;
              });
              comment += '\\n';
            }
            
            if (structure.key_files && structure.key_files.length > 0) {
              comment += `**Key Files Identified:**\\n`;
              structure.key_files.slice(0, 5).forEach(file => {
                comment += `- \`${file}\`\\n`;
              });
            }
          } catch (error) {
            comment += `Analysis encountered an error: ${error.message}`;
          }
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
"""
        return workflow.strip()
    
    @staticmethod
    def generate_scheduled_analysis_workflow() -> str:
        """
        Generate GitHub Actions workflow that analyzes entire repo on schedule
        Generates report and uploads as artifact
        """
        workflow = """name: RepoPilot Scheduled Analysis

on:
  schedule:
    # Run daily at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      with:
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install RepoPilot dependencies
      run: |
        python -m pip install --upgrade pip
        pip install streamlit networkx gitpython requests python-dotenv
    
    - name: Run full repository analysis
      run: |
        python -m analysis-engine.main . analysis-report.json
    
    - name: Generate HTML report
      run: |
        python << 'PYTHON_EOF'
        import json
        
        with open('analysis-report.json', 'r') as f:
            data = json.load(f)
        
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>RepoPilot Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; }
        .stat { display: inline-block; margin: 10px 20px 10px 0; }
        .stat-value { font-size: 24px; font-weight: bold; color: #3498db; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #3498db; color: white; }
    </style>
</head>
<body>
    <h1>RepoPilot Analysis Report</h1>
    <div class="stat">
        <div>Total Files</div>
        <div class="stat-value">''' + str(len(data['structure']['files'])) + '''</div>
    </div>
    <div class="stat">
        <div>Primary Language</div>
        <div class="stat-value">''' + str(data['structure'].get('primary_language', 'Unknown')) + '''</div>
    </div>
    <div class="stat">
        <div>Dependencies</div>
        <div class="stat-value">''' + str(data['dependencies'].get('edges', 0)) + '''</div>
    </div>
    <h2>Languages Used</h2>
    <table>
        <tr><th>Language</th><th>Files</th></tr>
        '''
        
        for lang, count in data['structure'].get('language_distribution', {}).items():
            html += f'<tr><td>{lang}</td><td>{count}</td></tr>'
        
        html += '''
    </table>
</body>
</html>
        '''
        
        with open('analysis-report.html', 'w') as f:
            f.write(html)
        PYTHON_EOF
    
    - name: Upload analysis as artifact
      uses: actions/upload-artifact@v3
      with:
        name: repopilot-analysis
        path: |
          analysis-report.json
          analysis-report.html
"""
        return workflow.strip()
    
    @staticmethod
    def get_workflow_files() -> Dict[str, str]:
        """Get all available workflow templates"""
        return {
            'pr-analysis.yml': {
                'name': 'PR Analysis (Comments results on PRs)',
                'description': 'Analyzes changed files in PRs and comments results',
                'content': GitHubActionsGenerator.generate_pr_analysis_workflow()
            },
            'scheduled-analysis.yml': {
                'name': 'Scheduled Analysis (Daily report)',
                'description': 'Analyzes entire repo daily and generates reports',
                'content': GitHubActionsGenerator.generate_scheduled_analysis_workflow()
            }
        }
