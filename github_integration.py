"""
GitHub Integration - Clone and analyze GitHub repositories
Free GitHub API (no authentication needed for public repos)
"""

import tempfile
import shutil
from pathlib import Path
from typing import Tuple, Optional
import git
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
            
            # Clone repository
            try:
                git.Repo.clone_from(
                    github_url,
                    temp_dir,
                    depth=1  # Shallow clone for speed
                )
                return True, f"Cloned {owner}/{repo} successfully", temp_dir
            except git.GitCommandError as e:
                # Clean up on clone failure
                if Path(temp_dir).exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                
                if "not found" in str(e).lower() or "404" in str(e):
                    return False, f"Repository not found: {github_url}", None
                elif "private" in str(e).lower():
                    return False, "Cannot access private repository without authentication", None
                else:
                    return False, f"Failed to clone repository: {str(e)}", None
        
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
