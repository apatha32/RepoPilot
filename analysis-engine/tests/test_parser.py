"""
Unit tests for the Repository Parser module
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from parser import RepositoryParser, FileInfo


class TestRepositoryParser(unittest.TestCase):
    """Test suite for RepositoryParser class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        Path(self.temp_dir, 'test.py').write_text('print("hello")')
        Path(self.temp_dir, 'test.js').write_text('console.log("hello")')
        Path(self.temp_dir, 'test.ts').write_text('console.log("hello")')
        Path(self.temp_dir, 'README.md').write_text('# Test')
        Path(self.temp_dir, 'package.json').write_text('{}')
        Path(self.temp_dir, 'tsconfig.json').write_text('{}')
        
        # Create subdirectory
        subdir = Path(self.temp_dir, 'src')
        subdir.mkdir()
        (subdir / 'index.py').write_text('print("index")')
    
    def test_parse_returns_dict_with_required_keys(self):
        """Test that parse() returns a dict with required keys"""
        parser = RepositoryParser(self.temp_dir)
        result = parser.parse()
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_files', result)
        self.assertIn('total_directories', result)
        self.assertIn('files', result)
        self.assertIn('languages', result)
        self.assertIn('key_files', result)
    
    def test_parse_finds_files(self):
        """Test that parser identifies all files"""
        parser = RepositoryParser(self.temp_dir)
        result = parser.parse()
        
        file_names = [f['name'] for f in result['files'] if f['type'] == 'file']
        
        self.assertIn('test.py', file_names)
        self.assertIn('test.js', file_names)
        self.assertIn('test.ts', file_names)
        self.assertIn('README.md', file_names)
        self.assertIn('package.json', file_names)
    
    def test_language_detection(self):
        """Test language detection for various file types"""
        parser = RepositoryParser(self.temp_dir)
        result = parser.parse()
        
        languages = {f['name']: f['language'] for f in result['files']}
        
        self.assertEqual(languages.get('test.py'), 'python')
        self.assertEqual(languages.get('test.js'), 'javascript')
        self.assertEqual(languages.get('test.ts'), 'typescript')
        self.assertEqual(languages.get('README.md'), 'markdown')
        self.assertEqual(languages.get('package.json'), 'json')
    
    def test_key_files_identification(self):
        """Test that key files are correctly identified"""
        parser = RepositoryParser(self.temp_dir)
        result = parser.parse()
        
        key_files = [f['name'] for f in result['files'] if f['is_key_file']]
        
        self.assertIn('package.json', key_files)
        self.assertIn('tsconfig.json', key_files)
        self.assertIn('README.md', key_files)
    
    def test_language_counting(self):
        """Test that language statistics are correct"""
        parser = RepositoryParser(self.temp_dir)
        result = parser.parse()
        
        languages = result['languages']
        
        self.assertIn('python', languages)
        self.assertIn('javascript', languages)
        self.assertIn('typescript', languages)
        self.assertGreaterEqual(languages['python'], 2)  # test.py and src/index.py
    
    def test_directories_found(self):
        """Test that directories are identified"""
        parser = RepositoryParser(self.temp_dir)
        result = parser.parse()
        
        dir_names = [f['name'] for f in result['files'] if f['type'] == 'directory']
        
        self.assertIn('src', dir_names)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()
