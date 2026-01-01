# RepoPilot

**Turn any repository into a navigable intelligence layer for new developers.**

RepoPilot reduces codebase ramp-up time from days to hours by providing an interactive explorer, dependency mapping, and code analysis - all completely free, no API keys required.

---

## Quick Start

```bash
# Clone or download RepoPilot
cd RepoPilot

# Install dependencies
pip install -r analysis-engine/requirements.txt

# Run the Streamlit dashboard
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

**RepoPilot solves this** with instant, free codebase intelligence using local analysis (no AI services required).

---

## Architecture Overview

```
---

## Architecture

**Current Phase 1 - Free Analysis Engine:**
```
Streamlit Dashboard (app.py)
        ↓
Analysis Engine (Python)
  ├─ parser.py          (Parse repository structure)
  ├─ dependency_mapper  (Map code dependencies)
  └─ summarizer        (Generate summaries - no APIs)
        ↓
JSON Analysis Results
```

**Future Phases:**
- Phase 2: REST API backend (Node.js)
- Phase 3: React web UI  
- Phase 4: GitHub integration

---

## Features

Current (Free, No API Keys):
- [x] Repository structure analysis
- [x] Language detection
- [x] Dependency graph mapping
- [x] Key file identification
- [x] Streamlit dashboard UI
- [x] Local file processing
- [x] Zero-cost operation

Future Phases:
- [ ] GitHub repository browser
- [ ] Interactive dependency visualization
- [ ] Code search and navigation
- [ ] Hot spot identification
- [ ] Project-wide Q&A
- [ ] Multiple language support

---

## Supported Languages

Automatic detection and analysis for:
- Python
- JavaScript / TypeScript
- Java
- Go
- Rust
- C / C++
- SQL
- HTML / CSS
- YAML
- JSON
- Markdown
- Shell/Bash

---

## Project Structure

```
RepoPilot/
├── app.py                    # Streamlit dashboard
├── analysis-engine/
│   ├── parser.py            # File structure parser
│   ├── dependency_mapper.py  # Dependency analysis
│   ├── summarizer.py        # File summarization
│   ├── main.py              # CLI interface
│   ├── requirements.txt      # Python dependencies
│   └── tests/               # Unit tests
├── .streamlit/              # Streamlit config
│   └── config.toml
├── DEPLOYMENT.md            # Free deployment guide
├── README.md                # This file
└── Other project files

Future:
├── frontend/                # React UI (Phase 3)
├── backend/                 # Node.js API (Phase 2)
└── docs/                    # Documentation
```

---

## Installation & Setup

### Local Development

```bash
# 1. Clone the repository
git clone <repository-url>
cd RepoPilot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r analysis-engine/requirements.txt

# 4. Run dashboard
streamlit run app.py

# 5. Open http://localhost:8501
```

### Run CLI Analysis

```bash
cd analysis-engine
python main.py /path/to/repo output.json
```

### Run Tests

```bash
cd analysis-engine
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Free Deployment Options

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

### Option 1: Streamlit Cloud (Recommended)
- Free tier includes:
  - Auto-deploy from GitHub
  - Custom domains
  - 1GB disk space
  - 48 core-hours/month
  - Public sharing

Visit: https://streamlit.io/cloud

### Option 2: Replit
- Free accounts
- Auto-deploy
- One-click deployment

Visit: https://replit.com

### Option 3: Railway.app
- Free tier
- GitHub integration
- Auto-scaling

Visit: https://railway.app

---

## Roadmap
````

- **Frontend**: React 18, TypeScript, Tailwind CSS, D3.js
- **Backend**: Node.js, Express, TypeScript
- **Analysis**: Python 3.9+
- **Database**: PostgreSQL (optional, initially SQLite)
- **LLM**: OpenAI API (GPT-4) for summarization
- **Deployment**: Vercel (Frontend) + AWS Lambda (Backend)

---

## MVP Roadmap

### Phase 1: Analysis Engine ✨
- [ ] Parse repo structure
- [ ] Generate dependency graph
- [ ] Identify key files
- [ ] Extract file metrics

### Phase 2: Backend API
- [ ] GitHub integration
- [ ] File storage system
- [ ] Analysis orchestration
- [ ] REST endpoints

### Phase 3: Frontend UI
- [ ] File explorer
- [ ] Code viewer
- [ ] Dependency visualization
- [ ] Search functionality

### Phase 4: AI Layer
- [ ] File summarization
- [ ] Q&A interface
- [ ] Context generation

### Phase 5: Deployment
- [ ] Vercel setup
- [ ] GitHub Actions CI/CD
- [ ] Environment config

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- OpenAI API key
- GitHub token (for private repos)

### Installation

```bash
# Clone repo
git clone https://github.com/yourusername/RepoPilot.git
cd RepoPilot

# Install dependencies
cd frontend && npm install
cd ../backend && npm install
cd ../analysis-engine && pip install -r requirements.txt
```

### Running Locally

```bash
# Terminal 1: Backend
cd backend
npm run dev

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Analysis Engine (if needed)
cd analysis-engine
python -m uvicorn main:app --reload
```

---

## API Endpoints (Backend)

```
POST   /api/analyze           - Submit repo for analysis
GET    /api/analysis/:id      - Get analysis results
GET    /api/files/:id         - Get file structure
GET    /api/dependencies/:id  - Get dependency graph
POST   /api/ask               - Q&A about codebase
```

---

## Environment Variables

Create `.env` files in respective folders:

**backend/.env**
```
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
DATABASE_URL=postgres://...
```

**frontend/.env**
```
REACT_APP_API_URL=http://localhost:3001
```

---

## Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT

---

## Next Steps

1. Initialize git locally
2. Create GitHub repository
3. Push initial structure
4. Start with Phase 1: Analysis Engine
