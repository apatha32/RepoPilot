"""
Summarizer - Generate summaries of files and repositories
Free implementation without requiring API keys
"""

import os
from typing import List, Dict, Any
from pathlib import Path


class Summarizer:
    """Generate summaries using free, local methods"""
    
    def __init__(self, api_key: str = None):
        """Initialize summarizer (api_key parameter kept for compatibility)"""
        self.api_available = False
    
    def summarize_file(self, file_path: str, content: str, language: str) -> str:
        """Generate summary of a single file using heuristic analysis"""
        
        lines = content.split('\n')
        
        # Extract meaningful lines (non-empty, non-comment-only)
        meaningful_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                meaningful_lines.append(stripped)
        
        # Analyze file content
        summary_parts = []
        
        # Purpose: Look for docstrings and comments
        if language == 'python':
            if '"""' in content or "'''" in content:
                summary_parts.append("Contains class/function documentation")
        elif language in ['javascript', 'typescript', 'java']:
            if '/*' in content or '*/' in content:
                summary_parts.append("Contains JSDoc/JavaDoc documentation")
        
        # Count functions/classes
        if language == 'python':
            func_count = content.count('def ')
            class_count = content.count('class ')
            if func_count > 0:
                summary_parts.append(f"Defines {func_count} function(s)")
            if class_count > 0:
                summary_parts.append(f"Defines {class_count} class(es)")
        
        elif language in ['javascript', 'typescript']:
            func_count = content.count('function ') + content.count('const ') + content.count('let ')
            class_count = content.count('class ')
            if func_count > 0:
                summary_parts.append(f"Contains {func_count} function/variable(s)")
            if class_count > 0:
                summary_parts.append(f"Defines {class_count} class(es)")
        
        # Identify imports/dependencies
        imports = []
        for line in lines:
            if line.strip().startswith(('import ', 'from ', 'require(')):
                imports.append(line.strip())
        
        if imports:
            summary_parts.append(f"Has {len(imports)} import(s)")
        
        # File size indicator
        if len(content) > 5000:
            summary_parts.append("Large file (>5KB)")
        elif len(content) < 500:
            summary_parts.append("Small utility file (<500B)")
        
        # Generate summary
        if summary_parts:
            return f"[{language.upper()}] {file_path}: " + "; ".join(summary_parts)
        else:
            return f"[{language.upper()}] {file_path}: {len(meaningful_lines)} lines of code"
    
    def generate_repo_overview(self, repo_info: Dict[str, Any], key_files: List[str]) -> str:
        """Generate an overview of the entire repository"""
        
        total_files = repo_info.get('total_files', 0)
        languages = repo_info.get('languages', {})
        
        # Determine primary language
        primary_lang = max(languages.items(), key=lambda x: x[1])[0] if languages else "Unknown"
        
        overview_parts = []
        
        # Project purpose based on key files
        if 'package.json' in key_files:
            overview_parts.append("Node.js/JavaScript project")
        if 'requirements.txt' in key_files or 'setup.py' in key_files:
            overview_parts.append("Python project")
        if 'pom.xml' in key_files:
            overview_parts.append("Maven/Java project")
        if 'Dockerfile' in key_files or 'docker-compose.yml' in key_files:
            overview_parts.append("Containerized application")
        if 'tsconfig.json' in key_files:
            overview_parts.append("TypeScript project")
        
        # Tech stack identification
        tech_stack = []
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]:
            tech_stack.append(f"{lang} ({count} files)")
        
        overview = f"""
Repository Overview
===================
Total Files: {total_files}
Primary Language: {primary_lang}

Project Type: {', '.join(overview_parts) if overview_parts else 'General project'}

Tech Stack:
{chr(10).join('  - ' + stack for stack in tech_stack)}

Key Files to Examine:
{chr(10).join('  - ' + f for f in key_files[:5])}
"""
        return overview
    
    def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """Answer a question about the codebase based on context"""
        
        key_files = context.get('key_files', [])
        languages = context.get('languages', {})
        dependencies = context.get('dependencies', {})
        
        question_lower = question.lower()
        
        # Simple keyword-based answers
        if any(word in question_lower for word in ['setup', 'install', 'start', 'run']):
            answer = "To get started with this project:\n"
            if 'package.json' in key_files:
                answer += "1. Run 'npm install' to install dependencies\n"
                answer += "2. Check package.json for available scripts\n"
            if 'requirements.txt' in key_files:
                answer += "1. Run 'pip install -r requirements.txt' to install dependencies\n"
            if 'Dockerfile' in key_files:
                answer += "1. Build with 'docker build -t myapp .'\n"
                answer += "2. Run with 'docker run myapp'\n"
            return answer if answer != "To get started with this project:\n" else "See README.md for setup instructions."
        
        elif any(word in question_lower for word in ['structure', 'organize', 'layout']):
            return f"Project Structure:\n- Languages: {', '.join(languages.keys())}\n- Key files: {', '.join(key_files[:5])}\nSee the file tree for detailed layout."
        
        elif any(word in question_lower for word in ['technology', 'tech', 'stack', 'framework']):
            return f"Technology Stack:\nLanguages: {', '.join(languages.keys())}\nKey frameworks/tools indicated by: {', '.join(key_files[:5])}"
        
        elif any(word in question_lower for word in ['purpose', 'what', 'about']):
            return f"This project uses: {', '.join(languages.keys() if languages else ['multiple languages'])} and appears to be a general code repository. Check README.md for more details."
        
        elif any(word in question_lower for word in ['dependency', 'depend', 'import']):
            if dependencies:
                return f"Dependencies found: {list(dependencies.keys())[:10]}"
            return "Check imports/requires in source files for dependencies."
        
        else:
            return f"Analysis shows a {list(languages.keys())[0] if languages else 'mixed-language'} project with {len(key_files)} key configuration files. Check README.md and source files for more information."


if __name__ == '__main__':
    print("Summarizer initialized. Free, API-key-free operation.")
