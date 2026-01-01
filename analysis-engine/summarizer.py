"""
Summarizer - Generate AI-powered summaries of files and repositories
"""

import os
from typing import List, Dict, Any
import openai
from pathlib import Path

class Summarizer:
    """Generate summaries using OpenAI API"""
    
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        openai.api_key = api_key
        self.model = 'gpt-4'
    
    def summarize_file(self, file_path: str, content: str, language: str) -> str:
        """Summarize a single file"""
        
        # Limit content size to avoid token limits
        if len(content) > 10000:
            content = content[:10000] + '\n... (truncated)'
        
        prompt = f"""
You are a code analyzer. Provide a concise summary of the following {language} file.
Focus on:
1. What this file does
2. Main functions/classes
3. Key dependencies
4. Purpose in the codebase

File content:
{content}

Summary:
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code analyzer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error summarizing file: {e}")
            return "Error generating summary"
    
    def generate_repo_overview(self, repo_info: Dict[str, Any], key_files: List[str]) -> str:
        """Generate an overview of the entire repository"""
        
        prompt = f"""
You are a code architect. Generate a concise overview of this repository based on the metadata below.

Repository Info:
- Total Files: {repo_info.get('total_files', 'N/A')}
- Languages: {repo_info.get('languages', {})}
- Key Files: {', '.join(key_files[:5])}

Provide:
1. Project purpose (2-3 sentences)
2. Tech stack identified
3. Key files and their roles
4. Getting started tip
5. Areas to explore first

Overview:
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code architect."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error generating overview: {e}")
            return "Error generating overview"
    
    def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """Answer a question about the codebase"""
        
        prompt = f"""
You are a code expert. Answer this question about a codebase.

Context:
- Repository structure: {context.get('structure', 'N/A')}
- Key files: {context.get('key_files', [])}
- Languages: {context.get('languages', {})}
- Dependencies: {context.get('dependencies', {})}

Question: {question}

Answer:
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error answering question: {e}")
            return "Error processing your question"


if __name__ == '__main__':
    print("Summarizer initialized. Use API methods to generate summaries.")
