"""
Unit tests for Code Clustering module
"""

import unittest
import tempfile
from pathlib import Path
from clustering import CodeClusterer


class TestCodeClusterer(unittest.TestCase):
    """Test suite for CodeClusterer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.clusterer = CodeClusterer()
        
        # Create sample file list
        self.sample_files = [
            {'path': 'config.py', 'type': 'file', 'language': 'python', 'size': 500},
            {'path': 'setup.py', 'type': 'file', 'language': 'python', 'size': 1000},
            {'path': 'test_main.py', 'type': 'file', 'language': 'python', 'size': 800},
            {'path': 'test_utils.py', 'type': 'file', 'language': 'python', 'size': 600},
            {'path': 'utils.py', 'type': 'file', 'language': 'python', 'size': 700},
            {'path': 'helpers.py', 'type': 'file', 'language': 'python', 'size': 900},
            {'path': 'main.py', 'type': 'file', 'language': 'python', 'size': 2000},
            {'path': 'core.py', 'type': 'file', 'language': 'python', 'size': 3000},
        ]
    
    def test_extract_code_features(self):
        """Test feature extraction from files"""
        features = self.clusterer.extract_code_features(self.sample_files)
        
        self.assertEqual(len(features), 8)
        
        # Check that all files have features
        for file_info in self.sample_files:
            self.assertIn(file_info['path'], features)
        
        # Verify feature structure
        config_features = features['config.py']
        self.assertIn('is_config', config_features)
        self.assertIn('path', config_features)
        self.assertIn('language', config_features)
    
    def test_cluster_files(self):
        """Test file clustering"""
        result = self.clusterer.cluster_files(self.sample_files, n_clusters=3)
        
        self.assertIn('clusters', result)
        self.assertIn('patterns', result)
        self.assertIn('n_clusters', result)
        
        # Check clusters contain files
        total_files = sum(len(files) for files in result['clusters'].values())
        self.assertGreater(total_files, 0)
    
    def test_identify_patterns(self):
        """Test pattern identification"""
        features = self.clusterer.extract_code_features(self.sample_files)
        
        # Manual cluster creation for testing
        test_clusters = {
            0: ['main.py', 'core.py'],
            1: ['test_main.py', 'test_utils.py'],
            2: ['config.py', 'setup.py'],
            3: ['utils.py', 'helpers.py']
        }
        
        patterns = self.clusterer._identify_patterns(test_clusters, features)
        
        # Should have patterns for all clusters
        self.assertEqual(len(patterns), 4)
        
        # Check pattern values are strings
        for pattern in patterns.values():
            self.assertIsInstance(pattern, str)
    
    def test_architecture_summary(self):
        """Test architecture summary generation"""
        result = self.clusterer.cluster_files(self.sample_files, n_clusters=3)
        summary = self.clusterer.get_architecture_summary(result)
        
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        
        # Should contain pattern names
        self.assertIn('[', summary)
        self.assertIn(']', summary)
    
    def test_clustering_with_directories(self):
        """Test that directories are skipped"""
        files_with_dirs = self.sample_files + [
            {'path': 'src', 'type': 'directory', 'language': None, 'size': 0},
            {'path': 'tests', 'type': 'directory', 'language': None, 'size': 0},
        ]
        
        features = self.clusterer.extract_code_features(files_with_dirs)
        
        # Only files should be extracted, not directories
        self.assertEqual(len(features), 8)
    
    def test_fallback_clustering(self):
        """Test fallback heuristic clustering (no sklearn)"""
        result = self.clusterer._fallback_clustering(self.sample_files)
        
        self.assertIn('clusters', result)
        self.assertIn('patterns', result)
        self.assertEqual(result['method'], 'Heuristic Clustering (sklearn not available)')
        
        # Should have cluster groups
        self.assertGreater(len(result['clusters']), 0)
    
    def test_empty_file_list(self):
        """Test handling of empty file list"""
        result = self.clusterer.cluster_files([], n_clusters=2)
        
        self.assertIn('clusters', result)
        self.assertIn('patterns', result)


if __name__ == '__main__':
    unittest.main()
