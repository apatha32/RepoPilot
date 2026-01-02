"""
RepoPilot Dashboard - Streamlit UI for Repository Analysis
Free, open-source, deployable on Streamlit Cloud
Supports both local paths and GitHub repository URLs
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path

# Add analysis-engine to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analysis-engine'))

from parser import RepositoryParser
from dependency_mapper import DependencyMapper
from summarizer import Summarizer
from github_integration import GitHubAnalyzer

# Try to import clustering (optional - gracefully falls back if ML dependencies unavailable)
try:
    from clustering import CodeClusterer
    clustering_available = True
except (ImportError, ModuleNotFoundError):
    clustering_available = False
    
import networkx as nx

# Page configuration
st.set_page_config(
    page_title="RepoPilot - Repository Analysis",
    page_icon="[REPO]",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("[REPO] RepoPilot - Code Repository Intelligence")
st.markdown("Analyze GitHub repositories or local code instantly. Completely free and open-source.")

# Sidebar controls
st.sidebar.header("Repository Analysis")
analysis_mode = st.sidebar.radio(
    "Select Analysis Mode",
    ["Local Path", "GitHub URL", "Analyze Example"]
)

if analysis_mode == "GitHub URL":
    repo_url = st.sidebar.text_input(
        "Enter GitHub repository URL:",
        value="https://github.com/user/repo",
        help="Example: https://github.com/torvalds/linux"
    )
    repo_path = None  # Will be set after cloning
elif analysis_mode == "Local Path":
    repo_path = st.sidebar.text_input(
        "Enter local repository path:",
        value=".",
        help="Full path to the repository you want to analyze"
    )
    repo_url = None
else:
    repo_path = "."
    repo_url = None
    st.sidebar.info("Using current RepoPilot repository as example")

# Main analysis function
def run_analysis(path: str, github_url: str = None):
    """Run complete analysis pipeline
    
    Args:
        path: Local file path or None if using GitHub URL
        github_url: GitHub repository URL or None if using local path
    """
    temp_github_path = None
    
    try:
        # Handle GitHub URL
        if github_url:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Cloning GitHub repository...")
            progress_bar.progress(10)
            
            success, message, temp_path = GitHubAnalyzer.clone_repository(github_url)
            
            if not success:
                st.error(f"GitHub Clone Failed: {message}")
                return None
            
            temp_github_path = temp_path
            path = temp_path
            
            status_text.text("Repository cloned successfully. Analyzing...")
            progress_bar.progress(15)
        
        # Check path exists
        if not Path(path).exists():
            st.error(f"Path not found: {path}")
            return None
        
        # Create progress bar if not already created
        if not github_url:
            progress_bar = st.progress(0)
            status_text = st.empty()
            progress_bar.progress(15)
        
        # Parse repository
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Parse repository
        status_text.text("Step 1: Parsing repository structure...")
        progress_bar.progress(20)
        parser = RepositoryParser(path)
        structure = parser.parse()
        
        # Step 2: Map dependencies
        status_text.text("Step 2: Mapping dependencies...")
        progress_bar.progress(40)
        mapper = DependencyMapper(path, structure['files'])
        dependencies = mapper.build_dependency_graph()
        
        # Step 3: Perform code clustering (if ML libraries available)
        clustering = None
        if clustering_available:
            status_text.text("Step 3: Analyzing architectural patterns...")
            progress_bar.progress(55)
            try:
                clusterer = CodeClusterer()
                clustering = clusterer.cluster_files(structure['files'], n_clusters=min(4, max(2, len(structure['files']) // 3)))
            except Exception as e:
                # Gracefully continue without clustering if it fails
                st.warning(f"Architectural pattern analysis unavailable: {str(e)}")
                clustering = None
        
        # Step 4: Generate summaries
        status_text.text("Step 4: Generating summaries...")
        progress_bar.progress(70)
        summarizer = Summarizer()
        
        # Create results dictionary
        status_text.text("Step 5: Compiling results...")
        progress_bar.progress(85)
        
        results = {
            'metadata': {
                'repository': path,
                'path': str(Path(path).absolute()),
            },
            'structure': structure,
            'dependencies': dependencies,
            'clustering': clustering,
            'summaries': {
                'overview': summarizer.generate_repo_overview(structure, structure['key_files']),
            }
        }
        
        progress_bar.progress(100)
        status_text.text("Analysis complete!")
        
        # Add GitHub info to metadata if analyzing GitHub repo
        if github_url:
            results['metadata']['github_url'] = github_url
            repo_info = GitHubAnalyzer.get_repo_info(github_url)
            results['metadata'].update(repo_info)
        
        return results
    
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return None
    
    finally:
        # Clean up temporary GitHub clone directory
        if temp_github_path:
            GitHubAnalyzer.cleanup_temp_directory(temp_github_path)

# Run analysis button
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Repository Analysis")
with col2:
    run_button = st.button("Analyze Repository", type="primary")

results = None
if run_button:
    if analysis_mode == "GitHub URL":
        if not repo_url or not GitHubAnalyzer.validate_github_url(repo_url):
            st.error("Please enter a valid GitHub URL (e.g., https://github.com/user/repo)")
        else:
            results = run_analysis(path=None, github_url=repo_url)
    else:
        results = run_analysis(path=repo_path, github_url=None)

if results:
    # Display results in tabs (conditionally include Architecture Patterns tab)
    if clustering_available and results.get('clustering'):
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            ["Overview", "Structure", "Dependencies", "Architecture Patterns", "Files", "Configuration"]
        )
    else:
        tab1, tab2, tab3, tab5, tab6 = st.tabs(
            ["Overview", "Structure", "Dependencies", "Files", "Configuration"]
        )
        tab4 = None  # No architecture patterns tab
    
    # TAB 1: Overview
    with tab1:
        st.subheader("Repository Overview")
        
        # Show GitHub info if available
        if 'github_url' in results['metadata']:
            st.info(f"Analyzing GitHub repository: [{results['metadata']['owner']}/{results['metadata']['name']}]({results['metadata']['github_url']})")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Files",
                results['structure']['total_files']
            )
        with col2:
            st.metric(
                "Directories",
                results['structure']['total_directories']
            )
        with col3:
            primary_lang = max(
                results['structure']['languages'].items(),
                key=lambda x: x[1]
            )[0] if results['structure']['languages'] else "N/A"
            st.metric("Primary Language", primary_lang.upper())
        with col4:
            total_nodes = results['dependencies']['complexity_metrics']['total_nodes']
            st.metric("Modules/Files", total_nodes)
        
        st.markdown("---")
        st.write(results['summaries']['overview'])
    
    # TAB 2: Structure
    with tab2:
        st.subheader("Repository Structure")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Language Distribution:**")
            languages = results['structure']['languages']
            if languages:
                st.bar_chart(languages)
            else:
                st.info("No recognized languages found")
        
        with col2:
            st.write("**Language Breakdown:**")
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {lang.upper()}: {count} files")
    
    # TAB 3: Dependencies
    with tab3:
        st.subheader("Dependency Analysis")
        
        metrics = results['dependencies']['complexity_metrics']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Nodes", metrics['total_nodes'])
        with col2:
            st.metric("Total Edges", metrics['total_edges'])
        with col3:
            st.metric("Graph Density", f"{metrics['density']:.4f}")
        
        st.markdown("---")
        
        st.write("**Most Connected Files (Hot Spots):**")
        hotspots = metrics['most_connected']
        if hotspots:
            for i, file in enumerate(hotspots[:10], 1):
                st.write(f"{i}. {file}")
        else:
            st.info("No dependency relationships detected")
        
        st.markdown("---")
        st.write("**Dependency Graph Data:**")
        st.json({
            'nodes': results['dependencies']['nodes'][:10],
            'edges': results['dependencies']['edges'][:10],
            'note': 'Showing first 10 items'
        })
    
    # TAB 4: Architecture Patterns (only if clustering available)
    if tab4 is not None and clustering_available and results.get('clustering'):
        with tab4:
            st.subheader("Architectural Patterns")
            st.markdown("Machine learning-based code clustering identifies architectural patterns in your repository.")
            
            clustering = results['clustering']
            
            # Display clustering method
            method = clustering.get('method', 'KMeans Clustering')
            st.info(f"Detection Method: {method}")
            
            # Display architecture summary
            st.markdown("---")
            st.write("**Architecture Summary:**")
            summary = clustering.get('summary', 'Unable to generate summary')
            st.write(summary)
            
            st.markdown("---")
            
            # Display pattern breakdown
            st.write("**Identified Patterns:**")
            patterns = clustering.get('patterns', {})
            
            if patterns:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Pattern Categories:**")
                    for pattern_id, pattern_name in patterns.items():
                        st.write(f"- **{pattern_name}**")
                
                with col2:
                    st.write("**Files by Pattern:**")
                    clusters = clustering.get('clusters', {})
                    for cluster_id, files in clusters.items():
                        pattern_name = patterns.get(str(cluster_id), f"Cluster {cluster_id}")
                        st.write(f"**{pattern_name}:** {len(files)} files")
            else:
                st.info("No patterns identified (repository may be too small)")
            
            st.markdown("---")
            st.write("**Detailed File Groupings:**")
            
            clusters = clustering.get('clusters', {})
            if clusters:
                for cluster_id, files in clusters.items():
                    pattern_name = patterns.get(str(cluster_id), f"Cluster {cluster_id}")
                    with st.expander(f"{pattern_name} ({len(files)} files)"):
                        for file in sorted(files)[:20]:  # Show first 20 files
                            st.write(f"- {file}")
                        if len(files) > 20:
                            st.caption(f"... and {len(files) - 20} more files")
            else:
                st.info("No file clusters generated")
    
    # TAB 5: Files
    with tab5:
        st.subheader("File Listing")
        
        # Filter by language
        languages = list(results['structure']['languages'].keys())
        selected_lang = st.selectbox(
            "Filter by language:",
            ["All"] + sorted(languages)
        )
        
        # Display files
        files = results['structure']['files']
        if selected_lang == "All":
            display_files = [f for f in files if f['type'] == 'file']
        else:
            display_files = [
                f for f in files
                if f['type'] == 'file' and f['language'] == selected_lang
            ]
        
        st.write(f"Found {len(display_files)} file(s)")
        
        if display_files:
            # Create a simple table
            file_data = []
            for f in display_files[:50]:  # Limit to 50 for performance
                file_data.append({
                    'Path': f['path'],
                    'Language': f['language'],
                    'Size (bytes)': f['size'],
                    'Key': 'Yes' if f['is_key_file'] else 'No'
                })
            
            st.dataframe(
                file_data,
                use_container_width=True,
                hide_index=True
            )
            
            if len(display_files) > 50:
                st.info(f"Showing first 50 of {len(display_files)} files")
    
    # TAB 6: Configuration
    with tab6:
        st.subheader("Key Configuration Files")
        
        key_files = results['structure']['key_files']
        
        if key_files:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Identified Key Files:**")
                for i, file in enumerate(key_files, 1):
                    st.write(f"{i}. `{file}`")
            
            with col2:
                st.write("**Common Configuration Files Found:**")
                found_configs = {}
                
                common_configs = {
                    'package.json': 'Node.js dependencies',
                    'requirements.txt': 'Python dependencies',
                    'setup.py': 'Python project setup',
                    'tsconfig.json': 'TypeScript configuration',
                    'Dockerfile': 'Container configuration',
                    'docker-compose.yml': 'Multi-container setup',
                    '.env': 'Environment variables',
                    'README.md': 'Project documentation',
                }
                
                for key_file in key_files:
                    for config_name, description in common_configs.items():
                        if config_name in key_file:
                            st.write(f"- {config_name}: {description}")
        else:
            st.info("No key configuration files detected")
        
        st.markdown("---")
        st.subheader("Raw Analysis Data")
        
        if st.checkbox("Show raw JSON data"):
            st.json(results)

else:
    # Initial state - show welcome message
    st.info(
        """
        **Welcome to RepoPilot Dashboard!**
        
        This tool analyzes code repositories without requiring any API keys.
        
        **How to use:**
        1. Enter a local repository path in the sidebar (or use the example)
        2. Click "Analyze Repository"
        3. Explore the results in the tabs below
        
        **Features:**
        - Free to use - no API keys required
        - Language detection and file analysis
        - Dependency graph visualization
        - Key file identification
        - Project structure analysis
        
        **Supported Languages:**
        Python, JavaScript, TypeScript, Java, Go, Rust, C++, C, SQL, JSON, YAML, Markdown, HTML, CSS, Shell
        """
    )
    
    st.markdown("---")
    st.subheader("Quick Info")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**No Cost**")
        st.write("Completely free to use and deploy")
    
    with col2:
        st.write("**No API Keys**")
        st.write("Works entirely offline and locally")
    
    with col3:
        st.write("**Open Source**")
        st.write("Available on GitHub for modification")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px;'>
    RepoPilot - Free Code Repository Analysis | No API keys required | Deploy on Streamlit Cloud
    </div>
    """,
    unsafe_allow_html=True
)
