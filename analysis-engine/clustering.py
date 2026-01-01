"""
Code Clustering - ML-based architectural pattern identification
Uses free scikit-learn for clustering and pattern recognition
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter
import json

class CodeClusterer:
    """Identify architectural patterns using code feature clustering"""
    
    def __init__(self):
        """Initialize clustering engine"""
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            self.KMeans = KMeans
            self.StandardScaler = StandardScaler
            self.sklearn_available = True
        except ImportError:
            self.sklearn_available = False
    
    def extract_code_features(self, files: List[Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """
        Extract numerical features from code files for clustering
        
        Features extracted:
        - Import count
        - Function/class count
        - File size
        - Complexity indicators
        """
        features = {}
        
        for file_info in files:
            if file_info['type'] != 'file':
                continue
            
            path = file_info['path']
            language = file_info.get('language', 'unknown')
            
            # Initialize feature vector
            feature_vector = {
                'path': path,
                'language': language,
                'import_count': 0,
                'function_count': 0,
                'class_count': 0,
                'file_size': file_info.get('size', 0),
                'is_test': 'test' in path.lower(),
                'is_config': any(x in path.lower() for x in ['config', 'setup', 'requirements']),
                'is_util': 'util' in path.lower() or 'helper' in path.lower(),
                'depth': path.count('/'),
            }
            
            features[path] = feature_vector
        
        return features
    
    def cluster_files(self, files: List[Dict[str, Any]], n_clusters: int = 4) -> Dict[str, Any]:
        """
        Cluster files into architectural groups
        
        Returns:
            Dictionary with cluster assignments and pattern descriptions
        """
        if not self.sklearn_available:
            return self._fallback_clustering(files)
        
        features = self.extract_code_features(files)
        
        if len(features) < n_clusters:
            n_clusters = max(2, len(features) // 2)
        
        # Build feature matrix
        paths = list(features.keys())
        feature_matrix = []
        
        for path in paths:
            feat = features[path]
            vector = [
                feat['import_count'],
                feat['function_count'],
                feat['class_count'],
                min(feat['file_size'] / 10000, 10),  # Normalize
                int(feat['is_test']),
                int(feat['is_config']),
                int(feat['is_util']),
                feat['depth'],
            ]
            feature_matrix.append(vector)
        
        feature_matrix = np.array(feature_matrix, dtype=float)
        
        # Normalize features
        scaler = self.StandardScaler()
        feature_matrix_scaled = scaler.fit_transform(feature_matrix)
        
        # Perform clustering
        kmeans = self.KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(feature_matrix_scaled)
        
        # Organize results
        clusters = {}
        for path, label in zip(paths, labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(path)
        
        # Generate pattern descriptions
        patterns = self._identify_patterns(clusters, features)
        
        return {
            'clusters': clusters,
            'patterns': patterns,
            'n_clusters': n_clusters,
            'method': 'KMeans Clustering'
        }
    
    def _identify_patterns(self, clusters: Dict[int, List[str]], 
                          features: Dict[str, Dict]) -> Dict[int, str]:
        """
        Identify architectural patterns from clusters
        """
        patterns = {}
        
        pattern_names = {
            0: "Core Logic & Algorithms",
            1: "Configuration & Setup",
            2: "Testing & Validation",
            3: "Utilities & Helpers",
            4: "API & Interfaces",
            5: "Data & Models"
        }
        
        for cluster_id, files in clusters.items():
            # Analyze files in cluster
            config_count = sum(1 for f in files if features[f]['is_config'])
            test_count = sum(1 for f in files if features[f]['is_test'])
            util_count = sum(1 for f in files if features[f]['is_util'])
            
            # Assign pattern name
            if config_count > len(files) * 0.5:
                pattern = "Configuration & Setup"
            elif test_count > len(files) * 0.5:
                pattern = "Testing & Validation"
            elif util_count > len(files) * 0.5:
                pattern = "Utilities & Helpers"
            else:
                pattern = pattern_names.get(cluster_id, f"Group {cluster_id}")
            
            patterns[cluster_id] = pattern
        
        return patterns
    
    def _fallback_clustering(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fallback clustering using simple heuristics (no sklearn)
        """
        clusters = {
            'config': [],
            'tests': [],
            'utils': [],
            'core': []
        }
        
        for file_info in files:
            if file_info['type'] != 'file':
                continue
            
            path = file_info['path'].lower()
            
            if any(x in path for x in ['config', 'setup', 'requirements', 'dockerfile']):
                clusters['config'].append(file_info['path'])
            elif 'test' in path:
                clusters['tests'].append(file_info['path'])
            elif any(x in path for x in ['util', 'helper', 'common']):
                clusters['utils'].append(file_info['path'])
            else:
                clusters['core'].append(file_info['path'])
        
        return {
            'clusters': clusters,
            'patterns': {
                'config': 'Configuration & Setup',
                'tests': 'Testing & Validation',
                'utils': 'Utilities & Helpers',
                'core': 'Core Logic'
            },
            'n_clusters': 4,
            'method': 'Heuristic Clustering (sklearn not available)'
        }
    
    def get_architecture_summary(self, clustering_result: Dict[str, Any]) -> str:
        """
        Generate human-readable architecture summary
        """
        patterns = clustering_result['patterns']
        clusters = clustering_result['clusters']
        
        summary = "Identified Architectural Pattern:\n\n"
        
        for cluster_id, pattern_name in patterns.items():
            files = clusters.get(cluster_id, [])
            summary += f"[{pattern_name}]\n"
            summary += f"  Files: {len(files)}\n"
            
            # Show a few example files
            examples = files[:3]
            for f in examples:
                summary += f"    - {f}\n"
            
            if len(files) > 3:
                summary += f"    ... and {len(files) - 3} more\n"
            
            summary += "\n"
        
        return summary


if __name__ == '__main__':
    print("Code Clustering module loaded. Free ML-based pattern recognition ready.")
