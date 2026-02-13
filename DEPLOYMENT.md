# Deployment Guide

## Frontend Deployment (Vercel)

### Option 1: Using Vercel Dashboard (Recommended)

1. **Import Project to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository

2. **Configure Project Settings**
   - **Root Directory**: Set to `frontend`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

3. **Set Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` with your backend URL
   - Example: `https://your-backend.railway.app` or `https://your-backend.render.com`

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow prompts and set NEXT_PUBLIC_API_URL when asked
```

## Backend Deployment

The FastAPI backend needs to be deployed separately. Here are recommended options:

### Option 1: Railway (Recommended)

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Set root directory to `backend`
4. Add environment variables:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./todos.db
   ```
5. Railway will auto-detect Python and deploy

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)

### Option 3: Vercel Serverless (Advanced)

Convert FastAPI to serverless functions - requires code modifications.

## Post-Deployment Steps

1. **Update Frontend Environment Variable**
   - In Vercel dashboard, go to your project settings
   - Navigate to "Environment Variables"
   - Update `NEXT_PUBLIC_API_URL` with your deployed backend URL
   - Redeploy frontend

2. **Test the Application**
   - Visit your Vercel URL
   - Try registering a new account
   - Create, update, and delete todos
   - Verify authentication works

## Troubleshooting

### 404 Error on Vercel
- **Cause**: Vercel is trying to deploy from root instead of frontend folder
- **Fix**: Set Root Directory to `frontend` in project settings

### CORS Errors
- **Cause**: Backend CORS not configured for frontend domain
- **Fix**: Update `backend/main.py` CORS origins to include your Vercel URL

### API Connection Failed
- **Cause**: `NEXT_PUBLIC_API_URL` not set or incorrect
- **Fix**: Set environment variable in Vercel dashboard and redeploy

### Database Issues
- **Cause**: SQLite file not persisting on serverless platforms
- **Fix**: Use PostgreSQL or MySQL for production (update backend configuration)

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend `NEXT_PUBLIC_API_URL` points to backend
- [ ] CORS configured with frontend domain
- [ ] Database configured for production (not SQLite)
- [ ] Secret keys are secure and not hardcoded
- [ ] SSL/HTTPS enabled on both frontend and backend
- [ ] Error monitoring configured (optional: Sentry)
- [ ] Analytics configured (optional: Vercel Analytics)
