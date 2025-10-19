# Deployment Guide - Grievance Filing Service

## Quick Local Deployment (Development)

### Already Complete!
The application is ready to run locally:

```bash
cd /Users/edmundbogen/GrievanceFilingService
source venv/bin/activate
python3 app.py
```

Visit: http://localhost:5000

## Production Deployment Options

### Option 1: Deploy to Heroku (Recommended for Quick Setup)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps

1. **Create Heroku app**:
   ```bash
   heroku create grievance-filing-service
   ```

2. **Add Procfile**:
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

3. **Add gunicorn to requirements**:
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-production-secret-key"
   heroku config:set FLASK_ENV=production
   ```

5. **Add PostgreSQL** (optional but recommended):
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

6. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

7. **Open app**:
   ```bash
   heroku open
   ```

### Option 2: Deploy to DigitalOcean App Platform

1. **Create new app** in DigitalOcean
2. **Connect GitHub repository**
3. **Configure build settings**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn app:app`
4. **Add environment variables**:
   - `SECRET_KEY`
   - `DATABASE_URL` (if using managed database)
5. **Deploy**

### Option 3: Deploy to AWS (EC2 + RDS)

#### EC2 Setup

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

4. **Clone/upload application**:
   ```bash
   git clone your-repo-url
   cd GrievanceFilingService
   ```

5. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **Create systemd service** (`/etc/systemd/system/grievance.service`):
   ```ini
   [Unit]
   Description=Grievance Filing Service
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/GrievanceFilingService
   Environment="PATH=/home/ubuntu/GrievanceFilingService/venv/bin"
   ExecStart=/home/ubuntu/GrievanceFilingService/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start service**:
   ```bash
   sudo systemctl start grievance
   sudo systemctl enable grievance
   ```

8. **Configure Nginx** (`/etc/nginx/sites-available/grievance`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }

       location /static {
           alias /home/ubuntu/GrievanceFilingService/static;
       }
   }
   ```

9. **Enable site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/grievance /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **Set up SSL with Let's Encrypt**:
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com
    ```

#### RDS Setup (PostgreSQL)

1. **Create RDS PostgreSQL instance**
2. **Update connection string**:
   ```bash
   export DATABASE_URL="postgresql://user:pass@rds-endpoint:5432/dbname"
   ```
3. **Update models to use PostgreSQL** (already compatible via SQLAlchemy)

### Option 4: Deploy to Vercel/Netlify (Serverless)

**Note**: Flask apps work better on traditional hosting. For serverless, consider refactoring to Next.js or using Vercel's Python support.

## Environment Variables for Production

Create a `.env` file or set environment variables:

```bash
# Required
SECRET_KEY=your-super-secret-production-key-change-this

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database

# Email (for future notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application
FLASK_ENV=production
```

## Database Migration

### From SQLite to PostgreSQL

1. **Install PostgreSQL adapter**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Update config.py**:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
   ```

3. **Export data from SQLite** (if needed):
   ```bash
   sqlite3 database.db .dump > backup.sql
   ```

4. **Create tables in PostgreSQL**:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

## File Storage Migration

### Move to AWS S3

1. **Install boto3**:
   ```bash
   pip install boto3
   ```

2. **Update upload function**:
   ```python
   import boto3
   s3 = boto3.client('s3')

   def upload_to_s3(file, bucket, key):
       s3.upload_fileobj(file, bucket, key)
       return f"https://{bucket}.s3.amazonaws.com/{key}"
   ```

3. **Set environment variables**:
   ```bash
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   S3_BUCKET=your-bucket-name
   ```

## Security Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Implement rate limiting
- [ ] Add CORS headers if needed
- [ ] Enable security headers
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Implement backup strategy
- [ ] Add monitoring/logging

## Performance Optimization

1. **Enable caching**:
   ```bash
   pip install Flask-Caching
   ```

2. **Use CDN for static files**:
   - CloudFlare
   - AWS CloudFront

3. **Database optimization**:
   - Add indexes
   - Connection pooling
   - Query optimization

4. **Implement Redis for sessions**:
   ```bash
   pip install redis flask-session
   ```

## Monitoring & Logging

### Add Sentry for Error Tracking

```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### Set up Application Logging

```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

## Backup Strategy

### Database Backups

```bash
# PostgreSQL
pg_dump -U username dbname > backup_$(date +%Y%m%d).sql

# Automate with cron
0 2 * * * pg_dump -U username dbname > /backups/db_$(date +\%Y\%m\%d).sql
```

### File Backups

```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz static/uploads/

# Sync to S3
aws s3 sync static/uploads/ s3://your-backup-bucket/uploads/
```

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple app servers behind load balancer
- Use managed database (RDS, Cloud SQL)
- Centralized file storage (S3, Google Cloud Storage)
- Redis for shared sessions

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes
- Implement caching

## Cost Estimates

### Heroku (Hobby)
- Dyno: $7/month
- PostgreSQL: $9/month
- **Total**: ~$16/month

### DigitalOcean
- App Platform: $12/month
- Managed Database: $15/month
- Spaces (Storage): $5/month
- **Total**: ~$32/month

### AWS (Small)
- EC2 t3.micro: $10/month
- RDS db.t3.micro: $15/month
- S3 Storage: $3/month
- **Total**: ~$28/month

### Self-Hosted (VPS)
- VPS (2GB RAM): $6-12/month
- Domain: $12/year
- SSL: Free (Let's Encrypt)
- **Total**: ~$6-12/month

## Post-Deployment Tasks

1. **Test all features**:
   - User registration
   - Login/logout
   - Complaint creation
   - Document upload
   - Deadline calculations

2. **Set up monitoring**:
   - Uptime monitoring (UptimeRobot, Pingdom)
   - Error tracking (Sentry)
   - Performance monitoring (New Relic)

3. **Configure backups**:
   - Automated database backups
   - File storage backups
   - Backup retention policy

4. **Set up CI/CD** (optional):
   - GitHub Actions
   - GitLab CI
   - CircleCI

5. **Create documentation**:
   - User guide
   - Admin manual
   - API documentation (if exposing APIs)

## Troubleshooting

### Application won't start
- Check logs: `journalctl -u grievance -f`
- Verify environment variables
- Check file permissions
- Ensure dependencies installed

### Database connection errors
- Verify DATABASE_URL
- Check firewall rules
- Confirm database is running
- Check connection limits

### File upload issues
- Check upload directory permissions
- Verify MAX_CONTENT_LENGTH setting
- Check disk space
- Review nginx client_max_body_size

## Support & Maintenance

### Regular Tasks
- Weekly: Check error logs
- Monthly: Review security patches
- Quarterly: Database optimization
- Annually: Security audit

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Restart application
sudo systemctl restart grievance
```

---

**Ready to deploy?** Choose the option that best fits your needs and budget!
