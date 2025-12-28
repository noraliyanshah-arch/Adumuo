# Deployment Guide - Adumuo

## Frontend Deployment (Netlify)

### Prerequisites
- Netlify account
- Git repository (optional, can use drag & drop)

### Steps

1. **Prepare Files**
   - File `netlify.toml` sudah dibuat di root project
   - File `_redirects` sudah dibuat di folder `frontend/`

2. **Deploy via Netlify Dashboard**
   - Login ke Netlify
   - Klik "Add new site" → "Deploy manually"
   - Drag & drop folder `frontend/` ke Netlify
   - Atau connect Git repository dan set:
     - **Publish directory**: `frontend`
     - **Build command**: (kosongkan)

3. **Update API URL untuk Production**
   - Edit `frontend/index.html`
   - Cari bagian `API_BASE_URL`
   - Update dengan URL backend production:
   ```javascript
   const API_BASE_URL = (() => {
       if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
           return 'http://localhost:8000';
       }
       // Update dengan URL backend production Anda
       return 'https://your-backend-domain.com';
   })();
   ```

## Backend Deployment

### Option 1: Railway
1. Sign up di Railway.app
2. New Project → Deploy from GitHub
3. Select repository
4. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `ADMIN_USERNAME`: Admin username
   - `ADMIN_PASSWORD`: Admin password
   - `SECRET_KEY`: Random secret key untuk JWT

### Option 2: Render
1. Sign up di Render.com
2. New Web Service
3. Connect repository
4. Build command: `cd backend && pip install -r ../requirements.txt`
5. Start command: `cd backend && python main.py`
6. Set environment variables (sama seperti Railway)

### Option 3: Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create adumuo-api`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
5. Set config vars:
   ```bash
   heroku config:set ADMIN_USERNAME=admin
   heroku config:set ADMIN_PASSWORD=your_password
   heroku config:set SECRET_KEY=your_secret_key
   ```
6. Deploy: `git push heroku main`

### Environment Variables untuk Backend

```bash
DATABASE_URL=postgresql://user:password@host:port/database
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=your_random_secret_key_here
```

## Post-Deployment Checklist

- [ ] Frontend deployed ke Netlify
- [ ] Backend deployed ke hosting service
- [ ] API URL updated di frontend
- [ ] Database connection working
- [ ] Admin login tested
- [ ] CORS configured untuk production domain
- [ ] Environment variables set
- [ ] SSL/HTTPS enabled
- [ ] Custom domain configured (optional)

## Troubleshooting

### Frontend shows "Page not found"
- Check `netlify.toml` exists in root
- Verify publish directory is set to `frontend`
- Check `_redirects` file exists in `frontend/` folder

### API calls failing
- Verify API_BASE_URL is correct
- Check CORS settings in backend
- Verify backend is running and accessible
- Check browser console for errors

### Database connection errors
- Verify DATABASE_URL is correct
- Check database is accessible from hosting service
- Verify firewall/network settings

