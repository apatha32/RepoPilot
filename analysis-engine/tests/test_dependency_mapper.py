"""
Unit tests for the Dependency Mapper module
"""

import unittest
import tempfile
from pathlib import Path
from dependency_mapper import DependencyMapper


class TestDependencyMapper(unittest.TestCase):
    """Test suite for DependencyMapper class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files with dependencies
        Path(self.temp_dir, 'main.py').write_text(
            'import os\nimport sys\nfrom utils import helper'
        )
        Path(self.temp_dir, 'utils.py').write_text(
            'import os\nfrom config import settings'
        )
        Path(self.temp_dir, 'config.py').write_text(
            'import json'
        )
        
        # Create TypeScript test files
        Path(self.temp_dir, 'index.ts').write_text(
            'import { helper } from "./utils";\nfrom "./config"'
        )
        Path(self.temp_dir, 'utils.ts').write_text(
            'export const helper = () => {}'
        )
        
        # Create mock file list
        self.files = [
            {'path': 'main.py', 'type': 'file', 'language': 'python'},
            {'path': 'utils.py', 'type': 'file', 'language': 'python'},
            {'path': 'config.py', 'type': 'file', 'language': 'python'},
            {'path': 'index.ts', 'type': 'file', 'language': 'typescript'},
            {'path': 'utils.ts', 'type': 'file', 'language': 'typescript'},
        ]
    
    def test_build_dependency_graph_returns_dict(self):
        """Test that build_dependency_graph returns required structure"""
        mapper = DependencyMapper(self.temp_dir, self.files)
        result = mapper.build_dependency_graph()
        
        self.assertIsInstance(result, dict)
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertIn('dependencies', result)
        self.assertIn('complexity_metrics', result)
    
    def test_graph_nodes_match_files(self):
        """Test that all files become graph nodes"""
        mapper = DependencyMapper(self.temp_dir, self.files)
        result = mapper.build_dependency_graph()
        
        nodes = result['nodes']
        
        self.assertEqual(len(nodes), len([f for f in self.files if f['type'] == 'file']))
        for file_info in self.files:
            if file_info['type'] == 'file':
                self.assertIn(file_info['path'], nodes)
    
    def test_complexity_metrics(self):
        """Test that complexity metrics are calculated"""
        mapper = DependencyMapper(self.temp_dir, self.files)
        result = mapper.build_dependency_graph()
        
        metrics = result['complexity_metrics']
        
        self.assertIn('total_nodes', metrics)
        self.assertIn('total_edges', metrics)
        self.assertIn('density', metrics)
        self.assertIn('most_connected', metrics)
        
        self.assertIsInstance(metrics['total_nodes'], int)
        self.assertIsInstance(metrics['total_edges'], int)
        self.assertGreaterEqual(metrics['total_nodes'], 0)
        self.assertGreaterEqual(metrics['total_edges'], 0)
    
    def test_dependencies_are_lists(self):
        """Test that dependencies are serializable (lists, not sets)"""
        mapper = DependencyMapper(self.temp_dir, self.files)
        result = mapper.build_dependency_graph()
        
        deps = result['dependencies']
        
        for file_path, dep_list in deps.items():
            self.assertIsInstance(dep_list, list)
            for dep in dep_list:
                self.assertIsInstance(dep, str)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()
