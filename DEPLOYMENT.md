Deployment Guide - RepoPilot
=============================

RepoPilot is completely free to deploy using Streamlit Cloud.

OPTION 1: Streamlit Cloud (RECOMMENDED - Completely Free)
=========================================================

1. Push code to GitHub:
   - Create a GitHub repository
   - Push all files to your repo
   - Make sure your repo is public

2. Deploy on Streamlit Cloud:
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your repository
   - Select main branch
   - Set main file path to: app.py
   - Click "Deploy"

3. Your app is now live and free!
   - Streamlit Cloud provides:
     * Free hosting
     * Auto-deploy on push
     * Custom domain support
     * 1GB disk space
     * 48 core-hours/month

OPTION 2: Replit (Free Alternative)
====================================

1. Create a Replit account (free)
2. Import from GitHub
3. Create a .replit file with:
   run = "pip install -r analysis-engine/requirements.txt && streamlit run app.py"
4. Click Run - your app starts automatically

OPTION 3: Railway.app (Free Tier)
=================================

1. Sign up at railway.app (free)
2. Create new project from GitHub
3. Add environment variable: PORT=8501
4. Deploy automatically

LOCAL DEVELOPMENT
=================

1. Install dependencies:
   cd analysis-engine
   pip install -r requirements.txt

2. Run dashboard:
   cd ..
   streamlit run app.py

3. Visit: http://localhost:8501

FEATURES
========

- Completely free - no API keys required
- Analyzes any Git repository
- Fast local processing
- Beautiful Streamlit UI
- Responsive design
- Works on mobile too

REQUIREMENTS
============

- Python 3.8+
- Streamlit
- NetworkX
- GitPython
- All dependencies in analysis-engine/requirements.txt

FILE STRUCTURE
==============

app.py                          - Main Streamlit dashboard
analysis-engine/
  parser.py                     - Repository structure parser
  dependency_mapper.py          - Dependency analysis
  summarizer.py                 - File/repo summaries (no APIs)
  requirements.txt              - Python dependencies
  main.py                       - CLI interface
  tests/                        - Unit tests
.streamlit/
  config.toml                   - Streamlit configuration
README.md                       - Project overview
DEPLOYMENT.md                   - This file

TROUBLESHOOTING
===============

Q: App crashes on import?
A: Make sure all requirements are installed:
   pip install -r analysis-engine/requirements.txt

Q: How do I analyze a GitHub repo?
A: Clone it locally first:
   git clone https://github.com/user/repo
   Then point the dashboard to the local path

Q: Can I modify the analysis?
A: Yes! All code is open source. Edit:
   - parser.py for file analysis
   - dependency_mapper.py for dependency detection
   - summarizer.py for summary generation

Q: Is there a cost?
A: Completely free:
   - No API keys
   - No paid services
   - Free hosting options
   - No credit card required

SUPPORT
=======

This is an open-source project. Contributions welcome!
