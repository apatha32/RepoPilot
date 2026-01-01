# Quick Start Guide

Get RepoPilot running locally in 10 minutes.

---

## ✅ Checklist

- [ ] **Step 1**: Verify git initialized
- [ ] **Step 2**: Set up backend
- [ ] **Step 3**: Set up frontend  
- [ ] **Step 4**: Configure environment
- [ ] **Step 5**: Run locally
- [ ] **Step 6**: Push to GitHub
- [ ] **Step 7**: Deploy to Vercel

---

## Step 1: Verify Local Repository ✓

```bash
cd /Users/ambarishpathak/Desktop/RepoPilot

# Check git status
git status

# Check commits
git log --oneline
```

Expected output:
```
master 536484e docs: add architecture, github setup, deployment guides and CI
master 542fd32 Initial commit: RepoPilot MVP boilerplate
```

---

## Step 2: Set Up Backend

```bash
cd /Users/ambarishpathak/Desktop/RepoPilot/backend

# Install dependencies
npm install

# Verify installation
npm list | head -20
```

**Takes ~2 minutes**

---

## Step 3: Set Up Frontend

```bash
cd /Users/ambarishpathak/Desktop/RepoPilot/frontend

# Install dependencies
npm install

# Verify installation
npm list | head -20
```

**Takes ~2 minutes**

---

## Step 4: Configure Environment Variables

### Backend Environment (.env)

```bash
cat > /Users/ambarishpathak/Desktop/RepoPilot/backend/.env << 'EOF'
PORT=3001
NODE_ENV=development
OPENAI_API_KEY=sk-your-key-here
GITHUB_TOKEN=ghp_your-token-here
DATABASE_URL=sqlite:./repopilot.db
EOF
```

**Note:** You'll need:
- **OpenAI API Key**: Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **GitHub Token** (optional): From GitHub Settings → Developer Settings → Personal access tokens

### Frontend Environment (.env)

```bash
cat > /Users/ambarishpathak/Desktop/RepoPilot/frontend/.env << 'EOF'
REACT_APP_API_URL=http://localhost:3001
EOF
```

### Analysis Engine Environment (.env)

```bash
cat > /Users/ambarishpathak/Desktop/RepoPilot/analysis-engine/.env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
EOF
```

---

## Step 5: Run Locally (Development Mode)

Open **3 terminal windows/tabs**:

### Terminal 1: Backend
```bash
cd /Users/ambarishpathak/Desktop/RepoPilot/backend
npm run dev
```

Expected output:
```
🚀 RepoPilot Backend running on port 3001
```

### Terminal 2: Frontend
```bash
cd /Users/ambarishpathak/Desktop/RepoPilot/frontend
npm start
```

Expected output:
```
Compiled successfully!

You can now view repopilot-frontend in the browser.
  http://localhost:3000
```

### Terminal 3 (Optional): Analysis Engine
```bash
cd /Users/ambarishpathak/Desktop/RepoPilot/analysis-engine
pip install -r requirements.txt
python -c "from parser import RepositoryParser; print('✓ Analysis engine ready')"
```

---

## Step 6: Verify Everything Works

### Test Backend API
```bash
curl http://localhost:3001/api/health
```

Expected response:
```json
{"status":"Server is running","timestamp":"2024-01-01T00:00:00.000Z"}
```

### Test Frontend
Open browser: **[http://localhost:3000](http://localhost:3000)**

You should see:
- RepoPilot header
- "AI-powered codebase intelligence for new developers" subtitle

---

## Step 7: Create GitHub Repository & Push

### 7.1 Create Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `RepoPilot`
3. Description: `AI-powered codebase intelligence for new developers`
4. **Click "Create repository"** (don't initialize with README)
5. Copy the HTTPS URL (e.g., `https://github.com/yourusername/RepoPilot.git`)

### 7.2 Connect & Push

```bash
cd /Users/ambarishpathak/Desktop/RepoPilot

# Add remote (replace with your URL)
git remote add origin https://github.com/yourusername/RepoPilot.git

# Rename to main
git branch -M main

# Push to GitHub
git push -u origin main
```

Expected output:
```
Enumerating objects: 19, done.
...
To github.com:yourusername/RepoPilot.git
 * [new branch]      main -> main
Branch 'main' is tracking 'origin/main'.
```

### 7.3 Verify on GitHub

Visit `https://github.com/yourusername/RepoPilot` and verify:
- ✓ Files are visible
- ✓ README displayed
- ✓ All folders present

---

## Step 8: Deploy to Vercel (Optional Now, Do Later)

When ready to deploy:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from frontend folder
cd frontend
vercel
```

Follow prompts and your frontend will be live!

---

## 📁 Project Structure

```
RepoPilot/
├── backend/              # Node.js Express API
│   ├── src/
│   ├── package.json
│   └── .env             ← Add your API keys here
├── frontend/            # React UI
│   ├── src/
│   ├── package.json
│   └── .env             ← API URL
├── analysis-engine/     # Python analysis
│   ├── parser.py
│   ├── dependency_mapper.py
│   ├── summarizer.py
│   ├── requirements.txt
│   └── .env             ← Add OpenAI key
├── .github/workflows/   # CI/CD
├── ARCHITECTURE.md      # System design
├── GITHUB_SETUP.md      # GitHub guide
├── DEPLOYMENT.md        # Deployment guide
└── README.md            # Project overview
```

---

## 🐛 Troubleshooting

### Port 3001 already in use
```bash
# Kill process on port 3001
lsof -ti:3001 | xargs kill -9
```

### Port 3000 already in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### npm install fails
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install
```

### Node modules issues
```bash
# Remove and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 🚀 Next Steps

1. ✅ **Local setup complete**
2. ⏳ **Build Phase 1: Analysis Engine**
   - Implement repo parser tests
   - Test dependency mapper
   - Add summarization logic
3. ⏳ **Build Phase 2: Backend API**
   - Create GitHub integration
   - Build storage layer
   - Implement analysis orchestration
4. ⏳ **Build Phase 3: Frontend Components**
   - File explorer component
   - Code viewer
   - Dependency graph visualization
5. ⏳ **Phase 4: Deploy to Vercel**

---

## 📚 Documentation

- **[README.md](./README.md)** - Project overview
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design & data flow
- **[GITHUB_SETUP.md](./GITHUB_SETUP.md)** - GitHub repository setup
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment guide

---

## 💡 Tips

- **Use `git log --oneline`** to see commits
- **Use `npm run dev`** for backend auto-reload
- **Use `npm start`** for frontend hot reload
- **Check logs** for errors when something fails
- **Ask questions** on GitHub issues

---

## ✨ You're All Set!

Your local development environment is ready. Start building! 🎉

Questions? Check the documentation or create a GitHub issue.
