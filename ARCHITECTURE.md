# Architecture & Setup Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         FRONTEND (React 18 + TypeScript)                 │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Components                                       │   │  │
│  │  │ - RepositorySelector                            │   │  │
│  │  │ - FileExplorer (Tree view)                      │   │  │
│  │  │ - CodeViewer (Syntax highlighted)               │   │  │
│  │  │ - DependencyGraph (D3 visualization)            │   │  │
│  │  │ - QAInterface (Chat-like)                       │   │  │
│  │  │ - SearchBar (File + semantic search)            │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └─────────────────────────┬────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                             │ HTTP/REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND (Node.js + Express + TypeScript)           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ API Routes (/api/)                                       │  │
│  │ - POST /analyze          → Trigger analysis             │  │
│  │ - GET /analysis/:id      → Retrieve results             │  │
│  │ - GET /files/:id         → Get file structure           │  │
│  │ - GET /dependencies/:id  → Get dependency graph         │  │
│  │ - GET /summary/:id       → Get AI summaries             │  │
│  │ - POST /ask              → Q&A endpoint                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Services                                                 │  │
│  │ - GitHubService    → Clone & fetch repos               │  │
│  │ - StorageService   → Store analysis results            │  │
│  │ - AnalysisService  → Orchestrate analysis engine       │  │
│  │ - LLMService       → Interface with OpenAI             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────┬──────────────────────────────┬──────────────────┬──────┘
          │                              │                  │
          ▼                              ▼                  ▼
    ┌──────────────┐         ┌─────────────────┐    ┌─────────────┐
    │ GitHub API   │         │  Analysis       │    │  OpenAI     │
    │              │         │  Engine (Python)│    │  API (GPT-4)│
    └──────────────┘         └─────────────────┘    └─────────────┘
                                     │
                         ┌──────────┬─┴────────────┐
                         ▼          ▼              ▼
                      Parser   Dependency      Summarizer
                               Mapper
```

---

## Component Breakdown

### Frontend Components

```typescript
src/
├── components/
│   ├── RepositorySelector.tsx      # GitHub URL input + analysis trigger
│   ├── FileExplorer.tsx            # Tree view with file navigation
│   ├── CodeViewer.tsx              # Syntax-highlighted code display
│   ├── DependencyGraph.tsx         # D3-based visualization
│   ├── QAInterface.tsx             # Chat interface for Q&A
│   ├── SearchBar.tsx               # File + semantic search
│   └── Dashboard.tsx               # Main layout component
│
├── pages/
│   ├── HomePage.tsx                # Landing page
│   ├── AnalysisPage.tsx            # Main analysis interface
│   └── NotFound.tsx
│
├── services/
│   ├── api.ts                      # API client (axios)
│   ├── types.ts                    # TypeScript interfaces
│   └── constants.ts                # Configuration
│
└── hooks/
    ├── useRepository.ts            # Repository context
    ├── useAnalysis.ts              # Analysis state management
    └── useSearch.ts                # Search functionality
```

### Backend Routes & Controllers

```typescript
src/
├── routes/
│   ├── analysis.routes.ts          # POST /analyze, GET /analysis/:id
│   ├── files.routes.ts             # GET /files/:id
│   ├── dependencies.routes.ts      # GET /dependencies/:id
│   ├── summary.routes.ts           # GET /summary/:id
│   └── qa.routes.ts                # POST /ask
│
├── controllers/
│   ├── analysisController.ts       # Analysis logic
│   ├── filesController.ts          # File retrieval
│   └── qaController.ts             # Q&A handling
│
├── services/
│   ├── githubService.ts            # GitHub API integration
│   ├── storageService.ts           # SQLite/PostgreSQL
│   ├── analysisService.ts          # Call Python analysis
│   └── llmService.ts               # OpenAI integration
│
├── models/
│   └── repository.ts               # Data models
│
└── middleware/
    ├── auth.ts                     # API key verification
    ├── errorHandler.ts             # Global error handling
    └── requestLogger.ts            # Request logging
```

### Analysis Engine (Python)

```python
analysis-engine/
├── parser.py                       # File structure parser
├── dependency_mapper.py            # Dependency graph
├── summarizer.py                   # AI summaries
├── main.py                         # Entry point
├── utils.py                        # Helper functions
└── config.py                       # Configuration
```

---

## Data Flow

### 1. User Submits Repository
```
User Input (GitHub URL)
         ↓
    Validation
         ↓
   Backend stores repo info
         ↓
   Trigger analysis worker
```

### 2. Analysis Pipeline
```
Clone Repository
         ↓
   Parse Structure (parser.py)
         ↓
   Extract Dependencies (dependency_mapper.py)
         ↓
   Identify Key Files
         ↓
   Generate Summaries (summarizer.py + OpenAI)
         ↓
   Store Results (SQLite)
         ↓
   Return to Frontend
