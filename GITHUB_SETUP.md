# GitHub Repository Setup Guide

## Step 1: Create GitHub Repository

1. **Go to GitHub** → [github.com/new](https://github.com/new)

2. **Fill in Repository Details:**
   - Repository name: `RepoPilot`
   - Description: `AI-powered codebase intelligence for new developers`
   - Visibility: **Public** (for portfolio/visibility) or **Private** (for personal)
   - Initialize with: **Do NOT initialize with README** (we already have one)

3. **Click "Create repository"**

4. **Copy the repository URL** (e.g., `https://github.com/yourusername/RepoPilot.git`)

---

## Step 2: Add Remote & Push to GitHub

Run these commands in your local RepoPilot folder:

```bash
cd /Users/ambarishpathak/Desktop/RepoPilot

# Add remote origin (replace with your repo URL)
git remote add origin https://github.com/yourusername/RepoPilot.git

# Rename branch to main (optional, but recommended)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
Delta compression using up to 8 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (16/16), 5.22 KiB | 5.22 MiB/s, done.
Total 16 (delta 0), reused 0 (delta 0)
To github.com:yourusername/RepoPilot.git
 * [new branch]      main -> main
Branch 'main' is tracking 'origin/main'.
```

---

## Step 3: Verify on GitHub

1. **Go to your repository** on GitHub
2. **Verify files are there:**
   - README.md ✓
   - .gitignore ✓
   - backend/ folder ✓
   - frontend/ folder ✓
   - analysis-engine/ folder ✓

---

## Step 4: Create Useful GitHub Files

### 4.1 Create CONTRIBUTING.md

```bash
cat > /Users/ambarishpathak/Desktop/RepoPilot/CONTRIBUTING.md << 'EOF'
# Contributing to RepoPilot

We love contributions! Here's how to help:

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/RepoPilot.git
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

Follow the setup instructions in [ARCHITECTURE.md](./ARCHITECTURE.md#development-setup)

## Making Changes

1. Make your changes
2. Test locally
3. Commit with clear messages:
   ```bash
   git commit -m "feat: add file preview component"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request** on GitHub

## Code Standards

- TypeScript strict mode enabled
- Follow ESLint rules
- Add tests for new features
- Update documentation

## Reporting Issues

Found a bug? Please create an issue with:
- Description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)

---

Thank you for contributing! 🚀
EOF
```

### 4.2 Create DEPLOYMENT.md

```bash
cat > /Users/ambarishpathak/Desktop/RepoPilot/DEPLOYMENT.md << 'EOF'
# Deployment Guide

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- GitHub repository connected

### Steps

1. **Go to Vercel** → [Import Project](https://vercel.com/import)
2. **Select your GitHub repository**
3. **Configure:**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Environment Variables:
     ```
     REACT_APP_API_URL=your-backend-url
     ```
4. **Deploy**

Your frontend will be live at: `your-project.vercel.app`

---

## Backend Deployment (AWS Lambda + API Gateway)

### Prerequisites
- AWS account
- AWS CLI configured
- Serverless Framework

### Steps

```bash
# Install Serverless Framework
npm install -g serverless

# Configure AWS credentials
serverless config credentials --provider aws --key YOUR_KEY --secret YOUR_SECRET

# Deploy backend
cd backend
serverless deploy
```

### Environment Variables on AWS

Set in Lambda function configuration:
- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- `DATABASE_URL`

---

## Database Setup (PostgreSQL on AWS RDS)

1. **Create RDS instance** on AWS
2. **Update DATABASE_URL** in Lambda environment
3. **Run migrations** (when applicable)

---

## Monitoring & Logging

- **Frontend**: Vercel Analytics
- **Backend**: AWS CloudWatch
- **Errors**: Sentry integration (optional)

---

## CI/CD Pipeline with GitHub Actions

See [.github/workflows/](.github/workflows/) for automated testing and deployment.

---

## Rollback Procedure

```bash
# Frontend (Vercel)
vercel rollback

# Backend (AWS Lambda)
serverless deploy function -f functionName --version NUMBER
```
EOF
```

---

## Step 5: Create GitHub Actions Workflow (Optional)

Create `.github/workflows/ci.yml` for automated testing:

```bash
mkdir -p /Users/ambarishpathak/Desktop/RepoPilot/.github/workflows

cat > /Users/ambarishpathak/Desktop/RepoPilot/.github/workflows/ci.yml << 'EOF'
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18.x]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies (Backend)
        run: cd backend && npm install
      
      - name: Install dependencies (Frontend)
        run: cd frontend && npm install
      
      - name: Lint
        run: |
          cd backend && npm run lint || true
          cd ../frontend && npm run lint || true
      
      - name: Build Backend
        run: cd backend && npm run build
      
      - name: Build Frontend
        run: cd frontend && npm run build
EOF
```

---

## Step 6: Push New Files to GitHub

```bash
cd /Users/ambarishpathak/Desktop/RepoPilot

git add CONTRIBUTING.md DEPLOYMENT.md .github/

git commit -m "docs: add contributing and deployment guides"

git push origin main
```

---

## Verification Checklist

- [ ] Repository created on GitHub
- [ ] Remote origin configured locally
- [ ] Initial commit pushed
- [ ] All files visible on GitHub
- [ ] CONTRIBUTING.md created
- [ ] DEPLOYMENT.md created
- [ ] GitHub Actions workflow added
- [ ] Repository description & topics added
- [ ] README links verified

---

## Your Repository is Ready! 🎉

Next step: **Build the Analysis Engine** (Phase 1)

Visit: `https://github.com/yourusername/RepoPilot`
