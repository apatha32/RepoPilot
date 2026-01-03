# RepoPilot - AI-Powered Code Repository Analysis Tool

**Turn any repository into a navigable intelligence layer for new developers.**

RepoPilot reduces codebase ramp-up time from days to hours by providing interactive analysis, dependency mapping, and architectural pattern identification - all completely free, no API keys required.

**Live Demo:** https://repopilot-dvj9on8jxgbwhy445sapts.streamlit.app/  
**GitHub:** https://github.com/apatha32/RepoPilot

---

## Table of Contents
- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [GitHub Integration](#github-integration)
- [ML Clustering](#ml-clustering)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## Quick Start

### Using the Live Web App (Easiest)
1. Go to: https://repopilot-dvj9on8jxgbwhy445sapts.streamlit.app/
2. Select **GitHub URL** mode
3. Paste a GitHub link: `https://github.com/user/repo`
4. Click **Analyze Repository**

### Running Locally

```bash
# Clone repository
git clone https://github.com/apatha32/RepoPilot.git
cd RepoPilot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py

# Open browser to http://localhost:8501
```

**That's it!** No API keys, no paid services. Works completely offline.

---

## Problem Statement

New engineers joining codebases waste **1-2 weeks** understanding:
- Project structure and organization
- Module dependencies and relationships  
- Where critical business logic lives
- How to run and test locally

**RepoPilot solves this** with instant, free codebase intelligence using local analysis.

---

## Features

### Core Features (Always Free)
- [x] Repository structure analysis (15+ languages)
- [x] Language detection and file statistics
- [x] Dependency graph mapping and hot-spot identification
- [x] Key file identification (config, setup, main entry points)
- [x] Interactive Streamlit dashboard with 6+ analysis tabs
- [x] Zero API costs - works 100% offline

### Enhanced Features
- [x] **GitHub Integration** - Paste GitHub URLs directly
- [x] **Local Path Analysis** - Analyze any local repository
- [x] **Architecture Patterns** - ML-based code clustering (optional)
- [x] **Dependency Visualization** - Network graph analysis

### Phase 1.5 Features (Batch Processing & CI/CD)
- [x] **Batch Analysis** - Upload CSV with multiple repo URLs, analyze all in sequence
- [x] **Results Export** - Download results as JSON or CSV
- [x] **GitHub Actions Integration** - Auto-generate CI/CD workflows for:
  - PR analysis (auto-comment results on pull requests)
  - Scheduled analysis (daily repo analysis with HTML reports)
- [x] **Repository Comparison** - Compare two repos side-by-side with metrics and charts

### Supported Languages
Python, JavaScript, TypeScript, Java, Go, Rust, C++, C, C#, PHP, Ruby, Kotlin, Scala, Swift, Shell/Bash, SQL, JSON, YAML, Markdown, HTML, CSS, and more.

---

## Architecture

```
Streamlit Dashboard (app.py)
        ↓
Analysis Engine
  ├─ parser.py              (Parse repository structure)
  ├─ dependency_mapper.py   (Map code dependencies using NetworkX)
  ├─ summarizer.py          (Generate summaries - no APIs)
  └─ clustering.py          (ML pattern identification - optional)
        ↓
GitHub Integration (github_integration.py)
  └─ Clone & analyze repos automatically
        ↓
JSON Analysis Results
```

### Technology Stack

**Frontend:**
- Streamlit 1.28.1 (interactive web interface)

**Analysis Engine:**
- Python 3.8+ (core language)
- NetworkX 3.2 (graph analysis for dependencies)
- GitPython 3.1.40 (GitHub integration)

**Optional ML:**
- scikit-learn (KMeans clustering - optional)
- numpy (numerical computing - optional)

**Deployment:**
- Streamlit Cloud (free tier)
- GitHub (version control)

**Cost:** Completely free - all dependencies are open-source (BSD/MIT licenses)

---

## Dashboard Features

### 4 Main Modes

1. **Single Repo Analysis** (Default)
   - Analyze one repository at a time
   - 6 interactive analysis tabs:
     * Overview - Statistics and metadata
     * Structure - Language distribution and organization
     * Dependencies - Code relationships and hot spots
     * Architecture Patterns - ML-based clustering (optional)
     * Files - Searchable file listing
     * Configuration - Key files and settings

2. **Batch Analysis** 🔄
   - Upload CSV with multiple repository URLs
   - Analyze all repos sequentially
   - Export results as JSON or CSV
   - Perfect for comparing multiple projects

3. **GitHub Actions** ⚙️
   - PR Analysis Workflow - Auto-analyzes changed files, comments results on PRs
   - Scheduled Analysis - Daily full repository analysis with HTML reports
   - Download ready-to-use workflow files
   - Setup: Copy file to `.github/workflows/`, commit, done

4. **Repository Comparison** 🔍
   - Compare 2 repositories side-by-side
   - Metrics comparison (files, languages, dependencies)
   - Language distribution charts
   - Works with GitHub URLs or local paths

---

## Installation

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/apatha32/RepoPilot.git
cd RepoPilot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py

# 5. Open in browser
# Local URL: http://localhost:8501
```

### Optional ML Features

For architectural pattern analysis with machine learning:

```bash
pip install scikit-learn numpy
```

---

## Usage

### Single Repository Analysis

#### Analyzing GitHub Repositories
1. Open RepoPilot dashboard
2. Select **"Single Repo Analysis"** mode
3. Select **"GitHub URL"** 
4. Paste URL: `https://github.com/facebook/react`
5. Click **"Analyze Repository"**

#### Analyzing Local Repositories
1. Select **"Single Repo Analysis"** mode
2. Select **"Local Path"**
3. Enter path: `/Users/username/Desktop/my-project`
4. Click **"Analyze Repository"**

#### Command Line Usage
```bash
cd analysis-engine
python main.py /path/to/repo output.json
```

### Batch Analysis (Multiple Repos)

1. Select **"Batch Analysis"** mode
2. Create CSV file with columns: `url,name,description`
   ```csv
   url,name,description
   https://github.com/facebook/react,React,UI library
   https://github.com/nodejs/node,Node.js,JavaScript runtime
   https://github.com/torvalds/linux,Linux,OS kernel
   ```
3. Upload CSV file in the app
4. Click **"Start Batch Analysis"**
5. Export results as **JSON** (full data) or **CSV** (summary)

**Use Cases:**
- Compare architecture across multiple projects
- Analyze team's repositories
- Generate reports for stakeholder presentations
- Track codebase metrics over time

### GitHub Actions Integration

Auto-analyze your repositories with GitHub Actions workflows.

#### PR Analysis Workflow
- Automatically analyzes every PR
- Comments results directly on PRs
- Shows file counts, languages, dependencies
- Helps maintain code quality standards

**Setup (2 minutes):**
1. Go to RepoPilot dashboard
2. Select **"GitHub Actions"** mode
3. Choose **"PR Analysis"** workflow
4. Click **"Download pr-analysis.yml"**
5. Create `.github/workflows/pr-analysis.yml` in your repo
6. Paste content and commit
7. Done! Workflow runs on next PR

#### Scheduled Analysis Workflow
- Analyzes entire repository daily
- Generates HTML report
- Uploads results as artifact
- Track metrics over time

**Same setup process**, choose "Scheduled Analysis" instead.

### Repository Comparison

Compare two repositories side-by-side.

1. Select **"Comparison Tool"** mode
2. Choose type for Repo 1: GitHub URL or Local Path
3. Choose type for Repo 2: GitHub URL or Local Path
4. Enter repository details
5. Click **"Compare Repositories"**

**Metrics Compared:**
- Total files and directories
- Primary programming language
- Language distribution
- Dependency counts and density

**Example:**
- Compare React vs Vue.js architecture
- Compare your project with industry benchmarks
- Analyze team repositories for consistency

---

## GitHub Integration

### How It Works

RepoPilot can automatically clone and analyze public GitHub repositories.

**Features:**
- ✓ Paste GitHub URL directly
- ✓ Automatic shallow cloning (fast)
- ✓ Temporary file cleanup
- ✓ Public repos (no authentication needed)
- ✓ Friendly error messages for private repos

**Cost:** Completely free - uses public GitHub access without API authentication

**Example Repositories to Try:**
```
https://github.com/facebook/react
https://github.com/docker/cli
https://github.com/stripe/stripe-ios
https://github.com/kubernetes/kubernetes
```

---

## ML Clustering

### How It Works

RepoPilot includes optional machine learning-based code clustering for architectural pattern identification.

**Features:**
- Extracts 6 code features per file (imports, functions, classes, size, test/config flags, depth)
- Uses scikit-learn KMeans for unsupervised clustering
- Identifies 4 architectural patterns:
  - **Configuration & Setup** (config files, setup scripts)
  - **Testing & Validation** (test files, assertions)
  - **Utilities & Helpers** (helper modules, shared code)
  - **Core Logic** (main application code)

**Installation:**
```bash
pip install scikit-learn numpy
```

**Note:** ML features are optional. RepoPilot works perfectly without them using heuristic analysis.

---

## Project Structure

```
RepoPilot/
├── app.py                        # Streamlit dashboard (main UI)
├── github_integration.py         # GitHub URL support
│
├── analysis-engine/
│   ├── parser.py                # Repository structure parser
│   ├── dependency_mapper.py      # Dependency graph analysis
│   ├── summarizer.py            # Code summarization (no APIs)
│   ├── clustering.py            # ML-based pattern identification
│   ├── main.py                  # CLI interface
│   ├── requirements.txt          # Python dependencies
│   │
│   └── tests/
│       ├── test_parser.py       # Parser unit tests
│       ├── test_dependency_mapper.py
│       ├── test_summarizer.py
│       └── test_clustering.py   # ML clustering tests
│
├── requirements.txt              # Root dependencies
├── README.md                     # This file
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

---

## Testing

Run the comprehensive test suite:

```bash
cd analysis-engine
python -m unittest discover tests -v
```

**Test Results:**
- Total Tests: 23
- Pass Rate: 100%
- Coverage: Core functionality
- Execution Time: <50ms

---

## Performance

| Operation | Time |
|-----------|------|
| Parse small repo (50 files) | <500ms |
| Parse medium repo (500 files) | 2-5s |
| Parse large repo (5000+ files) | 10-30s |
| ML clustering (100 files) | <500ms |
| Clone GitHub repo (average) | 5-15s |

**Memory Usage:** Linear in file count (~10MB per 1000 files)

---

## Deployment

### Streamlit Cloud (Recommended)

1. Fork the repository
2. Go to https://streamlit.io/cloud
3. Sign in with GitHub
4. Create new app → Select this repository
5. Deploy (takes ~2 minutes)

**Cost:** Free tier includes everything needed

### Local Deployment

```bash
streamlit run app.py
```

Accessible at: `http://localhost:8501`

### Python Version Support

- Python 3.8 - 3.13 supported
- Deployed on Streamlit Cloud with Python 3.13.9
- Optional ML dependencies work with all supported versions

---

## Free-First Philosophy

RepoPilot is designed with zero-cost operation:

**No Paid Dependencies:**
- No OpenAI API
- No cloud databases
- No commercial ML services
- All libraries are open-source (BSD/MIT licenses)

**Cost Breakdown:**
- Code analysis: $0.00
- ML clustering: $0.00
- GitHub integration: $0.00
- Deployment: $0.00 (Streamlit Cloud free tier)
- **Total: $0.00**

---

## Troubleshooting

### "Path not found" Error
- Use absolute path: `/Users/username/Desktop/my-project`
- Verify path exists in terminal: `ls /path/to/check`
- No spaces in paths (or quote them)

### "Invalid GitHub URL" Error
- Use correct format: `https://github.com/user/repo`
- No trailing slashes
- Public repository required

### "Repository not found" Error
- Check repo exists on GitHub
- Verify public access
- Try another repo

### ML Features Not Working
- Install ML dependencies: `pip install scikit-learn numpy`
- App continues working without them using heuristics

---

## Roadmap

### Phase 1 (Complete) ✅
- [x] Repository structure analysis
- [x] Dependency graph mapping
- [x] Key file identification
- [x] Streamlit dashboard (6 analysis tabs)
- [x] ML-based clustering
- [x] GitHub URL support
- [x] 23 unit tests (100% pass)

### Phase 1.5 (Complete) ✅
- [x] Batch analysis (CSV upload, multi-repo)
- [x] Results export (JSON/CSV)
- [x] GitHub Actions workflow generation
- [x] PR analysis workflow (auto-comment on PRs)
- [x] Scheduled analysis workflow (daily reports)
- [x] Repository comparison tool
- [x] Enterprise-ready multi-repo support

### Phase 2 (Planned)
- [ ] REST API backend (Node.js/Express)
- [ ] Database persistence (PostgreSQL)
- [ ] Multi-user support with authentication
- [ ] Saved analysis history
- [ ] Custom pattern definitions
- [ ] Scheduled analysis executor

### Phase 3 (Future)
- [ ] React web UI
- [ ] Advanced visualizations (D3.js)
- [ ] Code search functionality
- [ ] Mobile app support
- [ ] Private repository support

---

## Contributing

Contributions welcome! Areas for help:

- [ ] Additional language support
- [ ] Performance optimizations
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Bug fixes
- [ ] Feature requests

### Development Setup

```bash
# Create development environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
pip install scikit-learn numpy  # Optional ML

# Run tests
cd analysis-engine
python -m unittest discover

# Run app
streamlit run app.py
```

---

## License

MIT License - Feel free to use, modify, and distribute

---

## Contact

- **GitHub:** https://github.com/apatha32/RepoPilot
- **Live App:** https://repopilot-dvj9on8jxgbwhy445sapts.streamlit.app/
- **Author:** Ambarish Pathak

---

**Status:** Production Ready | **Cost:** Free Forever | **Maintenance:** Active Development