```

### 3. Frontend Displays Results
```
Fetch Analysis Results
         ↓
   Populate File Tree
         ↓
   Render Dependency Graph
         ↓
   Display File Summaries
         ↓
   Enable Q&A Interface
```

---

## Data Models

### Repository
```typescript
{
  id: string;
  url: string;
  name: string;
  description: string;
  owner: string;
  language: string;
  stars: number;
  createdAt: Date;
  updatedAt: Date;
}
```

### Analysis Result
```typescript
{
  id: string;
  repositoryId: string;
  timestamp: Date;
  structure: FileInfo[];
  dependencies: DependencyGraph;
  summary: string;
  keyFiles: string[];
  languages: { [key: string]: number };
  hotSpots: string[];
}
```

### File Info
```typescript
{
  path: string;
  name: string;
  type: 'file' | 'directory';
  language: string;
  size: number;
  summary: string;
  dependencies: string[];
  importance: number; // 0-1 score
}
```

---

## Development Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- Git
- OpenAI API key
- GitHub personal access token (optional, for private repos)

### Installation

```bash
# Navigate to project
cd /Users/ambarishpathak/Desktop/RepoPilot

# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install

# Install analysis engine dependencies
cd ../analysis-engine
pip install -r requirements.txt
```

### Environment Setup

**Create `.env` files in each directory:**

**backend/.env**
```
PORT=3001
NODE_ENV=development
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
DATABASE_URL=sqlite:./repopilot.db
```

**frontend/.env**
```
REACT_APP_API_URL=http://localhost:3001
```

**analysis-engine/.env**
```
OPENAI_API_KEY=sk-...
```

### Running Locally

**Terminal 1: Backend**
```bash
cd backend
npm run dev
# Server runs on http://localhost:3001
```

**Terminal 2: Frontend**
```bash
cd frontend
npm start
# App runs on http://localhost:3000
```

**Terminal 3: Analysis Engine (optional, for testing)**
```bash
cd analysis-engine
python main.py
```

---

## API Specification

### 1. POST /api/analyze
**Submit a repository for analysis**

Request:
```json
{
  "url": "https://github.com/owner/repo",
  "branch": "main"
}
```

Response:
```json
{
  "id": "analysis_123",
  "status": "processing",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### 2. GET /api/analysis/:id
**Retrieve analysis results**

Response:
```json
{
  "id": "analysis_123",
  "status": "completed",
  "repository": { ... },
  "structure": [ ... ],
  "dependencies": { ... },
  "summary": "...",
  "keyFiles": [ ... ],
  "languages": { "python": 45, "javascript": 23 },
  "hotSpots": [ ... ]
}
```

### 3. GET /api/files/:id
**Get file structure**

Response:
```json
{
  "files": [
    {
      "path": "src/index.ts",
      "name": "index.ts",
      "type": "file",
      "language": "typescript",
      "size": 1234,
      "summary": "...",
      "dependencies": [ ... ]
    }
  ]
}
```

### 4. GET /api/dependencies/:id
**Get dependency graph**

Response:
```json
{
  "nodes": [ ... ],
  "edges": [ ... ],
  "metrics": {
    "total_nodes": 150,
    "total_edges": 320,
    "density": 0.015,
    "most_connected": [ ... ]
  }
}
```

### 5. POST /api/ask
**Ask a question about the codebase**

Request:
```json
{
  "analysisId": "analysis_123",
  "question": "What does the authentication module do?"
}
```

Response:
```json
{
  "answer": "The authentication module...",
  "references": [ "src/auth.ts", "src/middleware/auth.ts" ]
}
```

---

## Testing Strategy

### Backend Tests
```bash
npm test          # Run all tests
npm run test:cov  # With coverage
```

### Frontend Tests
```bash
npm test          # Jest tests
npm run test:e2e  # Cypress E2E tests
```

### Analysis Engine Tests
```bash
python -m pytest  # Python tests
```

---

## Performance Considerations

1. **Large Repositories**: Cache analysis results, implement pagination
2. **File Preview**: Limit file size display (e.g., first 50KB)
3. **Dependency Graph**: Use force-directed graph with virtualization
4. **Search**: Implement debouncing and indexing
5. **API Calls**: Rate limit OpenAI API usage

---

## Security

- API key verification for backend endpoints
- GitHub token encryption for private repos
- Input validation on all user inputs
- CORS configuration for frontend
- Rate limiting on analysis endpoint
- Secure storage of sensitive data

---

## Next Steps

1. ✅ Boilerplate created
2. ⏳ Install dependencies: `npm install` in backend & frontend
3. ⏳ Set up environment variables
4. ⏳ Build analysis engine
5. ⏳ Implement backend API routes
6. ⏳ Create frontend components
7. ⏳ Connect frontend to backend
8. ⏳ Deploy to Vercel
