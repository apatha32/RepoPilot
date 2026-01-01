"""
Repository Parser - Extract structure and metadata from a repository
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class FileInfo:
    path: str
    name: str
    size: int
    type: str  # 'file' or 'directory'
    language: str = None
    is_key_file: bool = False

class RepositoryParser:
    """Parse repository structure and extract key metadata"""
    
    # File extensions to analyze
    LANGUAGE_EXTENSIONS = {
        'python': ['.py'],
        'javascript': ['.js', '.jsx'],
        'typescript': ['.ts', '.tsx'],
        'java': ['.java'],
        'go': ['.go'],
        'rust': ['.rs'],
        'cpp': ['.cpp', '.cc', '.cxx'],
        'c': ['.c', '.h'],
        'sql': ['.sql'],
        'json': ['.json'],
        'yaml': ['.yml', '.yaml'],
    }
    
    # Key files to identify
    KEY_FILES = {
        'package.json', 'requirements.txt', 'setup.py', 'Dockerfile',
        'docker-compose.yml', 'docker-compose.yaml', 'Makefile', 'Rakefile',
        'CMakeLists.txt', 'pom.xml', 'build.gradle', '.env', '.env.example',
        'README.md', 'README.rst', 'CONTRIBUTING.md', 'LICENSE',
        'tsconfig.json', 'webpack.config.js', '.eslintrc', '.prettier',
        'Procfile', 'tox.ini', 'pytest.ini', 'setup.cfg',
    }
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.files: List[FileInfo] = []
        
    def parse(self) -> Dict[str, Any]:
        """Parse repository and return structure"""
        self._walk_directory()
        return {
            'total_files': len(self.files),
            'total_directories': len([f for f in self.files if f.type == 'directory']),
            'files': [asdict(f) for f in self.files],
            'key_files': self._identify_key_files(),
            'languages': self._analyze_languages(),
        }
    
    def _walk_directory(self, current_path: Path = None) -> None:
        """Recursively walk through directory"""
        if current_path is None:
            current_path = self.repo_path
        
        try:
            for item in current_path.iterdir():
                if self._should_skip(item):
                    continue
                    
                relative_path = item.relative_to(self.repo_path)
                
                if item.is_dir():
                    self.files.append(FileInfo(
                        path=str(relative_path),
                        name=item.name,
                        size=0,
                        type='directory',
                    ))
                    self._walk_directory(item)
                else:
                    file_info = FileInfo(
                        path=str(relative_path),
                        name=item.name,
                        size=item.stat().st_size,
                        type='file',
                        language=self._detect_language(item),
                        is_key_file=item.name in self.KEY_FILES,
                    )
                    self.files.append(file_info)
        except PermissionError:
            pass
    
    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped"""
        skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build'}
        return path.name in skip_dirs or path.name.startswith('.')
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext = file_path.suffix.lower()
        for lang, exts in self.LANGUAGE_EXTENSIONS.items():
            if ext in exts:
                return lang
        return 'unknown'
    
    def _identify_key_files(self) -> List[str]:
        """Identify key configuration and metadata files"""
        return [f.path for f in self.files if f.is_key_file]
    
    def _analyze_languages(self) -> Dict[str, int]:
        """Count files by language"""
        lang_count = {}
        for file_info in self.files:
            if file_info.type == 'file' and file_info.language != 'unknown':
                lang_count[file_info.language] = lang_count.get(file_info.language, 0) + 1
        return lang_count


if __name__ == '__main__':
    # Example usage
    parser = RepositoryParser('.')
    result = parser.parse()
    print(json.dumps(result, indent=2))
