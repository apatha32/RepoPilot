"""
Batch Processor - Process multiple repositories in sequence
Supports CSV input with repo URLs and exports results
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import sys
import os

# Add analysis-engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analysis-engine'))

from parser import RepositoryParser
from dependency_mapper import DependencyMapper
from summarizer import Summarizer
from github_integration import GitHubAnalyzer

# Try to import clustering
try:
    from clustering import CodeClusterer
    clustering_available = True
except (ImportError, ModuleNotFoundError):
    clustering_available = False


class BatchProcessor:
    """Process multiple repositories in batch"""
    
    @staticmethod
    def validate_csv(csv_content: str) -> Tuple[bool, str, Optional[List[Dict]]]:
        """
        Validate CSV format and extract repository URLs
        
        Expected format:
        url,name,description
        https://github.com/user/repo,repo-name,optional description
        
        Returns:
            Tuple of (is_valid, error_message, repos_list)
        """
        try:
            lines = csv_content.strip().split('\n')
            if not lines:
                return False, "CSV is empty", None
            
            # Parse CSV
            reader = csv.DictReader(lines)
            repos = []
            
            for idx, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                if not row.get('url'):
                    return False, f"Row {idx}: Missing 'url' column", None
                
                url = row['url'].strip()
                if not GitHubAnalyzer.validate_github_url(url):
                    return False, f"Row {idx}: Invalid GitHub URL: {url}", None
                
                repos.append({
                    'url': url,
                    'name': row.get('name', '').strip() or url.split('/')[-1],
                    'description': row.get('description', '').strip()
                })
            
            if not repos:
                return False, "No valid repositories found in CSV", None
            
            return True, "", repos
        
        except Exception as e:
            return False, f"CSV parsing error: {str(e)}", None
    
    @staticmethod
    def analyze_repository(github_url: str) -> Tuple[bool, Dict]:
        """
        Analyze a single repository
        
        Returns:
            Tuple of (success, result_dict)
        """
        temp_github_path = None
        
        try:
            # Clone repository
            success, message, temp_path = GitHubAnalyzer.clone_repository(github_url)
            
            if not success:
                return False, {
                    'url': github_url,
                    'success': False,
                    'error': message,
                    'timestamp': datetime.now().isoformat()
                }
            
            temp_github_path = temp_path
            
            # Parse repository
            parser = RepositoryParser(temp_path)
            structure = parser.parse()
            
            # Map dependencies
            mapper = DependencyMapper(temp_path, structure['files'])
            dependencies = mapper.build_dependency_graph()
            
            # Perform clustering if available
            clustering = None
            if clustering_available:
                try:
                    clusterer = CodeClusterer()
                    clustering = clusterer.cluster_files(
                        structure['files'],
                        n_clusters=min(4, max(2, len(structure['files']) // 3))
                    )
                except Exception:
                    clustering = None
            
            # Generate summary
            summarizer = Summarizer()
            
            # Extract owner and repo info
            owner, repo = GitHubAnalyzer.parse_github_url(github_url)
            
            result = {
                'url': github_url,
                'owner': owner,
                'repo': repo,
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'total_files': len(structure['files']),
                    'total_directories': len(structure['directories']),
                    'primary_language': structure.get('primary_language', 'Unknown'),
                    'languages': structure.get('language_distribution', {}),
                    'key_files': structure.get('key_files', [])
                },
                'dependencies': {
                    'total_nodes': dependencies.get('nodes', 0),
                    'total_edges': dependencies.get('edges', 0),
                    'density': dependencies.get('density', 0),
                    'most_connected': dependencies.get('most_connected_files', [])[:5]
                },
                'clustering': clustering,
                'summary': summarizer.generate_repo_overview(structure, structure.get('key_files', []))
            }
            
            return True, result
        
        except Exception as e:
            return False, {
                'url': github_url,
                'success': False,
                'error': f"Analysis failed: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }
        
        finally:
            # Cleanup
            if temp_github_path:
                GitHubAnalyzer.cleanup_temp_directory(temp_github_path)
    
    @staticmethod
    def process_batch(repos: List[Dict], progress_callback=None) -> Dict:
        """
        Process multiple repositories
        
        Args:
            repos: List of repo dicts with 'url', 'name', 'description'
            progress_callback: Optional callback for progress updates
        
        Returns:
            Results dictionary
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_repos': len(repos),
            'successful': 0,
            'failed': 0,
            'analyses': []
        }
        
        for idx, repo in enumerate(repos):
            if progress_callback:
                progress_callback(f"Analyzing {idx + 1}/{len(repos)}: {repo['name']}...")
            
            success, analysis = BatchProcessor.analyze_repository(repo['url'])
            
            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
            
            results['analyses'].append(analysis)
        
        return results
    
    @staticmethod
    def export_to_json(results: Dict) -> str:
        """Export results to JSON format"""
        return json.dumps(results, indent=2)
    
    @staticmethod
    def export_to_csv(results: Dict) -> str:
        """Export results to CSV format (summary only)"""
        output = []
        output.append("Repository,Owner,Status,Total Files,Primary Language,Files Analyzed,Dependencies,Timestamp")
        
        for analysis in results['analyses']:
            if analysis['success']:
                output.append(
                    f"{analysis['repo']},"
                    f"{analysis['owner']},"
                    f"Success,"
                    f"{analysis['metadata']['total_files']},"
                    f"{analysis['metadata']['primary_language']},"
                    f"{analysis['metadata']['total_files']},"
                    f"{analysis['dependencies']['total_edges']},"
                    f"{analysis['timestamp']}"
                )
            else:
                output.append(
                    f"{analysis['url']},"
                    f"N/A,"
                    f"Failed: {analysis['error']},"
                    f"N/A,N/A,N/A,N/A,"
                    f"{analysis['timestamp']}"
                )
        
        return '\n'.join(output)
