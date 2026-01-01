# RepoPilot 🚀

**Turn any repository into a navigable intelligence layer for new developers.**

RepoPilot reduces codebase ramp-up time from days to hours by providing an interactive explorer, dependency mapping, and AI-powered insights.

---

## Problem Statement

New engineers joining codebases waste **1-2 weeks** understanding:
- Project structure & organization
- Module dependencies & relationships  
- Where critical business logic lives
- How to run/test locally

**RepoPilot solves this** with an instant, AI-enhanced codebase intelligence layer.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  - File Explorer | Code Viewer | Dependency Graph       │
│  - Search | Q&A Interface | Repository Selector         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (Node.js)                      │
│  - GitHub API Integration | File Storage                 │
│  - Analysis Orchestration | LLM API Calls               │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│            ANALYSIS ENGINE (Python/Node)                 │
│  - Repo Parser | Dependency Graph Generator             │
│  - Hot Spot Identification | Key File Detection         │
│  - Summarization & Context Extraction                   │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
RepoPilot/
├── frontend/                 # React + TypeScript
│   ├── src/
│   │   ├── components/       # UI Components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API calls
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # Node.js Express
│   ├── src/
│   │   ├── routes/          # API endpoints
│   │   ├── controllers/     # Business logic
│   │   ├── services/        # External integrations
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
│
├── analysis-engine/          # Analysis core
│   ├── parser.py            # File structure parser
│   ├── dependency_mapper.py  # Dependency graph
│   ├── summarizer.py        # AI summarization
│   └── requirements.txt
│
└── README.md
```

---

## Tech Stack

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
