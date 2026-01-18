# Deployment Guide - Todo Phase 2 Project

## Overview

This guide covers deploying the Todo full-stack application to production environments.

## Architecture

```
┌─────────────────┐
│   Vercel CDN    │  ← Frontend (Next.js)
│   (Edge)        │     URL: *.vercel.app
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  FastAPI Backend│  ← REST API
│  Docker/Render  │     URL: *.onrender.com or IP
│  PostgreSQL DB  │
└─────────────────┘
     ↑
     │ PostgreSQL Connection
     ▼
┌─────────────────┐
│   Neon Database │  ← Persistent Storage
│   Serverless    │     URL: ep-xxx.neon.tech
└─────────────────┘
```

---

## Deployment Options

### Option 1: Docker Compose (Production)

**Best for**: Full control, same environment as development

**Steps**:

1. **Prepare Environment**:
   ```bash
   # Update .env with production values
   # Set DEBUG=false
   # Use production Neon URL
   # Generate strong secret
   ```

2. **Build and Run**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Configure Nginx** (optional):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

**Pros**: ✅ Same environment as development
**Cons**: ❌ Requires server management

---

### Option 2: Vercel (Frontend) + Render (Backend)

**Best for**: Serverless, auto-scaling, free tier available

#### Step 1: Deploy Backend to Render

**Method A: Using Docker**:

1. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: todo-backend
       env: docker
       dockerfilePath: ./backend/Dockerfile
       plan: free
       envVars:
         - key: DATABASE_URL
           sync: false
         - key: BETTER_AUTH_SECRET
           generateValue: true
         - key: TODO_DEBUG
           value: false
   ```

2. Push to GitHub and connect Render

3. Add environment variables in Render dashboard

**Method B: Using Python Environment**:

1. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: todo-backend
       env: python
       plan: free
       buildCommand: |
         pip install uv
         uv pip install -e .
       startCommand: |
         uvicorn src.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: DATABASE_URL
           sync: false
         - key: BETTER_AUTH_SECRET
           sync: false
   ```

2. Deploy from GitHub

**Backend URL**: `https://todo-backend-xxx.onrender.com`

---

#### Step 2: Deploy Frontend to Vercel

**Method A: Using Vercel CLI**:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

**Method B: Using GitHub Integration**:

1. Push code to GitHub
2. Visit https://vercel.com
3. Import GitHub repository
4. Configure settings:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

5. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://todo-backend-xxx.onrender.com
   BETTER_AUTH_SECRET=<same-as-backend>
   ```

6. Deploy

**Frontend URL**: `https://todo-frontend-xxx.vercel.app`

---

#### Step 3: Configure CORS

Update `backend/src/main.py` with Vercel URL:

```python
# Update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-frontend-xxx.vercel.app",  # Production
        "http://localhost:3000"  # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Rebuild and redeploy backend** after CORS update.

---

### Option 3: Railway (Backend) + Vercel (Frontend)

**Best for**: Simple setup, great free tier

**Deploy Backend to Railway**:

1. Visit https://railway.app
2. Connect GitHub repository
3. Select backend directory
4. Add environment variables:
   ```
   DATABASE_URL=postgresql+asyncpg://...
   BETTER_AUTH_SECRET=your-secret
   TODO_DEBUG=false
   ```
5. Deploy

**Deploy Frontend to Vercel** (same as Option 2)

---

## 🔐 Environment Variables Setup

### Production Environment Variables

**Root `.env` file**:
```bash
# Neon Database
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require

# JWT Secret (MUST match frontend and backend)
# Generate: openssl rand -base64 32
BETTER_AUTH_SECRET=actual-generated-secret-not-placeholder

# JWT Algorithm
BETTER_AUTH_ALGORITHM=HS256

# Backend Configuration (for Docker)
TODO_HOST=0.0.0.0
TODO_PORT=8000
TODO_DEBUG=false

# Frontend Configuration
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

**Backend `.env`**:
```bash
# Same as root .env but with TODO_ prefix
TODO_DATABASE_URL=postgresql+asyncpg://...
TODO_BETTER_AUTH_SECRET=your-secret
TODO_BETTER_AUTH_ALGORITHM=HS256
TODO_HOST=0.0.0.0
TODO_PORT=8000
TODO_DEBUG=false
```

**Frontend `.env.local`**:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
BETTER_AUTH_SECRET=your-secret
BETTER_AUTH_URL=https://your-frontend-url.com
```

---

## 🔧 Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] CORS origins updated in backend
- [ ] Database schema created in Neon
- [ ] JWT secret generated (32+ characters)
- [ ] Frontend API URL points to production backend
- [ ] Backend debug mode disabled (`DEBUG=false`)
- [ ] SSL required for database connections (`?sslmode=require`)
- [ ] Domain/subdomain configured (optional)
- [ ] HTTPS enabled (Vercel/Render provide this automatically)
- [ ] Health check endpoint accessible
- [ ] Logs monitoring set up

---

## 📊 Post-Deployment Testing

### Health Checks

**Backend Health**:
```bash
curl https://your-backend-url.com/health
# Expected: {"status": "healthy"}
```

**Frontend Load**:
```bash
curl -I https://your-frontend-url.com
# Expected: HTTP/2 200
```

**API Documentation**:
```bash
open https://your-backend-url.com/docs
# Expected: Swagger UI loads
```

---

### End-to-End Flow Test

1. **Sign Up**: https://your-frontend-url.com/signup
2. **Create Task**: Add "Deploy Test Task"
3. **Verify Persistence**: Check Neon console
4. **Update Task**: Edit title/description
5. **Toggle Complete**: Mark as complete
6. **Sign Out**: Log out
7. **Sign Back In**: Verify tasks still there
8. **Delete Task**: Remove the test task

---

## 📈 Monitoring

### Backend Logs

**Render**: Dashboard → Logs tab
**Railway**: Dashboard → Logs
**Docker**: `docker compose logs -f backend`

### Key Metrics to Monitor

- API response times (< 500ms)
- Database connection pool
- Error rate (< 1%)
- JWT token validation failures
- User sign-up/sign-in attempts

---

## 🚀 Deployment Scripts

### Deploy Script (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend
```

