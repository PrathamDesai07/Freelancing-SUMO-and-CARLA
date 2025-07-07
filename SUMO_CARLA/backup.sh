### ✅ 4. **Daily S3 Backup Script + Cron**

#### File: `backup.sh`
#!/bin/bash
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"

echo "[Backup] Creating archive..."
tar -czf "/tmp/$BACKUP_NAME" config/ output/logs/

echo "[Backup] Uploading to S3..."
aws s3 cp "/tmp/$BACKUP_NAME" s3://your-bucket-name/backups/

echo "[Backup] Done at $TIMESTAMP"
