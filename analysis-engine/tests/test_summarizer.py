"""
Unit tests for the Summarizer module
"""

import unittest
import os
from summarizer import Summarizer


class TestSummarizer(unittest.TestCase):
    """Test suite for Summarizer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create summarizer without API key (will use fallback responses)
        self.summarizer = Summarizer(api_key=None)
    
    def test_summarizer_initializes_without_api_key(self):
        """Test that summarizer can initialize without API key"""
        summarizer = Summarizer(api_key=None)
        
        self.assertIsNotNone(summarizer)
        self.assertFalse(summarizer.api_available)
    
    def test_summarize_file_returns_string_without_api_key(self):
        """Test that summarize_file returns a string even without API key"""
        result = self.summarizer.summarize_file(
            'test.py',
            'def hello():\n    print("hello")',
            'python'
        )
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_generate_repo_overview_returns_string_without_api_key(self):
        """Test that generate_repo_overview returns string without API key"""
        repo_info = {
            'total_files': 10,
            'languages': {'python': 5, 'javascript': 3}
        }
        key_files = ['main.py', 'index.js', 'package.json']
        
        result = self.summarizer.generate_repo_overview(repo_info, key_files)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_answer_question_returns_string_without_api_key(self):
        """Test that answer_question returns string without API key"""
        context = {
            'structure': 'Flask API',
            'key_files': ['app.py'],
            'languages': {'python': 10},
            'dependencies': {'flask': '1.0', 'sqlalchemy': '1.4'}
        }
        
        result = self.summarizer.answer_question(
            'What is the main framework?',
            context
        )
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_summarizer_handles_long_content(self):
        """Test that summarizer handles very long file content"""
        long_content = "x = 1\n" * 5000  # Create very long content
        
        result = self.summarizer.summarize_file(
            'test.py',
            long_content,
            'python'
        )
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_summarizer_works_with_different_languages(self):
        """Test summarizer with different programming languages"""
        languages = ['python', 'javascript', 'java', 'go', 'rust']
        
        for lang in languages:
            result = self.summarizer.summarize_file(
                f'test.{lang}',
                f'code in {lang}',
                lang
            )
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