---

## 🔄 Continuous Deployment

### Setup Instructions

1. **Connect Repository**:
   - Vercel: Import Git repository
   - Render: Connect GitHub account
   - Railway: Connect GitHub account

2. **Configure Auto-Deploy**:
   - Enable deploy on every push
   - Set branch to `main`

3. **Add Secrets**:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - Any other environment variables

4. **Test Deployment**:
   - Make a small change
   - Push to main
   - Verify auto-deployment

---

## 📱 Mobile Deployment

### Progressive Web App (PWA)

Enable PWA features in `frontend/next.config.js`:

```javascript
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
})

module.exports = withPWA({
  // your existing config
})
```

Install:
```bash
npm install next-pwa
```

Benefits:
- ✅ Install as mobile app
- ✅ Offline capability
- ✅ Push notifications (with additional setup)

---

## 📤 Backup & Recovery

### Database Backup

Neon automatically backs up your database. To create additional backups:

```bash
# Export data
pg_dump $DATABASE_URL > backup.sql

# Import data
psql $DATABASE_URL < backup.sql
```

### Configuration Backup

Keep backups of:
- `.env` files (secure location)
- `docker-compose.yml`
- Deployment configs
- Database schema migrations

---

## 🛡️ Security Best Practices

✅ **DO**:
- Use strong, unique secrets
- Enable HTTPS (automatic on Vercel/Render)
- Keep dependencies updated
- Use environment variables for secrets
- Enable 2FA on all accounts
- Restrict CORS origins in production
- Validate all user input
- Use parameterized queries (SQLModel does this)

❌ **DON'T**:
- Commit secrets to Git
- Use default/weak passwords
- Expose database publicly
- Enable debug mode in production
- Log sensitive data
- Skip security updates

---

## 💰 Cost Considerations

### Free Tier Limits

**Vercel**:
- Bandwidth: 100GB/month
- Build time: 6,000 minutes/month
- Serverless Functions: 100GB-hours
- Edge Middleware: 1M invocations

**Render**:
- Web Services: 750 hours/month (always free tier)
- PostgreSQL: 90 days free trial

**Neon**:
- Storage: 3GB free
- Compute: 300 hours/month

**Railway**:
- Execution time: 500 hours/month
- Shared CPU/memory

### Production Costs (Estimates)

| Service | Monthly Cost |
|---------|--------------|
| Vercel Pro | $20 |
| Render Web Service | $7-25 |
| Neon Pro | $19 |
| Railway Pro | $5-20 |
| **Total** | **$51-84** |

---

## 📚 Troubleshooting

### Backend Won't Start

**Symptoms**: Container exits immediately

**Solutions**:
1. Check logs: `docker compose logs backend`
2. Verify DATABASE_URL format
3. Ensure Neon allows connections from your IP
4. Check for syntax errors in Python code

### Frontend Can't Connect to Backend

**Symptoms**: CORS errors, "Failed to fetch"

**Solutions**:
1. Verify NEXT_PUBLIC_API_URL is correct
2. Update CORS origins in backend
3. Check backend is running: `docker compose ps`
4. Verify network connectivity: `curl backend:8000/health`

### Database Connection Fails

**Symptoms**: "Connection refused", "timeout"

**Solutions**:
1. Verify DATABASE_URL includes `?sslmode=require`
2. Check Neon project is active (not suspended)
3. Whitelist IP in Neon dashboard
4. Test connection: `psql $DATABASE_URL`

### JWT Authentication Fails

**Symptoms**: 401 Unauthorized, "Invalid token"

**Solutions**:
1. Verify BETTER_AUTH_SECRET matches frontend/backend
2. Check token expiration
3. Ensure algorithm is HS256
4. Regenerate secret and redeploy both services

---

## 🎯 Deployment Checklist

Before going live:

- [ ] Production environment variables configured
- [ ] Secrets generated and stored securely
- [ ] CORS configured for production domain
- [ ] Database migrated to production
- [ ] SSL/TLS certificates active
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Logs accessible
- [ ] Backup strategy in place
- [ ] Rollback plan prepared
- [ ] Performance tested
- [ ] Security audit completed
- [ ] Documentation updated

---

## 📞 Support

If deployment fails:

1. Check service logs
2. Verify environment variables
3. Test database connection
4. Review CORS configuration
5. Check JWT secret consistency
6. Contact platform support:
   - Vercel: https://vercel.com/support
   - Render: https://render.com/support
   - Railway: https://railway.app/support

---

**Deployment Status**: Ready ✓
**Last Updated**: 2025-01-16
**Next Step**: Run deployment tests
