"""
GitHub Integration - Clone and analyze GitHub repositories
Free GitHub API (no authentication needed for public repos)
"""

import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Optional
import re


class GitHubAnalyzer:
    """Handle GitHub repository cloning and analysis"""
    
    @staticmethod
    def validate_github_url(url: str) -> bool:
        """Validate if URL is a valid GitHub repository URL"""
        pattern = r'^https?://github\.com/[\w\-\.]+/[\w\-\.]+/?$'
        return bool(re.match(pattern, url.strip()))
    
    @staticmethod
    def parse_github_url(url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse GitHub URL to extract owner and repo name
        
        Returns:
            Tuple of (owner, repo_name) or (None, None) if invalid
        """
        url = url.strip().rstrip('/')
        match = re.match(r'https?://github\.com/([\w\-\.]+)/([\w\-\.]+)', url)
        
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    @staticmethod
    def clone_repository(github_url: str) -> Tuple[bool, str, Optional[str]]:
        """
        Clone GitHub repository to temporary directory
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Tuple of (success: bool, message: str, temp_path: Optional[str])
        """
        try:
            # Validate URL
            if not GitHubAnalyzer.validate_github_url(github_url):
                return False, "Invalid GitHub URL format. Expected: https://github.com/user/repo", None
            
            # Parse URL
            owner, repo = GitHubAnalyzer.parse_github_url(github_url)
            if not owner or not repo:
                return False, "Could not parse GitHub repository information", None
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix=f"repopilot_{repo}_")
            
            # Clone repository using subprocess (avoiding GitPython timeout issues)
            try:
                result = subprocess.run(
                    ['git', 'clone', '--depth=1', '--', github_url, temp_dir],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    # Clean up on clone failure
                    if Path(temp_dir).exists():
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    
                    error_msg = result.stderr.lower()
                    if "not found" in error_msg or "404" in error_msg:
                        return False, f"Repository not found: {github_url}", None
                    elif "private" in error_msg:
                        return False, "Cannot access private repository without authentication", None
                    else:
                        return False, f"Failed to clone repository: {result.stderr}", None
                
                return True, f"Cloned {owner}/{repo} successfully", temp_dir
            except subprocess.TimeoutExpired:
                if Path(temp_dir).exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                return False, "Repository clone timed out (taking too long)", None
            except Exception as e:
                if Path(temp_dir).exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                return False, f"Error during GitHub integration: {str(e)}", None
        
        except Exception as e:
            return False, f"Error during GitHub integration: {str(e)}", None
    
    @staticmethod
    def cleanup_temp_directory(temp_path: str) -> bool:
        """
        Clean up temporary directory
        
        Args:
            temp_path: Path to temporary directory
            
        Returns:
            True if cleanup successful
        """
        try:
            if temp_path and Path(temp_path).exists():
                shutil.rmtree(temp_path, ignore_errors=True)
                return True
        except Exception:
            pass
        return False
    
    @staticmethod
    def get_repo_info(github_url: str) -> dict:
        """
        Get basic repository information from GitHub URL
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Dictionary with repo info
        """
        owner, repo = GitHubAnalyzer.parse_github_url(github_url)
        
        if owner and repo:
            return {
                'owner': owner,
                'name': repo,
                'url': github_url,
                'clone_url': github_url + '.git'
            }
        return {}
