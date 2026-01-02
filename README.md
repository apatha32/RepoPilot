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
- [x] Interactive Streamlit dashboard with 6 tabs
- [x] Zero API costs - works 100% offline

### Enhanced Features
- [x] **GitHub Integration** - Paste GitHub URLs directly
- [x] **Local Path Analysis** - Analyze any local repository
- [x] **Architecture Patterns** - ML-based code clustering (optional)
- [x] **Dependency Visualization** - Network graph analysis

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

## Dashboard Tabs

1. **Overview** - High-level repository statistics, GitHub metadata (if from GitHub URL)
2. **Structure** - Language distribution, file type breakdown, directory hierarchy
3. **Dependencies** - Dependency graph metrics, hot spots, import patterns
4. **Architecture Patterns** - ML-based code clustering and pattern identification (optional)
5. **Files** - Searchable file listing with language filtering and metadata
6. **Configuration** - Key files, setup files, raw analysis data export

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

### Analyzing GitHub Repositories

1. Open RepoPilot (local or web version)
2. Select **"GitHub URL"** in sidebar
3. Enter a GitHub repository URL: `https://github.com/torvalds/linux`
4. Click **"Analyze Repository"**
5. App clones, analyzes, and displays results
6. Temporary files automatically cleaned up

### Analyzing Local Repositories

1. Select **"Local Path"** in sidebar
2. Enter full path: `/Users/username/Desktop/my-project`
3. Click **"Analyze Repository"**
4. Results display immediately

### Command Line Usage

```bash
cd analysis-engine
python main.py /path/to/repo output.json
```

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

### Phase 1 (Complete)
- [x] Repository structure analysis
- [x] Dependency graph mapping
- [x] Key file identification
- [x] Streamlit dashboard
- [x] ML-based clustering
- [x] GitHub URL support
- [x] 23 unit tests (100% pass)

### Phase 2 (Planned)
- [ ] REST API backend (Node.js)
- [ ] Database persistence (PostgreSQL)
- [ ] Multi-user support
- [ ] Saved analysis history
- [ ] Custom pattern definitions

### Phase 3 (Future)
- [ ] React web UI
- [ ] Advanced visualizations
- [ ] Code search functionality
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
