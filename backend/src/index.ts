import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Health check
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'Server is running', timestamp: new Date() });
});

// TODO: Add routes
// - POST /api/analyze
// - GET /api/analysis/:id
// - GET /api/files/:id
// - GET /api/dependencies/:id
// - POST /api/ask

app.listen(PORT, () => {
  console.log(`🚀 RepoPilot Backend running on port ${PORT}`);
});
