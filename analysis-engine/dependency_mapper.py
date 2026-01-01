"""
Dependency Mapper - Extract and map dependencies between modules
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any
import networkx as nx

class DependencyMapper:
    """Map dependencies between files and modules in a repository"""
    
    # Import patterns for different languages
    PATTERNS = {
        'python': [
            r'^\s*import\s+([a-zA-Z0-9_\.]+)',
            r'^\s*from\s+([a-zA-Z0-9_\.]+)\s+import',
        ],
        'javascript': [
            r"require\(['\"]([^'\"]+)['\"]\)",
            r"import\s+.*from\s+['\"]([^'\"]+)['\"]",
            r"import\s+['\"]([^'\"]+)['\"]",
        ],
        'typescript': [
            r"require\(['\"]([^'\"]+)['\"]\)",
            r"import\s+.*from\s+['\"]([^'\"]+)['\"]",
            r"import\s+['\"]([^'\"]+)['\"]",
        ],
    }
    
    def __init__(self, repo_path: str, files: List[Dict[str, Any]]):
        self.repo_path = Path(repo_path)
        self.files = files
        self.graph = nx.DiGraph()
        
    def build_dependency_graph(self) -> Dict[str, Any]:
        """Build dependency graph from files"""
        # Add all files as nodes
        for file_info in self.files:
            if file_info['type'] == 'file':
                self.graph.add_node(file_info['path'])
        
        # Extract dependencies for each file
        dependencies = {}
        for file_info in self.files:
            if file_info['type'] != 'file':
                continue
            
            deps = self._extract_dependencies(file_info)
            dependencies[file_info['path']] = deps
            
            # Add edges to graph
            for dep in deps:
                if dep in [f['path'] for f in self.files]:
                    self.graph.add_edge(file_info['path'], dep)
        
        return {
            'nodes': list(self.graph.nodes()),
            'edges': [{'source': u, 'target': v} for u, v in self.graph.edges()],
            'dependencies': dependencies,
            'complexity_metrics': self._calculate_metrics(),
        }
    
    def _extract_dependencies(self, file_info: Dict[str, Any]) -> Set[str]:
        """Extract dependencies from a file"""
        file_path = self.repo_path / file_info['path']
        
        if not file_path.exists():
            return set()
        
        language = file_info.get('language', 'unknown')
        if language not in self.PATTERNS:
            return set()
        
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern in self.PATTERNS[language]:
                matches = re.findall(pattern, content, re.MULTILINE)
                dependencies.update(matches)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return dependencies
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate complexity metrics"""
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'most_connected': self._get_most_connected_nodes(),
        }
    
    def _get_most_connected_nodes(self, limit: int = 10) -> List[str]:
        """Get most connected nodes (hot spots)"""
        degrees = dict(self.graph.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return [node for node, _ in sorted_nodes[:limit]]


if __name__ == '__main__':
    # Example usage
    print("Dependency mapper initialized. Use build_dependency_graph() method.")
