"""
Analysis Engine - Main Orchestrator
Coordinates repository analysis across all modules
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from parser import RepositoryParser
from dependency_mapper import DependencyMapper
from summarizer import Summarizer
import dotenv

# Load environment variables
dotenv.load_dotenv()

class AnalysisOrchestrator:
    """Orchestrate complete repository analysis"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.parser = RepositoryParser(repo_path)
        self.summarizer = Summarizer()
        
    def analyze(self, output_file: str = None) -> Dict[str, Any]:
        """
        Run complete analysis pipeline
        
        Args:
            output_file: Optional path to save results as JSON
            
        Returns:
            Complete analysis results
        """
        print(f"[*] Analyzing repository: {self.repo_path}")
        
        # Step 1: Parse repository structure
        print("   1. Parsing repository structure...")
        structure_data = self.parser.parse()
        
        # Step 2: Build dependency graph
        print("   2. Mapping dependencies...")
        mapper = DependencyMapper(
            self.repo_path,
            structure_data['files']
        )
        dependency_data = mapper.build_dependency_graph()
        
        # Step 3: Generate summaries
        print("   3. Generating summaries...")
        repo_overview = self.summarizer.generate_repo_overview(
            structure_data,
            structure_data['key_files']
        )
        
        # Step 4: Compile results
        print("   4. Compiling results...")
        results = {
            'metadata': {
                'repository': os.path.basename(self.repo_path),
                'path': self.repo_path,
                'timestamp': str(Path(self.repo_path).stat().st_mtime),
            },
            'structure': structure_data,
            'dependencies': dependency_data,
            'summary': {
                'overview': repo_overview,
                'key_files': structure_data['key_files'],
                'languages': structure_data['languages'],
                'total_files': structure_data['total_files'],
            }
        }
        
        # Step 5: Save results (optional)
        if output_file:
            print(f"   5. Saving results to {output_file}...")
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
        
        print("[OK] Analysis complete!")
        return results
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        """Print a summary of analysis results"""
        print("\n" + "="*60)
        print("📊 ANALYSIS SUMMARY")
        print("="*60)
        
        metadata = results['metadata']
        structure = results['structure']
        deps = results['dependencies']
        
        print(f"\n[Repository] {metadata['repository']}")
        print(f"[Path] {metadata['path']}")
        
        print(f"\n[Statistics]")
        print(f"   Total Files: {structure['total_files']}")
        print(f"   Total Directories: {structure['total_directories']}")
        print(f"   Languages: {structure['languages']}")
        
        print(f"\n[Dependency Graph]")
        print(f"   Total Nodes: {deps['complexity_metrics']['total_nodes']}")
        print(f"   Total Edges: {deps['complexity_metrics']['total_edges']}")
        print(f"   Graph Density: {deps['complexity_metrics']['density']:.4f}")
        
        print(f"\n[Top Connected Files (Hot Spots)]")
        for i, file in enumerate(deps['complexity_metrics']['most_connected'][:5], 1):
            print(f"   {i}. {file}")
        
        print(f"\n[Key Files]")
        for file in structure['key_files'][:5]:
            print(f"   - {file}")
        
        print("\n" + "="*60)


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <repo_path> [output_file]")
        print("Example: python main.py /path/to/repo analysis_results.json")
        return
    
    repo_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Run analysis
    orchestrator = AnalysisOrchestrator(repo_path)
    results = orchestrator.analyze(output_file)
    
    # Print summary
    orchestrator.print_summary(results)


if __name__ == '__main__':
    main()
